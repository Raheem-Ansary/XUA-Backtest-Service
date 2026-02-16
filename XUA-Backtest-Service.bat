@echo off
setlocal EnableExtensions

set "PROJECT_ROOT=C:\XUA-Backtest-Service"

if not exist "%PROJECT_ROOT%\backend\main.py" (
    echo [ERROR] Backend entry not found: "%PROJECT_ROOT%\backend\main.py"
    echo Update PROJECT_ROOT in this file to your real repo path.
    pause
    exit /b 1
)

if not exist "%PROJECT_ROOT%\frontend\package.json" (
    echo [ERROR] Frontend entry not found: "%PROJECT_ROOT%\frontend\package.json"
    echo Update PROJECT_ROOT in this file to your real repo path.
    pause
    exit /b 1
)

set "BACKEND_ACTIVATE="
if exist "%PROJECT_ROOT%\backend\.venv\Scripts\activate.bat" (
    set "BACKEND_ACTIVATE=%PROJECT_ROOT%\backend\.venv\Scripts\activate.bat"
) else if exist "%PROJECT_ROOT%\backend\venv\Scripts\activate.bat" (
    set "BACKEND_ACTIVATE=%PROJECT_ROOT%\backend\venv\Scripts\activate.bat"
)

if defined BACKEND_ACTIVATE (
    start "XUA Backend" cmd /k "cd /d \"%PROJECT_ROOT%\" && call \"%BACKEND_ACTIVATE%\" && python -m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000"
) else (
    start "XUA Backend" cmd /k "cd /d \"%PROJECT_ROOT%\" && python -m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000"
)

start "XUA Frontend" cmd /k "cd /d \"%PROJECT_ROOT%\frontend\" && set NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000 && yarn dev"

timeout /t 3 /nobreak >NUL
start "" "http://localhost:3000"

echo Started backend and frontend.
echo Close the opened command windows to stop services.
exit /b 0
