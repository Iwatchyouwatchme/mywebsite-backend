from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import psycopg2
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ 正確寫法（重點）
DATABASE_URL = os.environ["DATABASE_URL"]

conn = psycopg2.connect(DATABASE_URL)
cursor = conn.cursor()

# 建表
cursor.execute("""
CREATE TABLE IF NOT EXISTS messages (
    id SERIAL PRIMARY KEY,
    text TEXT NOT NULL,
    ip TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")
conn.commit()


@app.get("/")
def home():
    return {"message": "API running (PostgreSQL)"}


@app.get("/messages")
def get_messages():
    cursor.execute("""
        SELECT id, text, ip, created_at
        FROM messages
        ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    return [
        {
            "id": r[0],
            "text": r[1],
            "ip": r[2],
            "created_at": r[3].strftime("%Y-%m-%d %H:%M:%S")
        }
        for r in rows
    ]


@app.post("/messages")
async def add_message(request: Request):
    data = await request.json()
    text = data.get("text")

    ip = request.client.host

    cursor.execute(
        "INSERT INTO messages (text, ip) VALUES (%s, %s)",
        (text, ip)
    )
    conn.commit()

    return {"success": True, "ip": ip}
