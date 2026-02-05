@echo off
chcp 65001 > nul
title مدیریت Ollama و مدل‌های AI

:: تغییر به دایرکتوری پروژه (یک سطح بالاتر از scripts)
cd /d "%~dp0\.."

echo.
echo ========================================
echo    🤖 مدیریت Ollama و مدل‌های AI
echo ========================================
echo.

:main_menu
echo انتخاب کنید:
echo 1. راه‌اندازی Ollama Server
echo 2. متوقف کردن Ollama Server
echo 3. مشاهده مدل‌های نصب شده
echo 4. دانلود مدل جدید
echo 5. حذف مدل
echo 6. بررسی وضعیت Ollama
echo 7. تست مدل
echo 0. خروج
echo.
set /p choice="انتخاب شما (0-7): "

if "%choice%"=="1" goto start_ollama
if "%choice%"=="2" goto stop_ollama
if "%choice%"=="3" goto list_models
if "%choice%"=="4" goto download_model
if "%choice%"=="5" goto remove_model
if "%choice%"=="6" goto check_status
if "%choice%"=="7" goto test_model
if "%choice%"=="0" goto exit
goto main_menu

:start_ollama
echo.
echo 📡 راه‌اندازی Ollama Server...
start "Ollama Server" ollama serve
timeout /t 3 > nul
curl -s http://localhost:11434/api/tags > nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Ollama Server با موفقیت راه‌اندازی شد
) else (
    echo ❌ خطا در راه‌اندازی Ollama Server
)
goto pause_and_menu

:stop_ollama
echo.
echo 🛑 متوقف کردن Ollama Server...
taskkill /f /im ollama.exe > nul 2>&1
echo ✅ Ollama Server متوقف شد
goto pause_and_menu

:list_models
echo.
echo 🧠 مدل‌های نصب شده:
ollama list
goto pause_and_menu

:download_model
echo.
echo 📥 مدل‌های پیشنهادی:
echo 1. partai/dorna-llama3:8b-instruct-q8_0 (فارسی - 8.5GB)
echo 2. llama3.2:3b (سریع - 2GB)
echo 3. deepseek-coder-v2:16b (کد - 9GB)
echo 4. deepseek-r1:7b (استدلال - 4GB)
echo 5. qwen2.5:32b (چندزبانه - 18GB)
echo.
set /p model_choice="انتخاب مدل (1-5) یا نام مدل: "

if "%model_choice%"=="1" set model_name=partai/dorna-llama3:8b-instruct-q8_0
if "%model_choice%"=="2" set model_name=llama3.2:3b
if "%model_choice%"=="3" set model_name=deepseek-coder-v2:16b
if "%model_choice%"=="4" set model_name=deepseek-r1:7b
if "%model_choice%"=="5" set model_name=qwen2.5:32b
if "%model_choice%" gtr "5" set model_name=%model_choice%

echo.
echo 📥 دانلود %model_name%...
echo ⚠️ این فرآیند ممکن است چند دقیقه تا چند ساعت طول بکشد
ollama pull %model_name%
if %errorlevel% equ 0 (
    echo ✅ مدل با موفقیت دانلود شد
) else (
    echo ❌ خطا در دانلود مدل
)
goto pause_and_menu

:remove_model
echo.
echo 🗑️ حذف مدل:
ollama list
echo.
set /p model_to_remove="نام مدل برای حذف: "
ollama rm %model_to_remove%
if %errorlevel% equ 0 (
    echo ✅ مدل حذف شد
) else (
    echo ❌ خطا در حذف مدل
)
goto pause_and_menu

:check_status
echo.
echo 📊 وضعیت Ollama:
ollama --version
echo.
curl -s http://localhost:11434/api/tags > nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Ollama Server: در حال اجرا
    echo 🔗 آدرس: http://localhost:11434
) else (
    echo ❌ Ollama Server: متوقف
)
goto pause_and_menu

:test_model
echo.
echo 🧪 تست مدل:
ollama list
echo.
set /p test_model="نام مدل برای تست: "
echo.
echo تست پیام: سلام، چطوری؟
ollama run %test_model% "سلام، چطوری؟"
goto pause_and_menu

:pause_and_menu
echo.
pause
cls
goto main_menu

:exit
echo.
echo 👋 خداحافظ!
exit /b