# AI Voice Assistant - Multi-Server Launcher
# PowerShell script to start all servers

Write-Host "🤖 AI VOICE ASSISTANT - MULTI-SERVER LAUNCHER" -ForegroundColor Green
Write-Host "=" * 60 -ForegroundColor Green
Write-Host ""

# Check if Python is available
try {
    $pythonVersion = python --version
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found. Please install Python." -ForegroundColor Red
    exit 1
}

# Change to script directory
Set-Location $PSScriptRoot

Write-Host "📋 Starting servers..." -ForegroundColor Yellow
Write-Host ""

# Start servers in separate PowerShell windows
Write-Host "🚀 Starting API Server (Port 5001)..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "python api_server.py"

Start-Sleep 3

Write-Host "🚀 Starting Unified Server (Port 5000)..." -ForegroundColor Blue  
Start-Process powershell -ArgumentList "-NoExit", "-Command", "python server/server.py"

Write-Host ""
Write-Host "✅ All servers are starting in separate windows!" -ForegroundColor Green
Write-Host ""
Write-Host "🔗 Server URLs:" -ForegroundColor Yellow
Write-Host "   • API Server:      http://localhost:5001" -ForegroundColor White
Write-Host "   • Unified Server:  http://localhost:5000" -ForegroundColor White  
Write-Host ""
Write-Host "📱 Flutter Integration:" -ForegroundColor Yellow
Write-Host "   Use http://localhost:5001 as your base URL for Flutter apps" -ForegroundColor White
Write-Host "   Use http://localhost:5000 for web UI and general API access" -ForegroundColor White
Write-Host ""
Write-Host "🧪 To test the APIs, run:" -ForegroundColor Yellow
Write-Host "   python launcher.py --test" -ForegroundColor White
Write-Host ""
Write-Host "📖 For Flutter integration guide, run:" -ForegroundColor Yellow  
Write-Host "   python launcher.py --guide" -ForegroundColor White
Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Gray
Read-Host
