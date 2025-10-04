@echo off
echo Starting Military Hierarchy System...
echo.

echo Activating virtual environment...
call venv\Scripts\activate

echo.
echo Initializing database...
python database_setup.py

echo.
echo Starting backend server in new window...
start "Backend Server" cmd /k "python backend.py"

echo.
echo Waiting 5 seconds for backend to start...
timeout /t 5 /nobreak > nul

echo.
echo Testing API endpoints...
python test_api.py

echo.
echo Starting frontend dashboard in new window...
cd mil_dashboard
start "Frontend Dashboard" cmd /k "npm run dev"

echo.
echo Starting reports UI in new window...
cd ..\ui-for-reports\frontend
start "Reports UI" cmd /k "npm run dev"

echo.
echo System started successfully!
echo.
echo Backend: http://localhost:8000 (or http://10.3.35.27:8000 from other devices)
echo Frontend Dashboard: http://localhost:3000 (or http://10.3.35.27:3000 from other devices)
echo Reports UI: http://localhost:3001 (or http://10.3.35.27:3001 from other devices)
echo.
echo Network Access:
echo - Backend API: http://10.3.35.27:8000
echo - Main Dashboard: http://10.3.35.27:3000
echo - Reports UI: http://10.3.35.27:3001
echo.
echo Press any key to exit...
pause > nul
