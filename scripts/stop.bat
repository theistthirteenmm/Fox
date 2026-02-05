@echo off
title 🦊 روباه - توقف سرویس‌ها

:: تغییر به دایرکتوری پروژه (یک سطح بالاتر از scripts)
cd /d "%~dp0\.."

echo 🛑 توقف سرویس‌های روباه...

:: توقف Nginx
call scripts\stop_nginx.bat >nul 2>&1

:: توقف فرآیندهای Python (Backend)
echo 🐍 توقف Backend...
taskkill /f /im python.exe >nul 2>&1
taskkill /f /im pythonw.exe >nul 2>&1

:: توقف فرآیندهای Node.js (Frontend)
echo ⚛️ توقف Frontend...
taskkill /f /im node.exe >nul 2>&1

:: توقف Ollama (اختیاری)
echo 🧠 توقف Ollama...
taskkill /f /im ollama.exe >nul 2>&1

:: پاک کردن پورت‌ها
echo 🧹 پاک کردن پورت‌ها...
netstat -ano | findstr :8000 >nul 2>&1
if %errorlevel% equ 0 (
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8000') do taskkill /f /pid %%a >nul 2>&1
)

netstat -ano | findstr :3000 >nul 2>&1
if %errorlevel% equ 0 (
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr :3000') do taskkill /f /pid %%a >nul 2>&1
)

netstat -ano | findstr :3001 >nul 2>&1
if %errorlevel% equ 0 (
    for /f "tokens=5" %%a in ('netstat -ano ^| findstr :3001') do taskkill /f /pid %%a >nul 2>&1
)

echo ✅ تمام سرویس‌های روباه متوقف شدند!
timeout /t 3 /nobreak >nul
