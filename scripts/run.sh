#!/bin/bash

echo "🦊 روباه در حال راه‌اندازی..."

# بررسی Ollama
if ! nc -z localhost 11434 >/dev/null 2>&1; then
    echo "🧠 راه‌اندازی Ollama..."
    ollama serve &
    sleep 5
fi

# راه‌اندازی Backend
echo "🐍 راه‌اندازی Backend..."
export PYTHONPATH="$(pwd)"
source venv/bin/activate
python backend/main.py &

# انتظار
sleep 8

# راه‌اندازی Frontend
echo "⚛️ راه‌اندازی Frontend..."
cd frontend
npm start &
cd ..

# انتظار و باز کردن مرورگر
sleep 10

if command -v xdg-open >/dev/null 2>&1; then
    xdg-open http://localhost:3000 >/dev/null 2>&1
elif command -v open >/dev/null 2>&1; then
    open http://localhost:3000 >/dev/null 2>&1
fi

echo "✅ روباه آماده است!"
echo "🌐 http://localhost:3000"

# منتظر ماندن
read -p "برای توقف Enter را فشار دهید..."