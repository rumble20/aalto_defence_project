from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Military Hierarchy Backend", version="1.0.0")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = "military_hierarchy.db"

def get_db_connection():
    """Get a database connection."""
    return sqlite3.connect(DB_PATH)

@app.get("/")
async def root():
    return {"message": "Military Hierarchy Backend API"}

@app.get("/hierarchy")
async def get_hierarchy():
    """Get the complete military hierarchy with nested structure."""
    try:
        conn = get_db_connection()
        c = conn.cursor()
        
        # Get all units with their hierarchy information
        c.execute("""
            SELECT u.unit_id, u.name, u.parent_unit_id, u.level, u.created_at
            FROM units u
            ORDER BY u.level, u.name
        """)
        units = c.fetchall()
        
        # Get all soldiers grouped by unit
        c.execute("""
            SELECT s.soldier_id, s.name, s.rank, s.unit_id, s.device_id, s.status, s.created_at, s.last_seen
            FROM soldiers s
            ORDER BY s.unit_id, s.name
        """)
        soldiers = c.fetchall()
        
        conn.close()
        
        # Group soldiers by unit
        soldiers_by_unit = {}
        for soldier in soldiers:
            unit_id = soldier[3]
            if unit_id not in soldiers_by_unit:
                soldiers_by_unit[unit_id] = []
            soldiers_by_unit[unit_id].append({
                "soldier_id": soldier[0],
                "name": soldier[1],
                "rank": soldier[2],
                "unit_id": soldier[3],
                "device_id": soldier[4],
                "status": soldier[5],
                "created_at": soldier[6],
                "last_seen": soldier[7]
            })
        
        # Build hierarchy structure
        hierarchy = []
        for unit in units:
            unit_data = {
                "unit_id": unit[0],
                "name": unit[1],
                "parent_unit_id": unit[2],
                "level": unit[3],
                "created_at": unit[4],
                "soldiers": soldiers_by_unit.get(unit[0], [])
            }
            hierarchy.append(unit_data)
        
        return {"hierarchy": hierarchy}
    except Exception as e:
        logger.error(f"Error in get_hierarchy: {e}")
        return {"error": str(e), "hierarchy": []}

@app.get("/units/{unit_id}/soldiers")
async def get_unit_soldiers(unit_id: str):
    """Get all soldiers in a specific unit."""
    try:
        conn = get_db_connection()
        c = conn.cursor()
        
        c.execute("""
            SELECT s.soldier_id, s.name, s.rank, s.unit_id, s.device_id, s.status, s.created_at, s.last_seen
            FROM soldiers s
            WHERE s.unit_id = ?
            ORDER BY s.name
        """, (unit_id,))
        
        soldiers = c.fetchall()
        conn.close()
        
        return {
            "soldiers": [
                {
                    "soldier_id": s[0],
                    "name": s[1],
                    "rank": s[2],
                    "unit_id": s[3],
                    "device_id": s[4],
                    "status": s[5],
                    "created_at": s[6],
                    "last_seen": s[7]
                }
                for s in soldiers
            ]
        }
    except Exception as e:
        logger.error(f"Error in get_unit_soldiers: {e}")
        return {"error": str(e), "soldiers": []}

@app.get("/soldiers/{soldier_id}/raw_inputs")
async def get_soldier_raw_inputs(soldier_id: str, limit: int = 50):
    """Get raw inputs from a specific soldier."""
    try:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("""
            SELECT * FROM soldier_raw_inputs 
            WHERE soldier_id = ? 
            ORDER BY timestamp DESC 
            LIMIT ?
        """, (soldier_id, limit))
        rows = c.fetchall()
        conn.close()
        
        columns = ["input_id", "soldier_id", "timestamp", "raw_text", "raw_audio_ref", "input_type", "confidence", "location_ref", "created_at"]
        return {"raw_inputs": [dict(zip(columns, row)) for row in rows]}
    except Exception as e:
        logger.error(f"Error in get_soldier_raw_inputs: {e}")
        return {"error": str(e), "raw_inputs": []}

@app.get("/soldiers/{soldier_id}/reports")
async def get_soldier_reports(soldier_id: str, limit: int = 50):
    """Get reports from a specific soldier."""
    try:
        conn = get_db_connection()
        c = conn.cursor()
        c.execute("""
            SELECT r.*, s.name as soldier_name, u.name as unit_name
            FROM reports r
            JOIN soldiers s ON r.soldier_id = s.soldier_id
            JOIN units u ON r.unit_id = u.unit_id
            WHERE r.soldier_id = ? 
            ORDER BY r.timestamp DESC 
            LIMIT ?
        """, (soldier_id, limit))
        rows = c.fetchall()
        conn.close()
        
        columns = ["report_id", "soldier_id", "unit_id", "timestamp", "report_type", "structured_json", "confidence", "source_input_id", "status", "reviewed_by", "reviewed_at", "created_at", "soldier_name", "unit_name"]
        return {"reports": [dict(zip(columns, row)) for row in rows]}
    except Exception as e:
        logger.error(f"Error in get_soldier_reports: {e}")
        return {"error": str(e), "reports": []}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
