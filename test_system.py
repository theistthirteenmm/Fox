#!/usr/bin/env python3
"""
تست سیستم روباه
بررسی عملکرد اجزای مختلف سیستم
"""

import asyncio
import requests
import json
from pathlib import Path

async def test_backend_status():
    """تست وضعیت backend"""
    try:
        response = requests.get("http://localhost:8000/status", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print("✅ Backend فعال است")
            print(f"   - مدل AI: {'✅' if data['brain_loaded'] else '❌'}")
            print(f"   - حافظه: {data['memory_size']} آیتم")
            print(f"   - سطح شخصیت: {data['personality_level']}")
            return True
        else:
            print(f"❌ Backend خطا: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Backend در دسترس نیست: {e}")
        return False

async def test_speech_system():
    """تست سیستم صوتی"""
    try:
        response = requests.get("http://localhost:8000/speech/debug", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data['success']:
                debug_info = data['debug_info']
                print("🎤 سیستم صوتی:")
                print(f"   - Whisper: {'✅' if debug_info['whisper_model_loaded'] else '❌'}")
                print(f"   - TTS: {'✅' if debug_info['tts_engine_ready'] else '❌'}")
                print(f"   - فرمت‌های پشتیبانی: {len(debug_info['supported_formats'])}")
                return True
            else:
                print("❌ سیستم صوتی مشکل دارد")
                return False
        else:
            print(f"❌ خطا در تست سیستم صوتی: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ تست سیستم صوتی ناموفق: {e}")
        return False

async def test_ai_brain():
    """تست مدل AI"""
    try:
        # تست ساده با API
        test_message = "سلام روباه، چطوری؟"
        
        # ایجاد WebSocket connection برای تست
        import websockets
        
        async with websockets.connect("ws://localhost:8000/chat") as websocket:
            # ارسال پیام تست
            await websocket.send(json.dumps({
                "message": test_message,
                "timestamp": "2026-01-22T12:00:00"
            }))
            
            # دریافت پاسخ
            response = await asyncio.wait_for(websocket.recv(), timeout=30)
            data = json.loads(response)
            
            if data.get('type') == 'ai' and data.get('message'):
                print("🧠 مدل AI:")
                print(f"   - پاسخ: {data['message'][:50]}...")
                return True
            else:
                print("❌ مدل AI پاسخ مناسب نداد")
                return False
                
    except asyncio.TimeoutError:
        print("❌ مدل AI timeout شد")
        return False
    except Exception as e:
        print(f"❌ تست مدل AI ناموفق: {e}")
        return False

async def test_file_structure():
    """بررسی ساختار فایل‌ها"""
    required_files = [
        "backend/main.py",
        "brain/core.py",
        "brain/memory.py",
        "brain/personality.py",
        "brain/speech_handler.py",
        "frontend/src/App.tsx",
        "frontend/src/components/ChatInterface.tsx",
        "frontend/src/components/MessageInput.tsx"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print("❌ فایل‌های مفقود:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    else:
        print("✅ تمام فایل‌های ضروری موجود هستند")
        return True

async def main():
    """تست کامل سیستم"""
    print("🦊 شروع تست سیستم روباه...")
    print("=" * 50)
    
    tests = [
        ("ساختار فایل‌ها", test_file_structure()),
        ("Backend", test_backend_status()),
        ("سیستم صوتی", test_speech_system()),
        ("مدل AI", test_ai_brain())
    ]
    
    results = []
    for test_name, test_coro in tests:
        print(f"\n🔍 تست {test_name}:")
        try:
            result = await test_coro
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ خطا در تست {test_name}: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 50)
    print("📊 نتایج تست:")
    
    passed = 0
    for test_name, result in results:
        status = "✅ موفق" if result else "❌ ناموفق"
        print(f"   {test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\n🎯 نتیجه کلی: {passed}/{len(results)} تست موفق")
    
    if passed == len(results):
        print("🎉 سیستم روباه کاملاً آماده است!")
    elif passed >= len(results) * 0.75:
        print("⚠️ سیستم تقریباً آماده است، برخی مشکلات جزئی وجود دارد")
    else:
        print("❌ سیستم نیاز به تعمیر دارد")

if __name__ == "__main__":
    asyncio.run(main())