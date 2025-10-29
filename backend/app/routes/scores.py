from fastapi import APIRouter
import psycopg2
from app.db import DATABASE_URL

router = APIRouter(prefix="/scores", tags=["Scores"])

@router.get("/at-risk")
def at_risk(limit: int = 20):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("""
        SELECT bike_id, risk_score 
        FROM bike_scores 
        ORDER BY risk_score DESC 
        LIMIT %s;
    """, (limit,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [{"bike_id": r[0], "risk_score": float(r[1])} for r in rows]
