@echo off
echo ========================================
echo Military Hierarchy System - Free ngrok
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
echo Step 4: Starting ngrok tunnels (FREE TIER)...
echo.

echo Starting Backend API tunnel...
start "ngrok Backend API" cmd /k "cd /d %~dp0 && ngrok.exe http 8000"

echo.
echo Starting Main Dashboard tunnel...
start "ngrok Main Dashboard" cmd /k "cd /d %~dp0 && ngrok.exe http 3000"

echo.
echo Starting Reports UI tunnel...
start "ngrok Reports UI" cmd /k "cd /d %~dp0 && ngrok.exe http 3001"

echo.
echo ========================================
echo SETUP COMPLETE!
echo ========================================
echo.
echo Your Military Hierarchy System is now running!
echo.
echo Check the ngrok windows for your public URLs:
echo - Backend API: https://xxxxx.ngrok-free.dev
echo - Main Dashboard: https://yyyyy.ngrok-free.dev
echo - Reports UI: https://zzzzz.ngrok-free.dev
echo.
echo NOTE: URLs will change each time you restart ngrok
echo For permanent URLs, upgrade to ngrok Pro plan
echo.
echo Press any key to exit...
pause > nul
