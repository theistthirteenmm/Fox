"""
🎭 سیستم یادگیری داینامیک نام و شخصیت
یادگیری نام و ویژگی‌های شخصیتی از طریق مکالمه
"""

import json
import os
import re
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

@dataclass
class NameLearningEvent:
    """رویداد یادگیری نام"""
    timestamp: str
    user_message: str
    extracted_name: str
    confidence: float
    context: str
    learning_type: str  # "direct", "suggestion", "correction"

class DynamicNameLearning:
    def __init__(self):
        self.learning_file = "data/personality/name_learning.json"
        self.current_name = "روباه"  # نام پیش‌فرض
        self.name_confidence = 0.5  # اعتماد به نام فعلی
        self.learning_history = []
        self.name_suggestions = []
        
        # بارگذاری تاریخچه یادگیری
        self._load_learning_history()
        
        print(f"🎭 سیستم یادگیری نام راه‌اندازی شد - نام فعلی: {self.current_name}")
    
    def _load_learning_history(self):
        """بارگذاری تاریخچه یادگیری نام"""
        if os.path.exists(self.learning_file):
            try:
                with open(self.learning_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.current_name = data.get("current_name", "روباه")
                    self.name_confidence = data.get("name_confidence", 0.5)
                    self.learning_history = data.get("learning_history", [])
                    self.name_suggestions = data.get("name_suggestions", [])
                    print(f"📂 تاریخچه یادگیری نام بارگذاری شد: {len(self.learning_history)} رویداد")
            except Exception as e:
                print(f"⚠️ خطا در بارگذاری تاریخچه نام: {e}")
    
    def _save_learning_history(self):
        """ذخیره تاریخچه یادگیری"""
        os.makedirs("data/personality", exist_ok=True)
        
        data = {
            "current_name": self.current_name,
            "name_confidence": self.name_confidence,
            "learning_history": self.learning_history,
            "name_suggestions": self.name_suggestions,
            "last_updated": datetime.now().isoformat()
        }
        
        with open(self.learning_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def analyze_message_for_name(self, message: str) -> Optional[Dict]:
        """تحلیل پیام برای یادگیری نام"""
        message_lower = message.lower().strip()
        
        # الگوهای مختلف یادگیری نام - بهبود یافته
        name_patterns = {
            "direct_assignment": [
                r"اسمت\s+(.+?)\s+باشه",
                r"اسمت\s+(.+?)\s+بذارم",
                r"اسمت\s+(.+?)\s+است",
                r"اسمت\s+(.+?)\s+هست",
                r"نامت\s+(.+?)\s+باشد",
                r"صدات\s+کنم\s+(.+)",
                r"بهت\s+بگم\s+(.+)",
                r"اسمت\s+رو\s+بذارم\s+(.+)",
                r"اسمت\s+(.+)",  # ساده‌تر
                r"نامت\s+(.+)",  # ساده‌تر
            ],
            "suggestion": [
                r"چطوره\s+اسمت\s+(.+?)\s+باشه",
                r"پیشنهاد\s+می‌کنم\s+اسمت\s+(.+)",
                r"بهتره\s+اسمت\s+(.+?)\s+باشه",
                r"می‌تونم\s+صدات\s+کنم\s+(.+)",
                r"دوست\s+داری\s+اسمت\s+(.+?)\s+باشه",
                r"چه\s+طور\s+(.+?)\s+باشه",
            ],
            "question": [
                r"اسمت\s+چی\s+بذارم",
                r"چه\s+اسمی\s+دوست\s+داری",
                r"اسم\s+دلخواهت\s+چیه",
                r"نامت\s+چه\s+باشد",
                r"چی\s+صدات\s+کنم",
                r"اسمت\s+چیه",
            ],
            "correction": [
                r"نه\s*،?\s*اسمت\s+(.+?)\s+است",
                r"اشتباه\s*،?\s*نامت\s+(.+)",
                r"درست\s+کن\s*،?\s*اسمت\s+(.+)",
            ]
        }
        
        # جستجو در الگوها
        for learning_type, patterns in name_patterns.items():
            for pattern in patterns:
                match = re.search(pattern, message_lower)
                if match:
                    if learning_type == "question":
                        return {
                            "type": "name_question",
                            "confidence": 0.9,
                            "context": message,
                            "response_needed": True
                        }
                    else:
                        # استخراج نام از گروه اول regex
                        if match.groups():
                            extracted_name = match.group(1).strip()
                        else:
                            # اگر گروهی نداشت، کل match را بگیر
                            extracted_name = match.group(0).strip()
                        
                        # پاک کردن کلمات اضافی
                        extracted_name = self._clean_extracted_name(extracted_name)
                        
                        if extracted_name:
                            return {
                                "type": learning_type,
                                "extracted_name": extracted_name,
                                "confidence": self._calculate_confidence(learning_type, message),
                                "context": message,
                                "response_needed": True
                            }
        
        # بررسی الگوهای ساده‌تر برای مکالمه طبیعی
        simple_patterns = [
            (r"(.+?)\s+باشه\s+اسمت", "direct_assignment"),
            (r"(.+?)\s+صدات\s+کنم", "direct_assignment"),
            (r"اسمت\s+بشه\s+(.+)", "direct_assignment"),
        ]
        
        for pattern, learning_type in simple_patterns:
            match = re.search(pattern, message_lower)
            if match:
                extracted_name = match.group(1).strip()
                extracted_name = self._clean_extracted_name(extracted_name)
                
                if extracted_name:
                    return {
                        "type": learning_type,
                        "extracted_name": extracted_name,
                        "confidence": self._calculate_confidence(learning_type, message),
                        "context": message,
                        "response_needed": True
                    }
        
        return None
    
    def _clean_extracted_name(self, name: str) -> str:
        """پاک کردن نام استخراج شده"""
        # حذف کلمات اضافی
        stop_words = ["که", "را", "رو", "هم", "باشه", "باشد", "کنم", "کن"]
        
        # حذف علائم نگارشی
        name = re.sub(r'[^\w\s]', '', name)
        
        # حذف کلمات اضافی
        words = name.split()
        cleaned_words = [word for word in words if word not in stop_words]
        
        return " ".join(cleaned_words).strip()
    
    def _calculate_confidence(self, learning_type: str, message: str) -> float:
        """محاسبه اعتماد به یادگیری"""
        base_confidence = {
            "direct_assignment": 0.9,
            "suggestion": 0.7,
            "correction": 0.95,
            "question": 0.8
        }
        
        confidence = base_confidence.get(learning_type, 0.5)
        
        # افزایش اعتماد بر اساس کلمات تأکیدی
        emphasis_words = ["حتماً", "قطعاً", "لطفاً", "خواهشاً", "می‌خوام"]
        if any(word in message.lower() for word in emphasis_words):
            confidence += 0.1
        
        return min(1.0, confidence)
    
    def learn_name(self, analysis: Dict) -> Dict:
        """یادگیری نام جدید"""
        if analysis["type"] == "name_question":
            return self._handle_name_question()
        
        extracted_name = analysis["extracted_name"]
        confidence = analysis["confidence"]
        learning_type = analysis["type"]
        
        # ثبت رویداد یادگیری
        event = NameLearningEvent(
            timestamp=datetime.now().isoformat(),
            user_message=analysis["context"],
            extracted_name=extracted_name,
            confidence=confidence,
            context=analysis["context"],
            learning_type=learning_type
        )
        
        self.learning_history.append({
            "timestamp": event.timestamp,
            "user_message": event.user_message,
            "extracted_name": event.extracted_name,
            "confidence": event.confidence,
            "context": event.context,
            "learning_type": event.learning_type
        })
        
        # تصمیم‌گیری برای تغییر نام
        should_change = self._should_change_name(extracted_name, confidence, learning_type)
        
        if should_change:
            old_name = self.current_name
            self.current_name = extracted_name
            self.name_confidence = confidence
            
            print(f"🎭 نام تغییر یافت: {old_name} → {self.current_name}")
            
            self._save_learning_history()
            
            return {
                "name_changed": True,
                "old_name": old_name,
                "new_name": self.current_name,
                "confidence": confidence,
                "response": self._generate_name_change_response(old_name, self.current_name)
            }
        else:
            # اضافه کردن به پیشنهادات
            self.name_suggestions.append({
                "name": extracted_name,
                "confidence": confidence,
                "timestamp": datetime.now().isoformat(),
                "learning_type": learning_type
            })
            
            self._save_learning_history()
            
            return {
                "name_changed": False,
                "suggestion_added": True,
                "suggested_name": extracted_name,
                "response": self._generate_suggestion_response(extracted_name)
            }
    
    def _should_change_name(self, new_name: str, confidence: float, learning_type: str) -> bool:
        """تصمیم‌گیری برای تغییر نام"""
        
        # اگر نام جدید همان نام فعلی باشد
        if new_name.lower() == self.current_name.lower():
            return False
        
        # اگر اعتماد بالا باشد، تغییر بده
        if confidence >= 0.8:
            return True
        
        # اگر نوع یادگیری correction باشد
        if learning_type == "correction":
            return True
        
        # اگر اعتماد به نام فعلی پایین باشد
        if self.name_confidence < 0.6 and confidence > self.name_confidence:
            return True
        
        return False
    
    def _handle_name_question(self) -> Dict:
        """پاسخ به سؤال درباره نام"""
        if self.name_suggestions:
            # اگر پیشنهادی داریم
            latest_suggestion = self.name_suggestions[-1]
            return {
                "name_changed": False,
                "response": f"چه اسمی دوست داری؟ اگر می‌خوای می‌تونم {latest_suggestion['name']} باشم، یا هر اسم دیگه‌ای که دوست داری رو بگو!"
            }
        else:
            return {
                "name_changed": False,
                "response": f"الان اسمم {self.current_name} هست. اگر دوست داری اسم دیگه‌ای برام انتخاب کن! چه اسمی دوست داری؟"
            }
    
    def _generate_name_change_response(self, old_name: str, new_name: str) -> str:
        """تولید پاسخ برای تغییر نام"""
        responses = [
            f"عالی! از الان اسمم {new_name} هست! ممنون که این اسم قشنگ رو برام انتخاب کردی 😊",
            f"خوشحالم! اسم {new_name} رو خیلی دوست دارم. از الان منو {new_name} صدا کن! 🦊",
            f"واو! اسم {new_name} عالیه! حالا که اسم جدیدم رو دارم، بیا بیشتر باهم آشنا بشیم 💙",
            f"ممنون! اسم {new_name} خیلی قشنگه. حس می‌کنم این اسم بهم میاد! 😄"
        ]
        
        import random
        return random.choice(responses)
    
    def _generate_suggestion_response(self, suggested_name: str) -> str:
        """تولید پاسخ برای پیشنهاد نام"""
        responses = [
            f"اسم {suggested_name} جالبه! بذار فکر کنم... مطمئنی که می‌خوای اسمم {suggested_name} باشه؟",
            f"{suggested_name}؟ اسم خوبیه! اگر واقعاً دوست داری، بگو تا اسمم رو عوض کنم",
            f"پیشنهاد {suggested_name} رو شنیدم. اگر مطمئنی، بگو که اسمم {suggested_name} باشه!"
        ]
        
        import random
        return random.choice(responses)
    
    def get_current_name(self) -> str:
        """دریافت نام فعلی"""
        return self.current_name
    
    def get_name_confidence(self) -> float:
        """دریافت اعتماد به نام فعلی"""
        return self.name_confidence
    
    def get_learning_stats(self) -> Dict:
        """آمار یادگیری نام"""
        return {
            "current_name": self.current_name,
            "name_confidence": self.name_confidence,
            "total_learning_events": len(self.learning_history),
            "suggestions_count": len(self.name_suggestions),
            "recent_suggestions": self.name_suggestions[-3:] if self.name_suggestions else []
        }
    
    def reset_name_learning(self):
        """ریست کردن یادگیری نام"""
        self.current_name = "روباه"
        self.name_confidence = 0.5
        self.learning_history = []
        self.name_suggestions = []
        self._save_learning_history()
        print("🔄 یادگیری نام ریست شد")

# نمونه سراسری
dynamic_name_learning = DynamicNameLearning()