@echo off
chcp 65001 >nul
title 🧪 تست سریع مدل‌های روباه

:: تغییر به دایرکتوری پروژه (یک سطح بالاتر از scripts)
cd /d "%~dp0\.."

echo.
echo ===============================================
echo 🧪 تست سریع مدل‌های روباه
echo ===============================================
echo.

echo 🔍 بررسی وضعیت Ollama...
ollama list >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Ollama در دسترس نیست
    echo 💡 ابتدا Ollama را راه‌اندازی کنید: scripts\manage_ollama.bat
    pause
    exit /b 1
)

echo ✅ Ollama فعال است
echo.

echo 📋 مدل‌های نصب شده:
ollama list
echo.

echo 🧪 برای تست کامل مدل‌ها: scripts\test.bat
echo 💡 برای مدیریت مدل‌ها: scripts\manage_ollama.bat
echo.
pause