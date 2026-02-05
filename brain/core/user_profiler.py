"""
🧑 پروفایل‌ساز کاربر
ایجاد و مدیریت پروفایل شخصی کاربر
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import re
from collections import defaultdict, Counter

class UserProfiler:
    def __init__(self):
        self.profile_file = "data/personality/user_profile.json"
        self.interactions_file = "data/personality/user_interactions.jsonl"
        
        # پروفایل کاربر
        self.user_profile = self._load_or_create_profile()
        
        # آمار تعاملات
        self.interaction_stats = {
            "total_messages": 0,
            "favorite_topics": [],
            "communication_style": "friendly",
            "activity_patterns": {},
            "interests": [],
            "skills": [],
            "goals": []
        }
        
        # بارگذاری آمار تعاملات از فایل
        self._load_interaction_stats()
        
        print("👤 سیستم پروفایل کاربر راه‌اندازی شد")
    
    def _load_interaction_stats(self):
        """بارگذاری آمار تعاملات از فایل"""
        if os.path.exists(self.interactions_file):
            try:
                with open(self.interactions_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    self.interaction_stats["total_messages"] = len(lines)
                    print(f"📊 بارگذاری آمار: {len(lines)} تعامل")
            except Exception as e:
                print(f"⚠️ خطا در بارگذاری آمار تعاملات: {e}")
                self.interaction_stats["total_messages"] = 0
    
    def _load_or_create_profile(self) -> Dict:
        """بارگذاری یا ایجاد پروفایل کاربر"""
        os.makedirs("data/personality", exist_ok=True)
        
        if os.path.exists(self.profile_file):
            try:
                with open(self.profile_file, 'r', encoding='utf-8') as f:
                    profile = json.load(f)
                print("📂 پروفایل کاربر موجود بارگذاری شد")
                return profile
            except:
                pass
        
        # ایجاد پروفایل جدید
        new_profile = {
            "created_at": datetime.now().isoformat(),
            "name": None,
            "preferences": {
                "communication_style": "friendly",
                "response_length": "medium",
                "topics_of_interest": [],
                "learning_goals": []
            },
            "personality_insights": {
                "communication_patterns": [],
                "emotional_tendencies": [],
                "interaction_frequency": {}
            },
            "relationship_level": 1,  # 1-10
            "trust_score": 5.0,       # 1-10
            "last_updated": datetime.now().isoformat()
        }
        
        self._save_profile(new_profile)
        print("✨ پروفایل جدید کاربر ایجاد شد")
        return new_profile
    
    def analyze_message(self, message: str) -> Dict:
        """تحلیل پیام کاربر برای استخراج اطلاعات"""
        analysis = {
            "topics": self._extract_topics(message),
            "emotions": self._detect_emotions(message),
            "personal_info": self._extract_personal_info(message),
            "communication_style": self._analyze_style(message),
            "complexity": self._measure_complexity(message)
        }
        
        return analysis
    
    def _extract_topics(self, message: str) -> List[str]:
        """استخراج موضوعات از پیام"""
        topics = []
        
        # موضوعات فنی
        tech_keywords = {
            "برنامه‌نویسی": ["کد", "برنامه", "پایتون", "جاوا", "اسکریپت"],
            "هوش مصنوعی": ["ai", "هوش مصنوعی", "یادگیری", "مدل"],
            "وب": ["سایت", "وب", "html", "css", "react"],
            "موبایل": ["اپ", "موبایل", "اندروید", "ios"]
        }
        
        # موضوعات شخصی
        personal_keywords = {
            "کار": ["کار", "شغل", "پروژه", "تیم"],
            "تحصیل": ["دانشگاه", "درس", "امتحان", "مطالعه"],
            "سرگرمی": ["فیلم", "بازی", "موزیک", "کتاب"],
            "ورزش": ["ورزش", "فوتبال", "بسکتبال", "دویدن"]
        }
        
        message_lower = message.lower()
        
        for topic, keywords in {**tech_keywords, **personal_keywords}.items():
            if any(keyword in message_lower for keyword in keywords):
                topics.append(topic)
        
        return topics
    
    def _detect_emotions(self, message: str) -> List[str]:
        """تشخیص احساسات از پیام"""
        emotions = []
        
        emotion_patterns = {
            "خوشحالی": ["خوشحال", "عالی", "فوق‌العاده", "😊", "😄", "👍"],
            "ناراحتی": ["ناراحت", "غمگین", "بد", "😢", "😞", "👎"],
            "تعجب": ["واو", "عجیب", "باورنکردنی", "😮", "😲"],
            "علاقه": ["جالب", "دوست دارم", "علاقه", "❤️", "💙"],
            "سردرگمی": ["نمی‌فهمم", "گیج", "چطور", "❓", "🤔"]
        }
        
        message_lower = message.lower()
        
        for emotion, patterns in emotion_patterns.items():
            if any(pattern in message_lower for pattern in patterns):
                emotions.append(emotion)
        
        return emotions if emotions else ["خنثی"]
    
    def _extract_personal_info(self, message: str) -> Dict:
        """استخراج اطلاعات شخصی"""
        info = {}
        
        # تشخیص نام
        name_patterns = [
            r"اسمم (.+) است",
            r"من (.+) هستم",
            r"نامم (.+)",
            r"صدام کن (.+)"
        ]
        
        for pattern in name_patterns:
            match = re.search(pattern, message)
            if match:
                info["name"] = match.group(1).strip()
                break
        
        # تشخیص شغل
        job_patterns = [
            r"شغلم (.+) است",
            r"کارم (.+)",
            r"برنامه‌نویس (.+)",
            r"توسعه‌دهنده (.+)"
        ]
        
        for pattern in job_patterns:
            match = re.search(pattern, message)
            if match:
                info["job"] = match.group(1).strip()
                break
        
        return info
    def _analyze_style(self, message: str) -> str:
        """تحلیل سبک ارتباطی"""
        message_lower = message.lower()
        
        # رسمی vs غیررسمی
        formal_indicators = ["لطفاً", "متشکرم", "با احترام", "خواهشمند"]
        informal_indicators = ["سلام", "چطوری", "ممنون", "دمت گرم"]
        
        formal_count = sum(1 for indicator in formal_indicators if indicator in message_lower)
        informal_count = sum(1 for indicator in informal_indicators if indicator in message_lower)
        
        if formal_count > informal_count:
            return "formal"
        elif informal_count > formal_count:
            return "informal"
        else:
            return "neutral"
    
    def _measure_complexity(self, message: str) -> str:
        """اندازه‌گیری پیچیدگی پیام"""
        words = len(message.split())
        sentences = len([s for s in message.split('.') if s.strip()])
        
        if words < 10:
            return "simple"
        elif words < 30:
            return "medium"
        else:
            return "complex"
    
    def update_profile(self, message: str, analysis: Dict):
        """به‌روزرسانی پروفایل بر اساس تحلیل"""
        
        # به‌روزرسانی موضوعات علاقه
        if analysis["topics"]:
            current_topics = self.user_profile["preferences"]["topics_of_interest"]
            for topic in analysis["topics"]:
                if topic not in current_topics:
                    current_topics.append(topic)
        
        # به‌روزرسانی اطلاعات شخصی
        if analysis["personal_info"]:
            for key, value in analysis["personal_info"].items():
                if key == "name" and not self.user_profile.get("name"):
                    self.user_profile["name"] = value
                    print(f"👤 نام کاربر ثبت شد: {value}")
        
        # به‌روزرسانی سبک ارتباطی
        current_style = self.user_profile["preferences"]["communication_style"]
        new_style = analysis["communication_style"]
        
        if new_style != "neutral":
            self.user_profile["preferences"]["communication_style"] = new_style
        
        # افزایش سطح رابطه
        self._increase_relationship_level()
        
        # ذخیره تعامل
        self._log_interaction(message, analysis)
        
        # ذخیره پروفایل
        self.user_profile["last_updated"] = datetime.now().isoformat()
        self._save_profile(self.user_profile)
    
    def _increase_relationship_level(self):
        """افزایش سطح رابطه"""
        self.interaction_stats["total_messages"] += 1
        
        # هر 10 پیام، سطح رابطه افزایش می‌یابد
        if self.interaction_stats["total_messages"] % 10 == 0:
            if self.user_profile["relationship_level"] < 10:
                self.user_profile["relationship_level"] += 0.5
                print(f"💙 سطح رابطه افزایش یافت: {self.user_profile['relationship_level']}")
    
    def _log_interaction(self, message: str, analysis: Dict):
        """ثبت تعامل در فایل"""
        interaction = {
            "timestamp": datetime.now().isoformat(),
            "message_length": len(message),
            "topics": analysis["topics"],
            "emotions": analysis["emotions"],
            "style": analysis["communication_style"],
            "complexity": analysis["complexity"]
        }
        
        os.makedirs("data/personality", exist_ok=True)
        with open(self.interactions_file, 'a', encoding='utf-8') as f:
            f.write(json.dumps(interaction, ensure_ascii=False) + '\n')
    
    def _save_profile(self, profile: Dict):
        """ذخیره پروفایل"""
        with open(self.profile_file, 'w', encoding='utf-8') as f:
            json.dump(profile, f, ensure_ascii=False, indent=2)
    
    def get_personalized_context(self) -> str:
        """دریافت context شخصی‌سازی شده"""
        context = []
        
        # نام کاربر
        if self.user_profile.get("name"):
            context.append(f"نام کاربر: {self.user_profile['name']}")
        
        # سطح رابطه
        relationship_level = self.user_profile["relationship_level"]
        if relationship_level < 3:
            context.append("رابطه: تازه آشنا")
        elif relationship_level < 6:
            context.append("رابطه: دوست")
        elif relationship_level < 9:
            context.append("رابطه: دوست نزدیک")
        else:
            context.append("رابطه: رفیق صمیمی")
        
        # موضوعات علاقه
        topics = self.user_profile["preferences"]["topics_of_interest"]
        if topics:
            context.append(f"علایق: {', '.join(topics[:3])}")
        
        # سبک ارتباطی
        style = self.user_profile["preferences"]["communication_style"]
        context.append(f"سبک ارتباطی: {style}")
        
        return "\n".join(context)
    
    def get_relationship_insights(self) -> Dict:
        """دریافت بینش‌های رابطه"""
        return {
            "relationship_level": self.user_profile["relationship_level"],
            "trust_score": self.user_profile["trust_score"],
            "total_interactions": self.interaction_stats.get("total_messages", 0),
            "favorite_topics": self.user_profile["preferences"]["topics_of_interest"][:5],
            "communication_style": self.user_profile["preferences"]["communication_style"],
            "name": self.user_profile.get("name", "ناشناس")
        }

# نمونه سراسری
user_profiler = UserProfiler()