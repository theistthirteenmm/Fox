#!/usr/bin/env python3
"""
بررسی صداهای موجود در سیستم
"""

import pyttsx3
import asyncio
import os

def check_available_voices():
    """بررسی صداهای موجود"""
    
    print("🔊 بررسی صداهای موجود در سیستم")
    print("=" * 40)
    
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        
        if not voices:
            print("❌ هیچ صدایی یافت نشد")
            return
        
        print(f"📊 تعداد صداهای موجود: {len(voices)}")
        print()
        
        for i, voice in enumerate(voices):
            print(f"{i+1}. نام: {voice.name}")
            print(f"   ID: {voice.id}")
            print(f"   زبان‌ها: {getattr(voice, 'languages', 'نامشخص')}")
            print(f"   جنسیت: {getattr(voice, 'gender', 'نامشخص')}")
            print(f"   سن: {getattr(voice, 'age', 'نامشخص')}")
            print("-" * 30)
        
        # تست صدای پیش‌فرض
        print("\n🎵 تست صدای پیش‌فرض:")
        test_text = "Hello, this is a test. سلام، این یک تست است."
        
        # تولید فایل تست
        os.makedirs("data/temp/audio", exist_ok=True)
        test_file = "data/temp/audio/voice_test.wav"
        
        engine.save_to_file(test_text, test_file)
        engine.runAndWait()
        
        if os.path.exists(test_file):
            file_size = os.path.getsize(test_file)
            print(f"✅ فایل تست تولید شد: {test_file} ({file_size} bytes)")
        else:
            print("❌ تولید فایل تست ناموفق")
        
        engine.stop()
        
    except Exception as e:
        print(f"❌ خطا: {e}")

if __name__ == "__main__":
    check_available_voices()