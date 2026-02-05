"""
🎙️ مدیریت صوتی روباه
Speech-to-Text و Text-to-Speech با پشتیبانی فارسی
"""

import os
import io
import tempfile
import asyncio
from typing import Optional, Dict, Any
import speech_recognition as sr
import pyttsx3
import whisper
from pathlib import Path
import requests
import json
import urllib.parse

class SpeechHandler:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = None
        self.tts_engine = None
        self.whisper_model = None
        self.is_initialized = False
        
        # تنظیمات
        self.supported_formats = ['.wav', '.mp3', '.m4a', '.ogg', '.flac', '.webm', '.opus']
        self.temp_dir = Path("data/temp/audio")
        self.temp_dir.mkdir(parents=True, exist_ok=True)
        
        # تلاش برای راه‌اندازی میکروفون
        try:
            self.microphone = sr.Microphone()
            print("🎙️ مدیر صوتی راه‌اندازی شد (میکروفون فعال)")
        except Exception as e:
            print(f"🎙️ مدیر صوتی راه‌اندازی شد (میکروفون غیرفعال: {e})")
    
    async def initialize(self):
        """راه‌اندازی اولیه سیستم صوتی"""
        if self.is_initialized:
            return True
        
        try:
            print("🔄 در حال بارگذاری مدل Whisper...")
            # بارگذاری مدل Whisper برای STT
            self.whisper_model = whisper.load_model("base")
            
            print("🔄 در حال راه‌اندازی TTS...")
            # راه‌اندازی TTS
            self.tts_engine = pyttsx3.init()
            
            # تنظیمات TTS
            voices = self.tts_engine.getProperty('voices')
            if voices:
                # انتخاب صدای مناسب (ترجیحاً زنانه)
                for voice in voices:
                    if 'female' in voice.name.lower() or 'woman' in voice.name.lower():
                        self.tts_engine.setProperty('voice', voice.id)
                        break
            
            # تنظیم سرعت و حجم
            self.tts_engine.setProperty('rate', 150)  # سرعت متوسط
            self.tts_engine.setProperty('volume', 0.8)  # حجم 80%
            
            # تنظیم میکروفون (اختیاری)
            try:
                self.microphone = sr.Microphone()
                with self.microphone as source:
                    print("🎤 تنظیم میکروفون...")
                    self.recognizer.adjust_for_ambient_noise(source, duration=1)
            except Exception as e:
                print(f"⚠️ میکروفون در دسترس نیست: {e}")
                self.microphone = None
            
            self.is_initialized = True
            print("✅ سیستم صوتی آماده است!")
            return True
            
        except Exception as e:
            print(f"❌ خطا در راه‌اندازی سیستم صوتی: {e}")
            return False
    
    async def speech_to_text(self, audio_data: bytes = None, audio_file: str = None) -> Optional[str]:
        """تبدیل صدا به متن"""
        if not self.is_initialized:
            await self.initialize()
        
        try:
            if audio_file:
                # از فایل صوتی
                return await self._transcribe_file(audio_file)
            elif audio_data:
                # از داده صوتی
                return await self._transcribe_bytes(audio_data)
            else:
                # ضبط زنده از میکروفون
                return await self._record_and_transcribe()
                
        except Exception as e:
            print(f"❌ خطا در تبدیل صدا به متن: {e}")
            return None
    
    async def _transcribe_file(self, audio_file: str) -> Optional[str]:
        """تبدیل فایل صوتی به متن"""
        try:
            if not os.path.exists(audio_file):
                print(f"❌ فایل صوتی یافت نشد: {audio_file}")
                return None
            
            file_size = os.path.getsize(audio_file)
            print(f"🔄 در حال تحلیل فایل: {audio_file} (حجم: {file_size} bytes)")
            
            if file_size < 1000:  # کمتر از 1KB
                print(f"⚠️ فایل صوتی خیلی کوچک است: {file_size} bytes")
                return None
            
            # بررسی فرمت فایل
            file_ext = Path(audio_file).suffix.lower()
            if file_ext not in self.supported_formats:
                print(f"⚠️ فرمت فایل پشتیبانی نمی‌شود: {file_ext}")
                # تلاش برای تبدیل فرمت
                try:
                    import subprocess
                    converted_file = audio_file.replace(file_ext, '.wav')
                    subprocess.run(['ffmpeg', '-i', audio_file, converted_file], 
                                 capture_output=True, check=True)
                    audio_file = converted_file
                    print(f"✅ فایل به WAV تبدیل شد: {converted_file}")
                except:
                    print("❌ تبدیل فرمت ناموفق بود")
                    return None
            
            result = self.whisper_model.transcribe(
                audio_file, 
                language="fa",  # فارسی
                fp16=False,     # برای سازگاری بیشتر
                verbose=True    # لاگ بیشتر
            )
            
            text = result["text"].strip()
            confidence = result.get("confidence", 0)
            
            print(f"📊 اطمینان تشخیص: {confidence}")
            print(f"🗣️ زبان تشخیص داده شده: {result.get('language', 'نامشخص')}")
            
            if text:
                print(f"✅ متن تشخیص داده شده: {text}")
                return text
            else:
                print("⚠️ متنی تشخیص داده نشد")
                return None
                
        except Exception as e:
            print(f"❌ خطا در تحلیل فایل صوتی: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    async def _transcribe_bytes(self, audio_data: bytes) -> Optional[str]:
        """تبدیل داده صوتی به متن"""
        try:
            # ذخیره موقت
            temp_file = self.temp_dir / f"temp_audio_{os.getpid()}.wav"
            
            with open(temp_file, "wb") as f:
                f.write(audio_data)
            
            # تحلیل
            result = await self._transcribe_file(str(temp_file))
            
            # پاک کردن فایل موقت
            if temp_file.exists():
                temp_file.unlink()
            
            return result
            
        except Exception as e:
            print(f"❌ خطا در تحلیل داده صوتی: {e}")
            return None
    
    async def _record_and_transcribe(self) -> Optional[str]:
        """ضبط زنده و تبدیل به متن"""
        try:
            print("🎤 شروع ضبط... (5 ثانیه)")
            
            with self.microphone as source:
                # ضبط صدا
                audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=5)
            
            print("🔄 در حال تحلیل صدا...")
            
            # تبدیل به فایل موقت
            temp_file = self.temp_dir / f"recorded_{os.getpid()}.wav"
            
            with open(temp_file, "wb") as f:
                f.write(audio.get_wav_data())
            
            # تحلیل با Whisper
            result = await self._transcribe_file(str(temp_file))
            
            # پاک کردن فایل موقت
            if temp_file.exists():
                temp_file.unlink()
            
            return result
            
        except sr.WaitTimeoutError:
            print("⏰ زمان ضبط تمام شد")
            return None
        except Exception as e:
            print(f"❌ خطا در ضبط صدا: {e}")
            return None
    
    async def text_to_speech(self, text: str, save_file: str = None) -> bool:
        """تبدیل متن به صدا"""
        if not self.is_initialized:
            await self.initialize()
        
        try:
            if not text.strip():
                return False
            
            print(f"🔊 در حال تولید صدا: {text[:50]}...")
            
            # تنظیمات بهتر برای TTS
            self.tts_engine.setProperty('rate', 120)  # سرعت کمتر برای فارسی
            self.tts_engine.setProperty('volume', 1.0)  # حجم کامل
            
            # انتخاب بهترین صدا
            voices = self.tts_engine.getProperty('voices')
            if voices:
                # ترجیح صدای زنانه
                for voice in voices:
                    if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
                        self.tts_engine.setProperty('voice', voice.id)
                        print(f"🎵 استفاده از صدا: {voice.name}")
                        break
            
            # برای فارسی، متن رو به انگلیسی transliterate می‌کنیم
            processed_text = self._prepare_persian_text(text)
            
            if save_file:
                # ذخیره در فایل
                self.tts_engine.save_to_file(processed_text, save_file)
                self.tts_engine.runAndWait()
                print(f"✅ فایل صوتی ذخیره شد: {save_file}")
            else:
                # پخش مستقیم
                self.tts_engine.say(processed_text)
                self.tts_engine.runAndWait()
                print("✅ صدا پخش شد")
            
            return True
            
        except Exception as e:
            print(f"❌ خطا در تولید صدا: {e}")
            return False
    
    def _prepare_persian_text(self, text: str) -> str:
        """آماده‌سازی متن فارسی برای TTS"""
        
        # اگر متن فارسی نیست، همون رو برگردون
        if not self._is_persian_text(text):
            return text
        
        # تبدیل برخی کلمات فارسی به انگلیسی برای تلفظ بهتر
        persian_to_english = {
            'سلام': 'salam',
            'روباه': 'robah',
            'چطوری': 'chetori',
            'خوبم': 'khobam',
            'ممنون': 'mamnoon',
            'متشکرم': 'moteshakeram',
            'خداحافظ': 'khodahafez',
            'بله': 'bale',
            'نه': 'na',
            'آره': 'are',
            'باشه': 'bashe',
            'اوکی': 'okay',
            'درست': 'dorost',
            'غلط': 'ghalat',
            'خوب': 'khob',
            'بد': 'bad',
            'عالی': 'ali',
            'فوق‌العاده': 'fogholade',
            'کار': 'kar',
            'کمک': 'komak',
            'می‌تونم': 'mitonam',
            'می‌خوام': 'mikham',
            'دوست دارم': 'doost daram'
        }
        
        # جایگزینی کلمات
        processed_text = text
        for persian, english in persian_to_english.items():
            processed_text = processed_text.replace(persian, english)
        
        # حذف علائم نگارشی فارسی که مشکل ایجاد می‌کنند
        processed_text = processed_text.replace('‌', ' ')  # نیم‌فاصله
        processed_text = processed_text.replace('؟', '?')
        processed_text = processed_text.replace('،', ',')
        
        return processed_text
    
    def _is_persian_text(self, text: str) -> bool:
        """تشخیص متن فارسی"""
        persian_chars = 'آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی'
        persian_count = sum(1 for char in text if char in persian_chars)
        total_chars = len([char for char in text if char.isalpha()])
        
        if total_chars == 0:
            return False
        
        return (persian_count / total_chars) > 0.3  # حداقل 30% فارسی
    
    def is_audio_file(self, filename: str) -> bool:
        """بررسی فرمت فایل صوتی"""
        supported_extensions = ['.wav', '.mp3', '.m4a', '.ogg', '.flac', '.webm', '.opus']
        return Path(filename).suffix.lower() in supported_extensions
    
    async def get_audio_info(self, audio_file: str) -> Dict[str, Any]:
        """اطلاعات فایل صوتی"""
        try:
            if not os.path.exists(audio_file):
                return {"error": "فایل یافت نشد"}
            
            file_size = os.path.getsize(audio_file)
            file_ext = Path(audio_file).suffix.lower()
            
            return {
                "filename": os.path.basename(audio_file),
                "size": file_size,
                "size_mb": round(file_size / (1024 * 1024), 2),
                "format": file_ext,
                "supported": file_ext in self.supported_formats
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    def cleanup_temp_files(self):
        """پاک کردن فایل‌های موقت"""
        try:
            for temp_file in self.temp_dir.glob("*"):
                if temp_file.is_file():
                    temp_file.unlink()
            print("🧹 فایل‌های موقت پاک شدند")
        except Exception as e:
            print(f"⚠️ خطا در پاک کردن فایل‌های موقت: {e}")
    
    def get_status(self) -> Dict[str, Any]:
        """وضعیت سیستم صوتی"""
        return {
            "initialized": self.is_initialized,
            "whisper_loaded": self.whisper_model is not None,
            "tts_ready": self.tts_engine is not None,
            "supported_formats": self.supported_formats,
            "temp_dir": str(self.temp_dir)
        }

# نمونه سراسری
speech_handler = SpeechHandler()