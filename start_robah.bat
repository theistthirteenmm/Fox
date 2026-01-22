@echo off
echo 🦊 راه‌اندازی سیستم روباه...
echo.

echo 📡 شروع Backend...
start "Robah Backend" cmd /k "python backend/main.py"

echo ⏳ صبر 5 ثانیه برای راه‌اندازی Backend...
timeout /t 5 /nobreak >nul

echo 🌐 شروع Frontend...
start "Robah Frontend" cmd /k "cd frontend && npm start"

echo.
echo ✅ سیستم روباه در حال راه‌اندازی است!
echo 📱 Frontend: http://localhost:3000
echo 🔧 Backend: http://localhost:8000
echo.
pause