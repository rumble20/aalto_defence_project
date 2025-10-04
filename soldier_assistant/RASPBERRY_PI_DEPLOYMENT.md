# Raspberry Pi Deployment Guide for Soldier Assistant

## 🎯 Overview
This guide explains how to deploy the soldier assistant to a Raspberry Pi and connect it to the main backend system via MQTT.

## 📋 Prerequisites
- Raspberry Pi 4 (recommended) or Pi 3B+
- MicroSD card (32GB+ recommended)
- USB microphone
- Internet connection
- Access to the main backend system

## 🚀 Quick Setup

### 1. Install Raspberry Pi OS
```bash
# Download Raspberry Pi Imager
# Flash Raspberry Pi OS Lite (64-bit) to microSD card
# Enable SSH and configure WiFi during imaging
```

### 2. Initial Pi Setup
```bash
# SSH into your Pi
ssh pi@<pi_ip_address>

# Update system
sudo apt update && sudo apt upgrade -y

# Install required packages
sudo apt install -y python3-pip python3-venv mosquitto mosquitto-clients portaudio19-dev git

# Clone the project (or copy files)
git clone <your_repo_url>
cd aalto_defence_project/soldier_assistant
```

### 3. Configure MQTT Broker
```bash
# Start Mosquitto
sudo systemctl start mosquitto
sudo systemctl enable mosquitto

# Test MQTT connection
mosquitto_pub -h localhost -t test -m "hello"
mosquitto_sub -h localhost -t test
```

### 4. Configure Soldier Assistant
```bash
# Edit configuration
nano config/settings.env

# Set your configuration:
MQTT_HOST=localhost
MQTT_PORT=1883
MQTT_USER=
MQTT_PASS=
SOLDIER_ID=soldier_001
SOLDIER_NAME=Alpha_Soldier
UNIT_ID=unit_001
PICOVOICE_ACCESS_KEY=your_key_here
BACKEND_API_URL=http://your_backend_ip:8000
BACKEND_MQTT_TOPIC=soldiers/inputs
```

### 5. Install Dependencies
```bash
# Run setup script
chmod +x scripts/setup.sh
./scripts/setup.sh

# Or manually:
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 6. Test Audio Setup
```bash
# Test microphone
arecord -l  # List audio devices
arecord -f cd -d 5 test.wav  # Record 5 seconds
aplay test.wav  # Play back

# Test with Python
python3 -c "import sounddevice as sd; print(sd.query_devices())"
```

## 🔧 Configuration for Different Soldiers

### Soldier 1 (Alpha Team)
```bash
# config/settings.env
SOLDIER_ID=soldier_001
SOLDIER_NAME=Alpha_Soldier
UNIT_ID=unit_001
```

### Soldier 2 (Bravo Team)
```bash
# config/settings.env
SOLDIER_ID=soldier_002
SOLDIER_NAME=Bravo_Soldier
UNIT_ID=unit_002
```

## 🌐 Network Configuration

### Option 1: Local Network (Same WiFi)
```bash
# Backend runs on: 192.168.1.100:8000
# Pi connects to: 192.168.1.100:1883

# In config/settings.env:
MQTT_HOST=192.168.1.100
BACKEND_API_URL=http://192.168.1.100:8000
```

### Option 2: Internet via ngrok
```bash
# Backend exposed via ngrok: https://abc123.ngrok-free.dev
# MQTT still needs local network or port forwarding

# In config/settings.env:
MQTT_HOST=192.168.1.100  # Still needs local MQTT
BACKEND_API_URL=https://abc123.ngrok-free.dev
```

## 🚀 Running the Assistant

### Manual Start
```bash
cd /path/to/soldier_assistant
source .venv/bin/activate
python -m assistant.main
```

### Auto-start on Boot
```bash
# Create systemd service
sudo nano /etc/systemd/system/soldier-assistant.service

# Add this content:
[Unit]
Description=Soldier Assistant
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/aalto_defence_project/soldier_assistant
ExecStart=/home/pi/aalto_defence_project/soldier_assistant/.venv/bin/python -m assistant.main
Restart=always

[Install]
WantedBy=multi-user.target

# Enable and start
sudo systemctl enable soldier-assistant
sudo systemctl start soldier-assistant
sudo systemctl status soldier-assistant
```

## 🔍 Troubleshooting

### MQTT Connection Issues
```bash
# Check if Mosquitto is running
sudo systemctl status mosquitto

# Check MQTT logs
sudo journalctl -u mosquitto -f

# Test MQTT connection
mosquitto_pub -h localhost -t soldiers/inputs -m '{"test": "message"}'
```

### Audio Issues
```bash
# Check audio devices
arecord -l
python3 -c "import sounddevice as sd; print(sd.query_devices())"

# Test microphone
python3 -c "
import sounddevice as sd
import numpy as np
import time

def callback(indata, frames, time, status):
    print(f'Recording: {np.max(indata):.3f}')

with sd.InputStream(callback=callback):
    time.sleep(5)
"
```

### Wake Word Issues
```bash
# Check Picovoice key
echo $PICOVOICE_ACCESS_KEY

# Test wake word detection
python3 -c "
from assistant.wake import wait_for_wake_word
print('Say wake word...')
wait_for_wake_word()
print('Wake word detected!')
"
```

## 📊 Monitoring

### View Logs
```bash
# System logs
sudo journalctl -u soldier-assistant -f

# MQTT messages
mosquitto_sub -h localhost -t "soldiers/inputs" -v
mosquitto_sub -h localhost -t "soldiers/heartbeat" -v
```

### Check Backend Integration
```bash
# Check if messages reach backend
curl http://your_backend_ip:8000/reports
curl http://your_backend_ip:8000/hierarchy
```

## 🔄 Updates

### Update Soldier Assistant
```bash
cd /path/to/soldier_assistant
git pull
source .venv/bin/activate
pip install -r requirements.txt
sudo systemctl restart soldier-assistant
```

## 📱 Mobile App Integration

The soldier assistant can be integrated with mobile apps by:
1. **Direct MQTT**: Mobile app connects to same MQTT broker
2. **Backend API**: Mobile app sends data via REST API
3. **WebSocket**: Real-time communication via WebSocket

### Example Mobile Integration
```javascript
// Connect to MQTT broker
const mqtt = require('mqtt');
const client = mqtt.connect('mqtt://your_backend_ip:1883');

// Subscribe to soldier inputs
client.subscribe('soldiers/inputs');
client.on('message', (topic, message) => {
    const data = JSON.parse(message);
    console.log('Soldier input:', data);
});
```

## 🎯 Production Deployment

### Security Considerations
1. **MQTT Authentication**: Enable username/password
2. **TLS Encryption**: Use MQTT over TLS
3. **Firewall**: Restrict MQTT port access
4. **VPN**: Use VPN for remote connections

### Performance Optimization
1. **Audio Quality**: Adjust sample rate and bit depth
2. **Model Size**: Use smaller Vosk models for faster processing
3. **Network**: Use wired connection for stability
4. **Power**: Use proper power supply for Pi

## 📞 Support

For issues:
1. Check logs: `sudo journalctl -u soldier-assistant -f`
2. Test MQTT: `mosquitto_sub -h localhost -t "soldiers/inputs" -v`
3. Test audio: `arecord -f cd -d 5 test.wav && aplay test.wav`
4. Check network: `ping your_backend_ip`
