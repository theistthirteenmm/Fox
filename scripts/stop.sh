#!/bin/bash

# تغییر به دایرکتوری پروژه (یک سطح بالاتر از scripts)
cd "$(dirname "$0")/.."

echo "🛑 توقف سرویس‌های روباه..."

# توقف Nginx
./scripts/stop_nginx.sh >/dev/null 2>&1

# توقف فرآیندهای Python (Backend)
echo "🐍 توقف Backend..."
pkill -f "python backend/main.py" 2>/dev/null
pkill -f "python.*main.py" 2>/dev/null

# توقف فرآیندهای Node.js (Frontend)
echo "⚛️ توقف Frontend..."
pkill -f "npm start" 2>/dev/null
pkill -f "react-scripts start" 2>/dev/null

# توقف Ollama (اختیاری)
echo "🧠 توقف Ollama..."
pkill -f "ollama serve" 2>/dev/null

# پاک کردن پورت‌ها
echo "🧹 پاک کردن پورت‌ها..."

# پیدا کردن و کشتن فرآیندهای استفاده کننده از پورت 8000
PORT_8000_PID=$(lsof -ti:8000 2>/dev/null)
if [[ ! -z "$PORT_8000_PID" ]]; then
    kill -9 $PORT_8000_PID 2>/dev/null
fi

# پیدا کردن و کشتن فرآیندهای استفاده کننده از پورت 3000
PORT_3000_PID=$(lsof -ti:3000 2>/dev/null)
if [[ ! -z "$PORT_3000_PID" ]]; then
    kill -9 $PORT_3000_PID 2>/dev/null
fi

# پیدا کردن و کشتن فرآیندهای استفاده کننده از پورت 3001
PORT_3001_PID=$(lsof -ti:3001 2>/dev/null)
if [[ ! -z "$PORT_3001_PID" ]]; then
    kill -9 $PORT_3001_PID 2>/dev/null
fi

echo "✅ تمام سرویس‌های روباه متوقف شدند!"
sleep 2
