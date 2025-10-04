@echo off
echo ========================================
echo Military Hierarchy System - Working Setup
echo ========================================
echo.

echo Starting Backend API...
start "Backend API" cmd /k "cd /d %~dp0.. && python backend.py"

echo Waiting 10 seconds for backend to start...
timeout /t 10 /nobreak > nul

echo.
echo Starting Main Dashboard...
start "Main Dashboard" cmd /k "cd /d %~dp0..\mil_dashboard && npm run dev"

echo Waiting 10 seconds for dashboard to start...
timeout /t 10 /nobreak > nul

echo.
echo Reports UI integrated into Main Dashboard...
echo (No separate Reports UI needed - unified frontend)

echo.
echo Starting ngrok tunnels...
echo.

echo Starting Backend API tunnel...
start "ngrok Backend API" cmd /k "cd /d %~dp0..\ngrok && ngrok.exe http 8000"

echo.
echo Starting Main Dashboard tunnel...
start "ngrok Main Dashboard" cmd /k "cd /d %~dp0..\ngrok && ngrok.exe http 3000"

echo.
echo Reports UI integrated - no separate tunnel needed...

echo.
echo ========================================
echo SETUP COMPLETE!
echo ========================================
echo.
echo Your Military Hierarchy System is now running!
echo.
echo Check the ngrok windows for your public URLs:
echo - Backend API: https://xxxxx.ngrok-free.dev
echo - Unified Dashboard: https://yyyyy.ngrok-free.dev (includes Reports)
echo.
echo NOTE: URLs will change each time you restart ngrok
echo.
echo Press any key to exit...
pause > nul
