#!/usr/bin/env python3
"""
🧪 تست مدل‌های جدید روباه 2025
آزمایش عملکرد و انتخاب مدل‌های بهبود یافته
"""

import asyncio
import requests
import time
from datetime import datetime
import json

class ModelTester:
    def __init__(self):
        self.ollama_url = "http://localhost:11434"
        self.models = {
            "persian": "partai/dorna-llama3:8b-instruct-q8_0",
            "general": "llama3.3:70b",
            "reasoning": "deepseek-r1:7b",
            "code": "deepseek-coder-v2:16b",
            "fast": "llama3.2:3b",
            "multilingual": "qwen2.5:32b"
        }
        
        self.test_messages = {
            "persian": "سلام! چطوری؟ امروز چه کارهایی انجام دادی؟",
            "code": "یک function در Python بنویس که اعداد فیبوناچی را محاسبه کند",
            "reasoning": "چرا آسمان آبی است؟ دلیل علمی این پدیده را تحلیل کن",
            "multilingual": "Please translate this to Persian: Hello, how are you today?",
            "fast": "چند تا؟",
            "general": "در مورد تأثیر هوش مصنوعی بر آینده بشریت یک تحلیل جامع ارائه بده"
        }
    
    def check_model_availability(self, model_name: str) -> bool:
        """بررسی در دسترس بودن مدل"""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get("models", [])
                available_models = [m["name"] for m in models]
                return model_name in available_models
            return False
        except Exception as e:
            print(f"❌ خطا در بررسی مدل {model_name}: {e}")
            return False
    
    def test_model_response(self, model_name: str, message: str) -> dict:
        """تست پاسخ مدل"""
        start_time = time.time()
        
        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": model_name,
                    "prompt": message,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "top_p": 0.9,
                        "max_tokens": 200
                    }
                },
                timeout=60
            )
            
            end_time = time.time()
            response_time = end_time - start_time
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "success": True,
                    "response": result.get("response", ""),
                    "response_time": response_time,
                    "model": model_name,
                    "tokens": len(result.get("response", "").split())
                }
            else:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}: {response.text}",
                    "response_time": response_time,
                    "model": model_name
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "response_time": time.time() - start_time,
                "model": model_name
            }
    
    def run_comprehensive_test(self):
        """اجرای تست جامع"""
        print("🧪 شروع تست مدل‌های جدید روباه 2025")
        print("=" * 60)
        
        results = {}
        
        # بررسی در دسترس بودن مدل‌ها
        print("\n📋 بررسی در دسترس بودن مدل‌ها:")
        available_models = {}
        for category, model_name in self.models.items():
            is_available = self.check_model_availability(model_name)
            available_models[category] = is_available
            status = "✅ موجود" if is_available else "❌ غیرموجود"
            print(f"  {category}: {model_name} - {status}")
        
        print("\n" + "=" * 60)
        
        # تست مدل‌های موجود
        for category, model_name in self.models.items():
            if not available_models[category]:
                print(f"\n⏭️  رد شدن تست {category} (مدل موجود نیست)")
                continue
                
            print(f"\n🔍 تست مدل {category}: {model_name}")
            print("-" * 40)
            
            test_message = self.test_messages.get(category, self.test_messages["persian"])
            print(f"📝 پیام تست: {test_message}")
            
            result = self.test_model_response(model_name, test_message)
            results[category] = result
            
            if result["success"]:
                print(f"✅ موفق - زمان پاسخ: {result['response_time']:.2f}s")
                print(f"📊 تعداد کلمات: {result['tokens']}")
                print(f"💬 پاسخ: {result['response'][:100]}...")
            else:
                print(f"❌ ناموفق - خطا: {result['error']}")
        
        # خلاصه نتایج
        print("\n" + "=" * 60)
        print("📊 خلاصه نتایج:")
        print("=" * 60)
        
        successful_tests = [k for k, v in results.items() if v.get("success", False)]
        failed_tests = [k for k, v in results.items() if not v.get("success", False)]
        
        print(f"✅ تست‌های موفق: {len(successful_tests)}")
        print(f"❌ تست‌های ناموفق: {len(failed_tests)}")
        
        if successful_tests:
            print(f"\n🎉 مدل‌های کارآمد: {', '.join(successful_tests)}")
            
            # بهترین عملکرد
            fastest_model = min(
                [results[k] for k in successful_tests], 
                key=lambda x: x["response_time"]
            )
            print(f"⚡ سریع‌ترین مدل: {fastest_model['model']} ({fastest_model['response_time']:.2f}s)")
        
        if failed_tests:
            print(f"\n⚠️  مدل‌های نیازمند بررسی: {', '.join(failed_tests)}")
        
        # توصیه‌ها
        print("\n💡 توصیه‌ها:")
        if len(successful_tests) >= 3:
            print("✅ سیستم آماده استفاده است")
        elif len(successful_tests) >= 1:
            print("⚠️  برخی مدل‌ها نیاز به دانلود دارند")
            print("🔧 برای دانلود: scripts\\download_models.bat")
        else:
            print("❌ هیچ مدلی در دسترس نیست")
            print("🔧 ابتدا Ollama را راه‌اندازی کنید")
        
        return results

def main():
    """تابع اصلی"""
    tester = ModelTester()
    
    print(f"🦊 تست مدل‌های روباه - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        results = tester.run_comprehensive_test()
        
        # ذخیره نتایج
        with open("test_results.json", "w", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        
        print(f"\n💾 نتایج در test_results.json ذخیره شد")
        
    except KeyboardInterrupt:
        print("\n⏹️  تست متوقف شد")
    except Exception as e:
        print(f"\n❌ خطای غیرمنتظره: {e}")

if __name__ == "__main__":
    main()