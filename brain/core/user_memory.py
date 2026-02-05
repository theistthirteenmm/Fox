"""
سیستم حافظه کاربر برای روباه
حفظ اطلاعات شخصی و تاریخچه مکالمات
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional

class UserMemory:
    def __init__(self):
        self.memory_file = "data/personality/user_profile.json"
        self.conversations_file = "data/personality/user_interactions.jsonl"
        
        # بارگذاری حافظه موجود
        self.user_data = self._load_user_memory()
        
        print(f"🧠 حافظه کاربر بارگذاری شد - کاربر: {self.get_user_name()}")
    
    def _load_user_memory(self) -> Dict:
        """بارگذاری حافظه کاربر"""
        os.makedirs("data/personality", exist_ok=True)
        
        if os.path.exists(self.memory_file):
            try:
                with open(self.memory_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except:
                pass
        
        # ایجاد حافظه جدید
        return {
            "name": None,
            "personal_info": {},
            "preferences": {},
            "conversation_history": [],
            "topics_discussed": [],
            "last_interaction": None,
            "total_conversations": 0,
            "created_at": datetime.now().isoformat()
        }
    
    def save_user_memory(self):
        """ذخیره حافظه کاربر"""
        try:
            with open(self.memory_file, "w", encoding="utf-8") as f:
                json.dump(self.user_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"خطا در ذخیره حافظه: {e}")
    
    def set_user_name(self, name: str):
        """تنظیم نام کاربر"""
        self.user_data["name"] = name
        self.save_user_memory()
        print(f"👤 نام کاربر ثبت شد: {name}")
    
    def get_user_name(self) -> Optional[str]:
        """دریافت نام کاربر"""
        return self.user_data.get("name")
    
    def add_personal_info(self, key: str, value: str):
        """اضافه کردن اطلاعات شخصی"""
        if "personal_info" not in self.user_data:
            self.user_data["personal_info"] = {}
        
        self.user_data["personal_info"][key] = value
        self.save_user_memory()
        print(f"📝 اطلاعات شخصی اضافه شد: {key} = {value}")
    
    def get_personal_info(self, key: str = None) -> Dict:
        """دریافت اطلاعات شخصی"""
        personal_info = self.user_data.get("personal_info", {})
        if key:
            return personal_info.get(key)
        return personal_info
    
    def remember_conversation(self, user_message: str, ai_response: str, topic: str = None):
        """ذخیره مکالمه در حافظه"""
        conversation = {
            "timestamp": datetime.now().isoformat(),
            "user_message": user_message[:200],  # محدود کردن طول
            "ai_response": ai_response[:200],
            "topic": topic
        }
        
        # نگه‌داری آخرین 50 مکالمه
        if "conversation_history" not in self.user_data:
            self.user_data["conversation_history"] = []
        
        self.user_data["conversation_history"].append(conversation)
        if len(self.user_data["conversation_history"]) > 50:
            self.user_data["conversation_history"] = self.user_data["conversation_history"][-50:]
        
        # به‌روزرسانی آمار
        if "total_conversations" not in self.user_data:
            self.user_data["total_conversations"] = 0
        self.user_data["total_conversations"] += 1
        self.user_data["last_interaction"] = datetime.now().isoformat()
        
        # اضافه کردن موضوع
        if topic and topic not in self.user_data.get("topics_discussed", []):
            if "topics_discussed" not in self.user_data:
                self.user_data["topics_discussed"] = []
            self.user_data["topics_discussed"].append(topic)
        
        self.save_user_memory()
    
    def get_recent_conversations(self, count: int = 5) -> List[Dict]:
        """دریافت مکالمات اخیر"""
        conversations = self.user_data.get("conversation_history", [])
        return conversations[-count:] if conversations else []
    
    def find_related_conversations(self, topic: str, count: int = 3) -> List[Dict]:
        """یافتن مکالمات مرتبط با موضوع"""
        conversations = self.user_data.get("conversation_history", [])
        related = []
        
        for conv in conversations:
            if (topic.lower() in conv.get("user_message", "").lower() or 
                topic.lower() in conv.get("ai_response", "").lower() or
                conv.get("topic", "").lower() == topic.lower()):
                related.append(conv)
        
        return related[-count:] if related else []
    
    def get_user_stats(self) -> Dict:
        """آمار کاربر"""
        return {
            "name": self.get_user_name(),
            "total_conversations": self.user_data.get("total_conversations", 0),
            "topics_discussed": len(self.user_data.get("topics_discussed", [])),
            "last_interaction": self.user_data.get("last_interaction"),
            "member_since": self.user_data.get("created_at")
        }
    
    def extract_user_info_from_message(self, message: str) -> Dict:
        """استخراج اطلاعات کاربر از پیام"""
        extracted = {}
        message_lower = message.lower()
        
        # تشخیص نام
        if "اسم من" in message_lower or "نام من" in message_lower:
            # استخراج نام از جملات مثل "اسم من حامد است"
            import re
            name_patterns = [
                r"اسم من ([^\s]+)",
                r"نام من ([^\s]+)", 
                r"من ([^\s]+) هستم",
                r"من ([^\s]+)م"
            ]
            
            for pattern in name_patterns:
                match = re.search(pattern, message)
                if match:
                    name = match.group(1)
                    if len(name) > 1 and name not in ["کسی", "کسیم"]:
                        extracted["name"] = name
                        break
        
        # تشخیص شغل
        if "شغل" in message_lower or "کار" in message_lower:
            job_keywords = ["برنامه‌نویس", "مهندس", "دکتر", "معلم", "دانشجو"]
            for job in job_keywords:
                if job in message_lower:
                    extracted["job"] = job
                    break
        
        # تشخیص علایق
        interests = []
        if "عاشق" in message_lower or "دوست دارم" in message_lower:
            interest_keywords = ["برنامه‌نویسی", "کوهنوردی", "نقاشی", "موسیقی", "ورزش", "مطالعه"]
            for interest in interest_keywords:
                if interest in message_lower:
                    interests.append(interest)
        
        if interests:
            extracted["interests"] = interests
        
        return extracted
    
    def update_user_info_from_message(self, message: str):
        """به‌روزرسانی اطلاعات کاربر از پیام"""
        extracted = self.extract_user_info_from_message(message)
        
        for key, value in extracted.items():
            if key == "name":
                self.set_user_name(value)
            elif key == "interests":
                for interest in value:
                    self.add_personal_info(f"interest_{interest}", "true")
            else:
                self.add_personal_info(key, value)

# نمونه سراسری
user_memory = UserMemory()