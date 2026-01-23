#!/usr/bin/env python3
"""
تست سیستم صوتی روباه
"""

import sys
import os
import asyncio

# اضافه کردن مسیر پروژه
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from brain.speech_handler import speech_handler

async def test_speech_system():
    """تست کامل سیستم صوتی"""
    
    print("🦊 تست سیستم صوتی روباه")
    print("=" * 40)
    
    # 1. بررسی وضعیت اولیه
    print("\n1️⃣ وضعیت اولیه:")
    initial_status = speech_handler.get_status()
    for key, value in initial_status.items():
        print(f"   {key}: {value}")
    
    # 2. راه‌اندازی سیستم
    print("\n2️⃣ راه‌اندازی سیستم...")
    try:
        success = await speech_handler.initialize()
        print(f"   ✅ راه‌اندازی: {'موفق' if success else 'ناموفق'}")
    except Exception as e:
        print(f"   ❌ خطا در راه‌اندازی: {e}")
        return
    
    # 3. بررسی وضعیت بعد از راه‌اندازی
    print("\n3️⃣ وضعیت بعد از راه‌اندازی:")
    final_status = speech_handler.get_status()
    for key, value in final_status.items():
        print(f"   {key}: {value}")
    
    # 4. تست Text-to-Speech (فقط تولید فایل)
    print("\n4️⃣ تست تولید صدا (TTS)...")
    test_texts = [
        "سلام، من روباه هستم!",
        "چطوری؟ حالت خوبه؟",
        "من می‌تونم با صدا باهات صحبت کنم."
    ]
    
    for i, text in enumerate(test_texts, 1):
        print(f"   تست {i}: {text}")
        try:
            # تولید فایل صوتی
            audio_file = f"data/temp/audio/test_tts_{i}.wav"
            os.makedirs("data/temp/audio", exist_ok=True)
            
            success = await speech_handler.text_to_speech(text, audio_file)
            
            if success and os.path.exists(audio_file):
                file_size = os.path.getsize(audio_file)
                print(f"   ✅ فایل صوتی تولید شد: {audio_file} ({file_size} bytes)")
            else:
                print(f"   ❌ تولید فایل صوتی ناموفق")
                
        except Exception as e:
            print(f"   ❌ خطا در TTS: {e}")
    
    print("\n💡 نکته: میکروفون تست نمی‌شود - فقط خروجی صوتی")
    
    # 5. بررسی فایل‌های تولید شده
    print("\n6️⃣ فایل‌های صوتی تولید شده:")
    audio_dir = "data/temp/audio"
    if os.path.exists(audio_dir):
        audio_files = [f for f in os.listdir(audio_dir) if f.endswith('.wav')]
        if audio_files:
            for audio_file in audio_files:
                file_path = os.path.join(audio_dir, audio_file)
                file_size = os.path.getsize(file_path)
                print(f"   📁 {audio_file}: {file_size} bytes")
        else:
            print("   📂 هیچ فایل صوتی یافت نشد")
    else:
        print("   📂 پوشه صوتی وجود ندارد")
    
    print("\n🎉 تست سیستم صوتی تکمیل شد!")

if __name__ == "__main__":
    asyncio.run(test_speech_system())