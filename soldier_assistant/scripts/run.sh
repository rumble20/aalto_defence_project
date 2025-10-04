#!/bin/bash
set -e

# Start Mosquitto if not running
# if ! pgrep -x "mosquitto" > /dev/null; then
#     echo "[RUN] Starting Mosquitto broker..."
#     sudo systemctl start mosquitto
# else
#     echo "[RUN] Mosquitto is already running."
# fi

# Activate the virtual environment
source .venv/bin/activate

# Run main
echo "[RUN] Starting assistant..."
python -m assistant.main
