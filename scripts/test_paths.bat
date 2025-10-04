@echo off
echo ========================================
echo Testing Script Paths
echo ========================================
echo.

echo Current script directory: %~dp0
echo.

echo Testing project root access...
cd /d %~dp0..
echo Project root: %CD%
echo.

echo Testing backend.py access...
if exist backend.py (
    echo ✅ backend.py found
) else (
    echo ❌ backend.py not found
)
echo.

echo Testing mil_dashboard access...
if exist mil_dashboard (
    echo ✅ mil_dashboard found
) else (
    echo ❌ mil_dashboard not found
)
echo.

echo Testing ui-for-reports access...
if exist ui-for-reports (
    echo ✅ ui-for-reports found
) else (
    echo ❌ ui-for-reports not found
)
echo.

echo Testing ngrok access...
if exist ngrok\ngrok.exe (
    echo ✅ ngrok.exe found
) else (
    echo ❌ ngrok.exe not found
)
echo.

echo Testing tools access...
if exist tools\check_status.py (
    echo ✅ check_status.py found
) else (
    echo ❌ check_status.py not found
)
echo.

echo ========================================
echo Path Test Complete
echo ========================================
echo.
echo Press any key to exit...
pause > nul
