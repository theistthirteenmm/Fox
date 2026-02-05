@echo off
setlocal enabledelayedexpansion
chcp 65001 >nul
title 🦊 روباه - دستیار هوش مصنوعی

:: تغییر به دایرکتوری پروژه (یک سطح بالاتر از scripts)
cd /d "%~dp0\.."

echo.
echo ===============================================
echo 🦊 روباه - دستیار هوش مصنوعی شخصی
echo ===============================================
echo.

:: رنگ‌ها برای خروجی
set "GREEN=[92m"
set "YELLOW=[93m"
set "RED=[91m"
set "BLUE=[94m"
set "RESET=[0m"

:: بررسی وجود فایل‌های مورد نیاز
echo %BLUE%🔍 بررسی فایل‌های پروژه...%RESET%
if not exist "backend\main.py" (
    echo %RED%❌ فایل backend\main.py یافت نشد!%RESET%
    pause
    exit /b 1
)

if not exist "frontend\package.json" (
    echo %RED%❌ فایل frontend\package.json یافت نشد!%RESET%
    pause
    exit /b 1
)

if not exist "requirements.txt" (
    echo %RED%❌ فایل requirements.txt یافت نشد!%RESET%
    pause
    exit /b 1
)

echo %GREEN%✅ فایل‌های پروژه موجود است%RESET%
echo.

:: بررسی Ollama
echo %BLUE%🧠 بررسی Ollama...%RESET%
curl -s http://localhost:11434/api/tags >nul 2>&1
if %errorlevel% neq 0 (
    echo %YELLOW%⚠️  Ollama در حال اجرا نیست. در حال راه‌اندازی...%RESET%
    start "Ollama Server" cmd /k "echo 🧠 Ollama Server && ollama serve"
    echo %BLUE%⏳ صبر برای راه‌اندازی Ollama...%RESET%
    timeout /t 5 /nobreak >nul
) else (
    echo %GREEN%✅ Ollama در حال اجرا است%RESET%
)

:: بررسی مدل
echo %BLUE%🔍 بررسی مدل AI...%RESET%
curl -s http://localhost:11434/api/tags > temp_models.txt 2>nul
findstr "partai/dorna-llama3" temp_models.txt >nul 2>&1
if %errorlevel% neq 0 (
    echo %YELLOW%⚠️  مدل فارسی یافت نشد. آیا می‌خواهید دانلود کنید؟ ^(y/n^) %RESET%
    set /p download_model="پاسخ: "
    if /i "!download_model!"=="y" (
        echo %BLUE%📥 در حال دانلود مدل فارسی...%RESET%
        ollama pull partai/dorna-llama3:8b-instruct-q8_0
    )
) else (
    echo %GREEN%✅ مدل فارسی موجود است%RESET%
)
if exist temp_models.txt del temp_models.txt

echo.

:: بررسی Virtual Environment
echo %BLUE%🐍 بررسی Python Virtual Environment...%RESET%
if not exist "venv\Scripts\activate.bat" (
    echo %YELLOW%⚠️  Virtual Environment یافت نشد. در حال ایجاد...%RESET%
    python -m venv venv
    if %errorlevel% neq 0 (
        echo %RED%❌ خطا در ایجاد Virtual Environment%RESET%
        pause
        exit /b 1
    )
)

:: فعال‌سازی Virtual Environment و نصب dependencies
echo %BLUE%📦 نصب Python Dependencies...%RESET%
call venv\Scripts\activate.bat
venv\Scripts\python -X utf8 -m pip install -r requirements.txt --quiet
if %errorlevel% neq 0 (
    echo %RED%❌ خطا در نصب Python packages%RESET%
    pause
    exit /b 1
)

echo %GREEN%✅ Python Dependencies نصب شد%RESET%

:: بررسی Node.js Dependencies
echo %BLUE%⚛️  بررسی Node.js Dependencies...%RESET%
cd frontend
if not exist "node_modules" (
    echo %YELLOW%⚠️  Node modules یافت نشد. در حال نصب...%RESET%
    npm install --silent
    if %errorlevel% neq 0 (
        echo %RED%❌ خطا در نصب npm packages%RESET%
        cd ..
        pause
        exit /b 1
    )
)
cd ..

echo %GREEN%✅ Node.js Dependencies آماده است%RESET%
echo.

:: ایجاد دایرکتوری‌های مورد نیاز
echo %BLUE%📁 ایجاد دایرکتوری‌های مورد نیاز...%RESET%
if not exist "data\memory" mkdir data\memory
if not exist "data\personality" mkdir data\personality
if not exist "data\learning" mkdir data\learning
if not exist "logs" mkdir logs

echo %GREEN%✅ دایرکتوری‌ها ایجاد شد%RESET%
echo.

:: راه‌اندازی سرویس‌ها
echo ===============================================
echo 🚀 راه‌اندازی سرویس‌ها
echo ===============================================
echo.

:: Backend
echo %BLUE%🐍 راه‌اندازی Backend...%RESET%
set PYTHONPATH=%CD%
start "🦊 Robah Backend" cmd /k "title 🦊 Robah Backend && call venv\Scripts\activate.bat && set PYTHONPATH=%CD% && python backend\main.py"

:: انتظار برای راه‌اندازی Backend
echo %BLUE%⏳ صبر برای راه‌اندازی Backend...%RESET%
timeout /t 8 /nobreak >nul

:: بررسی Backend
curl -s http://localhost:8000/status >nul 2>&1
if %errorlevel% neq 0 (
    echo %YELLOW%⚠️  Backend هنوز آماده نیست. کمی بیشتر صبر کنید...%RESET%
    timeout /t 5 /nobreak >nul
)

:: Frontend
echo %BLUE%⚛️  راه‌اندازی Frontend...%RESET%
cd frontend
start "🦊 Robah Frontend" cmd /k "title 🦊 Robah Frontend && npm start"
cd ..

:: انتظار برای راه‌اندازی Frontend
echo %BLUE%⏳ صبر برای راه‌اندازی Frontend...%RESET%
timeout /t 10 /nobreak >nul

:: Frontend 3D
echo %BLUE%🧊 راه‌اندازی Frontend 3D...%RESET%
cd frontend-3d
start "🦊 Robah Frontend 3D" cmd /k "title 🦊 Robah Frontend 3D && npm start"
cd ..

:: انتظار برای راه‌اندازی Frontend 3D
echo %BLUE%⏳ صبر برای راه‌اندازی Frontend 3D...%RESET%
timeout /t 10 /nobreak >nul

:: Nginx
echo %BLUE%🌐 راه‌اندازی Nginx...%RESET%
start "🦊 Robah Nginx" cmd /k "title 🦊 Robah Nginx && call scripts\start_nginx.bat"

echo.
echo ===============================================
echo 🎉 روباه آماده است!
echo ===============================================
echo.
echo %GREEN%🌐 رابط اصلی (Nginx):%RESET%  http://localhost:8080
echo %GREEN%🧊 رابط سه‌بعدی:%RESET%       http://localhost:8080/3d/
echo %GREEN%🌐 رابط وب مستقیم:%RESET%     http://localhost:3000
echo %GREEN%🔧 API Backend:%RESET%        http://localhost:8000
echo %GREEN%📚 مستندات:%RESET%           http://localhost:8000/docs
echo.
echo %BLUE%💡 نکات مهم:%RESET%
echo   • برای توقف سرویس‌ها، پنجره‌های terminal را ببندید
echo   • اگر مشکلی پیش آمد، فایل logs\robah.log را بررسی کنید
echo   • برای راه‌اندازی مجدد، این فایل را دوباره اجرا کنید
echo.

:: باز کردن مرورگر
echo %BLUE%🌐 باز کردن مرورگر...%RESET%
timeout /t 3 /nobreak >nul
start http://localhost:8080

echo.
echo %GREEN%✨ لذت ببرید از چت با روباه! 🦊%RESET%
echo.
pause
