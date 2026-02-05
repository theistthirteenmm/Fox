#!/usr/bin/env python3
"""
🦊 اسکریپت نصب خودکار روباه
نصب کامل و خودکار تمام dependencies و تنظیمات
"""

import os
import sys
import subprocess
import platform
import json
from pathlib import Path

# اطلاعات پروژه
PROJECT_INFO = {
    "name": "روباه",
    "name_en": "Robah", 
    "version": "1.0.0",
    "description": "دستیار هوش مصنوعی شخصی",
    "python_min": (3, 8),
    "node_min": "16.0.0"
}

class Colors:
    """رنگ‌های terminal"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_colored(message, color=Colors.END):
    """چاپ رنگی"""
    print(f"{color}{message}{Colors.END}")

def print_header():
    """چاپ هدر پروژه"""
    print_colored("=" * 60, Colors.CYAN)
    print_colored(f"🦊 {PROJECT_INFO['name']} - نصب خودکار", Colors.BOLD + Colors.PURPLE)
    print_colored(f"   {PROJECT_INFO['description']}", Colors.BLUE)
    print_colored(f"   نسخه: {PROJECT_INFO['version']}", Colors.YELLOW)
    print_colored("=" * 60, Colors.CYAN)

def run_command(command, cwd=None):
    """اجرای دستور و نمایش خروجی"""
    print(f"🔧 در حال اجرا: {command}")
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            cwd=cwd,
            capture_output=True, 
            text=True,
            encoding='utf-8'
        )
        
        if result.returncode == 0:
            print(f"✅ موفق: {command}")
            if result.stdout:
                print(result.stdout)
        else:
            print(f"❌ خطا در: {command}")
            print(result.stderr)
            return False
        return True
    except Exception as e:
        print(f"❌ خطای غیرمنتظره: {e}")
        return False

def check_requirements():
    """بررسی پیش‌نیازها"""
    print("🔍 بررسی پیش‌نیازها...")
    
    # بررسی Python
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ مورد نیاز است")
        return False
    print(f"✅ Python {sys.version}")
    
    # بررسی pip
    if not run_command("pip --version"):
        print("❌ pip یافت نشد")
        return False
    
    # بررسی Node.js
    if not run_command("node --version"):
        print("❌ Node.js یافت نشد. لطفاً نصب کنید: https://nodejs.org")
        return False
    
    # بررسی npm
    if not run_command("npm --version"):
        print("❌ npm یافت نشد")
        return False
    
    return True

def setup_backend():
    """راه‌اندازی backend"""
    print("\n🐍 راه‌اندازی Backend...")
    
    # ایجاد virtual environment
    if not os.path.exists("venv"):
        print("📦 ایجاد virtual environment...")
        if not run_command("python -m venv venv"):
            return False
    
    # فعال‌سازی virtual environment و نصب packages
    if os.name == 'nt':  # Windows
        activate_cmd = "venv\\Scripts\\activate && pip install -r requirements.txt"
    else:  # Linux/Mac
        activate_cmd = "source venv/bin/activate && pip install -r requirements.txt"
    
    if not run_command(activate_cmd):
        print("❌ خطا در نصب Python packages")
        return False
    
    # ایجاد دایرکتوری‌های مورد نیاز
    directories = [
        "data/memory",
        "data/personality", 
        "data/learning",
        "logs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"📁 ایجاد شد: {directory}")
    
    return True

def setup_frontend():
    """راه‌اندازی frontend"""
    print("\n⚛️ راه‌اندازی Frontend...")
    
    # نصب dependencies
    if not run_command("npm install", cwd="frontend"):
        print("❌ خطا در نصب npm packages")
        return False
    
    return True

def setup_ollama():
    """راهنمای نصب Ollama"""
    print("\n🧠 راهنمای نصب Ollama...")
    print("""
برای استفاده از روباه، باید Ollama را نصب کنید:

Windows:
1. از https://ollama.ai دانلود کنید
2. فایل نصب را اجرا کنید
3. در Command Prompt اجرا کنید: ollama pull llama3.2:3b

Linux/Mac:
1. اجرا کنید: curl -fsSL https://ollama.ai/install.sh | sh
2. اجرا کنید: ollama pull llama3.2:3b

بعد از نصب، Ollama را اجرا کنید:
ollama serve
    """)

def create_run_scripts():
    """ایجاد اسکریپت‌های اجرا"""
    print("\n📝 ایجاد اسکریپت‌های اجرا...")
    
    # اسکریپت Windows
    windows_script = """@echo off
echo 🦊 راه‌اندازی روباه...

echo 🧠 شروع Ollama...
start "Ollama" cmd /k "ollama serve"

timeout /t 3

echo 🐍 شروع Backend...
start "Backend" cmd /k "cd /d %~dp0 && venv\\Scripts\\activate && python backend/main.py"

timeout /t 5

echo ⚛️ شروع Frontend...
start "Frontend" cmd /k "cd /d %~dp0\\frontend && npm start"

echo ✅ روباه آماده است!
echo 🌐 Frontend: http://localhost:3000
echo 🔧 Backend: http://localhost:8000
pause
"""
    
    with open("start_robah.bat", "w", encoding="utf-8") as f:
        f.write(windows_script)
    
    # اسکریپت Linux/Mac
    unix_script = """#!/bin/bash
echo "🦊 راه‌اندازی روباه..."

echo "🧠 شروع Ollama..."
ollama serve &
OLLAMA_PID=$!

sleep 3

echo "🐍 شروع Backend..."
cd "$(dirname "$0")"
source venv/bin/activate
python backend/main.py &
BACKEND_PID=$!

sleep 5

echo "⚛️ شروع Frontend..."
cd frontend
npm start &
FRONTEND_PID=$!

echo "✅ روباه آماده است!"
echo "🌐 Frontend: http://localhost:3000"
echo "🔧 Backend: http://localhost:8000"

# منتظر ماندن برای Ctrl+C
trap "kill $OLLAMA_PID $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT
wait
"""
    
    with open("start_robah.sh", "w", encoding="utf-8") as f:
        f.write(unix_script)
    
    # اجازه اجرا برای Linux/Mac
    if os.name != 'nt':
        run_command("chmod +x start_robah.sh")
    
    print("✅ اسکریپت‌های اجرا ایجاد شدند")

def main():
    """تابع اصلی راه‌اندازی"""
    print("🦊 خوش آمدید به راه‌اندازی روباه!")
    print("=" * 50)
    
    # بررسی پیش‌نیازها
    if not check_requirements():
        print("\n❌ لطفاً پیش‌نیازها را نصب کنید و دوباره تلاش کنید")
        return False
    
    # راه‌اندازی backend
    if not setup_backend():
        print("\n❌ خطا در راه‌اندازی backend")
        return False
    
    # راه‌اندازی frontend
    if not setup_frontend():
        print("\n❌ خطا در راه‌اندازی frontend")
        return False
    
    # راهنمای Ollama
    setup_ollama()
    
    # ایجاد اسکریپت‌های اجرا
    create_run_scripts()
    
    print("\n" + "=" * 50)
    print("🎉 راه‌اندازی با موفقیت تمام شد!")
    print("\nمراحل بعدی:")
    print("1. Ollama را نصب و اجرا کنید")
    print("2. برای شروع:")
    if os.name == 'nt':
        print("   Windows: start_robah.bat را اجرا کنید")
    else:
        print("   Linux/Mac: ./start_robah.sh را اجرا کنید")
    print("\n🌐 رابط وب: http://localhost:3000")
    print("🔧 API: http://localhost:8000")
    
    return True

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1)