#!/usr/bin/env python3
"""
🧪 تست کامل سیستم روباه
تست همه قابلیت‌های اصلی روباه
"""

import requests
import time
import json
from datetime import datetime

class RobahTester:
    def __init__(self):
        self.backend_url = "http://localhost:8000"
        self.ollama_url = "http://localhost:11434"
        
    def test_backend_status(self):
        """تست وضعیت backend"""
        print("🔍 تست backend...")
        try:
            response = requests.get(f"{self.backend_url}/status", timeout=5)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ Backend فعال - مدل‌ها: {data.get('brain_loaded', False)}")
                return True
            else:
                print(f"❌ Backend خطا: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Backend در دسترس نیست: {e}")
            return False
    
    def test_models(self):
        """تست مدل‌های فعال"""
        print("🤖 تست مدل‌ها...")
        models = [
            ("llama3.2:3b", "سلام"),
            ("deepseek-r1:7b", "چرا؟"),
            ("deepseek-coder-v2:16b", "def hello():"),
            ("partai/dorna-llama3:8b-instruct-q8_0", "سلام چطوری؟")
        ]
        
        working = 0
        for model, prompt in models:
            try:
                start = time.time()
                response = requests.post(
                    f"{self.ollama_url}/api/generate",
                    json={"model": model, "prompt": prompt, "stream": False, "options": {"max_tokens": 10}},
                    timeout=30
                )
                if response.status_code == 200:
                    elapsed = time.time() - start
                    print(f"✅ {model}: {elapsed:.1f}s")
                    working += 1
                else:
                    print(f"❌ {model}: خطا")
            except:
                print(f"❌ {model}: timeout")
        
        print(f"📊 {working}/{len(models)} مدل کار می‌کند")
        return working >= 2
    
    def test_chat(self):
        """تست چت"""
        print("💬 تست چت...")
        try:
            response = requests.post(
                f"{self.backend_url}/chat",
                json={"message": "سلام تست"},
                timeout=30
            )
            if response.status_code == 200:
                print("✅ چت کار می‌کند")
                return True
            else:
                print("❌ چت خطا دارد")
                return False
        except Exception as e:
            print(f"❌ چت در دسترس نیست: {e}")
            return False
    
    def run_full_test(self):
        """اجرای تست کامل"""
        print("🦊 تست کامل سیستم روباه")
        print("=" * 50)
        
        results = {
            "backend": self.test_backend_status(),
            "models": self.test_models(),
            "chat": self.test_chat()
        }
        
        print("\n" + "=" * 50)
        print("📊 نتایج:")
        
        passed = sum(results.values())
        total = len(results)
        
        for test, result in results.items():
            status = "✅" if result else "❌"
            print(f"{status} {test}")
        
        print(f"\n🎯 نتیجه: {passed}/{total} تست موفق")
        
        if passed == total:
            print("🎉 همه چیز عالی کار می‌کند!")
        elif passed >= 2:
            print("⚠️  سیستم قابل استفاده است")
        else:
            print("❌ نیاز به بررسی دارد")
        
        return results

if __name__ == "__main__":
    tester = RobahTester()
    tester.run_full_test()