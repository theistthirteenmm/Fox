@echo off
chcp 65001 > nul
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8

echo.
echo 🦊 روباه CLI
echo.

REM بررسی Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python نصب نیست!
    pause
    exit /b 1
)

REM نصب کتابخانه‌ها (بی‌صدا)
pip install colorama requests >nul 2>&1

REM اجرای CLI
python robah_cli.py %*
