import os
import uuid
from datetime import datetime, date
from decimal import Decimal
import bcrypt
import psycopg2
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()


# ---- Database connection ----

def get_connection():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "db"),
        database="bankdb",
        user="myuser",
        password="mypassword"
    )


def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS accounts (
            id TEXT PRIMARY KEY,
            name TEXT,
            last_name TEXT,
            email TEXT UNIQUE,
            password_hash TEXT,
            balance NUMERIC NOT NULL DEFAULT 0
        )
    """)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id TEXT PRIMARY KEY,
            account_id TEXT REFERENCES accounts(id),
            type TEXT,
            amount NUMERIC,
            related_account_id TEXT,
            trns_date TEXT
        )
    """)
    conn.commit()
    cur.close()
    conn.close()


@app.on_event("startup")
def startup_event():
    init_db()


# ---- Password hashing ----

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password.encode(), password_hash.encode())


# ---- Request models ----

class RegisterInput(BaseModel):
    name: str
    last_name: str
    email: str
    password: str
    opening_balance: float = 0


class LoginInput(BaseModel):
    email: str
    password: str


class AmountInput(BaseModel):
    amount: float


class TransferInput(BaseModel):
    amount: float
    to_account_id: str


# ---- Helper: record a transaction row ----

def record_transaction(cur, account_id, trns_type, amount, related_account_id=None):
    cur.execute(
        "INSERT INTO transactions (id, account_id, type, amount, related_account_id, trns_date) "
        "VALUES (%s, %s, %s, %s, %s, %s)",
        (str(uuid.uuid4()), account_id, trns_type, amount, related_account_id, str(date.today()))
    )


# ---- Endpoints ----

@app.post("/accounts/register")
def register(data: RegisterInput):
    if data.opening_balance < 0:
        raise HTTPException(400, "Opening balance cannot be negative.")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT id FROM accounts WHERE email = %s", (data.email,))
    if cur.fetchone():
        cur.close()
        conn.close()
        raise HTTPException(400, "An account with this email already exists.")

    account_id = str(uuid.uuid4())
    cur.execute(
        "INSERT INTO accounts (id, name, last_name, email, password_hash, balance) "
        "VALUES (%s, %s, %s, %s, %s, %s)",
        (account_id, data.name, data.last_name, data.email, hash_password(data.password), data.opening_balance)
    )
    if data.opening_balance > 0:
        record_transaction(cur, account_id, "deposit", data.opening_balance)

    conn.commit()
    cur.close()
    conn.close()
    return {"account_id": account_id, "message": "Account registered successfully."}


@app.post("/accounts/login")
def login(data: LoginInput):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, password_hash FROM accounts WHERE email = %s", (data.email,))
    row = cur.fetchone()
    cur.close()
    conn.close()

    if row is None or not verify_password(data.password, row[1]):
        raise HTTPException(401, "Invalid email or password.")

    return {"account_id": row[0], "message": "Login successful."}


@app.post("/accounts/{account_id}/deposit")
def deposit(account_id: str, data: AmountInput):
    if data.amount <= 0:
        raise HTTPException(400, "Amount must be greater than zero.")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT balance FROM accounts WHERE id = %s", (account_id,))
    row = cur.fetchone()
    if row is None:
        cur.close()
        conn.close()
        raise HTTPException(404, "Account not found.")

    new_balance = row[0] + Decimal(str(data.amount))
    cur.execute("UPDATE accounts SET balance = %s WHERE id = %s", (new_balance, account_id))
    record_transaction(cur, account_id, "deposit", data.amount)
    conn.commit()
    cur.close()
    conn.close()
    return {"new_balance": float(new_balance)}


@app.post("/accounts/{account_id}/withdraw")
def withdraw(account_id: str, data: AmountInput):
    if data.amount <= 0:
        raise HTTPException(400, "Amount must be greater than zero.")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT balance FROM accounts WHERE id = %s", (account_id,))
    row = cur.fetchone()
    if row is None:
        cur.close()
        conn.close()
        raise HTTPException(404, "Account not found.")

    if Decimal(str(data.amount)) > row[0]:
        cur.close()
        conn.close()
        raise HTTPException(400, "Insufficient funds.")

    new_balance = row[0] - Decimal(str(data.amount))
    cur.execute("UPDATE accounts SET balance = %s WHERE id = %s", (new_balance, account_id))
    record_transaction(cur, account_id, "withdraw", data.amount)
    conn.commit()
    cur.close()
    conn.close()
    return {"new_balance": float(new_balance)}


@app.post("/accounts/{account_id}/transfer")
def transfer(account_id: str, data: TransferInput):
    if data.amount <= 0:
        raise HTTPException(400, "Amount must be greater than zero.")
    if account_id == data.to_account_id:
        raise HTTPException(400, "Cannot transfer to the same account.")

    amount = Decimal(str(data.amount))

    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("SELECT balance FROM accounts WHERE id = %s", (account_id,))
        from_row = cur.fetchone()
        cur.execute("SELECT balance FROM accounts WHERE id = %s", (data.to_account_id,))
        to_row = cur.fetchone()

        if from_row is None or to_row is None:
            raise HTTPException(404, "One or both accounts not found.")
        if amount > from_row[0]:
            raise HTTPException(400, "Insufficient funds.")

        new_from_balance = from_row[0] - amount
        new_to_balance = to_row[0] + amount

        cur.execute("UPDATE accounts SET balance = %s WHERE id = %s", (new_from_balance, account_id))
        cur.execute("UPDATE accounts SET balance = %s WHERE id = %s", (new_to_balance, data.to_account_id))
        record_transaction(cur, account_id, "transfer_out", data.amount, related_account_id=data.to_account_id)
        record_transaction(cur, data.to_account_id, "transfer_in", data.amount, related_account_id=account_id)

        conn.commit()
    except HTTPException:
        conn.rollback()
        raise
    except Exception:
        conn.rollback()
        raise HTTPException(500, "Transfer failed, no changes were made.")
    finally:
        cur.close()
        conn.close()

    return {"message": "Transfer successful.", "new_balance": float(new_from_balance)}


@app.get("/accounts/{account_id}/balance")
def get_balance(account_id: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT balance FROM accounts WHERE id = %s", (account_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row is None:
        raise HTTPException(404, "Account not found.")
    return {"balance": float(row[0])}


@app.get("/accounts/{account_id}/transactions")
def get_transactions(account_id: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, type, amount, related_account_id, trns_date FROM transactions "
        "WHERE account_id = %s ORDER BY trns_date DESC",
        (account_id,)
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [
        {"id": r[0], "type": r[1], "amount": float(r[2]), "related_account_id": r[3], "date": r[4]}
        for r in rows
    ]