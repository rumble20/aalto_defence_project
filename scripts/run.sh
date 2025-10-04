#!/bin/bash

# --- Step 0: Define paths ---
BACKEND_DIR="./"
FRONTEND_DIR="./mil_dashboard"

# --- Step 1: Install Python dependencies ---
echo "Installing Python dependencies..."
if [ -f "$BACKEND_DIR/requirements.txt" ]; then
    pip3 install --upgrade pip
    pip3 install -r "$BACKEND_DIR/requirements.txt"
else
    echo "No requirements.txt found in $BACKEND_DIR"
fi

# --- Step 2: Install and start Mosquitto if not installed ---
if ! command -v mosquitto &> /dev/null
then
    echo "Mosquitto not found. Installing..."
    # Linux (Debian/Ubuntu)
    sudo apt update
    sudo apt install -y mosquitto
    sudo systemctl enable mosquitto
    sudo systemctl start mosquitto
else
    echo "Mosquitto found, starting..."
    sudo systemctl start mosquitto || mosquitto -d
fi

# --- Step 3: Start Python MQTT server in background ---
echo "Starting Python MQTT server..."
python3 "$BACKEND_DIR/backend.py" &
PYTHON_PID=$!

# --- Step 4: Start Next.js frontend ---
echo "Starting Next.js frontend..."
cd "$FRONTEND_DIR"

# Fix npm React dependency conflicts
npm install --legacy-peer-deps

npm run dev &   # run frontend in background
FRONTEND_PID=$!

# --- Step 5: Wait for processes ---
echo "All services are running. Press Ctrl+C to stop."
trap "echo 'Stopping servers...'; kill $PYTHON_PID $FRONTEND_PID; exit" SIGINT SIGTERM
wait
