#!/usr/bin/env python3
"""
تست TTS انگلیسی
"""

import pyttsx3
import os

def test_english_tts():
    print("🔊 تست TTS انگلیسی...")
    
    try:
        engine = pyttsx3.init()
        
        # لیست صداها
        voices = engine.getProperty('voices')
        print(f"📢 تعداد صداهای موجود: {len(voices)}")
        
        for i, voice in enumerate(voices):
            print(f"   {i}: {voice.name} - {voice.languages}")
        
        # تنظیمات
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 0.9)
        
        # تست انگلیسی
        os.makedirs("data/temp/audio", exist_ok=True)
        
        texts = [
            "Hello, I am Robah AI Assistant",
            "How are you today?",
            "I can speak in English"
        ]
        
        for i, text in enumerate(texts, 1):
            test_file = f"data/temp/audio/english_test_{i}.wav"
            print(f"تولید: {text}")
            
            engine.save_to_file(text, test_file)
            engine.runAndWait()
            
            if os.path.exists(test_file):
                size = os.path.getsize(test_file)
                print(f"✅ {test_file} ({size} bytes)")
            else:
                print(f"❌ فایل تولید نشد")
                
    except Exception as e:
        print(f"❌ خطا: {e}")

if __name__ == "__main__":
    test_english_tts()