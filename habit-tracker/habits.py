from datetime import date
from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2
import uuid
import os


app = FastAPI()

class Habit:
    def __init__(self, id, name, created_at, completed_dates=None):
        self.id = id
        self.name = name
        self.created_at = created_at
        self.completed_dates = completed_dates or []

    def mark_completed(self, completed_date):
        if completed_date not in self.completed_dates:
            self.completed_dates.append(completed_date)

    def get_streak(self):
        if not self.completed_dates:
            return 0
        sorted_dates = sorted(self.completed_dates)
        streak = 1
        max_streak = 1
        for i in range(1, len(sorted_dates)):
            if (sorted_dates[i] - sorted_dates[i - 1]).days == 1:
                streak += 1
                max_streak = max(max_streak, streak)
            else:
                streak = 1
        return max_streak

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "created_at": str(self.created_at),
            "completed_dates": [str(d) for d in self.completed_dates]
        }


class HabitInput(BaseModel):
    name: str


def get_connection():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "db"),
        database="habitsdb",
        user="myuser",
        password="mypassword"
    )


def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS habits (
            id TEXT PRIMARY KEY,
            name TEXT,
            created_at TEXT,
            completed_dates TEXT
        )
    """)
    conn.commit()
    cur.close()
    conn.close()


@app.on_event("startup")
def startup_event():
    init_db()


def row_to_habit(row):
    """Converts one database row back into a Habit object."""
    id, name, created_at, completed_dates_str = row
    dates_list = []
    if completed_dates_str:
        dates_list = [date.fromisoformat(d) for d in completed_dates_str.split(",")]
    return Habit(id=id, name=name, created_at=created_at, completed_dates=dates_list)


@app.post("/habits")
def create_habit(habit_input: HabitInput):
    new_habit = Habit(id=str(uuid.uuid4()), name=habit_input.name, created_at=date.today())
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO habits (id, name, created_at, completed_dates) VALUES (%s, %s, %s, %s)",
        (new_habit.id, new_habit.name, str(new_habit.created_at), "")
    )
    conn.commit()
    cur.close()
    conn.close()
    return new_habit.to_dict()


@app.get("/habits")
def get_habits():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, created_at, completed_dates FROM habits;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [row_to_habit(r).to_dict() for r in rows]


@app.post("/habits/{habit_id}/complete")
def complete_habit(habit_id: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, created_at, completed_dates FROM habits WHERE id = %s", (habit_id,))
    row = cur.fetchone()
    if row is None:
        cur.close()
        conn.close()
        return {"message": "Habit not found."}

    habit = row_to_habit(row)
    habit.mark_completed(date.today())

    updated_dates_str = ",".join(str(d) for d in habit.completed_dates)
    cur.execute("UPDATE habits SET completed_dates = %s WHERE id = %s", (updated_dates_str, habit_id))
    conn.commit()
    cur.close()
    conn.close()
    return {"message": f"{habit.name} marked complete for today."}


@app.get("/habits/{habit_id}/streak")
def get_habit_streak(habit_id: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, created_at, completed_dates FROM habits WHERE id = %s", (habit_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    if row is None:
        return {"message": "Habit not found."}
    habit = row_to_habit(row)
    return {"habit": habit.name, "streak": habit.get_streak()}