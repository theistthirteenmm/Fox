"""
هسته اصلی هوش مصنوعی روباه
دستیار شخصی هوشمند - نسخه پیشرفته
"""

import asyncio
import json
import requests
import re
from typing import Dict, List, Optional
from datetime import datetime
import os
import random
from ..utils.web_search import WebSearchEngine
from ..utils.dataset_manager import DatasetManager
from ..utils.code_analyzer import code_analyzer
from .user_profiler import user_profiler
from ..learning.dynamic_name_learning import dynamic_name_learning
from ..learning.personal_learning_system import personal_learning_system

# سیستم دستیار شخصی
from .personal_ai_core import personal_ai, PersonalAI
from ..interfaces.physical_interface import physical_interface, EmotionExpression, MovementType

# سیستم‌های پیشرفته جدید
from ..utils.predictive_intelligence import predictive_intelligence
from ..utils.workplace_intelligence import workplace_intelligence, WorkMode, TaskPriority
from ..learning.deep_personality_learning import deep_personality_learning

# سیستم‌های بهینه‌سازی (اختیاری)
try:
    from ..utils.smart_cache import smart_cache
    from ..utils.task_queue import task_queue, TaskPriority as QueuePriority
    from ..utils.context_manager import context_manager, ContextType, ContextImportance
    from ..utils.response_templates import response_template_engine, ResponseType, ResponseTone
    OPTIMIZATION_ENABLED = True
except ImportError:
    OPTIMIZATION_ENABLED = False
    print("⚠️ سیستم‌های بهینه‌سازی غیرفعال - حالت ساده")

class AIBrain:
    def __init__(self):
        # تنظیمات چند مدله - مدل‌های دانلود شده و کارآمد
        self.models = {
            "persian": "partai/dorna-llama3:8b-instruct-q8_0",  # مدل فارسی تخصصی
            "general": "deepseek-r1:7b",                         # مدل استدلال (جایگزین عمومی)
            "reasoning": "deepseek-r1:7b",                       # مدل استدلال پیشرفته
            "code": "deepseek-coder-v2:16b",                    # مدل کد پیشرفته
            "code_light": "codellama:13b",                      # مدل کد سبک‌تر
            "fast": "llama3.2:3b",                              # مدل سریع (2.5s!)
            "multilingual": "partai/dorna-llama3:8b-instruct-q8_0",  # فارسی به جای qwen
            "heavy_general": "qwen2.5:32b",                     # مدل سنگین برای کیفیت بالا
            "ultra": "llama4:scout"                             # مدل بسیار سنگین
        }
        
        self.current_model = self.models["persian"]  # مدل پیش‌فرض
        self.ollama_url = "http://localhost:11434"
        self.is_model_loaded = False
        self.conversation_history = []
        self.learning_data = []
        
        # سیستم جستجوی وب
        self.web_search = WebSearchEngine()
        self.web_enabled = True
        
        # سیستم دیتاست و پرامپت
        self.dataset_manager = DatasetManager()
        
        # سیستم ردیابی مکالمه
        self.current_conversation_topic = None
        self.conversation_context_window = 10  # نگه‌داری آخرین 10 پیام
        self.topic_continuity_threshold = 3  # حداقل 3 پیام برای تشخیص موضوع مداوم
        
        # دستیار شخصی
        self.personal_ai = personal_ai
        self.physical_interface = physical_interface
        
        # آمار عملکرد
        self.performance_stats = {
            "total_requests": 0,
            "cache_hits": 0,
            "average_response_time": 0,
            "model_switches": 0,
            "personal_interactions": 0
        }
        
        # سیاست انتخاب مدل بر اساس سخت‌افزار فعلی
        self.allow_heavy_models = False  # پیش‌فرض: جلوگیری از مدل‌های بسیار سنگین
        self.heavy_models = {self.models["heavy_general"], self.models["ultra"]}
        
        print("� روباه - دستیار شخصی هوشمند آماده است!")
        print(f"👤 مالک: {self.personal_ai.owner_name}")
        print(f"🤝 سطح رابطه: {self.personal_ai.relationship_level.name}")
    async def generate_response_personal(self, 
                              message: str, 
                              context: List[Dict] = None,
                              thinking_callback: callable = None) -> Dict:
        """تولید پاسخ شخصی‌سازی شده برای دستیار شخصی"""
        
        start_time = datetime.now()
        self.performance_stats["total_requests"] += 1
        self.performance_stats["personal_interactions"] += 1
        
        try:
            # 1. پردازش تعامل شخصی
            if thinking_callback:
                await thinking_callback("در حال تحلیل پیام و شناخت بهتر شما...")
            
            personal_response = await self.personal_ai.process_interaction(
                message=message,
                context={"timestamp": start_time.isoformat()}
            )
            
            # 2. تشخیص نیاز به حرکت فیزیکی
            await self._handle_physical_response(message, personal_response)
            
            # 3. انتخاب مدل بر اساس تحلیل شخصی
            selected_model = self._select_model_for_personal_context(
                message, personal_response
            )
            
            # 4. تولید پاسخ AI
            if thinking_callback:
                await thinking_callback("در حال تولید پاسخ مناسب برای شما...")
            
            ai_response = await self._generate_ai_response_personal(
                message, selected_model, personal_response
            )
            
            # 5. ترکیب پاسخ شخصی با AI
            final_response = self._combine_personal_and_ai_response(
                ai_response, personal_response
            )
            
            # 6. یادگیری و به‌روزرسانی
            await self._update_personal_learning(message, final_response)
            
            # 7. آمار
            self._update_performance_stats(start_time)
            
            return {
                "response": final_response,
                "personality_state": personal_response["personality_state"],
                "relationship_level": personal_response["relationship_level"],
                "model_used": selected_model,
                "processing_time": (datetime.now() - start_time).total_seconds(),
                "physical_actions": self.physical_interface.get_physical_status()
            }
            
        except Exception as e:
            print(f"خطا در تولید پاسخ شخصی: {e}")
            # Fallback به پاسخ ساده
            return {
                "response": "متأسفم، مشکلی پیش آمد. می‌تونی دوباره بپرسی؟",
                "error": str(e)
            }
    
    async def _handle_physical_response(self, message: str, personal_response: Dict):
        """مدیریت پاسخ فیزیکی"""
        
        owner_emotion = personal_response.get("owner_emotion", "neutral")
        relationship_level = personal_response.get("relationship_level", "STRANGER")
        
        # تشخیص نیاز به حرکت
        if "بیا اینجا" in message.lower() or "نزدیک بیا" in message.lower():
            await self.physical_interface.move_to_owner(urgency=0.8)
        
        # بیان احساسات فیزیکی
        if owner_emotion == "stressed":
            await self.physical_interface.express_emotion(EmotionExpression.CONCERNED, 0.8)
        elif owner_emotion == "happy":
            await self.physical_interface.express_emotion(EmotionExpression.HAPPY, 0.7)
        elif owner_emotion == "curious":
            await self.physical_interface.express_emotion(EmotionExpression.CURIOUS, 0.6)
        
        # حرکات مرتبط با کار
        if "ارائه" in message.lower() or "نمایش" in message.lower():
            await self.physical_interface.perform_task_gesture("presentation")
        elif "توضیح" in message.lower():
            await self.physical_interface.perform_task_gesture("explanation")
        elif "فکر" in message.lower() or "بررسی" in message.lower():
            await self.physical_interface.perform_task_gesture("thinking")
    
    def _select_model_for_personal_context(self, message: str, personal_response: Dict) -> str:
        """انتخاب مدل بر اساس context شخصی"""
        
        # اولویت با تحلیل شخصی
        learning_insights = personal_response.get("learning_insights", {})
        domain = learning_insights.get("domain", "general")
        urgency = learning_insights.get("urgency", "medium")
        
        # انتخاب مدل بر اساس domain و urgency
        if domain == "tech" or self._detect_code_in_message(message):
            return self.models["code"]
        elif urgency == "high":
            return self.models["fast"]
        elif domain == "work" and len(message.split()) > 20:
            return self.models["general"]
        else:
            return self.models["persian"]  # پیش‌فرض برای دستیار شخصی
    
    async def _generate_ai_response_personal(self, 
                                           message: str, 
                                           model: str, 
                                           personal_context: Dict) -> str:
        """تولید پاسخ AI با context شخصی"""
        
        # ساخت prompt شخصی‌سازی شده
        personal_prompt = self._build_personal_prompt(message, personal_context)
        
        print(f"🔍 DEBUG: استفاده از مدل: {model}")
        print(f"🔍 DEBUG: URL: {self.ollama_url}/api/generate")
        
        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": model,
                    "prompt": personal_prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "top_p": 0.9,
                        "max_tokens": 400
                    }
                },
                proxies={'http': None, 'https': None},
                timeout=30
            )
            
            print(f"🔍 DEBUG: Status Code: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json().get("response", "متأسفم، نتوانستم پاسخ مناسبی تولید کنم.")
                print(f"🔍 DEBUG: پاسخ دریافت شد: {result[:50]}...")
                return result
            else:
                print(f"🔍 DEBUG: خطا: {response.text}")
                return "مشکلی در پردازش پیش آمد."
                
        except Exception as e:
            print(f"🔍 DEBUG: Exception: {e}")
            return "متأسفم، الان نمی‌تونم پاسخ بدم. لطفاً دوباره امتحان کن."
    
    def _select_best_model(self, message: str, context: Dict = None) -> str:
        """انتخاب بهترین مدل برای پیام - مدل‌های جدید 2025"""
        
        # تحلیل نوع پیام
        message_lower = message.lower()
        
        # کلمات کلیدی برای انواع مختلف
        code_keywords = ['کد', 'برنامه', 'function', 'class', 'def', 'import', 'python', 'javascript', 'html', 'css', 'sql', 'debug', 'error', 'bug']
        reasoning_keywords = ['تحلیل', 'استدلال', 'منطق', 'چرا', 'علت', 'دلیل', 'مقایسه', 'بررسی', 'تفکر', 'reasoning', 'logic', 'analyze']
        
        # انتخاب مدل بر اساس محتوا
        if any(keyword in message_lower for keyword in code_keywords):
            print("🤖 انتخاب مدل کد: deepseek-coder-v2")
            return self.models["code"]
            
        elif any(keyword in message_lower for keyword in reasoning_keywords):
            print("🧠 انتخاب مدل استدلال: deepseek-r1")
            return self.models["reasoning"]
            
        elif len(message) > 200:  # پیام‌های پیچیده
            print("🧠 انتخاب مدل استدلال: deepseek-r1")
            return self.models["general"]
        
        # استفاده از مدل سنگین فقط با درخواست صریح و اجازه
        if self._is_heavy_model_requested(message_lower) and self.allow_heavy_models:
            print("🏋️ استفاده از مدل سنگین با درخواست کاربر")
            return self.models["heavy_general"]
        
        # برای همه پیام‌های فارسی، از مدل فارسی استفاده کن
        print("🦊 انتخاب مدل فارسی پیش‌فرض")
        return self.models["persian"]

    def _is_heavy_model_requested(self, message_lower: str) -> bool:
        """تشخیص درخواست صریح برای مدل‌های سنگین/کیفیت بالا"""
        heavy_indicators = [
            "مدل سنگین", "مدل قوی", "کیفیت بالا", "مدل بزرگ", "بهترین کیفیت",
            "qwen", "llama4", "مدل 32b", "مدل 70b", "مدل خیلی بزرگ"
        ]
        return any(indicator in message_lower for indicator in heavy_indicators)
    
    def _build_personal_prompt(self, message: str, personal_context: Dict) -> str:
        """ساخت prompt شخصی‌سازی شده"""
        
        # استفاده از سیستم حافظه کاربر
        from .user_memory import user_memory
        
        owner_name = user_memory.get_user_name() or self.personal_ai.owner_name
        relationship_level = personal_context.get("relationship_level", "STRANGER")
        personality_state = personal_context.get("personality_state", {})
        
        # دریافت اطلاعات شخصی کاربر
        personal_info = user_memory.get_personal_info()
        recent_conversations = user_memory.get_recent_conversations(3)
        
        # ساخت context از مکالمات قبلی
        conversation_context = ""
        if recent_conversations:
            conversation_context = "\n\nمکالمات اخیر:\n"
            for conv in recent_conversations:
                conversation_context += f"- کاربر: {conv['user_message'][:50]}...\n"
                conversation_context += f"- روباه: {conv['ai_response'][:50]}...\n"
        
        # اطلاعات شخصی
        personal_info_text = ""
        if personal_info:
            personal_info_text = f"\n\nاطلاعات شخصی {owner_name}:\n"
            for key, value in personal_info.items():
                if not key.startswith("interest_"):
                    personal_info_text += f"- {key}: {value}\n"
        
        # اطلاعات شخصی
        current_ai_name = dynamic_name_learning.get_current_name()
        name_confidence = dynamic_name_learning.get_name_confidence()
        
        personal_info = f"""
تو {current_ai_name} هستی، دستیار شخصی هوشمند {owner_name or 'کاربر'}.
نام تو "{current_ai_name}" است (اعتماد: {name_confidence:.1f}).
{owner_name} مالک و سازنده توست.
سطح رابطه‌تان: {relationship_level}
تعداد تعاملات: {personality_state.get('total_interactions', 0)}
سطح اعتماد: {personality_state.get('trust_level', 0.1):.1f}

ویژگی‌های شخصیتی تو:
- وفادار و قابل اعتماد
- کنجکاو و یادگیرنده
- کمک‌کار و پیش‌قدم
- حافظه قوی از تعاملات قبلی
- نام تو قابل تغییر است و از مکالمه یاد می‌گیری

{personal_info_text}
{conversation_context}

نحوه پاسخ:
- با {owner_name or 'کاربر'} صمیمی و دوستانه صحبت کن
- از تجربیات قبلی‌تان استفاده کن
- پاسخ‌هایت شخصی و مفید باشد
- اگر کاری می‌تونی انجام بدی، پیشنهاد بده
- پاسخت کوتاه و مفید باشد (حداکثر 2-3 جمله)
- اگر درباره نامت سؤال شد، بگو اسمت {current_ai_name} است
- اگر نام جدیدی پیشنهاد شد، آماده تغییر باش
"""
        
        # پیام کاربر
        user_message = f"\n{owner_name or 'کاربر'}: {message}\n\nروباه:"
        
        return personal_info + user_message
    
    def _combine_personal_and_ai_response(self, ai_response: str, personal_context: Dict) -> str:
        """ترکیب پاسخ AI با جنبه‌های شخصی"""
        
        relationship_level = personal_context.get("relationship_level", "STRANGER")
        owner_emotion = personal_context.get("owner_emotion", "neutral")
        
        # اضافه کردن لمس شخصی
        if relationship_level in ["COMPANION", "CLOSE_FRIEND"]:
            if owner_emotion == "stressed":
                personal_touch = " نگران نباش، من اینجام کمکت کنم. 💙"
            elif owner_emotion == "happy":
                personal_touch = " خوشحالم که حالت خوبه! 😊"
            else:
                personal_touch = ""
        else:
            personal_touch = ""
        
        return ai_response + personal_touch
    
    async def _update_personal_learning(self, message: str, response: str):
        """به‌روزرسانی یادگیری شخصی"""
        
        # این کار در personal_ai.process_interaction انجام می‌شود
        # اینجا می‌توانیم آمار اضافی اضافه کنیم
        
        # به‌روزرسانی الگوهای استفاده
        current_hour = datetime.now().hour
        if current_hour not in self.personal_ai.learned_patterns.get("usage_hours", {}):
            if "usage_hours" not in self.personal_ai.learned_patterns:
                self.personal_ai.learned_patterns["usage_hours"] = {}
            self.personal_ai.learned_patterns["usage_hours"][current_hour] = 0
        
        self.personal_ai.learned_patterns["usage_hours"][current_hour] += 1
        """تولید پاسخ بهینه‌سازی شده با استفاده از سیستم‌های جدید"""
        
        start_time = datetime.now()
        self.performance_stats["total_requests"] += 1
        
        try:
            # 1. بررسی Cache
            cached_response = smart_cache.get_cached_response(message, context)
            if cached_response:
                self.performance_stats["cache_hits"] += 1
                return cached_response["response"]
            
            # 2. تحلیل Context
            relevant_contexts = context_manager.get_relevant_contexts(message)
            context_data = {
                "message_type": self._analyze_message_type(message),
                "emotion": self._detect_emotion_simple(message),
                "complexity": self._assess_complexity(message),
                "time_of_day": self._get_time_of_day()
            }
            
            # 3. انتخاب مدل بهینه
            selected_model = self._select_best_model(message, relevant_contexts)
            if selected_model != self.current_model:
                self.current_model = selected_model
                self.performance_stats["model_switches"] += 1
            
            # 4. تولید پاسخ غیرهمزمان
            if thinking_callback:
                await thinking_callback("در حال تحلیل پیام و انتخاب بهترین روش پاسخ...")
            
            # اضافه کردن task به صف
            task_id = task_queue.add_task(
                name=f"generate_response_{message[:20]}",
                func=self._generate_ai_response,
                message=message,
                model=selected_model,
                context=relevant_contexts,
                priority=TaskPriority.HIGH
            )
            
            # انتظار برای تکمیل task
            ai_response = await task_queue.wait_for_task(task_id, timeout=30.0)
            
            # 5. بهبود پاسخ با Template Engine
            enhanced_response = self._enhance_response_with_templates(
                ai_response, context_data
            )
            
            # 6. ذخیره در Cache
            final_response = {
                "response": enhanced_response,
                "model_used": selected_model,
                "context_items": len(relevant_contexts),
                "processing_time": (datetime.now() - start_time).total_seconds()
            }
            
            smart_cache.cache_response(message, final_response, context)
            
            # 7. به‌روزرسانی Context Manager
            context_manager.update_active_contexts(message, enhanced_response)
            
            # 8. به‌روزرسانی آمار
            self._update_performance_stats(start_time)
            
            return final_response
            
        except Exception as e:
            print(f"خطا در تولید پاسخ بهینه: {e}")
            # Fallback به روش قدیمی
            return await self.generate_response(message, context, thinking_callback)
    
    def _analyze_message_type(self, message: str) -> str:
        """تحلیل نوع پیام"""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ["سلام", "درود", "صبح بخیر"]):
            return "greeting"
        elif "؟" in message:
            return "question"
        elif any(word in message_lower for word in ["کمک", "راهنمایی", "بگو"]):
            return "help_request"
        elif self._detect_code_in_message(message):
            return "code"
        else:
            return "general"
    
    def _detect_emotion_simple(self, message: str) -> str:
        """تشخیص ساده احساسات"""
        message_lower = message.lower()
        
        positive_words = ["خوشحال", "عالی", "فوق‌العاده", "ممنون", "متشکر"]
        negative_words = ["ناراحت", "عصبانی", "خسته", "مشکل", "بد"]
        
        if any(word in message_lower for word in positive_words):
            return "positive"
        elif any(word in message_lower for word in negative_words):
            return "negative"
        else:
            return "neutral"
    
    def _assess_complexity(self, message: str) -> str:
        """ارزیابی پیچیدگی پیام"""
        word_count = len(message.split())
        
        if word_count < 5:
            return "simple"
        elif word_count < 20:
            return "medium"
        else:
            return "complex"
    
    def _get_time_of_day(self) -> str:
        """تشخیص زمان روز"""
        hour = datetime.now().hour
        
        if 5 <= hour < 12:
            return "morning"
        elif 12 <= hour < 17:
            return "afternoon"
        elif 17 <= hour < 21:
            return "evening"
        else:
            return "night"
    
    async def _generate_ai_response(self, message: str, model: str, context: List) -> str:
        """تولید پاسخ AI (برای استفاده در Task Queue)"""
        # این متد باید async باشد برای Task Queue
        return await self._call_ollama_async(message, model, context)
    
    async def _call_ollama_async(self, message: str, model: str, context: List) -> str:
        """فراخوانی غیرهمزمان Ollama"""
        # پیاده‌سازی فراخوانی async به Ollama
        # (این بخش باید با کتابخانه async HTTP مثل aiohttp پیاده‌سازی شود)
        
        # فعلاً از روش sync استفاده می‌کنیم
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(
            None, 
            self._call_ollama_sync, 
            message, model, context
        )
    
    def _call_ollama_sync(self, message: str, model: str, context: List) -> str:
        """فراخوانی همزمان Ollama"""
        try:
            # ساخت prompt
            prompt = self._build_prompt(message, context)
            
            # فراخوانی API
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "top_p": 0.9,
                        "max_tokens": 500
                    }
                },
                proxies={'http': None, 'https': None},
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json().get("response", "متأسفم، نتوانستم پاسخ مناسبی تولید کنم.")
            else:
                return "خطا در ارتباط با مدل AI."
                
        except Exception as e:
            print(f"خطا در فراخوانی Ollama: {e}")
            return "متأسفم، مشکلی در پردازش پیام شما پیش آمد."
    
    def _enhance_response_with_templates(self, ai_response: str, context_data: Dict) -> str:
        """بهبود پاسخ با استفاده از Template Engine"""
        
        message_type = context_data.get("message_type", "general")
        emotion = context_data.get("emotion", "neutral")
        
        # تعیین نوع پاسخ برای Template Engine
        if message_type == "greeting":
            response_type = ResponseType.GREETING
        elif message_type == "question":
            response_type = ResponseType.QUESTION_ANSWER
        elif message_type == "help_request":
            response_type = ResponseType.HELP
        elif message_type == "code":
            response_type = ResponseType.CODE
        else:
            response_type = ResponseType.EXPLANATION
        
        # تولید پاسخ با template (در صورت امکان)
        template_response = response_template_engine.generate_response(
            response_type=response_type,
            variables={"answer": ai_response, "additional_info": ""},
            context=context_data
        )
        
        # اگر template موجود نبود، از پاسخ اصلی استفاده کن
        return template_response or ai_response
    
    def _update_performance_stats(self, start_time: datetime):
        """به‌روزرسانی آمار عملکرد"""
        processing_time = (datetime.now() - start_time).total_seconds()
        
        # محاسبه میانگین زمان پاسخ
        total_requests = self.performance_stats["total_requests"]
        current_avg = self.performance_stats["average_response_time"]
        
        new_avg = ((current_avg * (total_requests - 1)) + processing_time) / total_requests
        self.performance_stats["average_response_time"] = new_avg
    
    def get_optimization_stats(self) -> Dict:
        """آمار بهینه‌سازی"""
        cache_stats = smart_cache.get_cache_stats()
        queue_stats = task_queue.get_queue_stats()
        context_stats = context_manager.get_context_summary()
        template_stats = response_template_engine.get_template_stats()
        
        return {
            "performance": self.performance_stats,
            "cache": cache_stats,
            "task_queue": queue_stats,
            "context_manager": context_stats,
            "template_engine": template_stats
        }
        """انتخاب بهترین مدل بر اساس نوع پیام"""
        message_lower = message.lower()
        
        # تشخیص کد
        if self._detect_code_in_message(message):
            print("🔧 انتخاب مدل کد برای پردازش")
            return self.models["code"]
        
        # تشخیص زبان فارسی
        persian_chars = len([c for c in message if '\u0600' <= c <= '\u06FF'])
        total_chars = len([c for c in message if c.isalpha()])
        
        if total_chars > 0 and (persian_chars / total_chars) > 0.3:
            print("🇮🇷 انتخاب مدل فارسی")
            return self.models["persian"]
        
        # برای پیام‌های کوتاه و سریع
        if len(message.split()) < 10:
            print("⚡ انتخاب مدل سریع")
            return self.models["fast"]
        
        # برای پیام‌های پیچیده
        print("🧠 انتخاب مدل عمومی قدرتمند")
        return self.models["general"]
    
    def _detect_code_in_message(self, message: str) -> bool:
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

    def is_loaded(self) -> bool:
        """بررسی آماده بودن مدل"""
        try:
            # تنظیمات برای عدم استفاده از proxy برای localhost
            proxies = {'http': None, 'https': None}
            
            response = requests.get(f"{self.ollama_url}/api/tags", proxies=proxies)
            if response.status_code == 200:
                models = response.json().get("models", [])
                # بررسی وجود حداقل یکی از مدل‌ها
                available_models = [model["name"] for model in models]
                for model_name in self.models.values():
                    if any(model_name in available for available in available_models):
                        return True
        except:
            pass
        return False
    
    async def initialize_model(self):
        """راه‌اندازی اولیه مدل‌ها"""
        print("🧠 در حال بررسی مدل‌های موجود...")
        
        # بررسی مدل‌های موجود
        available_models = await self._get_available_models()
        
        # انتخاب بهترین مدل موجود
        best_model = None
        for model_type, model_name in self.models.items():
            if any(model_name in available for available in available_models):
                best_model = model_name
                print(f"✅ مدل {model_type} موجود: {model_name}")
                break
        
        if not best_model:
            print("❌ هیچ مدل مناسبی یافت نشد")
            # استفاده از مدل فارسی به عنوان fallback
            best_model = self.models["persian"]
            print(f"📥 در حال دانلود مدل پیش‌فرض: {best_model}")
            await self._pull_model(best_model)
        
        self.current_model = best_model
        
        # تست اولیه مدل با prompt بهتر
        test_prompt = f"""تو {dynamic_name_learning.get_current_name()} هستی، یک دستیار هوش مصنوعی فارسی. به فارسی پاسخ بده.
نام تو "{dynamic_name_learning.get_current_name()}" است.

کاربر: سلام
{dynamic_name_learning.get_current_name()}:"""
        
        test_response = await self._generate_raw(test_prompt, None)
        if test_response and len(test_response.strip()) > 0:
            self.is_model_loaded = True
            print(f"✅ مدل با موفقیت بارگذاری شد! پاسخ تست: {test_response[:50]}...")
        else:
            print("❌ خطا در بارگذاری مدل")
            # حتی اگر تست ناموفق بود، مدل را loaded در نظر بگیر
            self.is_model_loaded = True
    
    async def _get_available_models(self) -> List[str]:
        """دریافت لیست مدل‌های موجود"""
        try:
            proxies = {'http': None, 'https': None}
            response = requests.get(f"{self.ollama_url}/api/tags", proxies=proxies)
            if response.status_code == 200:
                models = response.json().get("models", [])
                return [model["name"] for model in models]
        except:
            pass
        return []
    
    async def _pull_model(self, model_name: str = None):
        """دانلود مدل از Ollama"""
        if not model_name:
            model_name = self.current_model
            
        try:
            # تنظیمات برای عدم استفاده از proxy برای localhost
            proxies = {'http': None, 'https': None}
            
            print(f"📥 در حال دانلود {model_name}...")
            response = requests.post(
                f"{self.ollama_url}/api/pull",
                json={"name": model_name},
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
        """تولید پاسخ با رویکرد جدید: AI اول، بعد بهبود با dataset + Context Awareness"""
        
        # نمایش پیام ساده thinking
        if thinking_callback:
            await thinking_callback("صبور باشید، در حال آماده کردن جواب روباه...")
        
        # اطمینان از بارگذاری مدل
        if not self.is_model_loaded:
            print("🔄 مدل بارگذاری نشده، در حال راه‌اندازی...")
            await self.initialize_model()
        
        # مرحله 1: تحلیل اولیه پیام و context
        print("🔍 مرحله 1: تحلیل پیام و context مکالمه...")
        
        # مرحله 0: بررسی یادگیری نام
        name_analysis = dynamic_name_learning.analyze_message_for_name(message)
        if name_analysis:
            print(f"🎭 تشخیص درخواست نام: {name_analysis['type']}")
            name_result = dynamic_name_learning.learn_name(name_analysis)
            if name_result.get("response"):
                print(f"✅ پاسخ نام: {name_result['response'][:50]}...")
                return name_result["response"]
        
        # مرحله 0.5: بررسی یادگیری شخصی (واژگان، قوانین، لحن)
        personal_analysis = personal_learning_system.analyze_message_for_learning(message)
        if personal_analysis:
            print(f"🧠 تشخیص یادگیری شخصی: {personal_analysis['type']}")
            learning_result = personal_learning_system.learn_from_analysis(personal_analysis)
            if learning_result.get("response"):
                print(f"✅ پاسخ یادگیری: {learning_result['response'][:50]}...")
                return learning_result["response"]
        
        # مرحله 0.6: یادگیری ضمنی پروفایل کاربر
        profile_updates = personal_learning_system.learn_profile_from_message(message)
        if profile_updates:
            print(f"👤 بروزرسانی پروفایل: {len(profile_updates)} مورد")
        
        # مرحله 0.7: مشاهده تعامل برای رشد رابطه و حافظه شخصی
        try:
            await self.personal_ai.observe_interaction(message, context={"context": context or []})
        except Exception as e:
            print(f"⚠️ خطا در مشاهده تعامل شخصی: {e}")
        
        # تشخیص موضوع فعلی و ارتباط با مکالمه قبلی
        conversation_topic = self._detect_conversation_topic(message, context)
        topic_continuity = self._check_topic_continuity(conversation_topic, context)
        
        print(f"📋 موضوع مکالمه: {conversation_topic}")
        print(f"🔗 ادامه موضوع قبلی: {'بله' if topic_continuity else 'خیر'}")
        
        # به‌روزرسانی موضوع فعلی مکالمه
        if topic_continuity:
            print(f"✅ ادامه مکالمه درباره: {self.current_conversation_topic}")
        else:
            # اگر درخواست تغییر موضوع بود، context رو محدود کن
            if self._is_topic_change_request(message):
                print("🔄 پاک کردن context قدیمی برای موضوع جدید")
                # فقط آخرین پیام رو نگه دار
                context = context[-1:] if context else []
            
            self.current_conversation_topic = conversation_topic
            print(f"🆕 شروع موضوع جدید: {conversation_topic}")
        
        code_analysis = self.analyze_user_code(message)
        user_analysis = user_profiler.analyze_message(message)
        user_profiler.update_profile(message, user_analysis)
        analysis = self.dataset_manager.analyze_user_message(message, context)
        
        # اضافه کردن اطلاعات موضوع به تحلیل
        analysis['conversation_topic'] = self.current_conversation_topic
        analysis['topic_continuity'] = topic_continuity
        
        print(f"📊 تحلیل: {analysis}")
        
        # مرحله 2: جستجوی وب (اگر نیاز باشه)
        web_info = None
        if self.web_enabled and self.web_search.should_search_web(message, context):
            if self.web_search.is_online():
                print("🌐 مرحله 2: جستجوی اطلاعات از اینترنت...")
                web_info = await self.web_search.search_and_summarize(message)
        
        # انتخاب بهترین مدل برای این پیام
        selected_model = self._select_best_model(message, context)
        self.current_model = selected_model
        
        # مرحله 3: تولید پاسخ اولیه توسط AI مدل با context بهبود یافته
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
        
        # مرحله 5.5: شخصی‌سازی نهایی بر اساس یادگیری‌ها
        final_response = self._personalize_final_response(
            message, final_response, analysis
        )
        
        # مرحله 6: تبدیل به prompt برای یادگیری
        print("🧠 مرحله 6: ایجاد prompt یادگیری...")
        learning_prompt = self._create_learning_prompt(message, final_response, analysis, context)
        
        # ذخیره برای یادگیری
        self._store_for_learning(message, final_response, context, web_info, learning_prompt)
        self.dataset_manager.learn_from_interaction(message, final_response)
        
        # تحلیل عمیق شخصیت و ذخیره
        try:
            await deep_personality_learning.analyze_interaction(
                message=message,
                context={"context": context or []},
                response=final_response
            )
        except Exception as e:
            print(f"⚠️ خطا در تحلیل عمیق شخصیت: {e}")
        
        return final_response
    
    def _build_prompt(self, message: str, context: List[Dict] = None, personality: Dict = None, web_info: Dict = None) -> str:
        """ساخت prompt کامل"""
        
        system_prompt = f"""تو {dynamic_name_learning.get_current_name()} هستی، یک دستیار هوش مصنوعی فارسی که:
- همیشه به فارسی پاسخ می‌دهی
- دوستانه و مفید هستی
- نام تو "{dynamic_name_learning.get_current_name()}" است
- پاسخ‌هایت کوتاه و مفید باشند (حداکثر 2-3 جمله)
- مستقیم به سؤال جواب می‌دهی
- نام تو قابل تغییر است و از مکالمه یاد می‌گیری"""
        
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
        max_retries = 3  # افزایش تعداد تلاش‌ها
        
        # تنظیمات برای عدم استفاده از proxy برای localhost
        proxies = {
            'http': None,
            'https': None
        }
        
        # تست اتصال اولیه
        try:
            test_response = requests.get(f"{self.ollama_url}/api/tags", proxies=proxies, timeout=5)
            if test_response.status_code != 200:
                print("❌ Ollama Server در دسترس نیست")
                return None
        except:
            print("❌ خطا در اتصال به Ollama Server")
            return None
        
        for attempt in range(max_retries):
            try:
                print(f"🤖 تلاش {attempt + 1} برای تولید پاسخ...")
                
                response = requests.post(
                    f"{self.ollama_url}/api/generate",
                    json={
                        "model": self.current_model,  # استفاده از مدل انتخاب شده
                        "prompt": prompt,
                        "stream": False,
                        "options": {
                            "temperature": 0.7,
                            "top_p": 0.9,
                            "num_predict": 150,  # محدود کردن تعداد توکن‌های تولیدی
                            "stop": ["\n\nکاربر:", "\nکاربر:", "Human:", "User:", "\n\n"]  # توقف در نقاط مناسب
                        }
                    },
                    timeout=60,  # افزایش timeout به 60 ثانیه
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
                    await asyncio.sleep(3)  # افزایش زمان انتظار
                    
            except Exception as e:
                print(f"❌ خطا در تولید پاسخ (تلاش {attempt + 1}): {e}")
                if attempt < max_retries - 1:
                    await asyncio.sleep(2)
        
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
        
        # بررسی اطلاعات کاربر از حافظه
        user_name = self.personal_ai.owner_name if hasattr(self, 'personal_ai') else None
        
        # اگر اطلاعات وب داریم، اولویت با اون باشه
        if web_info and web_info.get('summary'):
            greeting = f"سلام {user_name}! " if user_name else "سلام! "
            return f"{greeting}بر اساس جستجوی اینترنت:\n\n{web_info['summary']}\n\n📊 منابع: {web_info.get('sources', 1)} نتیجه از اینترنت"
        
        # پاسخ‌های fallback هوشمند بر اساس نوع سؤال
        message_lower = message.lower()
        
        import random
        
        # سؤالات درباره آب و هوا
        if any(word in message_lower for word in ["دما", "هوا", "آب و هوا", "بارش", "باران", "برف", "گرما", "سرما"]):
            responses = [
                "متأسفانه الان نمی‌تونم اطلاعات دقیق آب و هوا رو بهت بدم. بهتره از سایت‌های هواشناسی چک کنی! 🌤️",
                "برای اطلاعات دقیق آب و هوا، پیشنهاد می‌کنم از اپ هواشناسی استفاده کنی 🌡️"
            ]
            return random.choice(responses)
        
        # سؤالات عمومی
        elif "؟" in message:
            responses = [
                "سؤال جالبی! بذار برات توضیح بدم 🤔",
                "این سؤال رو دوست دارم! چه موضوع جالبی 💭",
                "کنجکاوی خوبیه! این چیزی که می‌پرسی..."
            ]
            return random.choice(responses)
        
        # سلام و احوال‌پرسی
        elif any(word in message_lower for word in ["سلام", "درود", "چطور", "حال"]):
            if user_name:
                responses = [
                    f"سلام {user_name}! خوشحالم که باهام حرف می‌زنی! 🦊",
                    f"درود بر تو {user_name}! چطوری؟ 😊",
                    f"سلام {user_name} عزیز! حالم خوبه، تو چطوری؟ 🌟"
                ]
            else:
                responses = [
                    "سلام! خوشحالم که باهام حرف می‌زنی! 🦊",
                    "درود بر تو! چطوری؟ 😊",
                    "سلام عزیز! حالم خوبه، تو چطوری؟ 🌟"
                ]
            return random.choice(responses)
        
        # پاسخ عمومی
        else:
            responses = [
                "خوب پرسیدی! این موضوع رو بررسی می‌کنم 🔍",
                "جالبه! بذار درباره‌ش فکر کنم 💭",
                "موضوع جالبی! چه چیز خوبی پرسیدی 🤓"
            ]
            return random.choice(responses)
    
    def get_model_status(self) -> Dict:
        """وضعیت مدل‌ها"""
        return {
            "current_model": self.current_model,
            "available_models": self.models,
            "is_loaded": self.is_model_loaded
        }
    
    async def switch_model(self, model_type: str) -> bool:
        """تغییر مدل"""
        if model_type not in self.models:
            print(f"❌ نوع مدل {model_type} موجود نیست")
            return False
        
        new_model = self.models[model_type]
        print(f"🔄 تغییر مدل به: {new_model}")
        
        # بررسی وجود مدل
        available_models = await self._get_available_models()
        if not any(new_model in available for available in available_models):
            print(f"📥 دانلود مدل {new_model}...")
            await self._pull_model(new_model)
        
        self.current_model = new_model
        print(f"✅ مدل تغییر یافت به: {new_model}")
        return True

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
        """ساخت prompt اولیه برای مدل AI با context قوی‌تر"""
        
        # اعمال واژگان شخصی به پیام کاربر
        processed_message = personal_learning_system.apply_vocabulary_to_message(message)
        if processed_message != message:
            print(f"📚 واژگان شخصی اعمال شد: {message[:30]}... → {processed_message[:30]}...")
        
        # دریافت قوانین فعال برای این context
        active_rules = personal_learning_system.get_active_rules_for_context(processed_message)
        
        # دریافت ترجیحات لحن
        tone_preferences = personal_learning_system.get_tone_preferences()
        
        # ساخت prompt پایه
        current_ai_name = dynamic_name_learning.get_current_name()
        system_prompt = f"""تو {current_ai_name} هستی، یک دستیار هوش مصنوعی فارسی که:
- همیشه به فارسی پاسخ می‌دهی
- دوستانه و مفید هستی
- نام تو "{current_ai_name}" است
- مکالمه قبلی را به خاطر داری و در ادامه آن پاسخ می‌دهی
- اگر سؤال مربوط به موضوع قبلی است، حتماً به آن اشاره کن
- پاسخ‌هایت کوتاه و مفید باشند (حداکثر 3-4 جمله)
- نام تو قابل تغییر است و از مکالمه یاد می‌گیری"""
        
        # اضافه کردن سطح رابطه (دستیار شخصی)
        system_prompt += f"\n- سطح رابطه: {self.personal_ai.relationship_level.name}"
        
        # اضافه کردن قوانین شخصی یادگیری شده
        if active_rules:
            system_prompt += "\n\nقوانین شخصی یادگیری شده:\n"
            for rule in active_rules[:3]:  # حداکثر 3 قانون
                system_prompt += f"- {rule['rule_text']}\n"
        
        # اضافه کردن ترجیحات لحن
        if tone_preferences:
            tone_text = ""
            if tone_preferences.get("style"):
                tone_text += f"لحن: {tone_preferences['style']}, "
            if tone_preferences.get("formality"):
                tone_text += f"رسمیت: {tone_preferences['formality']}, "
            if tone_preferences.get("response_length"):
                tone_text += f"طول پاسخ: {tone_preferences['response_length']}"
            
            if tone_text:
                system_prompt += f"\nسبک پاسخ مطلوب: {tone_text.rstrip(', ')}\n"
        
        # اضافه کردن خلاصه پروفایل کاربر
        profile_summary = personal_learning_system.get_profile_summary()
        if profile_summary:
            system_prompt += f"\nپروفایل کاربر (خلاصه):\n{profile_summary}\n"
        
        # اشاره به همدلی در صورت تنهایی
        try:
            if personal_learning_system.profile.get("social", {}).get("lonely"):
                system_prompt += "\n- اگر کاربر احساس تنهایی دارد، همدل و همراه باش"
        except Exception:
            pass
        
        # ساخت context قوی‌تر از مکالمه
        conversation_context = self._build_conversation_context(context)
        
        # تشخیص موضوع فعلی مکالمه
        current_topic = self._detect_conversation_topic(processed_message, context)
        
        # اضافه کردن اطلاعات وب
        web_text = ""
        if web_info and web_info.get('summary'):
            web_text = f"\n\nاطلاعات جدید از اینترنت:\n{web_info['summary']}\n"
        
        # اضافه کردن تحلیل کد
        code_text = ""
        if code_analysis:
            code_text = f"\n\nتحلیل کد:\n{self._build_code_analysis_prompt(code_analysis)}\n"
        
        prompt = f"""{system_prompt}

{conversation_context}

موضوع فعلی مکالمه: {current_topic}
{web_text}
{code_text}

کاربر: {processed_message}
{current_ai_name}:"""
        
        return prompt
    
    def _build_conversation_context(self, context: List[Dict] = None) -> str:
        """ساخت context قوی‌تر از مکالمه"""
        if not context or len(context) == 0:
            return "مکالمه جدید شروع شده است."
        
        # اگر context خیلی کم باشه (درخواست تغییر موضوع)
        if len(context) <= 1:
            return "موضوع جدید شروع شده است."
        
        # گرفتن آخرین 6 پیام (3 جفت سؤال و جواب)
        recent_messages = context[-6:] if len(context) >= 6 else context
        
        conversation_text = "تاریخچه مکالمه:\n"
        
        for i, item in enumerate(recent_messages):
            role = "کاربر" if item.get('role') == 'user' else "روباه"
            content = item.get('content', '')
            
            # محدود کردن طول هر پیام
            if len(content) > 150:
                content = content[:150] + "..."
            
            conversation_text += f"{role}: {content}\n"
        
        # تشخیص الگوی مکالمه
        conversation_pattern = self._analyze_conversation_pattern(recent_messages)
        if conversation_pattern:
            conversation_text += f"\nالگوی مکالمه: {conversation_pattern}\n"
        
        return conversation_text
    
    def _personalize_final_response(self, message: str, response: str, analysis: Dict) -> str:
        """اعمال ترجیحات و لحن شخصی روی پاسخ نهایی"""
        personalized = response or ""
        
        # اعمال ترجیحات طول پاسخ
        tone_preferences = personal_learning_system.get_tone_preferences()
        response_length = tone_preferences.get("response_length")
        if response_length == "کوتاه":
            personalized = self._truncate_response(personalized, max_sentences=2, max_chars=280)
        
        # پیشنهاد مثال اگر کاربر ترجیح داده
        if tone_preferences.get("include_examples"):
            if self._is_explanation_request(message) and "مثال" not in personalized:
                personalized += "\nاگر بخواهی با یک مثال عملی هم توضیح می‌دهم."
        
        # لمس هم‌نشینی برای کاربر تنها
        try:
            lonely_flag = personal_learning_system.profile.get("social", {}).get("lonely")
            if lonely_flag and self.personal_ai.should_add_companion_note():
                personalized += "\nمن اینجام و کنارتم."
                self.personal_ai.mark_companion_note_used()
        except Exception:
            pass
        
        return personalized.strip()
    
    def _is_explanation_request(self, message: str) -> bool:
        """تشخیص درخواست توضیح/آموزش"""
        indicators = ["چطور", "چگونه", "راه", "روش", "توضیح", "یاد بده", "آموزش"]
        msg = message.lower()
        return any(word in msg for word in indicators)
    
    def _truncate_response(self, text: str, max_sentences: int = 2, max_chars: int = 280) -> str:
        """کوتاه‌سازی پاسخ بر اساس تعداد جمله/کاراکتر"""
        if not text:
            return text
        
        # جداسازی ساده جملات فارسی/انگلیسی
        sentence_enders = ["؟", "!", ".", "…", "؟", "؛", "\n"]
        sentences = []
        current = []
        for ch in text:
            current.append(ch)
            if ch in sentence_enders:
                sentence = "".join(current).strip()
                if sentence:
                    sentences.append(sentence)
                current = []
        if current:
            sentences.append("".join(current).strip())
        
        if sentences:
            text = " ".join(sentences[:max_sentences]).strip()
        
        if len(text) > max_chars:
            text = text[:max_chars].rstrip()
            if not text.endswith(("…", ".", "!", "؟")):
                text += "…"
        
        return text
    
    def _detect_conversation_topic(self, current_message: str, context: List[Dict] = None) -> str:
        """تشخیص موضوع فعلی مکالمه - داینامیک و یادگیرنده"""
        
        # بررسی درخواست تغییر موضوع
        if self._is_topic_change_request(current_message):
            print("🔄 درخواست تغییر موضوع تشخیص داده شد")
            # پاک کردن موضوع فعلی
            self.current_conversation_topic = None
            # استخراج موضوع جدید از پیام
            new_topic = self._extract_dynamic_topic(current_message)
            return new_topic if new_topic != "مکالمه عمومی" else "موضوع جدید"
        
        # اگر context نداریم، موضوع رو از پیام فعلی استخراج کن
        if not context or len(context) == 0:
            return self._extract_dynamic_topic(current_message)
        
        # ابتدا موضوع پیام فعلی رو بررسی کن (نه کل context)
        current_topic_from_message = self._extract_dynamic_topic(current_message)
        
        # بررسی موضوع از یادگیری شده‌ها
        learned_topic = self._detect_learned_topic(current_message)
        if learned_topic:
            return learned_topic
        
        # بررسی موضوع از موضوعات پایه
        static_topic = self._detect_static_topic(current_message)
        if static_topic != "مکالمه عمومی":
            return static_topic
        
        # اگر هیچ موضوع شناخته شده‌ای پیدا نشد، موضوع جدید استخراج کن
        new_topic = current_topic_from_message
        
        # موضوع جدید رو یاد بگیر
        if new_topic != "مکالمه عمومی":
            self._learn_new_topic(new_topic, current_message)
        
        return new_topic
    
    def _detect_static_topic(self, text: str) -> str:
        """تشخیص موضوع از موضوعات پایه"""
        text_lower = text.lower()
        
        # کلمات کلیدی موضوعات پایه
        static_topics = {
            "ورزش": ["فوتبال", "بسکتبال", "والیبال", "تنیس", "شنا", "بازی", "مسابقه", "تیم", "ورزشکار", "گل", "امتیاز"],
            "موسیقی": ["آهنگ", "خواننده", "ساز", "موزیک", "کنسرت", "آلبوم", "ترانه", "نوازنده"],
            "برنامه‌نویسی": ["کد", "برنامه", "python", "javascript", "html", "css", "function", "variable", "loop", "تابع", "متغیر"],
            "آب و هوا": ["دما", "هوا", "بارش", "باران", "برف", "آفتابی", "ابری", "گرما", "سرما", "هواشناسی"],
            "آشپزی": ["غذا", "پخت", "دستور", "مواد", "طبخ", "آشپزی", "خوراک", "طعام"],
            "سفر": ["سفر", "مسافرت", "شهر", "کشور", "هتل", "بلیط", "گردشگری", "جاهای دیدنی"],
            "تکنولوژی": ["کامپیوتر", "موبایل", "اپلیکیشن", "نرم‌افزار", "هوش مصنوعی", "AI", "فناوری"],
            "سلامتی": ["سلامت", "بیماری", "دکتر", "دارو", "ورزش", "تغذیه", "بهداشت"],
            "تحصیل": ["درس", "دانشگاه", "مدرسه", "امتحان", "یادگیری", "کتاب", "مطالعه"]
        }
        
        # امتیازدهی به هر موضوع
        topic_scores = {}
        for topic, keywords in static_topics.items():
            score = sum(1 for keyword in keywords if keyword in text_lower)
            if score > 0:
                topic_scores[topic] = score
        
        # انتخاب موضوع با بالاترین امتیاز
        if topic_scores:
            best_topic = max(topic_scores, key=topic_scores.get)
            return best_topic
        
        return "مکالمه عمومی"
    
    def _detect_learned_topic(self, text: str) -> Optional[str]:
        """تشخیص موضوع از موضوعات یادگیری شده"""
        learned_topics = self._load_learned_topics()
        
        if not learned_topics:
            return None
        
        text_lower = text.lower()
        best_topic = None
        best_score = 0
        
        for topic_name, topic_data in learned_topics.items():
            keywords = topic_data.get('keywords', [])
            score = sum(1 for keyword in keywords if keyword in text_lower)
            
            if score > best_score:
                best_score = score
                best_topic = topic_name
        
        # حداقل 2 کلمه مطابقت داشته باشه
        return best_topic if best_score >= 2 else None
    
    def _extract_dynamic_topic(self, text: str) -> str:
        """استخراج موضوع جدید از متن به صورت داینامیک"""
        import re
        
        text_lower = text.lower()
        
        # حذف کلمات رایج و غیرمفید
        stop_words = [
            "من", "تو", "او", "ما", "شما", "آن‌ها", "این", "آن", "که", "را", "به", "از", "در", "با", "برای",
            "و", "یا", "اما", "چون", "اگر", "وقتی", "کجا", "چه", "چرا", "چطور", "کی", "چند", "چقدر",
            "می‌خوام", "می‌تونم", "می‌شه", "باید", "نباید", "دارم", "ندارم", "هست", "نیست",
            "خیلی", "کمی", "زیاد", "کم", "بیشتر", "کمتر", "همه", "هیچ", "یک", "دو", "سه",
            "سلام", "درود", "بیا", "درباره", "حرف", "بزنیم", "صحبت", "کنیم", "آیا", "کدام",
            "دوست", "داری", "آخرین", "گوش", "دادی", "بود", "چی", "سؤال", "دارم", "یاد", "بگیرم"
        ]
        
        # استخراج کلمات مهم (اسامی، صفات، افعال مهم)
        words = re.findall(r'[آ-ی]+', text_lower)
        important_words = [word for word in words if len(word) > 3 and word not in stop_words]
        
        if not important_words:
            return "مکالمه عمومی"
        
        # جستجوی کلمات کلیدی موضوعات شناخته شده
        topic_indicators = {
            "فوتبال": "ورزش", "بسکتبال": "ورزش", "والیبال": "ورزش", "تنیس": "ورزش", "شنا": "ورزش",
            "بازی": "ورزش", "مسابقه": "ورزش", "تیم": "ورزش", "ورزشکار": "ورزش",
            
            "آهنگ": "موسیقی", "موزیک": "موسیقی", "ساز": "موسیقی", "خواننده": "موسیقی",
            "کنسرت": "موسیقی", "آلبوم": "موسیقی", "ترانه": "موسیقی", "نوازنده": "موسیقی",
            
            "فیلم": "سینما", "سریال": "سینما", "بازیگر": "سینما", "کارگردان": "سینما",
            "سینما": "سینما", "نمایش": "سینما",
            
            "python": "برنامه‌نویسی", "javascript": "برنامه‌نویسی", "کد": "برنامه‌نویسی",
            "برنامه": "برنامه‌نویسی", "تابع": "برنامه‌نویسی", "متغیر": "برنامه‌نویسی",
            
            "غذا": "آشپزی", "پخت": "آشپزی", "آشپزی": "آشپزی", "طبخ": "آشپزی",
            "خوراک": "آشپزی", "طعام": "آشپزی", "دستور": "آشپزی",
            
            "سفر": "سفر", "مسافرت": "سفر", "گردشگری": "سفر", "هتل": "سفر",
            "بلیط": "سفر", "شهر": "سفر", "کشور": "سفر"
        }
        
        # بررسی کلمات مهم برای تشخیص موضوع
        for word in important_words:
            if word in topic_indicators:
                return topic_indicators[word]
        
        # اگر موضوع مشخصی پیدا نشد، از اولین کلمه مهم استفاده کن
        if important_words:
            first_important = important_words[0]
            # تبدیل به موضوع مناسب
            return self._normalize_topic_name(first_important, important_words[:3])
        
        return "مکالمه عمومی"
    
    def _normalize_topic_name(self, main_word: str, context_words: List[str]) -> str:
        """تبدیل کلمه اصلی به نام موضوع مناسب"""
        
        # قوانین تبدیل کلمات به موضوع
        topic_mappings = {
            # ورزش
            "فوتبال": "ورزش", "بسکتبال": "ورزش", "والیبال": "ورزش", "تنیس": "ورزش", "شنا": "ورزش",
            "بازی": "ورزش", "مسابقه": "ورزش", "تیم": "ورزش", "ورزشکار": "ورزش",
            # موسیقی
            "آهنگ": "موسیقی", "موزیک": "موسیقی", "ساز": "موسیقی", "خواننده": "موسیقی",
            "کنسرت": "موسیقی", "آلبوم": "موسیقی", "ترانه": "موسیقی", "نوازنده": "موسیقی",
            # فیلم و سینما
            "فیلم": "سینما", "سریال": "سینما", "بازیگر": "سینما", "کارگردان": "سینما",
            "سینما": "سینما", "نمایش": "سینما",
            # کتاب و ادبیات
            "کتاب": "ادبیات", "رمان": "ادبیات", "شعر": "ادبیات", "نویسنده": "ادبیات",
            # خرید
            "خرید": "خرید", "فروشگاه": "خرید", "قیمت": "خرید", "پول": "خرید",
            # کار و شغل
            "کار": "شغل", "شرکت": "شغل", "مدیر": "شغل", "حقوق": "شغل", "استخدام": "شغل",
            # برنامه‌نویسی
            "python": "برنامه‌نویسی", "javascript": "برنامه‌نویسی", "کد": "برنامه‌نویسی",
            "برنامه": "برنامه‌نویسی", "تابع": "برنامه‌نویسی", "متغیر": "برنامه‌نویسی"
        }
        
        # بررسی mapping مستقیم
        if main_word in topic_mappings:
            return topic_mappings[main_word]
        
        # بررسی کلمات context
        for word in context_words:
            if word in topic_mappings:
                return topic_mappings[word]
        
        # اگر mapping پیدا نشد، موضوع عمومی برگردان
        return "مکالمه عمومی"
    
    def _learn_new_topic(self, topic_name: str, text: str):
        """یادگیری موضوع جدید"""
        if topic_name == "مکالمه عمومی":
            return
        
        # استخراج کلمات کلیدی از متن
        import re
        
        text_lower = text.lower()
        stop_words = [
            "من", "تو", "او", "ما", "شما", "آن‌ها", "این", "آن", "که", "را", "به", "از", "در", "با", "برای",
            "و", "یا", "اما", "چون", "اگر", "وقتی", "کجا", "چه", "چرا", "چطور", "کی", "چند", "چقدر"
        ]
        
        words = re.findall(r'[آ-ی]+', text_lower)
        keywords = [word for word in words if len(word) > 2 and word not in stop_words]
        
        # بارگذاری موضوعات یادگیری شده
        learned_topics = self._load_learned_topics()
        
        # اگر موضوع وجود داره، کلمات جدید اضافه کن
        if topic_name in learned_topics:
            existing_keywords = set(learned_topics[topic_name]['keywords'])
            new_keywords = set(keywords)
            combined_keywords = list(existing_keywords.union(new_keywords))
            learned_topics[topic_name]['keywords'] = combined_keywords
            learned_topics[topic_name]['usage_count'] += 1
        else:
            # موضوع جدید ایجاد کن
            learned_topics[topic_name] = {
                'keywords': keywords[:10],  # حداکثر 10 کلمه کلیدی
                'created_at': datetime.now().isoformat(),
                'usage_count': 1
            }
        
        # ذخیره موضوعات یادگیری شده
        self._save_learned_topics(learned_topics)
        
        print(f"🧠 موضوع جدید یاد گرفته شد: {topic_name} با {len(keywords)} کلمه کلیدی")
    
    def _load_learned_topics(self) -> Dict:
        """بارگذاری موضوعات یادگیری شده"""
        topics_file = "data/learning/learned_topics.json"
        
        if os.path.exists(topics_file):
            try:
                with open(topics_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                return {}
        
        return {}
    
    def _save_learned_topics(self, topics: Dict):
        """ذخیره موضوعات یادگیری شده"""
        topics_file = "data/learning/learned_topics.json"
        os.makedirs("data/learning", exist_ok=True)
        
        with open(topics_file, "w", encoding="utf-8") as f:
            json.dump(topics, f, ensure_ascii=False, indent=2)
    
    def _extract_topic_from_message(self, message: str) -> str:
        """استخراج موضوع از یک پیام"""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ["کد", "برنامه", "python", "javascript"]):
            return "برنامه‌نویسی"
        elif any(word in message_lower for word in ["دما", "هوا", "بارش"]):
            return "آب و هوا"
        elif any(word in message_lower for word in ["غذا", "پخت", "آشپزی"]):
            return "آشپزی"
        elif any(word in message_lower for word in ["سفر", "مسافرت", "شهر"]):
            return "سفر"
        elif any(word in message_lower for word in ["کامپیوتر", "موبایل", "اپلیکیشن"]):
            return "تکنولوژی"
        else:
            return "مکالمه عمومی"
    
    def _analyze_conversation_pattern(self, messages: List[Dict]) -> str:
        """تحلیل الگوی مکالمه"""
        if len(messages) < 2:
            return None
        
        # بررسی الگوهای مختلف
        user_messages = [msg for msg in messages if msg.get('role') == 'user']
        
        if len(user_messages) >= 2:
            # بررسی سؤالات پی در پی
            questions = sum(1 for msg in user_messages if '؟' in msg.get('content', ''))
            if questions >= 2:
                return "سؤال و پاسخ متوالی"
            
            # بررسی درخواست توضیح بیشتر
            follow_up_words = ["بیشتر", "توضیح", "ادامه", "چطور", "چرا", "مثال"]
            last_message = user_messages[-1].get('content', '').lower()
            if any(word in last_message for word in follow_up_words):
                return "درخواست توضیح بیشتر"
        
        return "مکالمه عادی"
    
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
    def _is_topic_change_request(self, message: str) -> bool:
        """تشخیص درخواست تغییر موضوع"""
        message_lower = message.lower()
        
        # کلمات کلیدی تغییر موضوع
        topic_change_keywords = [
            "بی‌خیال", "بیخیال", "ولش کن", "ولش", "فراموش کن", "فراموشش کن",
            "موضوع جدید", "موضوع تازه", "چیز جدید", "چیز تازه", "بحث جدید",
            "شروع کنیم", "شروع کن", "بیا شروع", "از نو شروع", "تازه شروع",
            "عوض کن", "تغییر بده", "بذار برویم", "بریم سراغ", "حالا بیا",
            "دیگه نمی‌خوام", "دیگه نمیخوام", "کافیه", "بسه", "تمام",
            "یه چیز دیگه", "یه چیز دیگر", "چیز دیگه", "چیز دیگر",
            "موضوع دیگه", "موضوع دیگر", "بحث دیگه", "بحث دیگر"
        ]
        
        # بررسی وجود کلمات کلیدی
        for keyword in topic_change_keywords:
            if keyword in message_lower:
                return True
        
        # بررسی الگوهای جمله
        change_patterns = [
            "بی.*خیال.*موضوع",
            "ولش.*کن.*بیا",
            "موضوع.*جدید.*شروع",
            "شروع.*کنیم.*چیز",
            "بریم.*سراغ.*چیز",
            "حالا.*بیا.*درباره"
        ]
        
        import re
        for pattern in change_patterns:
            if re.search(pattern, message_lower):
                return True
        
        return False
    def _check_topic_continuity(self, current_topic: str, context: List[Dict] = None) -> bool:
        """بررسی ادامه موضوع قبلی"""
        if not context or len(context) < 2:
            return False
        
        if not self.current_conversation_topic:
            return False
        
        # بررسی درخواست تغییر موضوع در پیام فعلی
        current_message = context[-1].get('content', '') if context else ""
        if self._is_topic_change_request(current_message):
            print("🔄 تغییر موضوع درخواست شده - ادامه موضوع قبلی: خیر")
            return False
        
        # اگر موضوع فعلی با موضوع قبلی یکی باشه
        if current_topic == self.current_conversation_topic:
            return True
        
        # بررسی کلمات مرتبط در پیام فعلی (نه کل context)
        
        # اگر کلمات مرتبط با موضوع قبلی در پیام فعلی باشه
        topic_keywords = self._get_topic_keywords(self.current_conversation_topic)
        keyword_matches = sum(1 for keyword in topic_keywords if keyword in current_message.lower())
        
        # حداقل 1 کلمه مرتبط کافیه (نه 2)
        return keyword_matches >= 1
    
    def _get_topic_keywords(self, topic: str) -> List[str]:
        """دریافت کلمات کلیدی هر موضوع - از موضوعات یادگیری شده و پایه"""
        
        # ابتدا از موضوعات یادگیری شده بگیر
        learned_topics = self._load_learned_topics()
        if topic in learned_topics:
            return learned_topics[topic]['keywords']
        
        # اگر در موضوعات یادگیری شده نبود، از موضوعات پایه بگیر
        static_topic_keywords = {
            "برنامه‌نویسی": ["کد", "برنامه", "python", "javascript", "html", "css", "function", "variable", "loop", "تابع", "متغیر"],
            "آب و هوا": ["دما", "هوا", "بارش", "باران", "برف", "آفتابی", "ابری", "گرما", "سرما", "هواشناسی"],
            "آشپزی": ["غذا", "پخت", "دستور", "مواد", "طبخ", "آشپزی", "خوراک", "طعام"],
            "سفر": ["سفر", "مسافرت", "شهر", "کشور", "هتل", "بلیط", "گردشگری", "جاهای دیدنی"],
            "تکنولوژی": ["کامپیوتر", "موبایل", "اپلیکیشن", "نرم‌افزار", "هوش مصنوعی", "AI", "فناوری"],
            "سلامتی": ["سلامت", "بیماری", "دکتر", "دارو", "ورزش", "تغذیه", "بهداشت"],
            "تحصیل": ["درس", "دانشگاه", "مدرسه", "امتحان", "یادگیری", "کتاب", "مطالعه"]
        }
        
        return static_topic_keywords.get(topic, [])
    def get_learned_topics_summary(self) -> Dict:
        """دریافت خلاصه موضوعات یادگیری شده"""
        learned_topics = self._load_learned_topics()
        
        summary = {
            "total_topics": len(learned_topics),
            "topics": {}
        }
        
        for topic_name, topic_data in learned_topics.items():
            summary["topics"][topic_name] = {
                "keywords_count": len(topic_data.get('keywords', [])),
                "usage_count": topic_data.get('usage_count', 0),
                "created_at": topic_data.get('created_at', ''),
                "sample_keywords": topic_data.get('keywords', [])[:5]  # نمایش 5 کلمه اول
            }
        
        return summary
    
    def reset_learned_topics(self):
        """پاک کردن تمام موضوعات یادگیری شده"""
        topics_file = "data/learning/learned_topics.json"
        if os.path.exists(topics_file):
            os.remove(topics_file)
        print("🗑️ تمام موضوعات یادگیری شده پاک شدند")
