from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

conn = sqlite3.connect("test.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT
)
""")

conn.commit()

@app.get("/")
def home():
    return {"message": "backend running"}

@app.get("/messages")
def get_messages():
    cursor.execute("SELECT * FROM messages")

    rows = cursor.fetchall()

    return [
        {
            "id": row[0],
            "text": row[1]
        }
        for row in rows
    ]

@app.post("/messages/{text}")
def add_message(text: str):
    cursor.execute(
        "INSERT INTO messages (text) VALUES (?)",
        (text,)
    )

    conn.commit()

    return {"success": True}