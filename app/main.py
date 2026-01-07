from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import get_connection, create_table

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

create_table()

@app.get("/readings")
def get_readings():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM blood_pressure")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.post("/readings")
def add_reading(data: dict):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO blood_pressure (systolic, diastolic) VALUES (?, ?)",
        (data["systolic"], data["diastolic"])
    )
    conn.commit()
    conn.close()
    return {"message": "Reading added"}
