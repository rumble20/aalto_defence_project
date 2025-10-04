@echo off
REM ----------------------------
REM Windows one-command setup
REM ----------------------------

REM --- Step 1: Install Python dependencies ---
echo Installing Python dependencies...
pip install -r backend\requirements.txt

REM --- Step 2: Start Mosquitto ---
echo Make sure Mosquitto is installed!
echo If not, download from https://mosquitto.org/download/ or install via Chocolatey.
start "" "C:\Program Files\mosquitto\mosquitto.exe"

REM --- Step 3: Start Python backend ---
echo Starting Python backend...
start "" python backend.py

REM --- Step 4: Start Next.js frontend ---
echo Starting Main Dashboard...
cd mil_dashboard
npm install --legacy-peer-deps
start "" npm run dev

REM Optionally, start Reports UI in another terminal
cd ..\ui-for-reports\frontend
npm install --legacy-peer-deps
start "" npm run dev

echo All services started. Press any key to continue...
pause
