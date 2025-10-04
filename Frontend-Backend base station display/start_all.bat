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
echo System started successfully!
echo.
echo Backend: http://localhost:8000
echo Frontend: http://localhost:3000
echo.
echo Press any key to exit...
pause > nul
