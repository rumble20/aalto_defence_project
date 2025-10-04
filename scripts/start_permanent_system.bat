@echo off
echo ========================================
echo Military Hierarchy System - Permanent URLs
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
echo Step 4: Starting ngrok tunnels with permanent URLs...
echo.

echo Starting Backend API tunnel (PERMANENT URL)...
start "ngrok Backend API (PERMANENT)" cmd /k "cd /d %~dp0 && ngrok.exe http 8000 --domain=military-api.ngrok.io"

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
echo Your Military Hierarchy System is now running with PERMANENT URLs!
echo.
echo PERMANENT URL (never changes):
echo - Backend API: https://military-api.ngrok.io
echo - API Documentation: https://military-api.ngrok.io/docs
echo.
echo Regular URLs (check ngrok windows for these):
echo - Main Dashboard: https://xxxxx.ngrok-free.dev
echo - Reports UI: https://yyyyy.ngrok-free.dev
echo.
echo Share the PERMANENT URL with anyone, anywhere!
echo https://military-api.ngrok.io
echo.
echo Press any key to exit...
pause > nul
