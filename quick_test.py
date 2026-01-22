#!/usr/bin/env python3
"""
تست سریع سیستم روباه
"""

import requests
import time

def test_backend():
    """تست سریع backend"""
    try:
        response = requests.get("http://localhost:8000/status", timeout=3)
        if response.status_code == 200:
            print("✅ Backend کار می‌کند")
            return True
        else:
            print(f"❌ Backend خطا: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend در دسترس نیست: {e}")
        return False

def test_frontend():
    """تست سریع frontend"""
    try:
        response = requests.get("http://localhost:3000", timeout=3)
        if response.status_code == 200:
            print("✅ Frontend کار می‌کند")
            return True
        else:
            print(f"❌ Frontend خطا: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Frontend در دسترس نیست: {e}")
        return False

if __name__ == "__main__":
    print("🦊 تست سریع سیستم روباه...")
    print("-" * 30)
    
    backend_ok = test_backend()
    frontend_ok = test_frontend()
    
    print("-" * 30)
    if backend_ok and frontend_ok:
        print("🎉 سیستم آماده است!")
        print("🌐 Frontend: http://localhost:3000")
        print("🔧 Backend: http://localhost:8000")
    elif backend_ok:
        print("⚠️ Backend آماده، Frontend نیاز به راه‌اندازی دارد")
        print("💡 دستور: cd frontend && npm start")
    elif frontend_ok:
        print("⚠️ Frontend آماده، Backend نیاز به راه‌اندازی دارد")
        print("💡 دستور: python backend/main.py")
    else:
        print("❌ هر دو سرویس نیاز به راه‌اندازی دارند")
        print("💡 Backend: python backend/main.py")
        print("💡 Frontend: cd frontend && npm start")