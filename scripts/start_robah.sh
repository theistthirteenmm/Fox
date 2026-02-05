#!/bin/bash
# Robah - AI Assistant Server

cd "$(dirname "$0")/.."

echo ""
echo "==============================================="
echo "  Robah - AI Assistant Server"
echo "==============================================="
echo ""

# بررسی Ollama
echo "[*] Checking Ollama..."
if ! curl -s http://localhost:11434/api/tags > /dev/null 2>&1; then
    echo "[!] Starting Ollama..."
    ollama serve &
    sleep 5
else
    echo "[+] Ollama is running"
fi

# Virtual Environment
if [ ! -d "venv" ]; then
    echo "[*] Creating virtual environment..."
    python3 -m venv venv
fi

# نصب dependencies
echo "[*] Installing dependencies..."
source venv/bin/activate
pip install -r requirements.txt -q

# ایجاد پوشه‌ها
mkdir -p data/memory data/personality data/learning logs

# اجرای Backend
echo ""
echo "[*] Starting Backend on http://localhost:8000"
echo "[*] Press Ctrl+C to stop"
echo ""
export PYTHONPATH=$(pwd)
python backend/main.py
