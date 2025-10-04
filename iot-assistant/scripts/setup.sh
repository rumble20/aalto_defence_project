#!/bin/bash
set -e

echo "[SETUP] Updating and installing dependencies..."
sudo apt update
sudo apt install -y python3-pip python3-venv mosquitto mosquitto-clients portaudio19-dev

echo "[SETUP] Creating virtual environment..."
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo "[SETUP] Creating Mosquitto password file..."
mkdir -p config/mosquitto
mosquitto_passwd -b -c config/mosquitto/passwd admin admin

echo "[SETUP] Copying Mosquitto config to system directory..."
sudo cp config/mosquitto/mosquitto.conf /etc/mosquitto/mosquitto.conf
sudo cp config/mosquitto/passwd /etc/mosquitto/passwd

echo "[SETUP] Enabling and restarting Mosquitto service..."
# sudo systemctl enable mosquitto
# sudo systemctl restart mosquitto

echo "[SETUP] Downloading Vosk model if needed..."
mkdir -p models
cd models

if [ ! -d "vosk-model-en-us-0.22" ]; then
  wget https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip -O vosk_f.zip
  unzip vosk_f.zip && rm vosk_f.zip
fi

if [ ! -d "vosk-model-small-en-us-0.15" ]; then
  wget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip -O vosk_l.zip
  unzip vosk_l.zip && rm vosk_l.zip
fi
cd ..

echo "[SETUP] Done!"

