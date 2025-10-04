@echo off
echo Setting up ngrok for Military Hierarchy System...
echo.

echo Step 1: Downloading ngrok...
powershell -Command "Invoke-WebRequest -Uri 'https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-windows-amd64.zip' -OutFile 'ngrok.zip'"

echo.
echo Step 2: Extracting ngrok...
powershell -Command "Expand-Archive -Path 'ngrok.zip' -DestinationPath '.' -Force"

echo.
echo Step 3: Starting ngrok tunnels...
echo.

echo Starting Backend API tunnel (port 8000)...
start "ngrok Backend API" cmd /k "ngrok http 8000 --log=stdout"

echo.
echo Starting Main Dashboard tunnel (port 3000)...
start "ngrok Main Dashboard" cmd /k "ngrok http 3000 --log=stdout"

echo.
echo Starting Reports UI tunnel (port 3001)...
start "ngrok Reports UI" cmd /k "ngrok http 3001 --log=stdout"

echo.
echo ========================================
echo NGROK SETUP COMPLETE!
echo ========================================
echo.
echo Your services will be available at public URLs shown in the ngrok windows.
echo Look for the "Forwarding" URLs in each ngrok window.
echo.
echo Example URLs (will be different for you):
echo - Backend API: https://abc123.ngrok.io
echo - Main Dashboard: https://def456.ngrok.io  
echo - Reports UI: https://ghi789.ngrok.io
echo.
echo Share these URLs with anyone, anywhere!
echo.
echo Press any key to exit...
pause > nul
