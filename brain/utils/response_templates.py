"""
🎨 سیستم Template های پاسخ هوشمند
تولید پاسخ‌های متنوع و طبیعی با استفاده از template ها
"""

import json
import random
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum
import re
from dataclasses import dataclass

class ResponseType(Enum):
    GREETING = "greeting"
    QUESTION_ANSWER = "question_answer"
    EXPLANATION = "explanation"
    HELP = "help"
    ERROR = "error"
    THINKING = "thinking"
    FAREWELL = "farewell"
    EMOTION = "emotion"
    CODE = "code"
    CREATIVE = "creative"

class ResponseTone(Enum):
    FORMAL = "formal"
    FRIENDLY = "friendly"
    CASUAL = "casual"
    PROFESSIONAL = "professional"
    HUMOROUS = "humorous"
    EMPATHETIC = "empathetic"

@dataclass
class ResponseTemplate:
    id: str
    type: ResponseType
    tone: ResponseTone
    template: str
    variables: List[str]
    conditions: Dict[str, Any]
    usage_count: int = 0
    success_rate: float = 1.0

class ResponseTemplateEngine:
    def __init__(self):
        self.templates = {}
        self.template_stats = {}
        self.user_preferences = {
            "preferred_tone": ResponseTone.FRIENDLY,
            "formality_level": 0.3,  # 0 = خیلی غیررسمی, 1 = خیلی رسمی
            "humor_level": 0.5,
            "detail_level": 0.7
        }
        
        # بارگذاری template های پیش‌فرض
        self._load_default_templates()
        
        print("🎨 Response Template Engine راه‌اندازی شد")
    
    def _load_default_templates(self):
        """بارگذاری template های پیش‌فرض"""
        
        default_templates = [
            # سلام و احوال‌پرسی
            {
                "id": "greeting_friendly_1",
                "type": ResponseType.GREETING,
                "tone": ResponseTone.FRIENDLY,
                "template": "سلام {name}! 😊 چطوری؟ چه کمکی می‌تونم برات بکنم؟",
                "variables": ["name"],
                "conditions": {"time_of_day": "any"}
            },
            {
                "id": "greeting_morning",
                "type": ResponseType.GREETING,
                "tone": ResponseTone.FRIENDLY,
                "template": "صبح بخیر {name}! ☀️ امیدوارم روز خوبی داشته باشی. چه برنامه‌ای داری؟",
                "variables": ["name"],
                "conditions": {"time_of_day": "morning"}
            },
            
            # پاسخ به سؤالات
            {
                "id": "answer_confident",
                "type": ResponseType.QUESTION_ANSWER,
                "tone": ResponseTone.PROFESSIONAL,
                "template": "بر اساس اطلاعاتی که دارم، {answer}. {additional_info}",
                "variables": ["answer", "additional_info"],
                "conditions": {"confidence": "high"}
            },
            {
                "id": "answer_uncertain",
                "type": ResponseType.QUESTION_ANSWER,
                "tone": ResponseTone.EMPATHETIC,
                "template": "متأسفانه اطلاعات دقیقی در این مورد ندارم، ولی {partial_answer}. بهتره از منابع معتبر هم بررسی کنی.",
                "variables": ["partial_answer"],
                "conditions": {"confidence": "low"}
            },
            
            # توضیحات
            {
                "id": "explanation_simple",
                "type": ResponseType.EXPLANATION,
                "tone": ResponseTone.FRIENDLY,
                "template": "بذار ساده توضیح بدم: {main_concept}. {example} مثلاً {concrete_example}.",
                "variables": ["main_concept", "example", "concrete_example"],
                "conditions": {"complexity": "simple"}
            },
            {
                "id": "explanation_detailed",
                "type": ResponseType.EXPLANATION,
                "tone": ResponseTone.PROFESSIONAL,
                "template": "{topic} یک مفهوم پیچیده است که شامل {components} می‌شود. {detailed_explanation} {conclusion}",
                "variables": ["topic", "components", "detailed_explanation", "conclusion"],
                "conditions": {"complexity": "detailed"}
            },
            
            # کمک
            {
                "id": "help_enthusiastic",
                "type": ResponseType.HELP,
                "tone": ResponseTone.FRIENDLY,
                "template": "البته که می‌تونم کمکت کنم! 🚀 {help_content} اگه سؤال دیگه‌ای داشتی، بپرس!",
                "variables": ["help_content"],
                "conditions": {"user_mood": "positive"}
            },
            
            # خطاها
            {
                "id": "error_apologetic",
                "type": ResponseType.ERROR,
                "tone": ResponseTone.EMPATHETIC,
                "template": "متأسفم، {error_description}. بذار دوباره امتحان کنم. {retry_suggestion}",
                "variables": ["error_description", "retry_suggestion"],
                "conditions": {"error_severity": "medium"}
            },
            
            # در حال فکر کردن
            {
                "id": "thinking_patient",
                "type": ResponseType.THINKING,
                "tone": ResponseTone.FRIENDLY,
                "template": "صبور باشید، در حال {thinking_process}... 🤔",
                "variables": ["thinking_process"],
                "conditions": {"processing_time": "long"}
            },
            
            # احساسات
            {
                "id": "emotion_happy",
                "type": ResponseType.EMOTION,
                "tone": ResponseTone.FRIENDLY,
                "template": "خوشحالم که {reason}! 😊 {positive_response}",
                "variables": ["reason", "positive_response"],
                "conditions": {"emotion": "happy"}
            },
            {
                "id": "emotion_sad",
                "type": ResponseType.EMOTION,
                "tone": ResponseTone.EMPATHETIC,
                "template": "متوجه می‌شم که {situation}. {empathetic_response} 💙",
                "variables": ["situation", "empathetic_response"],
                "conditions": {"emotion": "sad"}
            },
            
            # کد و برنامه‌نویسی
            {
                "id": "code_explanation",
                "type": ResponseType.CODE,
                "tone": ResponseTone.PROFESSIONAL,
                "template": "این کد {code_purpose} انجام می‌ده:\n\n```{language}\n{code}\n```\n\n{explanation}",
                "variables": ["code_purpose", "language", "code", "explanation"],
                "conditions": {"content_type": "code"}
            },
            
            # خلاقانه
            {
                "id": "creative_story",
                "type": ResponseType.CREATIVE,
                "tone": ResponseTone.HUMOROUS,
                "template": "بذار یه داستان جالب برات تعریف کنم: {story_beginning} {plot_twist} {conclusion} 📚",
                "variables": ["story_beginning", "plot_twist", "conclusion"],
                "conditions": {"request_type": "story"}
            }
        ]
        
        # تبدیل به ResponseTemplate objects
        for template_data in default_templates:
            template = ResponseTemplate(
                id=template_data["id"],
                type=ResponseType(template_data["type"]),
                tone=ResponseTone(template_data["tone"]),
                template=template_data["template"],
                variables=template_data["variables"],
                conditions=template_data["conditions"]
            )
            self.templates[template.id] = template
    
    def select_template(self, 
                       response_type: ResponseType,
                       context: Dict[str, Any] = None,
                       user_preferences: Dict[str, Any] = None) -> Optional[ResponseTemplate]:
        """انتخاب بهترین template بر اساس context"""
        
        context = context or {}
        user_prefs = user_preferences or self.user_preferences
        
        # فیلتر template ها بر اساس نوع
        candidate_templates = [
            template for template in self.templates.values()
            if template.type == response_type
        ]
        
        if not candidate_templates:
            return None
        
        # امتیازدهی template ها
        scored_templates = []
        
        for template in candidate_templates:
            score = self._calculate_template_score(template, context, user_prefs)
            scored_templates.append((template, score))
        
        # مرتب‌سازی بر اساس امتیاز
        scored_templates.sort(key=lambda x: x[1], reverse=True)
        
        # انتخاب تصادفی از 3 template برتر (برای تنوع)
        top_templates = scored_templates[:3]
        if top_templates:
            weights = [score for _, score in top_templates]
            selected_template = random.choices(
                [template for template, _ in top_templates],
                weights=weights,
                k=1
            )[0]
            
            return selected_template
        
        return None
    
    def _calculate_template_score(self, 
                                template: ResponseTemplate,
                                context: Dict[str, Any],
                                user_prefs: Dict[str, Any]) -> float:
        """محاسبه امتیاز template"""
        score = 0.0
        
        # امتیاز tone matching
        preferred_tone = user_prefs.get("preferred_tone", ResponseTone.FRIENDLY)
        if template.tone == preferred_tone:
            score += 0.3
        elif self._are_tones_compatible(template.tone, preferred_tone):
            score += 0.15
        
        # امتیاز condition matching
        condition_matches = 0
        total_conditions = len(template.conditions)
        
        for condition_key, condition_value in template.conditions.items():
            context_value = context.get(condition_key)
            
            if context_value == condition_value or condition_value == "any":
                condition_matches += 1
            elif self._is_condition_compatible(condition_key, condition_value, context_value):
                condition_matches += 0.5
        
        if total_conditions > 0:
            condition_score = condition_matches / total_conditions
            score += condition_score * 0.4
        
        # امتیاز success rate
        score += template.success_rate * 0.2
        
        # کاهش امتیاز برای template های پراستفاده (برای تنوع)
        usage_penalty = min(0.1, template.usage_count / 100)
        score -= usage_penalty
        
        # امتیاز تصادفی کم برای تنوع
        score += random.uniform(0, 0.1)
        
        return max(0, score)
    
    def _are_tones_compatible(self, tone1: ResponseTone, tone2: ResponseTone) -> bool:
        """بررسی سازگاری tone ها"""
        compatible_pairs = {
            (ResponseTone.FRIENDLY, ResponseTone.CASUAL),
            (ResponseTone.PROFESSIONAL, ResponseTone.FORMAL),
            (ResponseTone.EMPATHETIC, ResponseTone.FRIENDLY),
            (ResponseTone.HUMOROUS, ResponseTone.CASUAL)
        }
        
        return (tone1, tone2) in compatible_pairs or (tone2, tone1) in compatible_pairs
    
    def _is_condition_compatible(self, key: str, expected: Any, actual: Any) -> bool:
        """بررسی سازگاری شرایط"""
        if key == "time_of_day":
            time_compatibility = {
                "morning": ["early_morning", "late_morning"],
                "afternoon": ["early_afternoon", "late_afternoon"],
                "evening": ["early_evening", "late_evening"]
            }
            return actual in time_compatibility.get(expected, [])
        
        elif key == "confidence":
            confidence_levels = ["low", "medium", "high"]
            if expected in confidence_levels and actual in confidence_levels:
                expected_idx = confidence_levels.index(expected)
                actual_idx = confidence_levels.index(actual)
                return abs(expected_idx - actual_idx) <= 1
        
        return False
    
    def generate_response(self, 
                         response_type: ResponseType,
                         variables: Dict[str, str],
                         context: Dict[str, Any] = None) -> Optional[str]:
        """تولید پاسخ با استفاده از template"""
        
        template = self.select_template(response_type, context)
        if not template:
            return None
        
        try:
            # جایگزینی متغیرها
            response = template.template
            
            for var_name, var_value in variables.items():
                placeholder = f"{{{var_name}}}"
                response = response.replace(placeholder, str(var_value))
            
            # به‌روزرسانی آمار
            template.usage_count += 1
            
            # اضافه کردن تنوع با emoji ها و عبارات اضافی
            response = self._add_variety(response, template.tone)
            
            return response
            
        except Exception as e:
            print(f"خطا در تولید پاسخ: {e}")
            return None
    
    def _add_variety(self, response: str, tone: ResponseTone) -> str:
        """اضافه کردن تنوع به پاسخ"""
        
        # emoji های مناسب برای هر tone
        tone_emojis = {
            ResponseTone.FRIENDLY: ["😊", "😄", "🙂", "😉"],
            ResponseTone.PROFESSIONAL: ["👍", "✅", "📊", "💼"],
            ResponseTone.HUMOROUS: ["😂", "🤣", "😆", "🎭"],
            ResponseTone.EMPATHETIC: ["💙", "🤗", "😌", "🌟"],
            ResponseTone.CASUAL: ["👌", "🔥", "💯", "✨"]
        }
        
        # اضافه کردن emoji تصادفی (گاهی اوقات)
        if random.random() < 0.3 and tone in tone_emojis:
            emoji = random.choice(tone_emojis[tone])
            if emoji not in response:
                response += f" {emoji}"
        
        # عبارات تکمیلی
        completion_phrases = {
            ResponseTone.FRIENDLY: [
                "امیدوارم مفید باشه!",
                "خوشحال می‌شم کمکت کرده باشم!",
                "اگه سؤال دیگه‌ای داشتی، بپرس!"
            ],
            ResponseTone.PROFESSIONAL: [
                "در خدمت شما هستم.",
                "موفق باشید.",
                "امیدوارم راه‌گشا باشد."
            ]
        }
        
        # اضافه کردن عبارت تکمیلی (گاهی اوقات)
        if random.random() < 0.2 and tone in completion_phrases:
            phrase = random.choice(completion_phrases[tone])
            if not response.endswith(phrase):
                response += f" {phrase}"
        
        return response
    
    def update_template_success(self, template_id: str, success: bool):
        """به‌روزرسانی نرخ موفقیت template"""
        if template_id in self.templates:
            template = self.templates[template_id]
            
            # محاسبه نرخ موفقیت جدید با میانگین متحرک
            alpha = 0.1  # ضریب یادگیری
            if success:
                template.success_rate = template.success_rate * (1 - alpha) + alpha
            else:
                template.success_rate = template.success_rate * (1 - alpha)
    
    def get_template_stats(self) -> Dict:
        """آمار template ها"""
        stats = {
            "total_templates": len(self.templates),
            "templates_by_type": {},
            "templates_by_tone": {},
            "most_used": [],
            "highest_success_rate": []
        }
        
        # آمار بر اساس نوع
        for template in self.templates.values():
            type_name = template.type.value
            tone_name = template.tone.value
            
            stats["templates_by_type"][type_name] = stats["templates_by_type"].get(type_name, 0) + 1
            stats["templates_by_tone"][tone_name] = stats["templates_by_tone"].get(tone_name, 0) + 1
        
        # پراستفاده‌ترین template ها
        sorted_by_usage = sorted(
            self.templates.values(),
            key=lambda x: x.usage_count,
            reverse=True
        )
        stats["most_used"] = [
            {"id": t.id, "usage_count": t.usage_count}
            for t in sorted_by_usage[:5]
        ]
        
        # بالاترین نرخ موفقیت
        sorted_by_success = sorted(
            self.templates.values(),
            key=lambda x: x.success_rate,
            reverse=True
        )
        stats["highest_success_rate"] = [
            {"id": t.id, "success_rate": t.success_rate}
            for t in sorted_by_success[:5]
        ]
        
        return stats

# Instance سراسری
response_template_engine = ResponseTemplateEngine()