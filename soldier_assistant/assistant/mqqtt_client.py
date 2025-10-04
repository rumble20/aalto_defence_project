from dotenv import load_dotenv
import os
import paho.mqtt.client as mqtt

load_dotenv(dotenv_path="config/settings.env")

# Access config variables
mqtt_host = os.getenv("MQTT_HOST")
mqtt_port = int(os.getenv("MQTT_PORT"))
mqtt_user = os.getenv("MQTT_USER")
mqtt_pass = os.getenv("MQTT_PASS")

print(f"[INFO] Connecting to MQTT broker at {mqtt_host}:{mqtt_port} as {mqtt_user or 'anonymous'}")

client = mqtt.Client()
if mqtt_user and mqtt_pass:
    client.username_pw_set(mqtt_user, mqtt_pass)

client.connect(mqtt_host, mqtt_port)
client.loop_start()

print("[INFO] MQTT client connected and running...")

def publish_command(subject, action):
    topic = str(subject)
    payload = str(action)
    client.publish(topic, payload)
    print(f"[MQTT] Published to {topic}: {payload}")