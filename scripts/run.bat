@echo off
title 🦊 روباه - راه‌اندازی سریع

echo 🦊 روباه در حال راه‌اندازی...

:: بررسی Ollama
curl -s http://localhost:11434/api/tags >nul 2>&1
if %errorlevel% neq 0 (
    echo 🧠 راه‌اندازی Ollama...
    start "Ollama" cmd /k "ollama serve"
    timeout /t 5 /nobreak >nul
)

:: راه‌اندازی Backend
echo 🐍 راه‌اندازی Backend...
set PYTHONPATH=%CD%
start "Backend" cmd /k "call venv\Scripts\activate.bat && set PYTHONPATH=%CD% && python backend\main.py"

:: انتظار
timeout /t 8 /nobreak >nul

:: راه‌اندازی Frontend
echo ⚛️ راه‌اندازی Frontend...
start "Frontend" cmd /k "cd frontend && npm start"

:: انتظار و باز کردن مرورگر
timeout /t 10 /nobreak >nul
start http://localhost:3000

echo ✅ روباه آماده است!
echo 🌐 http://localhost:3000
pause