from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import paho.mqtt.client as mqtt
import json
import uuid
from datetime import datetime
from typing import List, Dict, Any
import threading
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

# Global MQTT client
mqtt_client = None

def get_db_connection():
    """Get a database connection."""
    return sqlite3.connect(DB_PATH)

# MQTT callback functions
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        logger.info("Connected to MQTT broker")
        client.subscribe("soldiers/inputs")
        client.subscribe("soldiers/heartbeat")
    else:
        logger.error(f"Failed to connect to MQTT broker. Return code: {rc}")

def on_message(client, userdata, msg):
    """Handle incoming MQTT messages from soldier devices."""
    try:
        payload = json.loads(msg.payload.decode())
        topic = msg.topic
        
        if topic == "soldiers/inputs":
            handle_soldier_input(payload)
        elif topic == "soldiers/heartbeat":
            handle_soldier_heartbeat(payload)
            
    except Exception as e:
        logger.error(f"Error processing MQTT message: {e}")

def handle_soldier_input(payload: Dict[str, Any]):
    """Save soldier input to database."""
    try:
        soldier_id = payload.get('soldier_id')
        timestamp = payload.get('timestamp', datetime.now().isoformat())
        raw_text = payload.get('raw_text', '')
        audio_ref = payload.get('audio_file_ref')

        if not soldier_id or not raw_text:
            logger.warning("Invalid soldier input: missing soldier_id or raw_text")
            return

        conn = get_db_connection()
        c = conn.cursor()
        input_id = str(uuid.uuid4())
        
        c.execute("""
            INSERT INTO soldier_raw_inputs (input_id, soldier_id, timestamp, raw_text, raw_audio_ref)
            VALUES (?, ?, ?, ?, ?)
        """, (input_id, soldier_id, timestamp, raw_text, audio_ref))
        
        conn.commit()
        conn.close()
        
        logger.info(f"Saved input from soldier {soldier_id} at {timestamp}")
        
        # Optionally trigger AI processing here
        # process_with_ai(input_id, raw_text)
        
    except Exception as e:
        logger.error(f"Error saving soldier input: {e}")

def handle_soldier_heartbeat(payload: Dict[str, Any]):
    """Handle soldier device heartbeat."""
    soldier_id = payload.get('soldier_id')
    timestamp = payload.get('timestamp', datetime.now().isoformat())
    logger.info(f"Heartbeat from soldier {soldier_id} at {timestamp}")

def start_mqtt_client():
    """Start the MQTT client in a separate thread."""
    global mqtt_client
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    
    try:
        mqtt_client.connect("localhost", 1883, 60)
        mqtt_client.loop_start()
        logger.info("MQTT client started successfully")
    except Exception as e:
        logger.error(f"Failed to start MQTT client: {e}")

# API Endpoints

@app.get("/")
async def root():
    """Root endpoint with system status."""
    return {
        "message": "Military Hierarchy Backend API",
        "status": "running",
        "mqtt_connected": mqtt_client.is_connected() if mqtt_client else False
    }

@app.get("/units")
async def get_units():
    """Get all military units."""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM units ORDER BY level, name")
    rows = c.fetchall()
    conn.close()
    
    columns = ["unit_id", "name", "parent_unit_id", "level"]
    return {"units": [dict(zip(columns, row)) for row in rows]}

@app.get("/units/{unit_id}/soldiers")
async def get_soldiers_by_unit(unit_id: str):
    """Get all soldiers in a specific unit."""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("""
        SELECT s.*, u.name as unit_name 
        FROM soldiers s 
        JOIN units u ON s.unit_id = u.unit_id 
        WHERE s.unit_id = ?
        ORDER BY s.rank, s.name
    """, (unit_id,))
    rows = c.fetchall()
    conn.close()
    
    columns = ["soldier_id", "name", "rank", "unit_id", "device_id", "unit_name"]
    return {"soldiers": [dict(zip(columns, row)) for row in rows]}

@app.get("/soldiers")
async def get_all_soldiers():
    """Get all soldiers."""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("""
        SELECT s.*, u.name as unit_name, u.level as unit_level
        FROM soldiers s 
        JOIN units u ON s.unit_id = u.unit_id 
        ORDER BY u.level, s.rank, s.name
    """)
    rows = c.fetchall()
    conn.close()
    
    columns = ["soldier_id", "name", "rank", "unit_id", "device_id", "unit_name", "unit_level"]
    return {"soldiers": [dict(zip(columns, row)) for row in rows]}

@app.get("/hierarchy")
async def get_hierarchy():
    """Get the complete military hierarchy with nested structure."""
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

@app.get("/units/{unit_id}/soldiers")
async def get_unit_soldiers(unit_id: str):
    """Get all soldiers in a specific unit."""
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

@app.get("/soldiers/{soldier_id}/raw_inputs")
async def get_soldier_raw_inputs(soldier_id: str, limit: int = 50):
    """Get raw inputs from a specific soldier."""
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
    
    columns = ["input_id", "soldier_id", "timestamp", "raw_text", "raw_audio_ref"]
    return {
        "soldier_id": soldier_id, 
        "raw_inputs": [dict(zip(columns, row)) for row in rows]
    }

@app.get("/soldiers/{soldier_id}/reports")
async def get_soldier_reports(soldier_id: str, limit: int = 50):
    """Get structured reports from a specific soldier."""
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
    
    columns = ["report_id", "soldier_id", "unit_id", "timestamp", "report_type", 
               "structured_json", "confidence", "soldier_name", "unit_name"]
    return {
        "soldier_id": soldier_id, 
        "reports": [dict(zip(columns, row)) for row in rows]
    }

@app.get("/reports")
async def get_all_reports(limit: int = 100):
    """Get all structured reports."""
    conn = get_db_connection()
    c = conn.cursor()
    c.execute("""
        SELECT r.*, s.name as soldier_name, u.name as unit_name
        FROM reports r
        JOIN soldiers s ON r.soldier_id = s.soldier_id
        JOIN units u ON r.unit_id = u.unit_id
        ORDER BY r.timestamp DESC 
        LIMIT ?
    """, (limit,))
    rows = c.fetchall()
    conn.close()
    
    columns = ["report_id", "soldier_id", "unit_id", "timestamp", "report_type", 
               "structured_json", "confidence", "soldier_name", "unit_name"]
    return {"reports": [dict(zip(columns, row)) for row in rows]}

@app.post("/soldiers/{soldier_id}/reports")
async def create_report(soldier_id: str, report_data: Dict[str, Any]):
    """Create a new structured report."""
    try:
        conn = get_db_connection()
        c = conn.cursor()
        
        # Get soldier's unit_id
        c.execute("SELECT unit_id FROM soldiers WHERE soldier_id = ?", (soldier_id,))
        result = c.fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="Soldier not found")
        
        unit_id = result[0]
        report_id = str(uuid.uuid4())
        timestamp = datetime.now().isoformat()
        
        c.execute("""
            INSERT INTO reports (report_id, soldier_id, unit_id, timestamp, report_type, structured_json, confidence)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            report_id, soldier_id, unit_id, timestamp,
            report_data.get("report_type", "UNKNOWN"),
            json.dumps(report_data.get("structured_json", {})),
            report_data.get("confidence", 0.0)
        ))
        
        conn.commit()
        conn.close()
        
        return {"message": "Report created successfully", "report_id": report_id}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/hierarchy")
async def get_military_hierarchy():
    """Get the complete military hierarchy structure."""
    conn = get_db_connection()
    c = conn.cursor()
    
    # Get all units
    c.execute("SELECT * FROM units ORDER BY level, name")
    units = c.fetchall()
    
    # Get all soldiers
    c.execute("""
        SELECT s.*, u.name as unit_name, u.level as unit_level
        FROM soldiers s 
        JOIN units u ON s.unit_id = u.unit_id 
        ORDER BY u.level, s.rank, s.name
    """)
    soldiers = c.fetchall()
    
    conn.close()
    
    # Build hierarchy structure
    units_dict = {}
    for unit in units:
        unit_id, name, parent_id, level = unit
        units_dict[unit_id] = {
            "unit_id": unit_id,
            "name": name,
            "parent_unit_id": parent_id,
            "level": level,
            "soldiers": [],
            "subunits": []
        }
    
    # Add soldiers to units
    soldier_columns = ["soldier_id", "name", "rank", "unit_id", "device_id", "unit_name", "unit_level"]
    for soldier in soldiers:
        soldier_data = dict(zip(soldier_columns, soldier))
        unit_id = soldier_data["unit_id"]
        if unit_id in units_dict:
            units_dict[unit_id]["soldiers"].append(soldier_data)
    
    # Build parent-child relationships
    hierarchy = []
    for unit_id, unit_data in units_dict.items():
        if unit_data["parent_unit_id"] is None:  # Top-level unit
            hierarchy.append(unit_data)
        else:
            parent_id = unit_data["parent_unit_id"]
            if parent_id in units_dict:
                units_dict[parent_id]["subunits"].append(unit_data)
    
    return {"hierarchy": hierarchy}

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize MQTT client on startup."""
    mqtt_thread = threading.Thread(target=start_mqtt_client)
    mqtt_thread.daemon = True
    mqtt_thread.start()

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Clean up MQTT client on shutdown."""
    global mqtt_client
    if mqtt_client:
        mqtt_client.loop_stop()
        mqtt_client.disconnect()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
