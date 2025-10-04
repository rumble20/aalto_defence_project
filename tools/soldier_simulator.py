"""
Soldier Device Simulator
Simulates a Raspberry Pi soldier device sending voice inputs via MQTT
"""

import paho.mqtt.client as mqtt
import json
import time
import random
from datetime import datetime

class SoldierSimulator:
    def __init__(self, soldier_id: str, device_id: str):
        self.soldier_id = soldier_id
        self.device_id = device_id
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_publish = self.on_publish
        
        # Sample voice inputs from the field
        self.sample_inputs = [
            "Enemy vehicle spotted north of the road, looks like a T-72 tank",
            "Squad is in position, no contact yet",
            "Need medical evacuation, one casualty at grid 123-456",
            "Moving to secondary position, will report when in place",
            "Company is advancing on objective, all platoons moving",
            "Artillery fire incoming, taking cover",
            "Objective secured, awaiting further orders",
            "Fuel low, need resupply at next checkpoint",
            "Weather deteriorating, visibility reduced to 100 meters",
            "Enemy unit withdrawing to the east",
            "Friendly fire incident, need immediate medical support",
            "Bridge ahead is clear, proceeding with caution",
            "Night vision equipment malfunctioning",
            "Communications restored, back online",
            "Mission complete, returning to base"
        ]
        
        self.report_types = [
            "SITREP", "EOINCREP", "CASEVAC", "FRAGO", "OPORD"
        ]

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print(f"Soldier {self.soldier_id} connected to MQTT broker")
        else:
            print(f"Soldier {self.soldier_id} failed to connect. Return code: {rc}")

    def on_publish(self, client, userdata, mid):
        print(f"Soldier {self.soldier_id} published message {mid}")

    def connect(self, host="localhost", port=1883):
        """Connect to MQTT broker."""
        try:
            self.client.connect(host, port, 60)
            self.client.loop_start()
            return True
        except Exception as e:
            print(f"Failed to connect: {e}")
            return False

    def send_voice_input(self, raw_text: str):
        """Send a voice input message."""
        message = {
            "soldier_id": self.soldier_id,
            "device_id": self.device_id,
            "timestamp": datetime.now().isoformat(),
            "raw_text": raw_text,
            "audio_file_ref": f"audio_{self.soldier_id}_{int(time.time())}.wav"
        }
        
        self.client.publish("soldiers/inputs", json.dumps(message))
        print(f"Soldier {self.soldier_id}: {raw_text}")

    def send_heartbeat(self):
        """Send a heartbeat message."""
        message = {
            "soldier_id": self.soldier_id,
            "device_id": self.device_id,
            "timestamp": datetime.now().isoformat(),
            "status": "active"
        }
        
        self.client.publish("soldiers/heartbeat", json.dumps(message))

    def simulate_random_input(self):
        """Send a random voice input."""
        input_text = random.choice(self.sample_inputs)
        self.send_voice_input(input_text)

    def run_simulation(self, duration_minutes=5, input_interval=30):
        """Run simulation for specified duration."""
        print(f"Starting simulation for soldier {self.soldier_id} for {duration_minutes} minutes")
        
        start_time = time.time()
        end_time = start_time + (duration_minutes * 60)
        last_input_time = 0
        
        while time.time() < end_time:
            current_time = time.time()
            
            # Send heartbeat every 60 seconds
            if int(current_time) % 60 == 0:
                self.send_heartbeat()
            
            # Send random input every input_interval seconds
            if current_time - last_input_time >= input_interval:
                self.simulate_random_input()
                last_input_time = current_time
            
            time.sleep(1)
        
        print(f"Simulation completed for soldier {self.soldier_id}")

    def disconnect(self):
        """Disconnect from MQTT broker."""
        self.client.loop_stop()
        self.client.disconnect()

def main():
    """Run multiple soldier simulators."""
    soldiers = [
        ("ALPHA_01", "DEVICE_001"),
        ("ALPHA_02", "DEVICE_002"),
        ("ALPHA_03", "DEVICE_003"),
        ("BRAVO_01", "DEVICE_005"),
    ]
    
    simulators = []
    
    # Create and connect simulators
    for soldier_id, device_id in soldiers:
        simulator = SoldierSimulator(soldier_id, device_id)
        if simulator.connect():
            simulators.append(simulator)
        time.sleep(1)  # Stagger connections
    
    if not simulators:
        print("No simulators connected. Make sure MQTT broker is running.")
        return
    
    print(f"Running {len(simulators)} soldier simulators...")
    print("Press Ctrl+C to stop")
    
    try:
        while True:
            # Randomly select a simulator to send input
            simulator = random.choice(simulators)
            simulator.simulate_random_input()
            
            # Wait random interval (10-60 seconds)
            time.sleep(random.randint(10, 60))
            
    except KeyboardInterrupt:
        print("\nStopping simulators...")
        for simulator in simulators:
            simulator.disconnect()
        print("All simulators stopped.")

if __name__ == "__main__":
    main()
