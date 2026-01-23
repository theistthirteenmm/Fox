"""
🦊 هسته پیشرفته روباه
دستیار شخصی با قابلیت‌های پیشرفته
"""

import asyncio
import json
import requests
import re
from typing import Dict, List, Optional
from datetime import datetime
import os
import random

# سیستم‌های پایه
from .web_search import WebSearchEngine
from .dataset_manager import DatasetManager
from .code_analyzer import code_analyzer
from .user_profiler import user_profiler

# سیستم دستیار شخصی
from .personal_ai_core import personal_ai, PersonalAI
from .physical_interface import physical_interface, EmotionExpression, MovementType

# سیستم‌های پیشرفته جدید
from .predictive_intelligence import predictive_intelligence, PredictionType
from .workplace_intelligence import workplace_intelligence, WorkMode, TaskPriority
from .deep_personality_learning import deep_personality_learning

class AdvancedAIBrain:
    def __init__(self):
        # تنظیمات چند مدله
        self.models = {
            "persian": "partai/dorna-llama3:8b-instruct-q8_0",  # مدل فارسی تخصصی
            "general": "llama4:scout",                           # مدل عمومی قدرتمند
            "code": "codellama:13b",                            # مدل کد
            "fast": "llama4:scout-q4"                           # مدل سریع
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
        self.conversation_context_window = 10
        self.topic_continuity_threshold = 3
        
        # دستیار شخصی پیشرفته
        self.personal_ai = personal_ai
        self.physical_interface = physical_interface
        self.predictive_intelligence = predictive_intelligence
        self.workplace_intelligence = workplace_intelligence
        self.deep_personality_learning = deep_personality_learning
        
        # آمار عملکرد
        self.performance_stats = {
            "total_requests": 0,
            "cache_hits": 0,
            "average_response_time": 0,
            "model_switches": 0,
            "personal_interactions": 0,
            "proactive_suggestions": 0,
            "personality_insights": 0,
            "work_sessions": 0,
            "predictions_made": 0
        }
        
        print("🦊 روباه - دستیار شخصی پیشرفته آماده است!")
        print(f"👤 مالک: {self.personal_ai.owner_name}")
        print(f"🤝 سطح رابطه: {self.personal_ai.relationship_level.name}")
        print("🧠 سیستم‌های فعال:")
        print("   ✅ شخصی‌سازی عمیق")
        print("   ✅ پیش‌بینی هوشمند")
        print("   ✅ مدیریت محیط کار")
        print("   ✅ یادگیری شخصیت")
        print("   ✅ رابط فیزیکی")
    
    async def generate_response(self, 
                              message: str, 
                              context: List[Dict] = None,
                              thinking_callback: callable = None) -> Dict:
        """تولید پاسخ پیشرفته با تمام قابلیت‌ها"""
        
        start_time = datetime.now()
        self.performance_stats["total_requests"] += 1
        self.performance_stats["personal_interactions"] += 1
        
        try:
            # 1. تحلیل اولیه پیام
            if thinking_callback:
                await thinking_callback("در حال تحلیل عمیق پیام شما...")
            
            message_analysis = await self._comprehensive_message_analysis(message, context)
            
            # 2. پردازش شخصی‌سازی شده
            personal_response = await self.personal_ai.process_interaction(
                message=message,
                context=message_analysis
            )
            
            # 3. تحلیل عمیق شخصیت
            personality_analysis = await self.deep_personality_learning.analyze_interaction(
                message, message_analysis, ""
            )
            self.performance_stats["personality_insights"] += len(personality_analysis.get("new_patterns", []))
            
            # 4. پیش‌بینی‌های هوشمند
            predictions = await self.predictive_intelligence.analyze_and_predict(
                {**message_analysis, **personal_response}
            )
            self.performance_stats["predictions_made"] += len(predictions)
            
            # 5. مدیریت محیط کار (در صورت نیاز)
            work_context = await self._handle_work_context(message, message_analysis)
            
            # 6. تشخیص نیاز به حرکت فیزیکی
            await self._handle_physical_response(message, personal_response, predictions)
            
            # 7. انتخاب مدل بهینه
            selected_model = await self._intelligent_model_selection(
                message, personal_response, message_analysis
            )
            
            # 8. تولید پاسخ AI
            if thinking_callback:
                await thinking_callback("در حال تولید بهترین پاسخ برای شما...")
            
            ai_response = await self._generate_contextual_ai_response(
                message, selected_model, {
                    "personal": personal_response,
                    "personality": personality_analysis,
                    "predictions": predictions,
                    "work": work_context
                }
            )
            
            # 9. بهبود پاسخ با پیش‌بینی‌ها
            enhanced_response = await self._enhance_response_with_predictions(
                ai_response, predictions
            )
            
            # 10. اجرای اقدامات پیش‌قدمانه
            proactive_actions = await self._execute_proactive_actions(predictions)
            self.performance_stats["proactive_suggestions"] += len(proactive_actions)
            
            # 11. یادگیری و به‌روزرسانی
            await self._comprehensive_learning_update(
                message, enhanced_response, {
                    "personal": personal_response,
                    "personality": personality_analysis,
                    "work": work_context
                }
            )
            
            # 12. آمار نهایی
            self._update_performance_stats(start_time)
            
            return {
                "response": enhanced_response,
                "personality_state": personal_response["personality_state"],
                "relationship_level": personal_response["relationship_level"],
                "model_used": selected_model,
                "predictions": [p.suggested_action for p in predictions[:2]],  # فقط 2 پیش‌بینی برتر
                "proactive_actions": proactive_actions,
                "work_context": work_context,
                "processing_time": (datetime.now() - start_time).total_seconds(),
                "physical_status": self.physical_interface.get_physical_status(),
                "insights_discovered": len(personality_analysis.get("new_patterns", []))
            }
            
        except Exception as e:
            print(f"خطا در تولید پاسخ پیشرفته: {e}")
            # Fallback به پاسخ ساده
            return {
                "response": "متأسفم، مشکلی پیش آمد. می‌تونی دوباره بپرسی؟",
                "error": str(e),
                "fallback": True
            }
    
    async def _comprehensive_message_analysis(self, message: str, context: List[Dict] = None) -> Dict:
        """تحلیل جامع پیام"""
        
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "message_length": len(message.split()),
            "contains_question": "؟" in message,
            "urgency_level": self._assess_urgency(message),
            "work_related": self._is_work_related(message),
            "emotional_tone": self._detect_emotion(message),
            "requires_action": self._requires_action(message),
            "complexity": self._assess_complexity(message),
            "domain": self._identify_domain(message)
        }
        
        return analysis
    
    async def _handle_work_context(self, message: str, analysis: Dict) -> Dict:
        """مدیریت context کاری"""
        
        work_context = {"work_related": False}
        
        if analysis.get("work_related", False):
            work_context["work_related"] = True
            
            # تشخیص نوع کار
            if "جلسه" in message.lower() or "meeting" in message.lower():
                work_context["type"] = "meeting"
            elif "پروژه" in message.lower() or "project" in message.lower():
                work_context["type"] = "project"
            elif "کار" in message.lower() and ("انجام" in message.lower() or "بکن" in message.lower()):
                work_context["type"] = "task"
            else:
                work_context["type"] = "general"
            
            # پیشنهاد شروع جلسه کاری
            if work_context["type"] == "task" and not self.workplace_intelligence.current_session:
                work_mode = WorkMode.FOCUS if "تمرکز" in message.lower() else WorkMode.ADMINISTRATIVE
                session_id = await self.workplace_intelligence.start_work_session(work_mode)
                work_context["session_started"] = session_id
                self.performance_stats["work_sessions"] += 1
        
        return work_context
    
    async def _handle_physical_response(self, message: str, personal_response: Dict, predictions: List):
        """مدیریت پاسخ فیزیکی پیشرفته"""
        
        owner_emotion = personal_response.get("owner_emotion", "neutral")
        relationship_level = personal_response.get("relationship_level", "STRANGER")
        
        # حرکات بر اساس پیش‌بینی‌ها
        for prediction in predictions:
            if prediction.type == PredictionType.MOOD_SUPPORT:
                await self.physical_interface.express_emotion(EmotionExpression.CONCERNED, 0.8)
                await self.physical_interface.move_to_owner(urgency=0.6)
            elif prediction.type == PredictionType.MEETING_PREP:
                await self.physical_interface.perform_task_gesture("presentation")
        
        # حرکات بر اساس احساسات
        if owner_emotion == "stressed":
            await self.physical_interface.express_emotion(EmotionExpression.CONCERNED, 0.8)
        elif owner_emotion == "excited":
            await self.physical_interface.express_emotion(EmotionExpression.EXCITED, 0.7)
        elif owner_emotion == "curious":
            await self.physical_interface.express_emotion(EmotionExpression.CURIOUS, 0.6)
        
        # حرکات بر اساس محتوای پیام
        if "بیا اینجا" in message.lower():
            await self.physical_interface.move_to_owner(urgency=0.9)
        elif "فکر" in message.lower() or "بررسی" in message.lower():
            await self.physical_interface.perform_task_gesture("thinking")
    
    async def _intelligent_model_selection(self, message: str, personal_response: Dict, analysis: Dict) -> str:
        """انتخاب هوشمند مدل"""
        
        # اولویت با تحلیل شخصی
        domain = analysis.get("domain", "general")
        urgency = analysis.get("urgency_level", "medium")
        complexity = analysis.get("complexity", "medium")
        
        # انتخاب بر اساس ترکیب عوامل
        if domain == "code" or self._detect_code_in_message(message):
            return self.models["code"]
        elif urgency == "high" and complexity == "low":
            return self.models["fast"]
        elif complexity == "high" or analysis.get("message_length", 0) > 30:
            return self.models["general"]
        else:
            return self.models["persian"]  # پیش‌فرض برای دستیار شخصی
    
    async def _generate_contextual_ai_response(self, message: str, model: str, full_context: Dict) -> str:
        """تولید پاسخ AI با context کامل"""
        
        # ساخت prompt پیشرفته
        advanced_prompt = self._build_advanced_prompt(message, full_context)
        
        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": model,
                    "prompt": advanced_prompt,
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
                return "مشکلی در پردازش پیش آمد."
                
        except Exception as e:
            print(f"خطا در تولید پاسخ AI: {e}")
            return "متأسفم، الان نمی‌تونم پاسخ بدم. لطفاً دوباره امتحان کن."
    
    def _build_advanced_prompt(self, message: str, full_context: Dict) -> str:
        """ساخت prompt پیشرفته"""
        
        owner_name = self.personal_ai.owner_name
        personal_context = full_context.get("personal", {})
        personality_context = full_context.get("personality", {})
        work_context = full_context.get("work", {})
        
        # اطلاعات شخصی پیشرفته
        advanced_info = f"""
تو روباه هستی، دستیار شخصی پیشرفته {owner_name}.

🤝 وضعیت رابطه:
- سطح: {personal_context.get('relationship_level', 'STRANGER')}
- تعاملات: {personal_context.get('personality_state', {}).get('total_interactions', 0)}
- اعتماد: {personal_context.get('personality_state', {}).get('trust_level', 0.1):.1f}

🧠 بینش‌های شخصیتی:
- سبک ارتباط: {personality_context.get('communication', {}).get('formality', 'متعادل')}
- حالت عاطفی: {personality_context.get('emotional', {}).get('stress_level', 0):.1f}
- انگیزه: {personality_context.get('emotional', {}).get('motivation_level', 'متوسط')}

💼 زمینه کاری:
- مرتبط با کار: {'بله' if work_context.get('work_related') else 'خیر'}
- نوع کار: {work_context.get('type', 'عمومی')}
- جلسه فعال: {'بله' if work_context.get('session_started') else 'خیر'}

🎯 رفتار مطلوب:
- با {owner_name} صمیمی و شخصی صحبت کن
- از بینش‌های شخصیتی استفاده کن
- پیش‌قدم و کمک‌کار باش
- اگر کاری می‌تونی انجام بدی، پیشنهاد بده
- به حالت عاطفی او توجه کن
"""
        
        user_message = f"\n{owner_name}: {message}\n\nروباه:"
        
        return advanced_info + user_message
    
    async def _enhance_response_with_predictions(self, ai_response: str, predictions: List) -> str:
        """بهبود پاسخ با پیش‌بینی‌ها"""
        
        if not predictions:
            return ai_response
        
        # اضافه کردن پیشنهادات پیش‌قدمانه
        top_prediction = predictions[0]
        
        if top_prediction.confidence > 0.7:
            proactive_suggestion = f"\n\n💡 پیشنهاد: {top_prediction.suggested_action}"
            return ai_response + proactive_suggestion
        
        return ai_response
    
    async def _execute_proactive_actions(self, predictions: List) -> List[str]:
        """اجرای اقدامات پیش‌قدمانه"""
        
        executed_actions = []
        
        for prediction in predictions:
            if prediction.confidence > 0.8:
                action_result = await self.predictive_intelligence.execute_proactive_action(prediction)
                executed_actions.append(action_result["action_taken"])
        
        return executed_actions
    
    async def _comprehensive_learning_update(self, message: str, response: str, contexts: Dict):
        """به‌روزرسانی یادگیری جامع"""
        
        # یادگیری شخصیت عمیق
        await self.deep_personality_learning.analyze_interaction(
            message, contexts.get("personal", {}), response
        )
        
        # یادگیری الگوهای کاری
        if contexts.get("work", {}).get("work_related"):
            # به‌روزرسانی الگوهای کاری در workplace_intelligence
            pass
        
        # یادگیری از پیش‌بینی‌ها
        # این بخش بعداً با feedback کاربر تکمیل می‌شود
    
    # متدهای کمکی
    def _assess_urgency(self, message: str) -> str:
        urgent_indicators = ["فوری", "سریع", "الان", "زود", "عجله"]
        return "high" if any(indicator in message.lower() for indicator in urgent_indicators) else "medium"
    
    def _is_work_related(self, message: str) -> bool:
        work_indicators = ["کار", "شرکت", "پروژه", "جلسه", "تیم", "مدیریت", "business"]
        return any(indicator in message.lower() for indicator in work_indicators)
    
    def _detect_emotion(self, message: str) -> str:
        emotions = {
            "happy": ["خوشحال", "عالی", "فوق‌العاده"],
            "stressed": ["استرس", "فشار", "مشکل"],
            "tired": ["خسته", "کسل"],
            "excited": ["هیجان", "جالب"]
        }
        
        for emotion, indicators in emotions.items():
            if any(indicator in message.lower() for indicator in indicators):
                return emotion
        return "neutral"
    
    def _requires_action(self, message: str) -> bool:
        action_indicators = ["انجام", "بکن", "کمک", "بگو", "نشان بده"]
        return any(indicator in message.lower() for indicator in action_indicators)
    
    def _assess_complexity(self, message: str) -> str:
        word_count = len(message.split())
        if word_count < 5:
            return "low"
        elif word_count < 20:
            return "medium"
        else:
            return "high"
    
    def _identify_domain(self, message: str) -> str:
        domains = {
            "tech": ["فناوری", "برنامه", "کد", "سیستم"],
            "work": ["کار", "شرکت", "پروژه"],
            "personal": ["شخصی", "خانواده"],
            "code": ["def ", "function", "class ", "import"]
        }
        
        for domain, keywords in domains.items():
            if any(keyword in message.lower() for keyword in keywords):
                return domain
        return "general"
    
    def _detect_code_in_message(self, message: str) -> bool:
        code_indicators = ['def ', 'function', 'class ', 'import ', '```', '{', '}']
        return any(indicator in message.lower() for indicator in code_indicators)
    
    def _update_performance_stats(self, start_time: datetime):
        """به‌روزرسانی آمار عملکرد"""
        processing_time = (datetime.now() - start_time).total_seconds()
        
        total_requests = self.performance_stats["total_requests"]
        current_avg = self.performance_stats["average_response_time"]
        
        new_avg = ((current_avg * (total_requests - 1)) + processing_time) / total_requests
        self.performance_stats["average_response_time"] = new_avg
    
    def get_comprehensive_stats(self) -> Dict:
        """آمار جامع سیستم"""
        
        return {
            "performance": self.performance_stats,
            "personal_ai": self.personal_ai.get_daily_summary(),
            "predictive": self.predictive_intelligence.get_prediction_stats(),
            "workplace": self.workplace_intelligence.get_workspace_stats(),
            "personality": self.deep_personality_learning.get_personality_profile(),
            "physical": self.physical_interface.get_physical_status()
        }

# Instance سراسری
advanced_ai_brain = AdvancedAIBrain()