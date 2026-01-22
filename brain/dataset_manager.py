"""
مدیر دیتاست و پرامپت روباه
مسئول جمع‌آوری، تحلیل و استفاده از داده‌های آموزشی
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional
import random

class DatasetManager:
    def __init__(self):
        self.datasets_dir = "data/datasets"
        self.prompts_dir = "data/prompts"
        
        # ایجاد دایرکتوری‌ها
        os.makedirs(self.datasets_dir, exist_ok=True)
        os.makedirs(self.prompts_dir, exist_ok=True)
        
        # بارگذاری دیتاست‌های موجود
        self.conversation_patterns = self._load_conversation_patterns()
        self.emotion_responses = self._load_emotion_responses()
        self.topic_knowledge = self._load_topic_knowledge()
        self.prompt_templates = self._load_prompt_templates()
        
        print("📊 مدیر دیتاست راه‌اندازی شد")
    
    def _load_conversation_patterns(self) -> List[Dict]:
        """بارگذاری الگوهای مکالمه"""
        patterns_file = f"{self.datasets_dir}/conversation_patterns.json"
        
        if os.path.exists(patterns_file):
            with open(patterns_file, "r", encoding="utf-8") as f:
                return json.load(f)
        
        # ایجاد الگوهای پایه
        default_patterns = [
            {
                "pattern": "greeting",
                "user_examples": ["سلام", "درود", "صبح بخیر", "سلام روباه"],
                "response_style": "دوستانه و گرم",
                "responses": [
                    "سلام! خوش آمدی! چطوری؟ 😊",
                    "درود بر تو! حالت چطوره؟",
                    "سلام عزیزم! چه خبر؟"
                ]
            }
        ]
        
        self._save_json(patterns_file, default_patterns)
        return default_patterns
    
    def _load_emotion_responses(self) -> Dict:
        """بارگذاری پاسخ‌های احساسی"""
        emotions_file = f"{self.datasets_dir}/emotion_responses.json"
        
        if os.path.exists(emotions_file):
            with open(emotions_file, "r", encoding="utf-8") as f:
                return json.load(f)
        
        # ایجاد پاسخ‌های احساسی پایه
        default_emotions = {
            "happy": {
                "indicators": ["خوشحالم", "عالیه", "فوق‌العاده", "😊", "😄", "🎉"],
                "responses": [
                    "چه خبر خوبی! منم خوشحالم 😊",
                    "عالیه! این انرژی مثبت رو دوست دارم!",
                    "واقعاً خوشحال‌کننده است! 🎉"
                ]
            },
            "sad": {
                "indicators": ["ناراحتم", "غمگینم", "بد", "😢", "😞"],
                "responses": [
                    "متوجه می‌شم که ناراحتی. می‌خوای درباره‌ش حرف بزنیم؟ 💙",
                    "گاهی همه ما روزهای سختی داریم. اینجام تا گوشت بدم",
                    "حس می‌کنم که چیزی آزارت می‌ده. می‌تونم کمک کنم؟"
                ]
            },
            "curious": {
                "indicators": ["چرا", "چطور", "چیست", "؟", "کنجکاوم"],
                "responses": [
                    "سؤال جالبی! بذار برات توضیح بدم 🤔",
                    "کنجکاوی خوبیه! این چیزی که می‌پرسی...",
                    "عالیه که می‌پرسی! اینطوری یاد می‌گیریم"
                ]
            }
        }
        
        self._save_json(emotions_file, default_emotions)
        return default_emotions
    
    def _load_topic_knowledge(self) -> Dict:
        """بارگذاری دانش موضوعی"""
        topics_file = f"{self.datasets_dir}/topic_knowledge.json"
        
        if os.path.exists(topics_file):
            with open(topics_file, "r", encoding="utf-8") as f:
                return json.load(f)
        
        # ایجاد دانش موضوعی پایه
        default_topics = {
            "programming": {
                "keywords": ["برنامه‌نویسی", "کد", "پایتون", "جاوا", "وب"],
                "intro_responses": [
                    "برنامه‌نویسی عاشقشم! 💻 چه زبانی می‌خوای یاد بگیری؟",
                    "کدنویسی دنیای جذابیه! از کجا شروع کنیم؟"
                ],
                "difficulty_levels": {
                    "beginner": "بیا با مفاهیم ساده شروع کنیم",
                    "intermediate": "حالا می‌تونیم وارد جزئیات بشیم",
                    "advanced": "بحث‌های پیشرفته‌تر رو بررسی کنیم"
                }
            }
        }
        
        self._save_json(topics_file, default_topics)
        return default_topics
    
    def _load_prompt_templates(self) -> Dict:
        """بارگذاری قالب‌های پرامپت"""
        prompts_file = f"{self.prompts_dir}/templates.json"
        
        if os.path.exists(prompts_file):
            with open(prompts_file, "r", encoding="utf-8") as f:
                return json.load(f)
        
        # ایجاد قالب‌های پرامپت پایه
        default_templates = {
            "base_personality": """تو روباه هستی، یک دستیار هوش مصنوعی شخصی که:
- شخصیت دوستانه و صمیمی داری
- از تجربیات قبلی یاد می‌گیری
- با احساسات کاربر همدلی می‌کنی
- پاسخ‌هایت خلاقانه و مفید هستند
- به فارسی و با لحن گرم صحبت می‌کنی
- از ایموجی استفاده می‌کنی تا پیام‌هات جذاب‌تر باشند""",
            
            "emotional_context": """وضعیت احساسی کاربر: {emotion}
راهنمای پاسخ: {emotion_guide}
سبک مناسب: {response_style}""",
            
            "topic_context": """موضوع مکالمه: {topic}
سطح دانش کاربر: {user_level}
اطلاعات مرتبط: {topic_info}""",
            
            "memory_context": """تاریخچه مکالمات:
{conversation_history}

اطلاعات شخصی کاربر:
{user_preferences}"""
        }
        
        self._save_json(prompts_file, default_templates)
        return default_templates
    
    def analyze_user_message(self, message: str, context: List[Dict] = None) -> Dict:
        """تحلیل پیام کاربر و استخراج اطلاعات"""
        analysis = {
            "emotion": self._detect_emotion(message),
            "topic": self._detect_topic(message),
            "intent": self._detect_intent(message),
            "complexity": self._assess_complexity(message),
            "patterns": self._find_patterns(message, context)
        }
        
        return analysis
    
    def _detect_emotion(self, message: str) -> str:
        """تشخیص احساسات پیام"""
        message_lower = message.lower()
        
        for emotion, data in self.emotion_responses.items():
            for indicator in data["indicators"]:
                if indicator in message_lower:
                    return emotion
        
        return "neutral"
    
    def _detect_topic(self, message: str) -> Optional[str]:
        """تشخیص موضوع پیام"""
        message_lower = message.lower()
        
        for topic, data in self.topic_knowledge.items():
            for keyword in data["keywords"]:
                if keyword in message_lower:
                    return topic
        
        return None
    
    def _detect_intent(self, message: str) -> str:
        """تشخیص هدف پیام"""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ["چیست", "چیه", "تعریف", "یعنی چی"]):
            return "definition"
        elif any(word in message_lower for word in ["چطور", "چگونه", "راه"]):
            return "how_to"
        elif "؟" in message:
            return "question"
        elif any(word in message_lower for word in ["کمک", "راهنمایی", "یاد بده"]):
            return "help"
        else:
            return "conversation"
    
    def _assess_complexity(self, message: str) -> str:
        """ارزیابی پیچیدگی پیام"""
        word_count = len(message.split())
        
        if word_count <= 3:
            return "simple"
        elif word_count <= 10:
            return "medium"
        else:
            return "complex"
    
    def _find_patterns(self, message: str, context: List[Dict] = None) -> List[str]:
        """یافتن الگوهای مکالمه"""
        patterns = []
        
        for pattern in self.conversation_patterns:
            for example in pattern["user_examples"]:
                if example.lower() in message.lower():
                    patterns.append(pattern["pattern"])
                    break
        
        return patterns
    
    def generate_enhanced_prompt(self, message: str, analysis: Dict, context: List[Dict] = None, personality: Dict = None) -> str:
        """تولید پرامپت بهبود یافته"""
        
        # شروع با شخصیت پایه
        prompt = self.prompt_templates["base_personality"]
        
        # اضافه کردن context احساسی
        if analysis["emotion"] != "neutral":
            emotion_data = self.emotion_responses.get(analysis["emotion"], {})
            emotion_context = self.prompt_templates["emotional_context"].format(
                emotion=analysis["emotion"],
                emotion_guide=f"کاربر {analysis['emotion']} به نظر می‌رسد",
                response_style=emotion_data.get("responses", ["پاسخ مناسب بده"])[0]
            )
            prompt += f"\n\n{emotion_context}"
        
        # اضافه کردن context موضوعی
        if analysis["topic"]:
            topic_data = self.topic_knowledge.get(analysis["topic"], {})
            topic_context = self.prompt_templates["topic_context"].format(
                topic=analysis["topic"],
                user_level="متوسط",  # می‌تونیم بعداً پیشرفته‌تر کنیم
                topic_info=str(topic_data.get("keywords", []))
            )
            prompt += f"\n\n{topic_context}"
        
        # اضافه کردن تاریخچه
        if context:
            history = "\n".join([f"- {item.get('content', '')[:50]}..." for item in context[-3:]])
            memory_context = self.prompt_templates["memory_context"].format(
                conversation_history=history,
                user_preferences=str(personality.get("favorite_topics", [])) if personality else "نامشخص"
            )
            prompt += f"\n\n{memory_context}"
        
        # اضافه کردن راهنمای خاص
        intent_guides = {
            "definition": "توضیح ساده و کاربردی بده، با مثال",
            "how_to": "مراحل را گام به گام توضیح بده",
            "question": "پاسخ کامل و مفید بده",
            "help": "راهنمایی عملی و قابل اجرا ارائه بده"
        }
        
        if analysis["intent"] in intent_guides:
            prompt += f"\n\nراهنمای پاسخ: {intent_guides[analysis['intent']]}"
        
        # اضافه کردن پیام کاربر
        prompt += f"\n\nکاربر: {message}\nروباه:"
        
        return prompt
    
    def get_similar_responses(self, message: str, analysis: Dict) -> List[str]:
        """پیدا کردن پاسخ‌های مشابه از dataset"""
        similar_responses = []
        
        # جستجو در الگوهای مکالمه
        for pattern in self.conversation_patterns:
            if any(keyword in message.lower() for keyword in pattern.get("user_examples", [])):
                similar_responses.extend(pattern.get("responses", []))
        
        # جستجو بر اساس احساس
        if analysis["emotion"] != "neutral":
            emotion_data = self.emotion_responses.get(analysis["emotion"])
            if emotion_data:
                similar_responses.extend(emotion_data.get("responses", []))
        
        return similar_responses[:5]  # حداکثر 5 مورد
    
    def get_conversation_patterns(self, analysis: Dict) -> List[Dict]:
        """پیدا کردن الگوهای مکالمه مرتبط"""
        relevant_patterns = []
        
        for pattern in self.conversation_patterns:
            # بررسی تطبیق با الگوهای تشخیص داده شده
            if pattern["pattern"] in analysis.get("patterns", []):
                relevant_patterns.append(pattern)
        
        return relevant_patterns[:3]  # حداکثر 3 مورد
        """پیشنهاد پاسخ بر اساس الگوها"""
        
        # اگر سؤال پیچیده یا تخصصی باشه، از دیتاست استفاده نکن
        if analysis["complexity"] in ["complex", "technical"]:
            return None
        
        # اگر موضوع خاصی داره (مثل آب و هوا، اخبار، اطلاعات فنی)، از دیتاست استفاده نکن
        if analysis["topic"] and analysis["topic"] not in ["conversation", "general"]:
            return None
        
        # فقط برای مکالمات ساده و عمومی از دیتاست استفاده کن
        if analysis["intent"] != "conversation":
            return None
        
        # اگر الگوی مشخصی پیدا شد
        if analysis["patterns"]:
            pattern_name = analysis["patterns"][0]
            for pattern in self.conversation_patterns:
                if pattern["pattern"] == pattern_name:
                    return random.choice(pattern["responses"])
        
        # اگر احساس خاصی تشخیص داده شد
        if analysis["emotion"] != "neutral":
            emotion_data = self.emotion_responses.get(analysis["emotion"])
            if emotion_data:
                return random.choice(emotion_data["responses"])
        
        return None
    
    def learn_from_interaction(self, user_message: str, ai_response: str, feedback: Optional[int] = None):
        """یادگیری از تعامل"""
        
        # تحلیل کیفیت پاسخ
        quality_score = feedback if feedback else self._assess_response_quality(user_message, ai_response)
        
        # ذخیره در دیتاست یادگیری
        learning_entry = {
            "timestamp": datetime.now().isoformat(),
            "user_message": user_message,
            "ai_response": ai_response,
            "quality_score": quality_score,
            "analysis": self.analyze_user_message(user_message)
        }
        
        # ذخیره در فایل
        learning_file = f"{self.datasets_dir}/learning_data.jsonl"
        with open(learning_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(learning_entry, ensure_ascii=False) + "\n")
        
        # اگر پاسخ خوب بود، به الگوها اضافه کن
        if quality_score >= 4:
            self._add_to_patterns(user_message, ai_response, learning_entry["analysis"])
    
    def _assess_response_quality(self, user_message: str, ai_response: str) -> int:
        """ارزیابی خودکار کیفیت پاسخ"""
        score = 3  # پایه
        
        # بررسی طول مناسب
        if 10 <= len(ai_response) <= 500:
            score += 1
        
        # بررسی وجود ایموجی (نشان دوستانه بودن)
        if any(emoji in ai_response for emoji in ["😊", "😄", "🦊", "💙", "🎉", "🤔"]):
            score += 1
        
        # بررسی پاسخ به سؤال
        if "؟" in user_message and len(ai_response) > 20:
            score += 1
        
        return min(score, 5)
    
    def _add_to_patterns(self, user_message: str, ai_response: str, analysis: Dict):
        """اضافه کردن به الگوهای مکالمه"""
        
        # اگر الگوی جدیدی است
        if not analysis["patterns"]:
            new_pattern = {
                "pattern": f"custom_{len(self.conversation_patterns)}",
                "user_examples": [user_message],
                "response_style": "یادگیری شده از تعامل",
                "responses": [ai_response]
            }
            self.conversation_patterns.append(new_pattern)
            
            # ذخیره در فایل
            patterns_file = f"{self.datasets_dir}/conversation_patterns.json"
            self._save_json(patterns_file, self.conversation_patterns)
    
    def _save_json(self, filepath: str, data):
        """ذخیره داده در فایل JSON"""
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def get_stats(self) -> Dict:
        """آمار دیتاست"""
        return {
            "conversation_patterns": len(self.conversation_patterns),
            "emotion_types": len(self.emotion_responses),
            "topics": len(self.topic_knowledge),
            "prompt_templates": len(self.prompt_templates)
        }