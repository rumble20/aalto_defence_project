from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
import paho.mqtt.client as mqtt
import json
import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional
import threading
import logging
import google.generativeai as genai

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure Gemini API
GEMINI_API_KEY = "AIzaSyB2LVUXt2a9nMCpJwGJWen4_EECudv9u_c"
genai.configure(api_key=GEMINI_API_KEY)
# Use gemini-2.5-pro - most capable model with advanced reasoning
gemini_model = genai.GenerativeModel('gemini-2.5-pro')

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

@app.get("/soldiers/{soldier_id}/raw_inputs")
async def get_soldier_raw_inputs(soldier_id: str, limit: int = 500):
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
async def get_soldier_reports(soldier_id: str, limit: int = 500):
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
async def get_all_reports(limit: int = 1000):
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
    
    # Get all units - select specific columns to avoid unpacking issues
    c.execute("SELECT unit_id, name, parent_unit_id, level FROM units ORDER BY level, name")
    units = c.fetchall()
    
    # Get all soldiers
    c.execute("""
        SELECT s.soldier_id, s.name, s.rank, s.unit_id, s.device_id
        FROM soldiers s 
        ORDER BY s.rank, s.name
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
    soldier_columns = ["soldier_id", "name", "rank", "unit_id", "device_id"]
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

# Pydantic models for API
class ChatMessage(BaseModel):
    message: str
    context: Dict[str, Any]

class FRAGOSuggestRequest(BaseModel):
    unit_id: str
    unit_name: str
    soldier_ids: List[str]
    reports: List[Dict[str, Any]]

class FRAGOGenerateRequest(BaseModel):
    unit_id: str
    unit_name: str
    frago_fields: Dict[str, Any]
    source_report_ids: List[str]

@app.post("/ai/chat")
async def ai_chat(chat_request: ChatMessage):
    """
    AI chat endpoint that analyzes reports using Google Gemini AI.
    """
    try:
        message = chat_request.message
        context = chat_request.context
        
        # Extract node info and reports from context
        node = context.get("node", {})
        reports = context.get("reports", [])
        
        # Log what we received for debugging
        logger.info(f"AI Chat request - Node: {node.get('name')}, Reports count: {len(reports)}")
        if reports and len(reports) > 0:
            logger.info(f"First report sample: {reports[0]}")
        
        # Build a response based on the message and reports
        if not reports:
            response = f"I don't have any reports available for {node.get('name', 'this node')}. Once reports are generated, I can help analyze them."
        else:
            report_count = len(reports)
            
            # Build a simple, direct prompt with all report data
            prompt = f"""You are a military intelligence analyst AI. Analyze these battlefield reports and answer the user's question.

Node: {node.get('name', 'Unknown')}
User Question: {message}

Reports ({report_count} total):
"""
            
            # Add all reports with full details (limit to 50 to avoid token overload)
            for i, report in enumerate(reports[:50], 1):
                try:
                    # Handle both original backend format and transformed frontend format
                    report_type = report.get('report_type') or report.get('type', 'UNKNOWN')
                    soldier_name = report.get('soldier_name') or report.get('from', 'Unknown')
                    timestamp = report.get('timestamp') or report.get('time', 'unknown')
                    
                    # Get structured data - could be in 'structured_json' or 'data' field
                    if 'structured_json' in report:
                        structured = json.loads(report.get("structured_json", "{}")) if isinstance(report.get("structured_json"), str) else report.get("structured_json", {})
                    else:
                        structured = report.get('data', {})
                    
                    prompt += f"\n{i}. [{report_type}] from {soldier_name} at {timestamp}\n"
                    prompt += f"   Data: {json.dumps(structured)}\n"
                except Exception as e:
                    logger.error(f"Error parsing report {i}: {e}")
                    logger.error(f"Report structure: {report}")
                    continue
            
            if report_count > 50:
                prompt += f"\n... and {report_count - 50} more reports (showing first 50)\n"
            
            prompt += "\n\nProvide a direct, clear answer using military terminology. Be concise and actionable."
            
            try:
                # Call Gemini API with safety settings to avoid blocks
                gemini_response = gemini_model.generate_content(
                    prompt,
                    safety_settings={
                        'HARM_CATEGORY_HARASSMENT': 'BLOCK_NONE',
                        'HARM_CATEGORY_HATE_SPEECH': 'BLOCK_NONE',
                        'HARM_CATEGORY_SEXUALLY_EXPLICIT': 'BLOCK_NONE',
                        'HARM_CATEGORY_DANGEROUS_CONTENT': 'BLOCK_NONE',
                    }
                )
                response = gemini_response.text
                logger.info(f"Gemini API success: Generated response for {report_count} reports")
            except Exception as e:
                logger.error(f"Gemini API error: {e}")
                # Simple fallback without confusing prompts
                response = f"Error: Unable to connect to AI service. Raw data: {report_count} reports available from {node.get('name')}. Please try again."
        
        return {
            "response": response,
            "timestamp": datetime.now().isoformat(),
            "reports_analyzed": len(reports)
        }
        
    except Exception as e:
        logger.error(f"Error in AI chat: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing chat request: {str(e)}")

@app.post("/frago/suggest")
async def suggest_frago(request: FRAGOSuggestRequest):
    """
    Analyze reports and suggest FRAGO fields using AI.
    """
    try:
        unit_name = request.unit_name
        reports = request.reports
        
        logger.info(f"FRAGO Suggest - Unit: {unit_name}, Reports: {len(reports)}")
        
        if not reports:
            raise HTTPException(status_code=400, detail="No reports available for analysis")
        
        # Build comprehensive prompt for FRAGO generation
        prompt = f"""You are a military operations officer AI. Analyze these battlefield reports and suggest a FRAGMENTARY ORDER (FRAGO) for {unit_name} and its subordinate units.

A FRAGO modifies an existing operation order. Use the 5-paragraph format:
1. SITUATION - Enemy forces, friendly forces, attachments/detachments
2. MISSION - Who, what, when, where, and why (task and purpose)
3. EXECUTION - Concept of operations, tasks to subordinate units, coordinating instructions
4. SERVICE SUPPORT - Logistics, medical, transportation
5. COMMAND AND SIGNAL - Command posts, succession of command, communications

REPORTS FROM {unit_name} ({len(reports)} total):
"""
        
        # Add all reports with full context
        for i, report in enumerate(reports[:100], 1):  # Limit to 100 for token management
            try:
                report_type = report.get('report_type') or report.get('type', 'UNKNOWN')
                soldier_name = report.get('soldier_name') or report.get('from', 'Unknown')
                timestamp = report.get('timestamp') or report.get('time', 'unknown')
                
                if 'structured_json' in report:
                    structured = json.loads(report.get("structured_json", "{}")) if isinstance(report.get("structured_json"), str) else report.get("structured_json", {})
                else:
                    structured = report.get('data', {})
                
                prompt += f"\n{i}. [{report_type}] from {soldier_name} at {timestamp}\n"
                prompt += f"   {json.dumps(structured)}\n"
            except Exception as e:
                logger.error(f"Error parsing report {i}: {e}")
                continue
        
        if len(reports) > 100:
            prompt += f"\n... and {len(reports) - 100} more reports\n"
        
        prompt += """\n\nBased on these reports, suggest a FRAGO with the following JSON structure:
{
  "situation": "Brief enemy and friendly situation update",
  "mission": "Clear mission statement with task and purpose",
  "execution": "Concept of operations and key tasks",
  "service_support": "Logistics and support requirements",
  "command_signal": "Command post locations and communication plan"
}

Provide ONLY the JSON object, no additional text."""
        
        try:
            # Call Gemini API
            gemini_response = gemini_model.generate_content(
                prompt,
                safety_settings={
                    'HARM_CATEGORY_HARASSMENT': 'BLOCK_NONE',
                    'HARM_CATEGORY_HATE_SPEECH': 'BLOCK_NONE',
                    'HARM_CATEGORY_SEXUALLY_EXPLICIT': 'BLOCK_NONE',
                    'HARM_CATEGORY_DANGEROUS_CONTENT': 'BLOCK_NONE',
                }
            )
            
            response_text = gemini_response.text.strip()
            
            # Try to extract JSON from response (handle markdown code blocks)
            if "```json" in response_text:
                json_start = response_text.find("```json") + 7
                json_end = response_text.find("```", json_start)
                response_text = response_text[json_start:json_end].strip()
            elif "```" in response_text:
                json_start = response_text.find("```") + 3
                json_end = response_text.find("```", json_start)
                response_text = response_text[json_start:json_end].strip()
            
            suggested_fields = json.loads(response_text)
            
            logger.info(f"FRAGO suggestion generated successfully for {unit_name}")
            
            return {
                "suggested_fields": suggested_fields,
                "reports_analyzed": len(reports),
                "timestamp": datetime.now().isoformat()
            }
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Gemini response as JSON: {e}")
            logger.error(f"Response text: {response_text}")
            # Return a fallback structure
            return {
                "suggested_fields": {
                    "situation": f"Analysis of {len(reports)} reports from {unit_name}",
                    "mission": "Continue current operations with increased vigilance",
                    "execution": "Maintain current posture and report any changes",
                    "service_support": "Continue current logistics operations",
                    "command_signal": "No changes to command structure"
                },
                "reports_analyzed": len(reports),
                "timestamp": datetime.now().isoformat(),
                "warning": "AI response parsing failed, using fallback template"
            }
        
    except Exception as e:
        logger.error(f"Error in FRAGO suggest: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating FRAGO suggestion: {str(e)}")

@app.post("/frago/generate")
async def generate_frago(request: FRAGOGenerateRequest):
    """
    Generate and save a formatted FRAGO document.
    """
    try:
        conn = get_db_connection()
        c = conn.cursor()
        
        # Get next FRAGO number
        c.execute("SELECT next_number FROM frago_sequence WHERE id = 1")
        frago_number = c.fetchone()[0]
        
        # Increment sequence
        c.execute("UPDATE frago_sequence SET next_number = next_number + 1 WHERE id = 1")
        
        # Format FRAGO document
        fields = request.frago_fields
        unit_name = request.unit_name
        timestamp = datetime.now()
        
        formatted_doc = f"""FRAGMENTARY ORDER {frago_number:04d}
{unit_name}
{timestamp.strftime('%d%H%M%S %b %Y').upper()}

1. SITUATION
{fields.get('situation', 'No change to current situation.')}

2. MISSION
{fields.get('mission', 'Continue current mission.')}

3. EXECUTION
{fields.get('execution', 'No change to current execution.')}

4. SERVICE SUPPORT
{fields.get('service_support', 'Continue current support operations.')}

5. COMMAND AND SIGNAL
{fields.get('command_signal', 'No change to command and signal.')}

ACKNOWLEDGE.
//END OF FRAGO//
"""
        
        # Save to database
        frago_id = str(uuid.uuid4())
        c.execute("""
            INSERT INTO fragos (
                frago_id, frago_number, unit_id, created_at, 
                suggested_fields, final_fields, formatted_document, source_reports
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            frago_id,
            frago_number,
            request.unit_id,
            timestamp.isoformat(),
            json.dumps(fields),  # For this version, suggested = final
            json.dumps(fields),
            formatted_doc,
            json.dumps(request.source_report_ids)
        ))
        
        conn.commit()
        conn.close()
        
        logger.info(f"FRAGO {frago_number:04d} generated for {unit_name}")
        
        return {
            "frago_id": frago_id,
            "frago_number": frago_number,
            "formatted_document": formatted_doc,
            "timestamp": timestamp.isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error generating FRAGO: {e}")
        raise HTTPException(status_code=500, detail=f"Error generating FRAGO: {str(e)}")

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
