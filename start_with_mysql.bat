@echo off
title School Website - MySQL Mode
cd /d "%~dp0"

echo ========================================================
echo       APEX INTERNATIONAL ACADEMY - WEB SERVER
echo ========================================================
echo.

echo [1/2] Checking MySQL database status (Port 3306)...
netstat -ano | findstr :3306 >nul
if %errorlevel% neq 0 (
    echo MySQL is not running. Starting XAMPP MySQL...
    if exist "C:\xampp\mysql\bin\mysqld.exe" (
        start /b "" "C:\xampp\mysql\bin\mysqld.exe" --defaults-file="C:\xampp\mysql\bin\my.ini" --standalone
        timeout /t 3 /nobreak >nul
        echo MySQL started successfully!
    ) else (
        echo [WARNING] MySQL not found at C:\xampp\mysql. Please start MySQL from your XAMPP Control Panel.
    )
) else (
    echo [OK] MySQL is active and listening on port 3306.
)

echo.
echo [2/2] Starting Flask Web Server on http://localhost:5000 ...
echo Press Ctrl+C in this window to stop the server.
echo.

if exist ".\venv\Scripts\python.exe" (
    .\venv\Scripts\python.exe run.py
) else (
    py run.py
)

pause
