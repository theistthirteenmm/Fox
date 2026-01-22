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
        
        test_response = await self._generate_raw(test_prompt, None)
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
    
    async def generate_response(self, message: str, context: List[Dict] = None, personality: Dict = None, thinking_callback=None) -> str:
        """تولید پاسخ با رویکرد جدید: AI اول، بعد بهبود با dataset"""
        
        # نمایش پیام ساده thinking
        if thinking_callback:
            await thinking_callback("صبور باشید، در حال آماده کردن جواب روباه...")
        
        # اطمینان از بارگذاری مدل
        if not self.is_model_loaded:
            print("🔄 مدل بارگذاری نشده، در حال راه‌اندازی...")
            await self.initialize_model()
        
        # مرحله 1: تحلیل اولیه پیام
        print("🔍 مرحله 1: تحلیل پیام کاربر...")
        code_analysis = self.analyze_user_code(message)
        user_analysis = user_profiler.analyze_message(message)
        user_profiler.update_profile(message, user_analysis)
        analysis = self.dataset_manager.analyze_user_message(message, context)
        print(f"� تحلیل: {analysis}")
        
        # مرحله 2: جستجوی وب (اگر نیاز باشه)
        web_info = None
        if self.web_enabled and self.web_search.should_search_web(message, context):
            if self.web_search.is_online():
                print("🌐 مرحله 2: جستجوی اطلاعات از اینترنت...")
                web_info = await self.web_search.search_and_summarize(message)
        
        # مرحله 3: تولید پاسخ اولیه توسط AI مدل
        print("🤖 مرحله 3: تولید پاسخ اولیه توسط مدل AI...")
        initial_prompt = self._build_initial_prompt(message, context, personality, web_info, code_analysis)
        initial_response = await self._generate_raw(initial_prompt, thinking_callback)
        
        if not initial_response or initial_response.strip() == "":
            print("⚠️ مدل پاسخ خالی داد، استفاده از fallback")
            initial_response = self._generate_fallback_response(message, web_info)
        
        print(f"✅ پاسخ اولیه: {initial_response[:100]}...")
        
        # مرحله 4: بهبود پاسخ با dataset ها
        print("📚 مرحله 4: بهبود پاسخ با dataset ها...")
        enhanced_response = await self._enhance_response_with_datasets(
            message, initial_response, analysis, web_info, code_analysis
        )
        
        # مرحله 5: ساختاردهی نهایی پاسخ
        print("🎯 مرحله 5: ساختاردهی نهایی پاسخ...")
        final_response = self._structure_final_response(
            message, enhanced_response, analysis, web_info, code_analysis
        )
        
        # مرحله 6: تبدیل به prompt برای یادگیری
        print("🧠 مرحله 6: ایجاد prompt یادگیری...")
        learning_prompt = self._create_learning_prompt(message, final_response, analysis, context)
        
        # ذخیره برای یادگیری
        self._store_for_learning(message, final_response, context, web_info, learning_prompt)
        self.dataset_manager.learn_from_interaction(message, final_response)
        
        return final_response
    
    def _build_prompt(self, message: str, context: List[Dict] = None, personality: Dict = None, web_info: Dict = None) -> str:
        """ساخت prompt کامل"""
        
        system_prompt = """تو روباه هستی، یک دستیار هوش مصنوعی فارسی که:
- همیشه به فارسی پاسخ می‌دهی
- دوستانه و مفید هستی
- پاسخ‌هایت کوتاه و مفید باشند (حداکثر 2-3 جمله)
- مستقیم به سؤال جواب می‌دهی"""
        
        # اضافه کردن اطلاعات وب اگر موجود باشه
        web_text = ""
        if web_info and web_info.get('summary'):
            web_text = f"\n\nاطلاعات جدید از اینترنت:\n{web_info['summary']}\n"
        
        # اضافه کردن context کوتاه از حافظه
        context_text = ""
        if context:
            recent_context = context[-2:]  # فقط آخرین 2 مورد
            if recent_context:
                context_text = "\n\nمکالمه قبلی:\n"
                for item in recent_context:
                    content = item.get('content', '')[:100]  # محدود کردن طول
                    context_text += f"- {content}\n"
        
        full_prompt = f"""{system_prompt}
{context_text}
{web_text}

کاربر: {message}
روباه:"""
        
        return full_prompt
    
    async def _generate_raw(self, prompt: str, thinking_callback=None) -> Optional[str]:
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
                            "num_predict": 150,  # محدود کردن تعداد توکن‌های تولیدی
                            "stop": ["\n\nکاربر:", "\nکاربر:", "Human:", "User:", "\n\n"]  # توقف در نقاط مناسب
                        }
                    },
                    timeout=30,  # کاهش timeout به 30 ثانیه
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
    
    def _store_for_learning(self, user_message: str, ai_response: str, context: List[Dict], web_info: Dict = None, learning_prompt: str = None):
        """ذخیره داده برای یادگیری آینده"""
        learning_entry = {
            "timestamp": datetime.now().isoformat(),
            "user_message": user_message,
            "ai_response": ai_response,
            "context_used": len(context) if context else 0,
            "web_search_used": bool(web_info),
            "web_sources": web_info.get('sources', 0) if web_info else 0,
            "learning_prompt": learning_prompt,
            "quality_score": None  # بعداً با feedback کاربر پر می‌شود
        }
        
        self.learning_data.append(learning_entry)
        
        # ذخیره در فایل
        os.makedirs("data/learning", exist_ok=True)
        with open("data/learning/conversations.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps(learning_entry, ensure_ascii=False) + "\n")
        
        # ذخیره prompt یادگیری جداگانه
        if learning_prompt:
            with open("data/learning/learning_prompts.md", "a", encoding="utf-8") as f:
                f.write(f"\n\n---\n\n{learning_prompt}")
        
        print("📚 داده‌های یادگیری ذخیره شد")
    
    def _generate_fallback_response(self, message: str, web_info: Dict = None) -> str:
        """تولید پاسخ fallback وقتی مدل کار نمی‌کند"""
        
        # اگر اطلاعات وب داریم، اولویت با اون باشه
        if web_info and web_info.get('summary'):
            return f"بر اساس جستجوی اینترنت:\n\n{web_info['summary']}\n\n(مدل AI من الان کمی کند هست، اما این اطلاعات رو از اینترنت برات پیدا کردم! 🦊)"
        
        # پاسخ‌های fallback هوشمند بر اساس نوع سؤال
        message_lower = message.lower()
        
        import random
        
        # سؤالات درباره آب و هوا
        if any(word in message_lower for word in ["دما", "هوا", "آب و هوا", "بارش", "باران", "برف", "گرما", "سرما"]):
            responses = [
                "متأسفانه الان نمی‌تونم اطلاعات دقیق آب و هوا رو بهت بدم. بهتره از سایت‌های هواشناسی چک کنی! 🌤️",
                "برای اطلاعات دقیق آب و هوا، پیشنهاد می‌کنم از اپ هواشناسی استفاده کنی 🌡️",
                "الان مشکل فنی دارم برای دریافت اطلاعات آب و هوا. سایت هواشناسی رو چک کن! ☁️"
            ]
            return random.choice(responses)
        
        # سؤالات عمومی
        elif "؟" in message:
            responses = [
                "متأسفانه الان مشکل فنی دارم و نمی‌تونم جواب کاملی بدم. دوباره تلاش کن! 🤔",
                "ببخشید، الان کمی کندم! می‌تونی سؤالت رو ساده‌تر بپرسی؟ 😅",
                "مدل AI من الان مشکل داره. لطفاً دوباره امتحان کن! 🔄"
            ]
            return random.choice(responses)
        
        # سلام و احوال‌پرسی
        elif any(word in message_lower for word in ["سلام", "درود", "چطور", "حال"]):
            responses = [
                "سلام! خوشحالم که باهام حرف می‌زنی! 🦊",
                "درود بر تو! چطوری؟ 😊",
                "سلام عزیز! حالم خوبه، تو چطوری؟ 🌟"
            ]
            return random.choice(responses)
        
        # پاسخ عمومی
        else:
            responses = [
                "متأسفانه الان مشکل فنی دارم. لطفاً دوباره تلاش کن! 🔄",
                "ببخشید، مدل AI من کمی کنده. دوباره امتحان کن! 😅",
                "الان مشکل دارم، اما خوشحالم که باهام حرف می‌زنی! 💙"
            ]
            return random.choice(responses)
    
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
    
    def _build_initial_prompt(self, message: str, context: List[Dict] = None, personality: Dict = None, web_info: Dict = None, code_analysis: Dict = None) -> str:
        """ساخت prompt اولیه برای مدل AI"""
        
        system_prompt = """تو روباه هستی، یک دستیار هوش مصنوعی فارسی که:
- همیشه به فارسی پاسخ می‌دهی
- دوستانه و مفید هستی
- پاسخ‌هایت کوتاه و مفید باشند (حداکثر 3-4 جمله)
- مستقیم به سؤال جواب می‌دهی"""
        
        # اضافه کردن اطلاعات وب
        web_text = ""
        if web_info and web_info.get('summary'):
            web_text = f"\n\nاطلاعات جدید از اینترنت:\n{web_info['summary']}\n"
        
        # اضافه کردن تحلیل کد
        code_text = ""
        if code_analysis:
            code_text = f"\n\nتحلیل کد:\n{self._build_code_analysis_prompt(code_analysis)}\n"
        
        # اضافه کردن context کوتاه
        context_text = ""
        if context:
            recent_context = context[-2:]
            if recent_context:
                context_text = "\n\nمکالمه قبلی:\n"
                for item in recent_context:
                    content = item.get('content', '')[:100]
                    context_text += f"- {content}\n"
        
        prompt = f"""{system_prompt}
{context_text}
{web_text}
{code_text}

کاربر: {message}
روباه:"""
        
        return prompt
    
    async def _enhance_response_with_datasets(self, message: str, initial_response: str, analysis: Dict, web_info: Dict = None, code_analysis: Dict = None) -> str:
        """بهبود پاسخ اولیه با استفاده از dataset ها"""
        
        # دریافت پاسخ‌های مشابه از dataset
        similar_responses = self.dataset_manager.get_similar_responses(message, analysis)
        
        # دریافت الگوهای مکالمه مرتبط
        conversation_patterns = self.dataset_manager.get_conversation_patterns(analysis)
        
        # اگر dataset های مفیدی پیدا شد، پاسخ رو بهبود بده (بدون AI مدل)
        if similar_responses or conversation_patterns:
            print(f"📊 پیدا شد: {len(similar_responses)} پاسخ مشابه، {len(conversation_patterns)} الگو")
            
            # بهبود ساده بر اساس الگوها
            enhanced_response = initial_response
            
            # اگر الگوی خاصی داره، سبک رو بهبود بده
            if conversation_patterns:
                pattern = conversation_patterns[0]
                style = pattern.get('response_style', '')
                if 'دوستانه' in style and '😊' not in enhanced_response:
                    enhanced_response += " 😊"
                elif 'گرم' in style and '🦊' not in enhanced_response:
                    enhanced_response += " 🦊"
            
            return enhanced_response
        
        print("📊 dataset مفیدی پیدا نشد، پاسخ اولیه حفظ می‌شود")
        return initial_response
    
    def _structure_final_response(self, message: str, enhanced_response: str, analysis: Dict, web_info: Dict = None, code_analysis: Dict = None) -> str:
        """ساختاردهی نهایی پاسخ"""
        
        # اگر کد داشت، ساختار تخصصی
        if code_analysis:
            return self._structure_code_response(enhanced_response, code_analysis)
        
        # اگر اطلاعات وب داشت، ساختار اطلاعاتی
        if web_info and web_info.get('summary'):
            return self._structure_web_response(enhanced_response, web_info)
        
        # اگر سؤال پیچیده بود، ساختار تفصیلی
        if analysis.get('complexity') == 'complex':
            return self._structure_complex_response(enhanced_response, analysis)
        
        # ساختار عادی
        return enhanced_response
    
    def _structure_code_response(self, response: str, code_analysis: Dict) -> str:
        """ساختاردهی پاسخ برای کد"""
        analysis = code_analysis['analysis']
        
        structured = f"{response}\n\n"
        
        if analysis['issues']:
            structured += "🚨 مشکلات:\n"
            for issue in analysis['issues'][:3]:
                structured += f"• خط {issue['line']}: {issue['message']}\n"
            structured += "\n"
        
        if analysis['suggestions']:
            structured += "💡 پیشنهادات:\n"
            for suggestion in analysis['suggestions'][:3]:
                structured += f"• {suggestion['message']}\n"
        
        return structured.strip()
    
    def _structure_web_response(self, response: str, web_info: Dict) -> str:
        """ساختاردهی پاسخ برای اطلاعات وب"""
        structured = f"{response}\n\n"
        
        if web_info.get('sources'):
            structured += f"📊 منابع: {web_info['sources']} نتیجه از اینترنت"
        
        return structured.strip()
    
    def _structure_complex_response(self, response: str, analysis: Dict) -> str:
        """ساختاردهی پاسخ برای سؤالات پیچیده"""
        # برای سؤالات پیچیده، پاسخ رو بهتر ساختار بده
        lines = response.split('.')
        if len(lines) > 2:
            # اولین جمله به عنوان خلاصه
            summary = lines[0].strip() + "."
            # بقیه به عنوان جزئیات
            details = '. '.join(lines[1:]).strip()
            
            return f"{summary}\n\n📝 جزئیات: {details}"
        
        return response
    
    def _create_learning_prompt(self, message: str, response: str, analysis: Dict, context: List[Dict] = None) -> str:
        """تبدیل مکالمه به prompt برای یادگیری مجدد"""
        
        # ساخت prompt ساختاریافته
        learning_prompt = f"""# مکالمه یادگیری روباه

## تحلیل پیام کاربر:
- احساس: {analysis.get('emotion', 'نامشخص')}
- موضوع: {analysis.get('topic', 'عمومی')}
- هدف: {analysis.get('intent', 'مکالمه')}
- پیچیدگی: {analysis.get('complexity', 'ساده')}

## Context قبلی:
{self._format_context_for_learning(context)}

## مکالمه:
کاربر: {message}
روباه: {response}

## الگوی یادگیری:
این مکالمه نشان می‌دهد که برای پیام‌هایی با ویژگی‌های مشابه، پاسخ مناسب شامل:
- سبک: {self._extract_response_style(response)}
- طول: {len(response.split())} کلمه
- ساختار: {self._analyze_response_structure(response)}

## برای یادگیری آینده:
اگر کاربر پیام مشابهی با همین ویژگی‌ها فرستاد، می‌توان از این الگو استفاده کرد.
"""
        
        return learning_prompt
    
    def _format_context_for_learning(self, context: List[Dict] = None) -> str:
        """فرمت کردن context برای یادگیری"""
        if not context:
            return "هیچ context قبلی موجود نیست"
        
        formatted = ""
        for item in context[-3:]:  # آخرین 3 مورد
            content = item.get('content', '')[:100]
            formatted += f"- {content}\n"
        
        return formatted.strip()
    
    def _extract_response_style(self, response: str) -> str:
        """استخراج سبک پاسخ"""
        if "😊" in response or "🦊" in response:
            return "دوستانه و شاد"
        elif "🤔" in response or "💭" in response:
            return "تفکری و تحلیلی"
        elif "⚠️" in response or "❌" in response:
            return "هشداردهنده"
        elif "✅" in response or "👍" in response:
            return "مثبت و تأییدی"
        else:
            return "عادی و خنثی"
    
    def _analyze_response_structure(self, response: str) -> str:
        """تحلیل ساختار پاسخ"""
        lines = response.split('\n')
        sentences = response.split('.')
        
        if len(lines) > 3:
            return "چندخطی و ساختاریافته"
        elif len(sentences) > 3:
            return "چندجمله‌ای و تفصیلی"
        elif '?' in response:
            return "تعاملی و سؤال‌محور"
        else:
            return "ساده و مستقیم"
        """تولید پاسخ fallback وقتی مدل کار نمی‌کند"""
        
        # اگر اطلاعات وب داریم، اولویت با اون باشه
        if web_info and web_info.get('summary'):
            return f"بر اساس جستجوی اینترنت:\n\n{web_info['summary']}\n\n(مدل AI من الان کمی کند هست، اما این اطلاعات رو از اینترنت برات پیدا کردم! 🦊)"
        
        # پاسخ‌های fallback هوشمند بر اساس نوع سؤال
        message_lower = message.lower()
        
        import random
        
        # سؤالات درباره آب و هوا
        if any(word in message_lower for word in ["دما", "هوا", "آب و هوا", "بارش", "باران", "برف", "گرما", "سرما"]):
            responses = [
                "متأسفانه الان نمی‌تونم اطلاعات دقیق آب و هوا رو بهت بدم. بهتره از سایت‌های هواشناسی چک کنی! 🌤️",
                "برای اطلاعات دقیق آب و هوا، پیشنهاد می‌کنم از اپ هواشناسی استفاده کنی 🌡️",
                "الان مشکل فنی دارم برای دریافت اطلاعات آب و هوا. سایت هواشناسی رو چک کن! ☁️"
            ]
            return random.choice(responses)
        
        # سؤالات عمومی
        elif "؟" in message:
            responses = [
                "متأسفانه الان مشکل فنی دارم و نمی‌تونم جواب کاملی بدم. دوباره تلاش کن! �",
                "ببخشید، الان کمی کندم! می‌تونی سؤالت رو ساده‌تر بپرسی؟ 😅",
                "مدل AI من الان مشکل داره. لطفاً دوباره امتحان کن! �"
            ]
            return random.choice(responses)
        
        # سلام و احوال‌پرسی
        elif any(word in message_lower for word in ["سلام", "درود", "چطور", "حال"]):
            responses = [
                "سلام! خوشحالم که باهام حرف می‌زنی! 🦊",
                "درود بر تو! چطوری؟ �",
                "سلام عزیز! حالم خوبه، تو چطوری؟ 🌟"
            ]
            return random.choice(responses)
        
        # پاسخ عمومی
        else:
            responses = [
                "متأسفانه الان مشکل فنی دارم. لطفاً دوباره تلاش کن! �",
                "ببخشید، مدل AI من کمی کنده. دوباره امتحان کن! 😅",
                "الان مشکل دارم، اما خوشحالم که باهام حرف می‌زنی! 💙"
            ]
            return random.choice(responses)