# Think through the shape of a habit entry — what would you want to track? 
# A reasonable starting point:

# id — unique identifier
# name — e.g. "Drink water", "Read 10 pages"
# created_at — when it was added
# completed_dates — a list of dates it was marked done (or maybe just a streak counter, your choice)

from datetime import date
from fastapi import FastAPI
from pydantic import BaseModel
import uuid

app = FastAPI()

class Habit:
    def __init__(self, id, name, created_at):
        self.id = id
        self.name = name
        self.created_at = created_at
        self.completed_dates = []

    def mark_completed(self, date):
        if date not in self.completed_dates:
            self.completed_dates.append(date)

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


habits = []  # shared in-memory list, holds Habit objects

class HabitInput(BaseModel):
    name: str


@app.post("/habits")
def create_habit(habit_input: HabitInput):
    new_habit = Habit(
        id=str(uuid.uuid4()),
        name=habit_input.name,
        created_at=date.today()
    )
    habits.append(new_habit)
    return new_habit.to_dict()


@app.get("/habits")
def get_habits():
    return [h.to_dict() for h in habits]


@app.post("/habits/{habit_id}/complete")
def complete_habit(habit_id: str):
    for h in habits:
        if h.id == habit_id:
            h.mark_completed(date.today())
            return {"message": f"{h.name} marked complete for today."}
    return {"message": "Habit not found."}


@app.get("/habits/{habit_id}/streak")
def get_habit_streak(habit_id: str):
    for h in habits:
        if h.id == habit_id:
            return {"habit": h.name, "streak": h.get_streak()}
    return {"message": "Habit not found."}