@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
title Robah Server

cd /d "%~dp0\.."

echo.
echo ===============================================
echo   Robah - AI Assistant Server
echo ===============================================
echo.

:: بررسی Ollama
echo [*] Checking Ollama...
curl -s http://localhost:11434/api/tags >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Starting Ollama...
    start "" ollama serve
    timeout /t 5 /nobreak >nul
) else (
    echo [+] Ollama is running
)

:: Virtual Environment
if not exist "venv\Scripts\activate.bat" (
    echo [*] Creating virtual environment...
    python -m venv venv
)

:: نصب dependencies
echo [*] Installing dependencies...
call venv\Scripts\activate.bat
pip install -r requirements.txt -q

:: ایجاد پوشه‌ها
if not exist "data\memory" mkdir data\memory
if not exist "data\personality" mkdir data\personality
if not exist "data\learning" mkdir data\learning
if not exist "logs" mkdir logs

:: اجرای Backend
echo.
echo [*] Starting Backend on http://localhost:8000
echo [*] Press Ctrl+C to stop
echo.
set PYTHONPATH=%CD%
python backend\main.py
