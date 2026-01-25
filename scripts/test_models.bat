@echo off
chcp 65001 >nul
title 🧪 تست مدل‌های روباه

echo.
echo ===============================================
echo 🧪 تست سریع مدل‌های روباه 2025
echo ===============================================
echo.

cd ..

echo 🔍 بررسی وضعیت Ollama...
ollama list >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Ollama در دسترس نیست
    echo 💡 ابتدا Ollama را راه‌اندازی کنید
    pause
    exit /b 1
)

echo ✅ Ollama فعال است
echo.

echo 📋 مدل‌های نصب شده:
ollama list
echo.

echo 🧪 شروع تست مدل‌ها...
python quick_model_test.py

echo.
echo 💡 برای تست کامل: python test_new_models.py
echo.
pause