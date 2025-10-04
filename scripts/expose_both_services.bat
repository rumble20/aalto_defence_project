@echo off
echo ========================================
echo Military Hierarchy System - Expose Both Services
echo ========================================
echo.

:: --- Step 1: Start Backend API ---
echo Step 1: Starting Backend API...
start "Backend API" cmd /k "cd /d %~dp0.. && python backend.py"

echo Waiting 10 seconds for backend to start...
timeout /t 10 /nobreak > nul

:: --- Step 2: Start Unified Dashboard ---
echo.
echo Step 2: Starting Unified Dashboard...
start "Unified Dashboard" cmd /k "cd /d %~dp0..\mil_dashboard && npm run dev"

echo Waiting 10 seconds for dashboard to start...
timeout /t 10 /nobreak > nul

:: --- Step 3: Start ngrok tunnels ---
echo.
echo Step 3: Starting ngrok tunnels for BOTH services...
echo.

:: Kill any previous ngrok instances to avoid ERR_NGROK_334
echo Checking for existing ngrok processes...
taskkill /IM ngrok.exe /F > nul 2>&1

echo Starting Backend API tunnel (Port 8000)...
start "ngrok Backend API" cmd /k "cd /d %~dp0..\ngrok && ngrok.exe http 8000"

echo Waiting 5 seconds...
timeout /t 5 /nobreak > nul

echo.
echo Starting Unified Dashboard tunnel (Port 3000)...
start "ngrok Unified Dashboard" cmd /k "cd /d %~dp0..\ngrok && ngrok.exe http 3000"

:: --- Final Info ---
echo.
echo ========================================
echo SETUP COMPLETE!
echo ========================================
echo.
echo Your Military Hierarchy System is now running!
echo.
echo Check the ngrok windows for your public URLs:
echo - Backend API: https://xxxxx.ngrok-free.dev  (for POST requests)
echo - Unified Dashboard: https://yyyyy.ngrok-free.dev  (for UI)
echo.
echo Local URLs:
echo - Backend API: http://localhost:8000
echo - Unified Dashboard: http://localhost:3000
echo.
echo IMPORTANT:
echo - Each service has its own unique ngrok URL.
echo - Use Backend API URL for POST requests from external apps.
echo - Use Dashboard URL for the web interface.
echo.
echo Press any key to exit...
pause > nul
