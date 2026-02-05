#!/usr/bin/env python3
"""
🧪 تست کامل سیستم روباه
تست همه قابلیت‌های اصلی شامل backend، مدل‌ها، حافظه، و سیستم صوتی
"""

import asyncio
import requests
import json
import time
import sys
import os
from pathlib import Path
from datetime import datetime

# اضافه کردن مسیر پروژه به sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class RobahCompleteTester:
    def __init__(self):
        self.backend_url = "http://localhost:8000"
        self.ollama_url = "http://localhost:11434"
        self.results = {}
        
    def print_header(self, title):
        """چاپ عنوان با فرمت زیبا"""
        print(f"\n{'='*50}")
        print(f"🔍 {title}")
        print('='*50)
    
    def test_file_structure(self):
        """بررسی ساختار فایل‌ها"""
        self.print_header("تست ساختار فایل‌ها")
        
        required_files = [
            "backend/main.py",
            "brain/core/core.py", 
            "brain/core/memory.py",
            "brain/core/personality.py",
            "brain/interfaces/speech_handler.py",
            "brain/learning/personal_learning_system.py",
            "brain/learning/dynamic_name_learning.py",
            "frontend/src/App.tsx",
            "frontend/src/components/ChatInterface.tsx",
            "robah_cli.py",
            "requirements.txt"
        ]
        
        missing_files = []
        for file_path in required_files:
            if not Path(file_path).exists():
                missing_files.append(file_path)
                print(f"❌ {file_path}")
            else:
                print(f"✅ {file_path}")
        
        if missing_files:
            print(f"\n❌ {len(missing_files)} فایل مفقود")
            return False
        else:
            print(f"\n✅ تمام {len(required_files)} فایل ضروری موجود است")
            return True
    
    def test_backend_status(self):
        """تست وضعیت backend"""
        self.print_header("تست Backend")
        
        try:
            response = requests.get(f"{self.backend_url}/status", timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Backend فعال")
                print(f"   - مدل AI: {'✅' if data.get('brain_loaded', False) else '❌'}")
                print(f"   - حافظه: {data.get('memory_size', 0)} آیتم")
                print(f"   - سطح شخصیت: {data.get('personality_level', 'نامشخص')}")
                return True
            else:
                print(f"❌ Backend خطا: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Backend در دسترس نیست: {e}")
            return False
    
    def test_ollama_models(self):
        """تست مدل‌های Ollama"""
        self.print_header("تست مدل‌های AI")
        
        # بررسی دسترسی به Ollama
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            if response.status_code != 200:
                print("❌ Ollama در دسترس نیست")
                return False
        except:
            print("❌ Ollama در دسترس نیست")
            return False
        
        # لیست مدل‌های مورد تست
        test_models = [
            ("partai/dorna-llama3:8b-instruct-q8_0", "سلام چطوری؟"),
            ("llama3.2:3b", "Hello"),
            ("deepseek-r1:7b", "چرا آسمان آبی است؟"),
            ("deepseek-coder-v2:16b", "def hello():")
        ]
        
        working_models = 0
        total_models = len(test_models)
        
        for model, prompt in test_models:
            try:
                print(f"🧪 تست {model}...")
                start_time = time.time()
                
                response = requests.post(
                    f"{self.ollama_url}/api/generate",
                    json={
                        "model": model, 
                        "prompt": prompt, 
                        "stream": False,
                        "options": {"max_tokens": 20}
                    },
                    timeout=30
                )
                
                if response.status_code == 200:
                    elapsed = time.time() - start_time
                    print(f"   ✅ پاسخ در {elapsed:.1f} ثانیه")
                    working_models += 1
                else:
                    print(f"   ❌ خطا: {response.status_code}")
                    
            except requests.exceptions.Timeout:
                print(f"   ❌ timeout")
            except Exception as e:
                print(f"   ❌ خطا: {e}")
        
        print(f"\n📊 نتیجه: {working_models}/{total_models} مدل کار می‌کند")
        return working_models >= 1  # حداقل یک مدل کار کند
    
    def test_memory_system(self):
        """تست سیستم حافظه"""
        self.print_header("تست سیستم حافظه")
        
        try:
            from brain.core.memory import MemoryManager
            
            # ایجاد memory manager
            memory = MemoryManager()
            print("✅ MemoryManager ایجاد شد")
            
            # تست ذخیره
            test_message = f"تست حافظه - {datetime.now()}"
            memory.store_conversation("user", test_message)
            print("✅ ذخیره مکالمه موفق")
            
            # تست بازیابی
            context = memory.get_relevant_context("تست")
            print(f"✅ بازیابی context: {len(context)} آیتم")
            
            # تست آمار
            stats = memory.get_memory_count()
            print(f"✅ آمار حافظه: {stats}")
            
            return True
            
        except Exception as e:
            print(f"❌ خطا در تست حافظه: {e}")
            return False
    
    def test_chat_functionality(self):
        """تست عملکرد چت"""
        self.print_header("تست عملکرد چت")
        
        try:
            test_message = "سلام روباه، این یک تست است"
            
            response = requests.post(
                f"{self.backend_url}/chat",
                json={"message": test_message},
                timeout=30
            )
            
            if response.status_code == 200:
                data = response.json()
                if data.get('response'):
                    print("✅ چت کار می‌کند")
                    print(f"   پاسخ: {data['response'][:100]}...")
                    return True
                else:
                    print("❌ پاسخ خالی دریافت شد")
                    return False
            else:
                print(f"❌ خطا در چت: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"❌ خطا در تست چت: {e}")
            return False
    
    def test_learning_systems(self):
        """تست سیستم‌های یادگیری"""
        self.print_header("تست سیستم‌های یادگیری")
        
        try:
            # تست سیستم یادگیری نام
            from brain.learning.dynamic_name_learning import DynamicNameLearning
            name_learning = DynamicNameLearning()
            print("✅ سیستم یادگیری نام")
            
            # تست سیستم یادگیری شخصی
            from brain.learning.personal_learning_system import PersonalLearningSystem
            personal_learning = PersonalLearningSystem()
            print("✅ سیستم یادگیری شخصی")
            
            return True
            
        except Exception as e:
            print(f"❌ خطا در تست سیستم‌های یادگیری: {e}")
            return False
    
    async def test_speech_system(self):
        """تست سیستم صوتی"""
        self.print_header("تست سیستم صوتی")
        
        try:
            response = requests.get(f"{self.backend_url}/speech/debug", timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    debug_info = data.get('debug_info', {})
                    print(f"✅ Whisper: {'✅' if debug_info.get('whisper_model_loaded') else '❌'}")
                    print(f"✅ TTS: {'✅' if debug_info.get('tts_engine_ready') else '❌'}")
                    print(f"✅ فرمت‌های پشتیبانی: {len(debug_info.get('supported_formats', []))}")
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
    
    async def run_complete_test(self):
        """اجرای تست کامل"""
        print("🦊 شروع تست کامل سیستم روباه")
        print(f"⏰ زمان: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # لیست تست‌ها
        tests = [
            ("ساختار فایل‌ها", self.test_file_structure),
            ("Backend", self.test_backend_status),
            ("مدل‌های AI", self.test_ollama_models),
            ("سیستم حافظه", self.test_memory_system),
            ("عملکرد چت", self.test_chat_functionality),
            ("سیستم‌های یادگیری", self.test_learning_systems),
            ("سیستم صوتی", self.test_speech_system)
        ]
        
        # اجرای تست‌ها
        for test_name, test_func in tests:
            try:
                if asyncio.iscoroutinefunction(test_func):
                    result = await test_func()
                else:
                    result = test_func()
                self.results[test_name] = result
            except Exception as e:
                print(f"❌ خطا در تست {test_name}: {e}")
                self.results[test_name] = False
        
        # نمایش نتایج نهایی
        self.print_final_results()
    
    def print_final_results(self):
        """نمایش نتایج نهایی"""
        print(f"\n{'='*60}")
        print("📊 نتایج نهایی تست کامل روباه")
        print('='*60)
        
        passed = 0
        total = len(self.results)
        
        for test_name, result in self.results.items():
            status = "✅ موفق" if result else "❌ ناموفق"
            print(f"   {test_name:<20}: {status}")
            if result:
                passed += 1
        
        print(f"\n🎯 نتیجه کلی: {passed}/{total} تست موفق ({passed/total*100:.1f}%)")
        
        # ارزیابی کلی
        if passed == total:
            print("🎉 عالی! سیستم روباه کاملاً آماده و عملکرد بی‌نقص دارد!")
        elif passed >= total * 0.8:
            print("✅ خوب! سیستم روباه آماده است، برخی مشکلات جزئی وجود دارد")
        elif passed >= total * 0.6:
            print("⚠️ متوسط! سیستم قابل استفاده است اما نیاز به بهبود دارد")
        else:
            print("❌ ضعیف! سیستم نیاز به تعمیر و بررسی جدی دارد")
        
        # پیشنهادات
        failed_tests = [name for name, result in self.results.items() if not result]
        if failed_tests:
            print(f"\n💡 پیشنهادات برای بهبود:")
            for test in failed_tests:
                if test == "Backend":
                    print("   - Backend را راه‌اندازی کنید: scripts/start_robah.bat")
                elif test == "مدل‌های AI":
                    print("   - مدل‌ها را دانلود کنید: scripts/manage_ollama.bat")
                elif test == "ساختار فایل‌ها":
                    print("   - فایل‌های مفقود را بررسی کنید")

def main():
    """تابع اصلی"""
    tester = RobahCompleteTester()
    asyncio.run(tester.run_complete_test())

if __name__ == "__main__":
    main()