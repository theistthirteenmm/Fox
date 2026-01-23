#!/usr/bin/env python3
"""
تست TTS فارسی روباه
"""

import sys
import os
import asyncio

# اضافه کردن مسیر پروژه
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from brain.speech_handler import speech_handler

async def test_persian_tts():
    """تست TTS فارسی"""
    
    print("🦊 تست TTS فارسی روباه")
    print("=" * 30)
    
    # راه‌اندازی
    print("🔄 راه‌اندازی سیستم...")
    success = await speech_handler.initialize()
    if not success:
        print("❌ راه‌اندازی ناموفق")
        return
    
    # تست متن‌های فارسی
    persian_texts = [
        "سلام، من روباه هستم!",
        "چطوری؟ حالت خوبه؟",
        "من می‌تونم فارسی صحبت کنم."
    ]
    
    print("\n🔊 تست تولید صدای فارسی...")
    
    for i, text in enumerate(persian_texts, 1):
        print(f"\n{i}. متن: {text}")
        
        # تولید فایل صوتی
        audio_file = f"data/temp/audio/persian_test_{i}.mp3"
        os.makedirs("data/temp/audio", exist_ok=True)
        
        try:
            success = await speech_handler.text_to_speech(text, audio_file)
            
            if success and os.path.exists(audio_file):
                file_size = os.path.getsize(audio_file)
                print(f"   ✅ فایل تولید شد: {file_size} bytes")
                print(f"   📁 مسیر: {audio_file}")
            else:
                print(f"   ❌ تولید ناموفق")
                
        except Exception as e:
            print(f"   ❌ خطا: {e}")
    
    # نمایش فایل‌های تولید شده
    print("\n📂 فایل‌های تولید شده:")
    audio_dir = "data/temp/audio"
    if os.path.exists(audio_dir):
        files = [f for f in os.listdir(audio_dir) if f.startswith("persian_test")]
        for file in files:
            file_path = os.path.join(audio_dir, file)
            file_size = os.path.getsize(file_path)
            print(f"   🎵 {file}: {file_size} bytes")
    
    print("\n🎉 تست تکمیل شد!")
    print("💡 فایل‌های MP3 رو می‌تونی با هر پلیر صوتی پخش کنی")

if __name__ == "__main__":
    asyncio.run(test_persian_tts())