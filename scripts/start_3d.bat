@echo off
chcp 65001 >nul
title روباه سه‌بعدی - راه‌اندازی

:: تغییر به دایرکتوری پروژه (یک سطح بالاتر از scripts)
cd /d "%~dp0\.."

echo.
echo 🦊 ================================
echo    روباه - رابط سه‌بعدی تعاملی
echo ================================
echo.

echo 🚀 در حال راه‌اندازی...
echo.

:: چک کردن Node.js
echo 📦 بررسی Node.js...
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js نصب نیست! لطفاً از nodejs.org نصب کنید
    pause
    exit /b 1
)

:: رفتن به پوشه frontend-3d
cd frontend-3d

:: نصب dependencies
if not exist "node_modules" (
    echo 📥 نصب Dependencies...
    npm install
    if errorlevel 1 (
        echo ❌ خطا در نصب Dependencies
        pause
        exit /b 1
    )
)

:: اجرای سرور توسعه
echo.
echo ✅ همه چیز آماده است!
echo 🌐 رابط سه‌بعدی در حال اجرا روی: http://localhost:3001
echo 🦊 روباه آماده تعامل!
echo.
echo 💡 نکته: Backend باید روی پورت 8000 اجرا باشه
echo.

npm start