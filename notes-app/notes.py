#import uuid
'''from datetime import datetime
from fastapi import FastAPI

def text_return():
    text = input("Enter some text: ")
    return {
        #"id": str(uuid.uuid4()),
        "id": 1,
        "text": f"This is the text you entered: {text}",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #"timestamp": datetime.now()
    }

result = text_return()
print(result)'''

#ALTERNATIVE WAY TO CALL THE FUNCTION
#result = text_return()
#print(f"This is the text you entered: {result['text']}")

'''import uuid
from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

notes = []  # shared list, defined once, at the top level

class NoteInput(BaseModel):
    text: str

@app.post("/notes")
def create_note(note: NoteInput):
    new_note = {
        "id": str(uuid.uuid4()),
        "text": note.text,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    notes.append(new_note)
    return new_note

@app.get("/notes")
def get_notes():
    return notes'''

import uuid
from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2
import os

app = FastAPI()

class NoteInput(BaseModel):
    text: str

def get_connection():
    return psycopg2.connect(
        host=os.environ.get("DB_HOST", "db"),
        database="notesdb",
        user="myuser",
        password="mypassword"
    )

def init_db():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id TEXT PRIMARY KEY,
            text TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    cur.close()
    conn.close()

@app.on_event("startup")
def startup_event():
    init_db()

@app.post("/notes")
def create_note(note: NoteInput):
    conn = get_connection()
    cur = conn.cursor()
    new_id = str(uuid.uuid4())
    new_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cur.execute(
        "INSERT INTO notes (id, text, timestamp) VALUES (%s, %s, %s)",
        (new_id, note.text, new_timestamp)
    )
    conn.commit()
    cur.close()
    conn.close()
    return {"id": new_id, "text": note.text, "timestamp": new_timestamp}

@app.get("/notes")
def get_notes():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, text, timestamp FROM notes;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    notes = [{"id": r[0], "text": r[1], "timestamp": r[2]} for r in rows]
    return notes

@app.delete("/notes/{note_id}")
def delete_note(note_id: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM notes WHERE id = %s", (note_id,))
    rows_deleted = cur.rowcount
    conn.commit()
    cur.close()
    conn.close()
    if rows_deleted == 0:
        return {"message": f"No note found with id {note_id}."}
    return {"message": f"Note with id {note_id} deleted."}

    