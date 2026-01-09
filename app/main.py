from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import sqlite3
from datetime import datetime, timedelta

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

conn = sqlite3.connect("bp.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS readings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    systolic INTEGER,
    diastolic INTEGER,
    date TEXT
)
""")
conn.commit()

class Reading(BaseModel):
    systolic: int
    diastolic: int

@app.get("/", response_class=HTMLResponse)
def home():
    with open("static/index.html") as f:
        return f.read()

@app.post("/add")
def add_reading(reading: Reading):
    date = datetime.now().strftime("%Y-%m-%d")
    cursor.execute("INSERT INTO readings (systolic, diastolic, date) VALUES (?, ?, ?)",
                   (reading.systolic, reading.diastolic, date))
    conn.commit()
    return {"message": "Reading saved successfully!"}

@app.get("/readings")
def get_readings(range: str):
    today = datetime.now()

    if range == "today":
        start = today.strftime("%Y-%m-%d")
    elif range == "week":
        start = (today - timedelta(days=7)).strftime("%Y-%m-%d")
    elif range == "month":
        start = (today - timedelta(days=30)).strftime("%Y-%m-%d")
    else:
        start = (today - timedelta(days=365)).strftime("%Y-%m-%d")

    cursor.execute("SELECT systolic, diastolic, date FROM readings WHERE date >= ?", (start,))
    rows = cursor.fetchall()

    return [{"systolic": r[0], "diastolic": r[1], "date": r[2]} for r in rows]
