from fastapi import APIRouter
import psycopg2
from app.db import DATABASE_URL

router = APIRouter(prefix="/maintenance", tags=["Maintenance"])

@router.get("/records")
def get_records():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("SELECT * FROM maintenance_records ORDER BY maintenance_date DESC LIMIT 50;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [{"record_id": r[0], "bike_id": r[1], "maintenance_date": str(r[2]), "component_failed": r[3]} for r in rows]
