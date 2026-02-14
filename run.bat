@echo off
setlocal

set "PROJECT_ROOT=C:\XUA-Backtest-Service"
set "BACKEND_DIR=%PROJECT_ROOT%\backend"
set "FRONTEND_DIR=%PROJECT_ROOT%\frontend"

if not exist "%PROJECT_ROOT%" (
    echo Project folder not found at C:\XUA-Backtest-Service
    pause
    exit /b
)

echo Starting Backend...
start "XUA Backend" cmd /k "cd /d "%BACKEND_DIR%" && call venv\Scripts\activate.bat && uvicorn main:app --host 127.0.0.1 --port 8000"

timeout /t 5 /nobreak >nul

echo Starting Frontend...
start "XUA Frontend" cmd /k "cd /d "%FRONTEND_DIR%" && yarn dev"

timeout /t 6 /nobreak >nul

start "" "http://localhost:3000"

echo.
echo Service is running.
echo Close the opened terminal windows to stop the system.
echo.

endlocal
