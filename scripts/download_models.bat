@echo off
chcp 65001 >nul
title 🦊 دانلود مدل‌های روباه

:: تغییر به دایرکتوری پروژه (یک سطح بالاتر از scripts)
cd /d "%~dp0\.."

echo.
echo ===============================================
echo 🦊 دانلود مدل‌های هوش مصنوعی روباه
echo ===============================================
echo.

:: تنظیم مسیر مدل‌ها در پروژه
set "OLLAMA_MODELS=%CD%\models"
echo 📁 مسیر مدل‌ها: %OLLAMA_MODELS%
echo.

:: ایجاد پوشه مدل‌ها اگر وجود نداشته باشد
if not exist "models" mkdir models

echo 📋 مدل‌های پیشنهادی روباه:
echo.
echo   🔥 ضروری:
echo   1. partai/dorna-llama3:8b-instruct-q8_0 (فارسی - 8.5GB)
echo   2. llama3.2:3b (سریع - 2GB)
echo.
echo   🚀 پیشرفته:
echo   3. deepseek-r1:7b (استدلال - 4GB)
echo   4. deepseek-coder-v2:16b (برنامه‌نویسی - 9GB)
echo   5. qwen2.5:32b (چندزبانه - 18GB)
echo.
echo   💪 قدرتمند:
echo   6. llama3.3:70b (بهترین - 43GB)
echo.

echo ⚠️  توجه: دانلود ممکن است چندین ساعت طول بکشد
echo 💾 فضای کل مورد نیاز: حدود 85 گیگابایت
echo 📍 محل ذخیره: %CD%\models
echo.

echo انتخاب کنید:
echo 1. دانلود مدل‌های ضروری (10.5GB)
echo 2. دانلود مدل‌های پیشرفته (31.5GB)
echo 3. دانلود همه مدل‌ها (85GB)
echo 4. انتخاب دستی
echo 0. خروج
echo.

set /p choice="انتخاب شما (0-4): "

if "%choice%"=="1" goto essential_models
if "%choice%"=="2" goto advanced_models
if "%choice%"=="3" goto all_models
if "%choice%"=="4" goto manual_selection
if "%choice%"=="0" goto exit
goto main_menu

:essential_models
echo.
echo 🔥 دانلود مدل‌های ضروری...
call :download_model "partai/dorna-llama3:8b-instruct-q8_0" "مدل فارسی اصلی"
call :download_model "llama3.2:3b" "مدل سریع"
goto finish

:advanced_models
echo.
echo 🚀 دانلود مدل‌های پیشرفته...
call :download_model "partai/dorna-llama3:8b-instruct-q8_0" "مدل فارسی اصلی"
call :download_model "llama3.2:3b" "مدل سریع"
call :download_model "deepseek-r1:7b" "مدل استدلال"
call :download_model "deepseek-coder-v2:16b" "مدل برنامه‌نویسی"
call :download_model "qwen2.5:32b" "مدل چندزبانه"
goto finish

:all_models
echo.
echo 💪 دانلود همه مدل‌ها...
call :download_model "partai/dorna-llama3:8b-instruct-q8_0" "مدل فارسی اصلی"
call :download_model "llama3.2:3b" "مدل سریع"
call :download_model "deepseek-r1:7b" "مدل استدلال"
call :download_model "deepseek-coder-v2:16b" "مدل برنامه‌نویسی"
call :download_model "qwen2.5:32b" "مدل چندزبانه"
call :download_model "llama3.3:70b" "مدل قدرتمند"
goto finish

:manual_selection
echo.
echo 🎯 انتخاب دستی مدل‌ها:
echo.
set /p model_name="نام مدل (مثال: llama3.2:3b): "
if "%model_name%"=="" goto manual_selection
call :download_model "%model_name%" "مدل انتخابی"
echo.
set /p continue="مدل دیگری دانلود کنید؟ (y/n): "
if /i "%continue%"=="y" goto manual_selection
goto finish

:download_model
echo.
echo ===============================================
echo 📥 دانلود %~2: %~1
echo ===============================================
ollama pull %~1
if %errorlevel% equ 0 (
    echo ✅ %~1 با موفقیت دانلود شد
) else (
    echo ❌ خطا در دانلود %~1
)
goto :eof

:finish
echo.
echo ===============================================
echo 🎉 دانلود کامل شد!
echo ===============================================
echo.

echo 📋 بررسی مدل‌های نصب شده:
ollama list

echo.
echo ✅ مدل‌ها در %CD%\models ذخیره شدند!
echo 🦊 حالا می‌توانید روباه را استفاده کنید
echo.

echo 💡 برای تست مدل‌ها: scripts\test.bat
echo 💡 برای راه‌اندازی روباه: start.bat
echo.
goto exit

:main_menu
cls
goto start

:exit
pause
exit /b