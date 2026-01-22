"""
هسته اصلی هوش مصنوعی روباه
مسئول تولید پاسخ‌ها و یادگیری
"""

import asyncio
import json
import requests
import re
from typing import Dict, List, Optional
from datetime import datetime
import os
import random
from .web_search import WebSearchEngine
from .dataset_manager import DatasetManager
from .code_analyzer import code_analyzer
from .user_profiler import user_profiler

class AIBrain:
    def __init__(self):
        self.model_name = "partai/dorna-llama3:8b-instruct-q8_0"  # مدل فارسی بهینه
        self.ollama_url = "http://localhost:11434"
        self.is_model_loaded = False
        self.conversation_history = []
        self.learning_data = []
        
        # سیستم جستجوی وب
        self.web_search = WebSearchEngine()
        self.web_enabled = True
        
        # سیستم دیتاست و پرامپت
        self.dataset_manager = DatasetManager()
        
    def is_loaded(self) -> bool:
        """بررسی آماده بودن مدل"""
        try:
            # تنظیمات برای عدم استفاده از proxy برای localhost
            proxies = {'http': None, 'https': None}
            
            response = requests.get(f"{self.ollama_url}/api/tags", proxies=proxies)
            if response.status_code == 200:
                models = response.json().get("models", [])
                return any(model["name"].startswith(self.model_name) for model in models)
        except:
            pass
        return False
    
    async def initialize_model(self):
        """راه‌اندازی اولیه مدل"""
        print("🧠 در حال بارگذاری مدل هوش مصنوعی...")
        
        if not self.is_loaded():
            print(f"📥 در حال دانلود مدل {self.model_name}...")
            # دانلود مدل اگر وجود نداشته باشد
            await self._pull_model()
        
        # تست اولیه مدل با prompt بهتر
        test_prompt = """تو روباه هستی، یک دستیار هوش مصنوعی فارسی. به فارسی پاسخ بده.

کاربر: سلام
روباه:"""
        
        test_response = await self._generate_raw(test_prompt)
        if test_response and len(test_response.strip()) > 0:
            self.is_model_loaded = True
            print(f"✅ مدل با موفقیت بارگذاری شد! پاسخ تست: {test_response[:50]}...")
        else:
            print("❌ خطا در بارگذاری مدل")
            # حتی اگر تست ناموفق بود، مدل را loaded در نظر بگیر
            self.is_model_loaded = True
    
    async def _pull_model(self):
        """دانلود مدل از Ollama"""
        try:
            # تنظیمات برای عدم استفاده از proxy برای localhost
            proxies = {'http': None, 'https': None}
            
            response = requests.post(
                f"{self.ollama_url}/api/pull",
                json={"name": self.model_name},
                stream=True,
                proxies=proxies
            )
            
            for line in response.iter_lines():
                if line:
                    data = json.loads(line)
                    if "status" in data:
                        print(f"📊 {data['status']}")
                        
        except Exception as e:
            print(f"خطا در دانلود مدل: {e}")
    
    async def generate_response(self, message: str, context: List[Dict] = None, personality: Dict = None) -> str:
        """تولید پاسخ اصلی با استفاده از دیتاست"""
        
        # اطمینان از بارگذاری مدل
        if not self.is_model_loaded:
            print("🔄 مدل بارگذاری نشده، در حال راه‌اندازی...")
            await self.initialize_model()
        
        # بررسی وجود کد در پیام
        code_analysis = self.analyze_user_code(message)
        
        # تحلیل کاربر و به‌روزرسانی پروفایل
        user_analysis = user_profiler.analyze_message(message)
        user_profiler.update_profile(message, user_analysis)
        
        # تحلیل پیام کاربر
        analysis = self.dataset_manager.analyze_user_message(message, context)
        print(f"🔍 تحلیل پیام: {analysis}")
        
        # بررسی پاسخ پیشنهادی از دیتاست
        suggested_response = self.dataset_manager.get_suggested_response(analysis)
        if suggested_response and analysis["intent"] == "conversation":
            print("💡 استفاده از پاسخ پیشنهادی دیتاست")
            self.dataset_manager.learn_from_interaction(message, suggested_response)
            return suggested_response
        
        # بررسی نیاز به جستجوی وب
        web_info = None
        if self.web_enabled and self.web_search.should_search_web(message, context):
            if self.web_search.is_online():
                print("🌐 در حال جستجوی اطلاعات از اینترنت...")
                web_info = await self.web_search.search_and_summarize(message)
        
        # ساخت prompt بهبود یافته
        enhanced_prompt = self.dataset_manager.generate_enhanced_prompt(
            message, analysis, context, personality
        )
        
        # اگر enhanced_prompt خالی بود، از _build_prompt استفاده کن
        if not enhanced_prompt or enhanced_prompt.strip() == "":
            enhanced_prompt = self._build_prompt(message, context, personality, web_info)
        
        # اضافه کردن تحلیل کد به prompt
        if code_analysis:
            code_prompt = self._build_code_analysis_prompt(code_analysis)
            enhanced_prompt += f"\n\n{code_prompt}"
        
        # اضافه کردن context شخصی‌سازی شده
        personalized_context = user_profiler.get_personalized_context()
        if personalized_context:
            enhanced_prompt += f"\n\nاطلاعات شخصی کاربر:\n{personalized_context}\n"
        
        # اضافه کردن اطلاعات وب به prompt
        if web_info and web_info.get('summary'):
            enhanced_prompt += f"\n\nاطلاعات جدید از اینترنت:\n{web_info['summary']}\n"
        
        # تولید پاسخ
        response = await self._generate_raw(enhanced_prompt)
        
        # اگر پاسخ خالی بود، یک پاسخ fallback بده
        if not response or response.strip() == "":
            print("⚠️ مدل پاسخ خالی داد، استفاده از fallback")
            response = self._generate_fallback_response(message, web_info)
        
        # یادگیری از تعامل
        self.dataset_manager.learn_from_interaction(message, response)
        
        # ذخیره برای یادگیری
        self._store_for_learning(message, response, context, web_info)
        
        return response
    
    def _build_prompt(self, message: str, context: List[Dict] = None, personality: Dict = None, web_info: Dict = None) -> str:
        """ساخت prompt کامل"""
        
        system_prompt = """تو روباه هستی، یک دستیار هوش مصنوعی شخصی فارسی که:
- همیشه به فارسی پاسخ می‌دهی
- دوستانه و مفید هستی
- با کاربر رشد می‌کنی و او را می‌شناسی
- از تجربیات قبلی یاد می‌گیری
- شخصیت منحصر به فردی داری
- در صورت نیاز از اینترنت اطلاعات جدید می‌گیری
- پاسخ‌هایت کوتاه و مفید باشند (حداکثر 2-3 جمله)"""
        
        # اضافه کردن context از حافظه
        context_text = ""
        if context:
            context_text = "\n\nاطلاعات مرتبط از حافظه:\n"
            for item in context[-3:]:  # آخرین 3 مورد
                context_text += f"- {item.get('content', '')}\n"
        
        # اضافه کردن اطلاعات شخصیت
        personality_text = ""
        if personality:
            personality_text = f"\n\nسطح رشد شخصیت: {personality.get('level', 1)}\n"
            personality_text += f"حالت فعلی: {personality.get('mood', 'خنثی')}\n"
        
        # اضافه کردن اطلاعات وب
        web_text = ""
        if web_info and web_info.get('summary'):
            web_text = f"\n\nاطلاعات جدید از اینترنت:\n{web_info['summary']}\n"
            web_text += "توجه: این اطلاعات تازه از اینترنت دریافت شده و می‌توانی از آن‌ها استفاده کنی.\n"
        
        full_prompt = f"""{system_prompt}
        
{context_text}
{personality_text}
{web_text}

کاربر: {message}
روباه:"""
        
        return full_prompt
    
    async def _generate_raw(self, prompt: str) -> Optional[str]:
        """تولید پاسخ خام از مدل"""
        max_retries = 2
        
        # تنظیمات برای عدم استفاده از proxy برای localhost
        proxies = {
            'http': None,
            'https': None
        }
        
        for attempt in range(max_retries):
            try:
                print(f"🤖 تلاش {attempt + 1} برای تولید پاسخ...")
                
                response = requests.post(
                    f"{self.ollama_url}/api/generate",
                    json={
                        "model": self.model_name,
                        "prompt": prompt,
                        "stream": False,
                        "options": {
                            "temperature": 0.7,
                            "top_p": 0.9,
                            "max_tokens": 300,  # کاهش تعداد توکن‌ها برای سرعت بیشتر
                            "stop": ["\n\nکاربر:", "\nکاربر:", "Human:", "User:"]  # توقف در نقاط مناسب
                        }
                    },
                    timeout=60,  # کاهش timeout به 1 دقیقه
                    proxies=proxies  # عدم استفاده از proxy
                )
                
                if response.status_code == 200:
                    result = response.json()
                    generated_text = result.get("response", "").strip()
                    
                    if generated_text:
                        print(f"✅ پاسخ تولید شد: {generated_text[:50]}...")
                        return generated_text
                    else:
                        print("⚠️ پاسخ خالی دریافت شد")
                        
                else:
                    print(f"❌ خطای HTTP: {response.status_code}")
                    
            except requests.exceptions.Timeout:
                print(f"⏰ Timeout در تلاش {attempt + 1}")
                if attempt < max_retries - 1:
                    print("🔄 تلاش مجدد...")
                    await asyncio.sleep(2)  # صبر 2 ثانیه قبل از تلاش مجدد
                    
            except Exception as e:
                print(f"❌ خطا در تولید پاسخ (تلاش {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(1)
        
        print("❌ تمام تلاش‌ها ناموفق بود")
        return None
    
    def _store_for_learning(self, user_message: str, ai_response: str, context: List[Dict], web_info: Dict = None):
        """ذخیره داده برای یادگیری آینده"""
        learning_entry = {
            "timestamp": datetime.now().isoformat(),
            "user_message": user_message,
            "ai_response": ai_response,
            "context_used": len(context) if context else 0,
            "web_search_used": bool(web_info),
            "web_sources": web_info.get('sources', 0) if web_info else 0,
            "quality_score": None  # بعداً با feedback کاربر پر می‌شود
        }
        
        self.learning_data.append(learning_entry)
        
        # ذخیره در فایل
        os.makedirs("data/learning", exist_ok=True)
        with open("data/learning/conversations.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps(learning_entry, ensure_ascii=False) + "\n")
    
    async def fine_tune_from_data(self):
        """Fine-tuning مدل بر اساس داده‌های جمع‌آوری شده"""
        # این بخش بعداً پیاده‌سازی می‌شود
        print("🎯 Fine-tuning در نسخه‌های آینده اضافه خواهد شد")
        pass
    
    def toggle_web_search(self, enabled: bool = None) -> bool:
        """فعال/غیرفعال کردن جستجوی وب"""
        if enabled is not None:
            self.web_enabled = enabled
        else:
            self.web_enabled = not self.web_enabled
        
        status = "فعال" if self.web_enabled else "غیرفعال"
        print(f"🌐 جستجوی وب {status} شد")
        return self.web_enabled
    
    def get_web_status(self) -> Dict:
        """وضعیت جستجوی وب"""
        return {
            "web_enabled": self.web_enabled,
            "internet_connected": self.web_search.is_online() if hasattr(self, 'web_search') else False,
            "search_engines": list(self.web_search.search_engines.keys()) if hasattr(self, 'web_search') else []
        }
    
    def _build_code_analysis_prompt(self, code_analysis: Dict) -> str:
        """ساخت prompt برای تحلیل کد"""
        analysis = code_analysis['analysis']
        original_code = code_analysis['original_code']
        
        prompt = f"""
🔍 تحلیل کد ارائه شده:

کد اصلی:
```{analysis['language']}
{original_code}
```

نتایج تحلیل:
- زبان برنامه‌نویسی: {analysis['language']}
- تعداد خطوط: {analysis['lines_count']}
- پیچیدگی: {analysis['complexity']}
- صحت syntax: {'✅ صحیح' if analysis['syntax_valid'] else '❌ خطا دارد'}

"""
        
        # اضافه کردن مشکلات
        if analysis['issues']:
            prompt += "🚨 مشکلات یافت شده:\n"
            for issue in analysis['issues']:
                prompt += f"- خط {issue['line']}: {issue['message']} ({issue['severity']})\n"
            prompt += "\n"
        
        # اضافه کردن پیشنهادات
        if analysis['suggestions']:
            prompt += "💡 پیشنهادات بهبود:\n"
            for suggestion in analysis['suggestions']:
                prompt += f"- خط {suggestion['line']}: {suggestion['message']}\n"
            prompt += "\n"
        
        # اضافه کردن پیشنهادات عمومی
        if analysis.get('general_suggestions'):
            prompt += "🎯 پیشنهادات عمومی:\n"
            for suggestion in analysis['general_suggestions']:
                prompt += f"- {suggestion}\n"
            prompt += "\n"
        
        # اضافه کردن کد اصلاح شده
        if analysis['fixed_code'] != original_code:
            prompt += f"🔧 کد اصلاح شده:\n```{analysis['language']}\n{analysis['fixed_code']}\n```\n\n"
        
        prompt += """
لطفاً به عنوان یک برنامه‌نویس ماهر:
1. کد را بررسی کن و مشکلات احتمالی را توضیح بده
2. راه‌حل‌های بهتر پیشنهاد بده
3. اگر کد خطا داره، نحوه اصلاح را بگو
4. بهترین practices را توضیح بده
5. به زبان فارسی و به صورت ساده توضیح بده
"""
        
        return prompt

    def detect_code_in_message(self, message: str) -> bool:
        """تشخیص وجود کد در پیام"""
        code_indicators = [
            'def ', 'function', 'class ', 'import ', 'from ',
            'var ', 'let ', 'const ', 'if (', 'for (', 'while (',
            'public class', '#include', 'SELECT', 'INSERT',
            '```', 'کد', 'برنامه', 'اسکریپت', 'function',
            '{', '}', '()', '=>', '==', '!=', '&&', '||'
        ]
        
        message_lower = message.lower()
        return any(indicator in message_lower for indicator in code_indicators)
    
    def extract_code_from_message(self, message: str) -> str:
        """استخراج کد از پیام"""
        # اگر کد در ``` قرار داره
        code_blocks = re.findall(r'```(?:\w+)?\n?(.*?)\n?```', message, re.DOTALL)
        if code_blocks:
            return code_blocks[0].strip()
        
        # اگر کد در خطوط جداگانه هست
        lines = message.split('\n')
        code_lines = []
        in_code_block = False
        
        for line in lines:
            if any(indicator in line for indicator in ['def ', 'function', 'class ', 'import']):
                in_code_block = True
            
            if in_code_block:
                code_lines.append(line)
                
                # اگر خط خالی یا غیرکد بود، توقف
                if line.strip() == '' or (not any(c in line for c in ['{', '}', '(', ')', '=', ';'])):
                    if len(code_lines) > 1:
                        break
        
        return '\n'.join(code_lines).strip()
    
    def analyze_user_code(self, message: str) -> Optional[Dict]:
        """تحلیل کد کاربر"""
        if not self.detect_code_in_message(message):
            return None
        
        code = self.extract_code_from_message(message)
        if not code:
            return None
        
        print(f"🔍 کد تشخیص داده شد: {code[:50]}...")
        
        # تحلیل کد
        analysis = code_analyzer.analyze_code(code)
        
        return {
            'original_code': code,
            'analysis': analysis,
            'has_issues': len(analysis['issues']) > 0,
            'has_suggestions': len(analysis['suggestions']) > 0
        }
        """تولید پاسخ fallback وقتی مدل کار نمی‌کند"""
        
        # اگر اطلاعات وب داریم
        if web_info and web_info.get('summary'):
            return f"بر اساس جستجوی اینترنت:\n\n{web_info['summary']}\n\nمتأسفانه مدل AI من الان مشکل دارد، اما این اطلاعات رو از اینترنت برات پیدا کردم! 🦊"
        
        # پاسخ‌های fallback متنوع بر اساس نوع سؤال
        message_lower = message.lower()
        
        import random
        
        if "سلام" in message_lower or "درود" in message_lower:
            responses = [
                "سلام! خوشحالم که باهام حرف می‌زنی! 🦊",
                "درود بر تو! چطوری؟ 😊",
                "سلام عزیز! امروز چه خبر؟ 🌟",
                "هی سلام! حالت چطوره؟ 💙"
            ]
            return random.choice(responses)
        
        elif "چطور" in message_lower or "حال" in message_lower:
            responses = [
                "ممنون که پرسیدی! من خوبم، تو چطوری؟ 😊",
                "عالی هستم! امیدوارم تو هم خوب باشی 🦊",
                "خوبم، مرسی! تو چه خبر؟ ✨",
                "حالم فوق‌العادست! تو چطوری؟ 💙"
            ]
            return random.choice(responses)
        
        elif "؟" in message:
            responses = [
                "سؤال جالبی پرسیدی! بذار فکر کنم... 🤔",
                "این سؤال رو دوست دارم! چه موضوع جالبی 💭",
                "خوب پرسیدی! این موضوع رو بررسی می‌کنم 🔍",
                "سؤال خوبی بود! بذار راجعش فکر کنم 🧠"
            ]
            return random.choice(responses)
        
        else:
            responses = [
                "جالب بود! بیشتر بگو 😊",
                "موضوع جذابی مطرح کردی! 🦊",
                "خوشحالم که باهام حرف می‌زنی! ✨",
                "این حرفت رو دوست داشتم! 💙",
                "جالبه! ادامه بده 🌟"
            ]
            return random.choice(responses)