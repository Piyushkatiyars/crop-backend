from fastapi import FastAPI
import psycopg2
import os

app = FastAPI()

DATABASE_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

@app.get("/")
def home():
    return {"message": "Crop Backend Running with PostgreSQL!"}

@app.get("/test-db")
def test_db():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT now();")
        result = cursor.fetchone()
        conn.close()
        return {"db_time": result}
    except Exception as e:
        return {"error": str(e)}
