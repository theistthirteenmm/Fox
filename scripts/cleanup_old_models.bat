@echo off
chcp 65001 >nul
title 🦊 پاک‌سازی مدل‌های قدیمی

echo.
echo ===============================================
echo 🗑️  پاک‌سازی مدل‌های قدیمی از درایو C
echo ===============================================
echo.

:: تنظیم مسیر پروژه (یک سطح بالاتر از scripts)
cd ..

set "OLD_PATH=%USERPROFILE%\.ollama\models"
set "NEW_PATH=%CD%\models"

echo 📍 مسیر قدیمی: %OLD_PATH%
echo 📍 مسیر جدید: %NEW_PATH%
echo.

:: بررسی وجود مدل‌های جدید
echo 🔍 بررسی مدل‌های جدید...
set OLLAMA_MODELS=%NEW_PATH%
ollama list
if %errorlevel% neq 0 (
    echo ❌ مدل‌های جدید یافت نشدند! عملیات متوقف شد.
    pause
    exit /b 1
)

echo.
echo ⚠️  توجه: این عملیات مدل‌های قدیمی را برای همیشه پاک می‌کند
echo 💾 فضای آزاد شده: ~8.5 گیگابایت
echo 📁 مسیر پاک شونده: %OLD_PATH%
echo.

set /p confirm="آیا مطمئن هستید؟ (y/n): "
if /i not "%confirm%"=="y" (
    echo عملیات لغو شد.
    pause
    exit /b
)

echo.
echo 🗑️  پاک کردن مدل‌های قدیمی...
rmdir /s /q "%OLD_PATH%"

if %errorlevel% neq 0 (
    echo ❌ خطا در پاک کردن مدل‌های قدیمی!
    pause
    exit /b 1
)

echo ✅ مدل‌های قدیمی با موفقیت پاک شدند!
echo 💾 فضای آزاد شده: ~8.5 گیگابایت
echo.

echo 🎉 تمیزکاری کامل شد!
echo 📁 مدل‌ها اکنون فقط در: %NEW_PATH%
echo.
pause