@echo off
chcp 65001 >nul
title 🦊 تنظیم مسیر مدل‌های روباه

echo.
echo ===============================================
echo 🦊 تنظیم مسیر مدل‌های روباه
echo ===============================================
echo.

:: تنظیم مسیر پروژه (یک سطح بالاتر از scripts)
cd ..

:: ایجاد پوشه مدل‌ها اگر وجود نداشته باشد
if not exist "models" (
    echo 📁 ایجاد پوشه models...
    mkdir models
)

:: تنظیم متغیر محیطی برای جلسه فعلی
set "OLLAMA_MODELS=%CD%\models"
echo ✅ متغیر محیطی تنظیم شد: OLLAMA_MODELS=%OLLAMA_MODELS%

:: نمایش اطلاعات
echo.
echo 📋 اطلاعات:
echo   📍 مسیر پروژه: %CD%
echo   📁 مسیر مدل‌ها: %CD%\models
echo   💾 فضای خالی: 
dir "%CD%" | find "bytes free"

echo.
echo 💡 برای تنظیم دائمی متغیر محیطی:
echo   1. کلیک راست روی "This PC" یا "My Computer"
echo   2. Properties → Advanced System Settings
echo   3. Environment Variables
echo   4. اضافه کردن متغیر جدید:
echo      نام: OLLAMA_MODELS
echo      مقدار: %CD%\models

echo.
echo 🔧 یا از PowerShell (به عنوان Administrator):
echo   [Environment]::SetEnvironmentVariable("OLLAMA_MODELS", "%CD%\models", "User")

echo.
echo ✅ تنظیمات کامل شد!
echo 🦊 حالا می‌توانید مدل‌ها را دانلود کنید: download_models.bat
echo.
pause