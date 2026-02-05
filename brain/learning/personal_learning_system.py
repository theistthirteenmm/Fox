"""
🧠 سیستم یادگیری شخصی جامع
یادگیری واژگان، قوانین، و ترجیحات از مکالمه
"""

import json
import os
import re
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass

@dataclass
class LearningEvent:
    """رویداد یادگیری"""
    timestamp: str
    learning_type: str  # "vocabulary", "rule", "tone", "preference"
    user_message: str
    extracted_data: Dict
    confidence: float
    context: str

class PersonalLearningSystem:
    def __init__(self):
        self.learning_file = "data/personality/personal_learning.json"
        self.profile_file = "data/personality/personal_profile.json"
        self.vocabulary = {}  # {"انی": "این", "اونا": "آن‌ها"}
        self.rules = []  # [{"condition": "وقتی کد می‌خوام", "action": "توضیحات فارسی اضافه کن"}]
        self.tone_preferences = {}  # {"style": "دوستانه", "formality": "غیررسمی"}
        self.learning_history = []
        self.passive_facts = []  # یادگیری غیرمستقیم
        self.profile = {
            "facts": {},
            "preferences": {},
            "habits": {},
            "goals": {},
            "skills": {},
            "dislikes": {},
            "social": {}
        }
        
        # بارگذاری یادگیری‌های قبلی
        self._load_learning_data()
        self._load_profile_data()
        
        print(f"🧠 سیستم یادگیری شخصی راه‌اندازی شد")
        print(f"📚 واژگان: {len(self.vocabulary)} مورد")
        print(f"📋 قوانین: {len(self.rules)} مورد")
    
    def _load_learning_data(self):
        """بارگذاری داده‌های یادگیری"""
        if os.path.exists(self.learning_file):
            try:
                with open(self.learning_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.vocabulary = data.get("vocabulary", {})
                    self.rules = data.get("rules", [])
                    self.tone_preferences = data.get("tone_preferences", {})
                    self.learning_history = data.get("learning_history", [])
                    self.passive_facts = data.get("passive_facts", [])  # بارگذاری یادگیری غیرمستقیم
                    print(f"📂 یادگیری‌های قبلی بارگذاری شد")
            except Exception as e:
                print(f"⚠️ خطا در بارگذاری یادگیری‌ها: {e}")
    
    def _load_profile_data(self):
        """بارگذاری پروفایل شخصی"""
        if os.path.exists(self.profile_file):
            try:
                with open(self.profile_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, dict):
                        for key in self.profile.keys():
                            if key in data and isinstance(data[key], dict):
                                self.profile[key] = data[key]
                print("📂 پروفایل شخصی بارگذاری شد")
            except Exception as e:
                print(f"⚠️ خطا در بارگذاری پروفایل: {e}")
    
    def _save_learning_data(self):
        """ذخیره داده‌های یادگیری"""
        os.makedirs("data/personality", exist_ok=True)
        
        data = {
            "vocabulary": self.vocabulary,
            "rules": self.rules,
            "tone_preferences": self.tone_preferences,
            "learning_history": self.learning_history,
            "passive_facts": self.passive_facts,  # ذخیره یادگیری غیرمستقیم
            "last_updated": datetime.now().isoformat()
        }
        
        with open(self.learning_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def _save_profile_data(self):
        """ذخیره پروفایل شخصی"""
        os.makedirs("data/personality", exist_ok=True)
        with open(self.profile_file, 'w', encoding='utf-8') as f:
            json.dump(self.profile, f, ensure_ascii=False, indent=2)
    
    def analyze_message_for_learning(self, message: str) -> Optional[Dict]:
        """تحلیل پیام برای یادگیری"""
        message_lower = message.lower()
        
        # ۱. تشخیص یادگیری واژگان
        vocab_result = self._detect_vocabulary_learning(message)
        if vocab_result:
            return vocab_result
        
        # ۲. تشخیص قوانین شخصی
        rule_result = self._detect_rule_learning(message)
        if rule_result:
            return rule_result
        
        # ۳. تشخیص تغییر لحن
        tone_result = self._detect_tone_learning(message)
        if tone_result:
            return tone_result
        
        # ۴. تشخیص ترجیحات عمومی
        pref_result = self._detect_preference_learning(message)
        if pref_result:
            return pref_result
        
        return None
    
    def learn_profile_from_message(self, message: str) -> List[Dict]:
        """یادگیری ضمنی پروفایل از پیام کاربر"""
        updates = self._extract_profile_updates(message)
        for update in updates:
            self._update_profile_entry(**update)
        if updates:
            self._save_profile_data()
        return updates
    
    def _detect_vocabulary_learning(self, message: str) -> Optional[Dict]:
        """تشخیص یادگیری واژگان شخصی"""
        
        vocab_patterns = [
            r"وقتی میگم ['\"](.+)['\"] منظورم ['\"](.+)['\"] هست",
            r"وقتی میگم ['\"](.+)['\"] منظورم (.+) هست",
            r"وقتی میگم (.+) منظورم (.+) هست",
            r"(.+) یعنی (.+)",
            r"منظورم از (.+) همین (.+) است",
            r"(.+) به معنی (.+) است",
            r"وقتی (.+) میگم، منظورم (.+) هست",
            r"یاد بگیر که (.+) یعنی (.+)",
            r"بدون (.+) همون (.+) هست"
        ]
        
        for pattern in vocab_patterns:
            match = re.search(pattern, message.lower())
            if match:
                word = match.group(1).strip().strip('"\'')
                meaning = match.group(2).strip().strip('"\'')
                
                # پاک کردن کلمات اضافی
                word = self._clean_word(word)
                meaning = self._clean_word(meaning)
                
                if word and meaning:
                    return {
                        "type": "vocabulary",
                        "word": word,
                        "meaning": meaning,
                        "confidence": 0.9,
                        "context": message,
                        "response_needed": True
                    }
        
        return None
    
    def _detect_rule_learning(self, message: str) -> Optional[Dict]:
        """تشخیص یادگیری قوانین شخصی"""
        
        rule_patterns = [
            r"از این به بعد (.+)",
            r"همیشه (.+)",
            r"هر وقت (.+) بکنم، (.+)",
            r"هر وقت (.+) بپرسم، (.+)",
            r"وقتی (.+) می‌خوام، (.+)",
            r"وقتی درخواست (.+) کردم، (.+)",
            r"یاد بگیر که (.+)",
            r"قانون جدید: (.+)",
            r"حتماً (.+)"
        ]
        
        for pattern in rule_patterns:
            match = re.search(pattern, message.lower())
            if match:
                if len(match.groups()) == 1:
                    rule_text = match.group(1).strip()
                    return {
                        "type": "rule",
                        "rule_text": rule_text,
                        "condition": "همیشه",
                        "action": rule_text,
                        "confidence": 0.8,
                        "context": message,
                        "response_needed": True
                    }
                else:
                    condition = match.group(1).strip()
                    action = match.group(2).strip()
                    return {
                        "type": "rule",
                        "rule_text": f"وقتی {condition}، {action}",
                        "condition": condition,
                        "action": action,
                        "confidence": 0.9,
                        "context": message,
                        "response_needed": True
                    }
        
        return None
    
    def _detect_tone_learning(self, message: str) -> Optional[Dict]:
        """تشخیص تغییر لحن و سبک"""
        
        tone_patterns = [
            r"لحنت (.+) باشه",
            r"لحن (.+) استفاده کن",
            r"می‌خوام (.+) باهام صحبت کنی",
            r"سبک پاسخت (.+) باشه",
            r"طرز صحبتت (.+) باشه",
            r"(.+) حرف بزن",
            r"لحن صحبتت رو (.+) کن"
        ]
        
        for pattern in tone_patterns:
            match = re.search(pattern, message.lower())
            if match:
                tone_style = match.group(1).strip()
                
                return {
                    "type": "tone",
                    "tone_style": tone_style,
                    "confidence": 0.85,
                    "context": message,
                    "response_needed": True
                }
        
        return None
    
    def _detect_preference_learning(self, message: str) -> Optional[Dict]:
        """تشخیص ترجیحات عمومی - بهبود یافته با ایده‌های پرامپت"""
        
        pref_patterns = [
            r"ترجیح می‌دم (.+)",
            r"دوست دارم (.+)",
            r"بهتره (.+)",
            r"پاسخ‌هات (.+) باشه",
            r"جواب‌هات (.+) باشه",
            # الگوهای جدید از پرامپت:
            r"می‌خوام (.+) باشه",
            r"سبک پاسخت (.+)",
            r"فرمت ترجیحی (.+)",
            r"همیشه (.+) استفاده کن"
        ]
        
        for pattern in pref_patterns:
            match = re.search(pattern, message.lower())
            if match:
                preference = match.group(1).strip()
                
                return {
                    "type": "preference",
                    "preference": preference,
                    "confidence": 0.7,
                    "context": message,
                    "response_needed": True
                }
        
        return None
    
    def _clean_word(self, word: str) -> str:
        """پاک کردن کلمه از کلمات اضافی"""
        # حذف کلمات اضافی
        stop_words = ["که", "را", "رو", "هم", "باشه", "باشد", "کنم", "کن", "است", "هست"]
        
        # حذف علائم نگارشی
        word = re.sub(r'[^\w\s]', '', word)
        
        # حذف کلمات اضافی
        words = word.split()
        cleaned_words = [w for w in words if w not in stop_words]
        
        return " ".join(cleaned_words).strip()
    
    def _update_profile_entry(self, category: str, key: str, value: str, confidence: float, source: str, evidence: str):
        """به‌روزرسانی یا ثبت آیتم پروفایل"""
        if category not in self.profile:
            return
        
        entry = self.profile[category].get(key)
        now = datetime.now().isoformat()
        
        if entry:
            # تقویت اعتماد و به‌روزرسانی
            entry["value"] = value
            entry["confidence"] = min(0.95, max(entry.get("confidence", 0.5), confidence) + 0.05)
            entry["last_seen"] = now
            entry["evidence_count"] = entry.get("evidence_count", 1) + 1
        else:
            self.profile[category][key] = {
                "value": value,
                "confidence": confidence,
                "source": source,
                "created_at": now,
                "last_seen": now,
                "evidence_count": 1,
                "evidence": evidence[:120]
            }
    
    def _extract_profile_updates(self, message: str) -> List[Dict]:
        """استخراج ترجیحات، عادت‌ها، اهداف و اطلاعات از متن"""
        updates: List[Dict] = []
        msg = message.strip()
        msg_lower = msg.lower()
        
        patterns = [
            # حقایق و هویت
            (r"من (.+) هستم", "facts", "identity"),
            (r"اسم من (.+) است", "facts", "name"),
            (r"نام من (.+) است", "facts", "name"),
            (r"من (.+) کار می‌کنم", "facts", "job"),
            (r"من در (.+) زندگی می‌کنم", "facts", "location"),
            (r"من در (.+) ساکن هستم", "facts", "location"),
            (r"سن من (.+) است", "facts", "age"),
            (r"من (.+) تحصیل کردم", "facts", "education"),
            
            # ترجیحات
            (r"ترجیح می‌دم (.+)", "preferences", "preference"),
            (r"دوست دارم (.+)", "preferences", "like"),
            (r"علاقه دارم (.+)", "preferences", "like"),
            (r"از (.+) خوشم میاد", "preferences", "like"),
            
            # عدم ترجیح / dislike
            (r"دوست ندارم (.+)", "dislikes", "dislike"),
            (r"از (.+) خوشم نمیاد", "dislikes", "dislike"),
            
            # عادت‌ها
            (r"معمولاً (.+)", "habits", "habit"),
            (r"اغلب (.+)", "habits", "habit"),
            (r"هر روز (.+)", "habits", "habit"),
            
            # اهداف
            (r"هدفم (.+) است", "goals", "goal"),
            (r"می‌خوام (.+) بشم", "goals", "goal"),
            (r"برنامه دارم (.+)", "goals", "goal"),
            
            # مهارت‌ها
            (r"من (.+) بلدم", "skills", "skill"),
            (r"در (.+) خوبم", "skills", "skill"),
            (r"تخصصم (.+) است", "skills", "skill"),
            
            # روابط / اجتماعی
            (r"من تنها هستم", "social", "lonely"),
            (r"اغلب تنها میشم", "social", "lonely")
        ]
        
        for pattern, category, key in patterns:
            match = re.search(pattern, msg_lower)
            if match:
                value = match.group(1).strip()
                value = self._clean_word(value)
                if value:
                    updates.append({
                        "category": category,
                        "key": key,
                        "value": value,
                        "confidence": 0.7,
                        "source": "implicit",
                        "evidence": msg
                    })
        
        return updates
    
    def learn_from_analysis(self, analysis: Dict) -> Dict:
        """یادگیری از تحلیل پیام"""
        
        learning_type = analysis["type"]
        
        # ثبت رویداد یادگیری
        event = LearningEvent(
            timestamp=datetime.now().isoformat(),
            learning_type=learning_type,
            user_message=analysis["context"],
            extracted_data=analysis,
            confidence=analysis["confidence"],
            context=analysis["context"]
        )
        
        self.learning_history.append({
            "timestamp": event.timestamp,
            "learning_type": event.learning_type,
            "user_message": event.user_message,
            "extracted_data": event.extracted_data,
            "confidence": event.confidence,
            "context": event.context
        })
        
        # یادگیری بر اساس نوع
        if learning_type == "vocabulary":
            return self._learn_vocabulary(analysis)
        elif learning_type == "rule":
            return self._learn_rule(analysis)
        elif learning_type == "tone":
            return self._learn_tone(analysis)
        elif learning_type == "preference":
            return self._learn_preference(analysis)
        
        return {"learned": False, "response": "متوجه نشدم چی باید یاد بگیرم"}
    
    def _learn_vocabulary(self, analysis: Dict) -> Dict:
        """یادگیری واژگان شخصی"""
        word = analysis["word"]
        meaning = analysis["meaning"]
        
        # اگر قبلاً وجود داشت، به‌روزرسانی کن
        old_meaning = self.vocabulary.get(word)
        self.vocabulary[word] = meaning
        
        self._save_learning_data()
        
        if old_meaning:
            response = f"باشه! معنی '{word}' رو از '{old_meaning}' به '{meaning}' تغییر دادم 🔄"
        else:
            response = f"فهمیدم! از این به بعد وقتی '{word}' رو بگی، می‌دونم منظورت '{meaning}' هست 📚"
        
        print(f"📚 واژه جدید یاد گرفته شد: {word} = {meaning}")
        
        return {
            "learned": True,
            "type": "vocabulary",
            "word": word,
            "meaning": meaning,
            "response": response
        }
    
    def _learn_rule(self, analysis: Dict) -> Dict:
        """یادگیری قوانین شخصی"""
        rule_text = analysis["rule_text"]
        condition = analysis.get("condition", "همیشه")
        action = analysis.get("action", rule_text)
        
        # بررسی تکراری نبودن
        for existing_rule in self.rules:
            if existing_rule["condition"].lower() == condition.lower():
                # به‌روزرسانی قانون موجود
                existing_rule["action"] = action
                existing_rule["rule_text"] = rule_text
                existing_rule["updated_at"] = datetime.now().isoformat()
                
                self._save_learning_data()
                
                response = f"باشه! قانون '{condition}' رو به‌روزرسانی کردم 🔄"
                return {
                    "learned": True,
                    "type": "rule_updated",
                    "rule": rule_text,
                    "response": response
                }
        
        # اضافه کردن قانون جدید
        new_rule = {
            "condition": condition,
            "action": action,
            "rule_text": rule_text,
            "created_at": datetime.now().isoformat(),
            "is_active": True
        }
        
        self.rules.append(new_rule)
        self._save_learning_data()
        
        response = f"چشم! یاد گرفتم: {rule_text} 📋"
        
        print(f"📋 قانون جدید یاد گرفته شد: {rule_text}")
        
        return {
            "learned": True,
            "type": "rule",
            "rule": rule_text,
            "response": response
        }
    
    def _learn_tone(self, analysis: Dict) -> Dict:
        """یادگیری لحن و سبک"""
        tone_style = analysis["tone_style"]
        
        # تشخیص نوع لحن
        if any(word in tone_style for word in ["دوستانه", "راحت", "صمیمی"]):
            self.tone_preferences["formality"] = "غیررسمی"
            self.tone_preferences["style"] = "دوستانه"
        elif any(word in tone_style for word in ["رسمی", "محترمانه", "جدی"]):
            self.tone_preferences["formality"] = "رسمی"
            self.tone_preferences["style"] = "محترمانه"
        elif any(word in tone_style for word in ["شاد", "خوشحال", "انرژی"]):
            self.tone_preferences["mood"] = "شاد"
        
        self.tone_preferences["custom_style"] = tone_style
        self.tone_preferences["updated_at"] = datetime.now().isoformat()
        
        self._save_learning_data()
        
        response = f"باشه! از این به بعد لحنم {tone_style} می‌شه 🎭"
        
        print(f"🎭 لحن جدید یاد گرفته شد: {tone_style}")
        
        return {
            "learned": True,
            "type": "tone",
            "tone_style": tone_style,
            "response": response
        }
    
    def _learn_preference(self, analysis: Dict) -> Dict:
        """یادگیری ترجیحات عمومی"""
        preference = analysis["preference"]
        
        # دسته‌بندی ترجیحات
        if any(word in preference for word in ["کوتاه", "مختصر", "خلاصه"]):
            self.tone_preferences["response_length"] = "کوتاه"
        elif any(word in preference for word in ["بلند", "تفصیلی", "کامل"]):
            self.tone_preferences["response_length"] = "تفصیلی"
        elif any(word in preference for word in ["مثال", "نمونه"]):
            self.tone_preferences["include_examples"] = True
        
        self.tone_preferences["general_preference"] = preference
        self.tone_preferences["updated_at"] = datetime.now().isoformat()
        
        # ثبت در پروفایل ترجیحات
        self._update_profile_entry(
            category="preferences",
            key="general_preference",
            value=preference,
            confidence=analysis.get("confidence", 0.7),
            source="explicit",
            evidence=analysis.get("context", "")
        )
        
        self._save_learning_data()
        self._save_profile_data()
        
        response = f"فهمیدم! ترجیحت رو یادداشت کردم: {preference} ✅"
        
        print(f"✅ ترجیح جدید یاد گرفته شد: {preference}")
        
        return {
            "learned": True,
            "type": "preference",
            "preference": preference,
            "response": response
        }
    
    def apply_vocabulary_to_message(self, message: str) -> str:
        """اعمال واژگان شخصی به پیام"""
        processed_message = message
        
        for word, meaning in self.vocabulary.items():
            # جایگزینی کلمات (با در نظر گیری مرزهای کلمه)
            pattern = r'\b' + re.escape(word) + r'\b'
            processed_message = re.sub(pattern, meaning, processed_message, flags=re.IGNORECASE)
        
        return processed_message
    
    def get_active_rules_for_context(self, context: str) -> List[Dict]:
        """دریافت قوانین فعال برای context مشخص"""
        relevant_rules = []
        
        for rule in self.rules:
            if not rule.get("is_active", True):
                continue
            
            condition = rule["condition"].lower()
            context_lower = context.lower()
            
            # بررسی مطابقت شرط با context
            if condition == "همیشه" or any(word in context_lower for word in condition.split()):
                relevant_rules.append(rule)
        
        return relevant_rules
    
    def get_tone_preferences(self) -> Dict:
        """دریافت ترجیحات لحن"""
        return self.tone_preferences
    
    def get_profile_summary(self, max_items: int = 6) -> str:
        """خلاصه کوتاه از پروفایل کاربر برای prompt"""
        lines = []
        
        def _add_from_category(cat: str, title: str):
            items = list(self.profile.get(cat, {}).items())
            if not items:
                return
            for k, v in items[:max_items]:
                value = v.get("value", "")
                conf = v.get("confidence", 0.0)
                lines.append(f"- {title}: {value} (اعتماد: {conf:.2f})")
        
        _add_from_category("facts", "حقیقت")
        _add_from_category("preferences", "ترجیح")
        _add_from_category("habits", "عادت")
        _add_from_category("goals", "هدف")
        _add_from_category("skills", "مهارت")
        _add_from_category("dislikes", "عدم ترجیح")
        
        return "\n".join(lines[:max_items]) if lines else ""
    
    def get_learning_summary(self) -> Dict:
        """خلاصه یادگیری‌ها - بهبود یافته با ایده پرامپت"""
        passive_facts_count = len(getattr(self, 'passive_facts', []))
        profile_counts = {k: len(v) for k, v in self.profile.items()}
        
        return {
            "vocabulary_count": len(self.vocabulary),
            "rules_count": len(self.rules),
            "tone_preferences": self.tone_preferences,
            "passive_facts_count": passive_facts_count,  # اطلاعات یادگیری غیرمستقیم
            "profile_counts": profile_counts,
            "total_learning_events": len(self.learning_history),
            "recent_vocabulary": list(self.vocabulary.items())[-5:],
            "recent_rules": [rule["rule_text"] for rule in self.rules[-3:]],
            "learning_summary_text": self._generate_summary_text()  # متن خلاصه مثل پرامپت
        }
    
    def _generate_summary_text(self) -> str:
        """تولید متن خلاصه مثل مثال پرامپت"""
        vocab_count = len(self.vocabulary)
        rules_count = len(self.rules)
        total_events = len(self.learning_history)
        passive_count = len(getattr(self, 'passive_facts', []))
        
        summary = f"""از زمانی که باهم شروع کردیم، من یاد گرفتم:

📚 {vocab_count} واژه و اصطلاح شخصی تو
📋 {rules_count} قانون و ترجیح که همیشه رعایت می‌کنم
💬 {total_events} رویداد یادگیری داشتیم
🔍 {passive_count} اطلاعات شخصی از مکالمات استخراج کردم"""

        # اضافه کردن ترجیحات لحن
        if self.tone_preferences:
            if self.tone_preferences.get("style"):
                summary += f"\n🎯 لحن من رو تنظیم کردی که {self.tone_preferences['style']} باشه"
            if self.tone_preferences.get("response_length"):
                summary += f"\n⚙️ ترجیح می‌دی جواب‌ها {self.tone_preferences['response_length']} باشه"
        
        summary += "\n\nمی‌خوای جزئیات بیشتری ببینی؟"
        
        return summary
    
    def reset_learning(self):
        """ریست کردن تمام یادگیری‌ها"""
        self.vocabulary = {}
        self.rules = []
        self.tone_preferences = {}
        self.learning_history = []
        self.passive_facts = []
        self.profile = {
            "facts": {},
            "preferences": {},
            "habits": {},
            "goals": {},
            "skills": {},
            "dislikes": {},
            "social": {}
        }
        self._save_learning_data()
        self._save_profile_data()
        print("🔄 تمام یادگیری‌ها ریست شدند")
    
    def passive_learning_from_conversation(self, user_message: str, ai_response: str) -> Dict:
        """یادگیری غیرمستقیم از مکالمه - ایده از پرامپت"""
        learned_facts = []
        
        # استخراج اطلاعات شخصی کاربر
        personal_patterns = [
            (r"من (.+) هستم", "identity"),
            (r"من (.+) کار می‌کنم", "job"),
            (r"من (.+) دوست دارم", "interest"),
            (r"من در (.+) زندگی می‌کنم", "location"),
            (r"سن من (.+) است", "age"),
            (r"من (.+) تحصیل کردم", "education")
        ]
        
        for pattern, fact_type in personal_patterns:
            match = re.search(pattern, user_message.lower())
            if match:
                fact_value = match.group(1).strip()
                learned_facts.append({
                    "type": fact_type,
                    "value": fact_value,
                    "confidence": 0.8,
                    "source": "passive_learning"
                })
        
        # استخراج ترجیحات ضمنی
        if "خسته‌ام" in user_message.lower() or "کلافه‌ام" in user_message.lower():
            learned_facts.append({
                "type": "mood_pattern",
                "value": "needs_support_when_tired",
                "confidence": 0.6,
                "source": "mood_detection"
            })
        
        # ذخیره اطلاعات یادگیری شده
        if learned_facts:
            self._store_passive_learning(learned_facts)
        
        return {
            "facts_learned": len(learned_facts),
            "facts": learned_facts
        }
    
    def _store_passive_learning(self, facts: List[Dict]):
        """ذخیره یادگیری‌های غیرمستقیم"""
        if not hasattr(self, 'passive_facts'):
            self.passive_facts = []
        
        for fact in facts:
            fact['timestamp'] = datetime.now().isoformat()
            self.passive_facts.append(fact)
            
            # نگاشت یادگیری غیرمستقیم به پروفایل
            fact_type = fact.get("type")
            value = fact.get("value", "")
            if not value:
                continue
            
            if fact_type in ["identity", "job", "location", "age", "education"]:
                self._update_profile_entry(
                    category="facts",
                    key=fact_type,
                    value=value,
                    confidence=fact.get("confidence", 0.6),
                    source=fact.get("source", "passive"),
                    evidence=value
                )
            elif fact_type == "interest":
                self._update_profile_entry(
                    category="preferences",
                    key="interest",
                    value=value,
                    confidence=fact.get("confidence", 0.6),
                    source=fact.get("source", "passive"),
                    evidence=value
                )
            elif fact_type == "mood_pattern":
                self._update_profile_entry(
                    category="habits",
                    key="mood_pattern",
                    value=value,
                    confidence=fact.get("confidence", 0.5),
                    source=fact.get("source", "passive"),
                    evidence=value
                )
        
        # ذخیره در فایل
        self._save_learning_data()
        self._save_profile_data()
        
        print(f"🔍 یادگیری غیرمستقیم: {len(facts)} اطلاعات جدید")

# نمونه سراسری
personal_learning_system = PersonalLearningSystem()
