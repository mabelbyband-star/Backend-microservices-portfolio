from fastapi import FastAPI
import psycopg2
import os
import time

app = FastAPI()

def get_connection():
    return psycopg2.connect(
        host="db",
        database="mydb",
        user="myuser",
        password="mypassword"
    )

@app.get("/")
def read_root():
    return {"message": "FastAPI + Postgres running in Docker!"}

@app.get("/dbcheck")
def db_check():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT version();")
        version = cur.fetchone()
        cur.close()
        conn.close()
        return {"status": "connected", "postgres_version": version}
    except Exception as e:
        return {"status": "error", "detail": str(e)}