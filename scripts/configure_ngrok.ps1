# Configure ngrok with authtoken
Write-Host "Configuring ngrok with authtoken..." -ForegroundColor Green

# Try different possible locations for ngrok
$ngrokPaths = @(
    "ngrok",
    "C:\Users\henri\AppData\Local\Microsoft\WindowsApps\ngrok.exe",
    "C:\Program Files\ngrok\ngrok.exe",
    "C:\Program Files (x86)\ngrok\ngrok.exe"
)

$ngrokFound = $false
foreach ($path in $ngrokPaths) {
    try {
        if ($path -eq "ngrok") {
            $result = & ngrok version 2>$null
            if ($LASTEXITCODE -eq 0) {
                Write-Host "Found ngrok in PATH" -ForegroundColor Green
                & ngrok config add-authtoken 33bQDyBGjGsGrNXeqEVbMkqY5v7_2EAARiJ7eGPMa4stCVZ62
                $ngrokFound = $true
                break
            }
        } else {
            if (Test-Path $path) {
                Write-Host "Found ngrok at: $path" -ForegroundColor Green
                & $path config add-authtoken 33bQDyBGjGsGrNXeqEVbMkqY5v7_2EAARiJ7eGPMa4stCVZ62
                $ngrokFound = $true
                break
            }
        }
    } catch {
        # Continue to next path
    }
}

if (-not $ngrokFound) {
    Write-Host "ngrok not found. Please install ngrok from Microsoft Store or download from ngrok.com" -ForegroundColor Red
    Write-Host "After installing, run this script again." -ForegroundColor Yellow
} else {
    Write-Host "ngrok configured successfully!" -ForegroundColor Green
    Write-Host "You can now run: setup_complete_system.bat" -ForegroundColor Cyan
}
