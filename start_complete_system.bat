@echo off
echo 🦊 راه‌اندازی سیستم کامل ROBAH
echo =====================================

echo.
echo 🔧 در حال راه‌اندازی Ollama...
start "Ollama" cmd /c "set OLLAMA_MODELS=%CD%\models && ollama serve"
timeout /t 3

echo.
echo 🐍 در حال راه‌اندازی Backend Python...
start "Backend" cmd /c "set OLLAMA_MODELS=%CD%\models && python backend/main.py"
timeout /t 5

echo.
echo ⚛️ در حال راه‌اندازی Frontend اصلی...
start "Frontend" cmd /c "cd frontend && npm start"
timeout /t 3

echo.
echo 🎨 در حال راه‌اندازی Frontend سه‌بعدی...
start "Frontend-3D" cmd /c "cd frontend-3d && npm start"
timeout /t 3

echo.
echo ✅ همه سرویس‌ها شروع شدند!
echo.
echo 📋 لیست سرویس‌ها:
echo - Ollama: http://localhost:11434
echo - Backend API: http://localhost:8000
echo - Frontend اصلی: http://localhost:3000
echo - Frontend سه‌بعدی: http://localhost:3001
echo.
echo 🌐 برای باز کردن رابط‌ها:
timeout /t 2
start http://localhost:3000
timeout /t 1
start http://localhost:3001

echo.
echo 🎉 سیستم آماده است!
pause