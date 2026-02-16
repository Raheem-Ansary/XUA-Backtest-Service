@echo off
setlocal EnableExtensions EnableDelayedExpansion

for %%I in ("%~dp0.") do set "REPO_ROOT=%%~fI"
cd /c "%REPO_ROOT%" || (
    echo [ERROR] Failed to switch to repo root: "%REPO_ROOT%"
    exit /b 1
)

if exist ".venv\Scripts\activate.bat" (
    echo [env] Activating .venv
    call ".venv\Scripts\activate.bat"
) else if exist "backend\venv\Scripts\activate.bat" (
    echo [env] Activating backend\venv
    call "backend\venv\Scripts\activate.bat"
) else (
    echo [env] No virtual environment found. Using system Python.
)

set "BACKEND_LOG=%REPO_ROOT%\backend.log"
if exist "%BACKEND_LOG%" del /f /q "%BACKEND_LOG%"

echo [backend] Starting python -m uvicorn backend.main:app
start "" /b cmd /c "cd /d ""%REPO_ROOT%"" && python -m uvicorn backend.main:app --host 127.0.0.1 --port 8000 --reload 1> ""%BACKEND_LOG%"" 2>&1"

set "OK=0"
for /l %%i in (1,1,30) do (
    set "CODE="
    for /f %%s in ('python -c "import urllib.request;print(urllib.request.urlopen(''http://127.0.0.1:8000/health'', timeout=2).status)" 2^>NUL') do set "CODE=%%s"
    if "!CODE!"=="200" (
        set "OK=1"
        goto :backend_ready
    )
    timeout /t 1 /nobreak >NUL
)

:backend_ready
if not "%OK%"=="1" (
    echo [ERROR] Backend failed to start. Expected 200 from /health.
    if exist "%BACKEND_LOG%" (
        echo ===== backend.log =====
        type "%BACKEND_LOG%"
    ) else (
        echo [ERROR] backend.log was not created.
    )
    exit /b 1
)

echo [backend] Healthy: http://127.0.0.1:8000/health

if exist "frontend\package.json" (
    echo [frontend] Starting yarn dev
    start "XUA Frontend" cmd /k "cd /d ""%REPO_ROOT%\frontend"" && yarn dev"
) else (
    echo [frontend] frontend\package.json not found. Skipping frontend start.
)

echo [info] Backend running. Log: "%BACKEND_LOG%"
exit /b 0
