@echo off
echo ========================================
echo Military Hierarchy System with ngrok
echo ========================================
echo.

echo Step 1: Starting Backend API...
start "Backend API" cmd /k "cd /d %~dp0 && python backend.py"

echo Waiting 5 seconds for backend to start...
timeout /t 5 /nobreak > nul

echo.
echo Step 2: Starting Main Dashboard...
start "Main Dashboard" cmd /k "cd /d %~dp0\mil_dashboard && npm run dev"

echo Waiting 3 seconds for dashboard to start...
timeout /t 3 /nobreak > nul

echo.
echo Step 3: Starting Reports UI...
start "Reports UI" cmd /k "cd /d %~dp0\ui-for-reports\frontend && npm run dev"

echo Waiting 3 seconds for reports UI to start...
timeout /t 3 /nobreak > nul

echo.
echo Step 4: Starting ngrok tunnels...
echo.

echo Starting Backend API tunnel (port 8000)...
start "ngrok Backend API" cmd /k "ngrok http 8000"

echo.
echo Starting Main Dashboard tunnel (port 3000)...
start "ngrok Main Dashboard" cmd /k "ngrok http 3000"

echo.
echo Starting Reports UI tunnel (port 3001)...
start "ngrok Reports UI" cmd /k "ngrok http 3001"

echo.
echo ========================================
echo SETUP COMPLETE!
echo ========================================
echo.
echo Your services are now running locally and via ngrok!
echo.
echo Look for the "Forwarding" URLs in the ngrok windows:
echo - Backend API: https://xxxxx.ngrok-free.dev
echo - Main Dashboard: https://yyyyy.ngrok-free.dev
echo - Reports UI: https://zzzzz.ngrok-free.dev
echo.
echo Share these URLs with anyone, anywhere!
echo.
echo Press any key to exit...
pause > nul
