#!/usr/bin/env python3
"""
تست سریع TTS
"""

import pyttsx3
import os

def quick_tts_test():
    print("🔊 تست سریع TTS...")
    
    try:
        # راه‌اندازی TTS
        engine = pyttsx3.init()
        
        # تنظیمات
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 0.8)
        
        # تولید فایل
        os.makedirs("data/temp/audio", exist_ok=True)
        test_file = "data/temp/audio/quick_test.wav"
        
        text = "سلام، من روباه هستم!"
        
        engine.save_to_file(text, test_file)
        engine.runAndWait()
        
        if os.path.exists(test_file):
            size = os.path.getsize(test_file)
            print(f"✅ فایل تولید شد: {test_file} ({size} bytes)")
        else:
            print("❌ فایل تولید نشد")
            
    except Exception as e:
        print(f"❌ خطا: {e}")

if __name__ == "__main__":
    quick_tts_test()