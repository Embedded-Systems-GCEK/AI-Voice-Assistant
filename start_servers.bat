@echo off
title AI Voice Assistant - Multi-Server Launcher

echo.
echo =====================================================
echo    🤖 AI VOICE ASSISTANT - UNIFIED SERVER LAUNCHER
echo =====================================================
echo.

:: Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python.
    pause
    exit /b 1
)

echo ✅ Python found
echo.
echo 📋 Starting servers...
echo.

:: Change to script directory
cd /d "%~dp0"

:: Start API Server
echo 🚀 Starting API Server (Port 5001)...
start "API Server" cmd /k python src/server/server.py

:: Wait a bit
timeout /t 3 /nobreak >nul

:: Start Unified Server  
echo 🚀 Starting Unified Server (Port 5000)...
start "Unified Server" cmd /k python server/server.py

echo.
echo ✅ All servers are starting in separate windows!
echo.
echo 🔗 Server URLs:
echo    • API Server:      http://localhost:5001
echo    • Unified Server:  http://localhost:5000
echo.
echo 📱 Flutter Integration:
echo    Use http://localhost:5001 as your base URL
echo.
echo 🧪 To test the APIs, run:
echo    python launcher.py --test
echo.
echo 📖 For Flutter integration guide, run:
echo    python launcher.py --guide
echo.
echo Press any key to exit...
pause >nul
