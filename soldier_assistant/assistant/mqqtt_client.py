import paho.mqtt.client as mqtt
import json
from datetime import datetime

# Hardcoded configuration
MQTT_HOST = "localhost"
MQTT_PORT = 1883
SOLDIER_ID = "soldier_001"
SOLDIER_NAME = "Alpha_Soldier"
UNIT_ID = "unit_001"
BACKEND_TOPIC = "soldiers/inputs"

print(f"[INFO] Connecting to MQTT broker at {MQTT_HOST}:{MQTT_PORT}")
print(f"[INFO] Soldier ID: {SOLDIER_ID}, Unit ID: {UNIT_ID}")

client = mqtt.Client()
client.connect(MQTT_HOST, MQTT_PORT, 60)
client.loop_start()

print("[INFO] MQTT client connected and running...")

def publish_command(payload):
    """Publish command to backend MQTT topic with soldier context."""
    try:
        # Parse the incoming payload
        if isinstance(payload, str):
            command_data = json.loads(payload)
        else:
            command_data = payload
            
        # Create backend-compatible payload
        backend_payload = {
            "soldier_id": SOLDIER_ID,
            "soldier_name": SOLDIER_NAME,
            "unit_id": UNIT_ID,
            "timestamp": datetime.now().isoformat(),
            "raw_text": command_data.get("text", ""),
            "action": command_data.get("action", "UNKNOWN"),
            "audio_file_ref": None  # Could be added later for audio storage
        }
        
        # Publish to backend topic
        client.publish(BACKEND_TOPIC, json.dumps(backend_payload))
        print(f"[MQTT] Published to {BACKEND_TOPIC}: {json.dumps(backend_payload, indent=2)}")
        
    except Exception as e:
        print(f"[ERROR] Failed to publish command: {e}")

def publish_heartbeat():
    """Publish heartbeat to backend."""
    try:
        heartbeat_payload = {
            "soldier_id": SOLDIER_ID,
            "soldier_name": SOLDIER_NAME,
            "unit_id": UNIT_ID,
            "timestamp": datetime.now().isoformat(),
            "status": "active"
        }
        
        client.publish("soldiers/heartbeat", json.dumps(heartbeat_payload))
        print(f"[MQTT] Published heartbeat: {json.dumps(heartbeat_payload, indent=2)}")
        
    except Exception as e:
        print(f"[ERROR] Failed to publish heartbeat: {e}")