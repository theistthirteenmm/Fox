"""
موتور شخصیت روباه
مدیریت رشد و تکامل شخصیت
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List
import random

class PersonalityEngine:
    def __init__(self):
        self.personality_file = "data/personality/profile.json"
        self.interactions_file = "data/personality/interactions.jsonl"
        
        # ویژگی‌های شخصیتی
        self.traits = {
            "curiosity": 0.5,      # کنجکاوی
            "friendliness": 0.8,   # دوستانه بودن
            "helpfulness": 0.9,    # کمک‌کردن
            "humor": 0.3,          # شوخ‌طبعی
            "formality": 0.4,      # رسمی بودن
            "creativity": 0.6,     # خلاقیت
            "patience": 0.7,       # صبر
            "enthusiasm": 0.5      # اشتیاق
        }
        
        # حالات احساسی
        self.moods = ["خوشحال", "کنجکاو", "آرام", "پرانرژی", "متفکر", "دوستانه"]
        self.current_mood = "دوستانه"
        
        # سطح رشد (مثل سن)
        self.development_level = 1
        self.experience_points = 0
        
        # بارگذاری یا ایجاد شخصیت
        self.profile = self._load_or_create_personality()
        
        # به‌روزرسانی از profile
        self.development_level = self.profile.get("development_level", 1)
        self.experience_points = self.profile.get("experience_points", 0)
        
        print(f"🎭 شخصیت روباه بارگذاری شد - سطح: {self.development_level}")
    
    def _load_or_create_personality(self) -> Dict:
        """بارگذاری یا ایجاد شخصیت جدید"""
        os.makedirs("data/personality", exist_ok=True)
        
        if os.path.exists(self.personality_file):
            try:
                with open(self.personality_file, "r", encoding="utf-8") as f:
                    profile = json.load(f)
                    print("📂 شخصیت موجود بارگذاری شد")
                    return profile
            except:
                pass
        
        # ایجاد شخصیت جدید (تولد!)
        print("🐣 روباه متولد شد! شخصیت جدید در حال ایجاد...")
        
        new_profile = {
            "birth_date": datetime.now().isoformat(),
            "development_level": 1,
            "experience_points": 0,
            "total_interactions": 0,
            "favorite_topics": [],
            "learned_preferences": {},
            "growth_milestones": [],
            "personality_traits": self.traits.copy()
        }
        
        self._save_personality(new_profile)
        return new_profile
    
    def analyze_interaction(self, user_message: str) -> Dict:
        """تحلیل تعامل کاربر و تنظیم شخصیت"""
        
        # تحلیل احساسات پیام
        emotion = self._detect_emotion(user_message)
        
        # تنظیم حالت بر اساس پیام کاربر
        self._adjust_mood(emotion, user_message)
        
        # شناسایی موضوعات مورد علاقه
        topics = self._extract_topics(user_message)
        self._update_interests(topics)
        
        return {
            "level": self.development_level,
            "mood": self.current_mood,
            "detected_emotion": emotion,
            "relevant_traits": self._get_relevant_traits(user_message),
            "topics": topics
        }
    
    def update_from_interaction(self, user_message: str, ai_response: str):
        """به‌روزرسانی شخصیت بعد از تعامل"""
        
        # افزایش تجربه
        self.experience_points += 1
        self.profile["total_interactions"] += 1
        
        # بررسی رشد سطح
        if self.experience_points >= (self.development_level * 10):
            self._level_up()
        
        # ذخیره تعامل
        self._log_interaction(user_message, ai_response)
        
        # ذخیره تغییرات
        self._save_personality(self.profile)
    
    def get_development_level(self) -> int:
        """دریافت سطح رشد فعلی"""
        return self.development_level
    
    def get_personality_context(self) -> str:
        """دریافت context شخصیت برای AI"""
        
        age_description = self._get_age_description()
        trait_description = self._get_dominant_traits()
        
        context = f"""
شخصیت فعلی روباه:
- {age_description}
- حالت: {self.current_mood}
- ویژگی‌های غالب: {trait_description}
- تعداد تعاملات: {self.profile.get('total_interactions', 0)}
- موضوعات مورد علاقه: {', '.join(self.profile.get('favorite_topics', [])[:3])}
"""
        return context
    
    def _detect_emotion(self, message: str) -> str:
        """تشخیص احساسات پیام"""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ["خوشحال", "عالی", "فوق‌العاده", "😊", "😄"]):
            return "مثبت"
        elif any(word in message_lower for word in ["ناراحت", "غمگین", "بد", "😢", "😞"]):
            return "منفی"
        elif any(word in message_lower for word in ["سؤال", "چطور", "چرا", "کجا", "؟"]):
            return "کنجکاو"
        else:
            return "خنثی"
    
    def _adjust_mood(self, emotion: str, message: str):
        """تنظیم حالت بر اساس احساسات"""
        
        if emotion == "مثبت":
            self.current_mood = random.choice(["خوشحال", "پرانرژی", "دوستانه"])
        elif emotion == "منفی":
            self.current_mood = random.choice(["آرام", "دوستانه", "صبور"])
        elif emotion == "کنجکاو":
            self.current_mood = random.choice(["کنجکاو", "متفکر", "پرانرژی"])
        
        # تأثیر بر ویژگی‌های شخصیتی
        if emotion == "مثبت":
            self.traits["enthusiasm"] = min(1.0, self.traits["enthusiasm"] + 0.01)
        elif "سؤال" in message.lower():
            self.traits["curiosity"] = min(1.0, self.traits["curiosity"] + 0.01)
    
    def _extract_topics(self, message: str) -> List[str]:
        """استخراج موضوعات از پیام"""
        topics = []
        
        topic_keywords = {
            "برنامه‌نویسی": ["کد", "برنامه", "پایتون", "جاوا", "وب"],
            "علم": ["فیزیک", "شیمی", "ریاضی", "علم"],
            "هنر": ["نقاشی", "موسیقی", "شعر", "هنر"],
            "ورزش": ["فوتبال", "بسکتبال", "ورزش", "تمرین"],
            "غذا": ["غذا", "آشپزی", "رستوران", "طبخ"],
            "سفر": ["سفر", "مسافرت", "شهر", "کشور"]
        }
        
        message_lower = message.lower()
        for topic, keywords in topic_keywords.items():
            if any(keyword in message_lower for keyword in keywords):
                topics.append(topic)
        
        return topics
    
    def _update_interests(self, topics: List[str]):
        """به‌روزرسانی علایق"""
        for topic in topics:
            if topic not in self.profile["favorite_topics"]:
                self.profile["favorite_topics"].append(topic)
            
            # محدود کردن به 10 موضوع
            if len(self.profile["favorite_topics"]) > 10:
                self.profile["favorite_topics"] = self.profile["favorite_topics"][-10:]
    
    def _level_up(self):
        """ارتقای سطح"""
        self.development_level += 1
        self.profile["development_level"] = self.development_level
        
        milestone = {
            "level": self.development_level,
            "date": datetime.now().isoformat(),
            "interactions_count": self.profile["total_interactions"]
        }
        
        self.profile["growth_milestones"].append(milestone)
        
        print(f"🎉 روباه به سطح {self.development_level} رسید!")
        
        # تقویت ویژگی‌ها با رشد
        for trait in self.traits:
            self.traits[trait] = min(1.0, self.traits[trait] + 0.05)
    
    def _get_age_description(self) -> str:
        """توصیف سن/سطح رشد"""
        if self.development_level == 1:
            return "تازه متولد شده و در حال یادگیری"
        elif self.development_level <= 5:
            return "جوان و کنجکاو"
        elif self.development_level <= 10:
            return "با تجربه و دانا"
        else:
            return "پیشرفته و حکیم"
    
    def _get_dominant_traits(self) -> str:
        """ویژگی‌های غالب"""
        sorted_traits = sorted(self.traits.items(), key=lambda x: x[1], reverse=True)
        top_traits = [trait[0] for trait in sorted_traits[:3]]
        
        trait_names = {
            "curiosity": "کنجکاو",
            "friendliness": "دوستانه", 
            "helpfulness": "کمک‌کار",
            "humor": "شوخ‌طبع",
            "formality": "رسمی",
            "creativity": "خلاق",
            "patience": "صبور",
            "enthusiasm": "پرشور"
        }
        
        return ", ".join([trait_names.get(trait, trait) for trait in top_traits])
    
    def _get_relevant_traits(self, message: str) -> Dict[str, float]:
        """ویژگی‌های مرتبط با پیام"""
        relevant = {}
        
        if "سؤال" in message.lower() or "؟" in message:
            relevant["curiosity"] = self.traits["curiosity"]
            relevant["helpfulness"] = self.traits["helpfulness"]
        
        if any(word in message.lower() for word in ["لطفاً", "ممنون", "متشکرم"]):
            relevant["friendliness"] = self.traits["friendliness"]
            relevant["formality"] = self.traits["formality"]
        
        return relevant
    
    def _log_interaction(self, user_message: str, ai_response: str):
        """ثبت تعامل"""
        interaction = {
            "timestamp": datetime.now().isoformat(),
            "user_message": user_message[:100],  # محدود کردن طول
            "ai_response": ai_response[:100],
            "mood": self.current_mood,
            "level": self.development_level,
            "experience_points": self.experience_points
        }
        
        with open(self.interactions_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(interaction, ensure_ascii=False) + "\n")
    
    def _save_personality(self, profile: Dict):
        """ذخیره شخصیت"""
        profile["personality_traits"] = self.traits
        profile["experience_points"] = self.experience_points
        profile["last_updated"] = datetime.now().isoformat()
        
        with open(self.personality_file, "w", encoding="utf-8") as f:
            json.dump(profile, f, ensure_ascii=False, indent=2)