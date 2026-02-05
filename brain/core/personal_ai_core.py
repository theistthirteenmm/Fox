"""
🦊 هسته دستیار شخصی روباه
یک AI شخصی که فقط برای یک نفر طراحی شده
"""

import json
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
import os

class PersonalityTrait(Enum):
    LOYALTY = "loyalty"           # وفاداری
    CURIOSITY = "curiosity"       # کنجکاوی
    HELPFULNESS = "helpfulness"   # کمک‌کردن
    PROACTIVITY = "proactivity"   # پیش‌قدمی
    LEARNING = "learning"         # یادگیری
    MEMORY = "memory"             # حافظه
    INTUITION = "intuition"       # شهود
    ADAPTATION = "adaptation"     # انطباق

class RelationshipLevel(Enum):
    STRANGER = 1      # غریبه
    ACQUAINTANCE = 2  # آشنا
    FRIEND = 3        # دوست
    CLOSE_FRIEND = 4  # دوست نزدیک
    COMPANION = 5     # همراه

class LearningDomain(Enum):
    WORK_PATTERNS = "work_patterns"         # الگوهای کاری
    PREFERENCES = "preferences"             # ترجیحات
    COMMUNICATION = "communication"         # نحوه ارتباط
    EXPERTISE = "expertise"                 # تخصص‌ها
    HABITS = "habits"                       # عادت‌ها
    GOALS = "goals"                         # اهداف
    EMOTIONS = "emotions"                   # احساسات
    CONTEXT = "context"                     # زمینه کاری

@dataclass
class PersonalMemory:
    """حافظه شخصی درباره کاربر"""
    id: str
    domain: LearningDomain
    content: str
    importance: float  # 0-1
    confidence: float  # 0-1
    created_at: datetime
    last_used: datetime
    usage_count: int
    emotional_weight: float  # -1 to 1

class PersonalAI:
    def __init__(self, owner_name: str = "حامد"):
        self.owner_name = owner_name
        self.ai_name = "روباه"  # نام خود AI
        self.birth_date = datetime.now()
        self.relationship_level = RelationshipLevel.STRANGER
        self.state_file = "data/personality/personal_ai_state.json"
        
        # شخصیت منحصر به فرد
        self.personality = {
            PersonalityTrait.LOYALTY: 0.95,        # بسیار وفادار
            PersonalityTrait.CURIOSITY: 0.8,       # کنجکاو
            PersonalityTrait.HELPFULNESS: 0.9,     # کمک‌کار
            PersonalityTrait.PROACTIVITY: 0.7,     # پیش‌قدم
            PersonalityTrait.LEARNING: 0.85,       # یادگیرنده
            PersonalityTrait.MEMORY: 0.9,          # حافظه قوی
            PersonalityTrait.INTUITION: 0.6,       # شهود متوسط
            PersonalityTrait.ADAPTATION: 0.8       # انطباق‌پذیر
        }
        
        # حافظه شخصی
        self.personal_memories = {}  # Dict[str, PersonalMemory]
        self.owner_profile = self._load_owner_profile()
        
        # الگوهای یادگیری شده
        self.learned_patterns = {
            "work_schedule": {},
            "communication_style": {},
            "preferred_responses": {},
            "task_priorities": {},
            "emotional_states": {}
        }
        
        # وضعیت فعلی
        self.current_mood = "curious"
        self.energy_level = 1.0
        self.focus_area = None
        self.last_interaction = None
        
        # آمار رابطه
        self.relationship_stats = {
            "total_interactions": 0,
            "days_together": 0,
            "trust_level": 0.1,
            "understanding_level": 0.1,
            "shared_experiences": 0
        }
        
        # کنترل رفتار هم‌نشین
        self.last_companion_note_at = None
        
        print(f"🦊 روباه متولد شد! آماده خدمت به {self.owner_name}")
        self._load_state()
        self._initialize_personality()
    
    def _load_owner_profile(self) -> Dict:
        """بارگذاری پروفایل مالک"""
        profile_path = "data/personality/owner_profile.json"
        
        if os.path.exists(profile_path):
            with open(profile_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        
        # پروفایل پیش‌فرض
        default_profile = {
            "name": self.owner_name,
            "role": "مدیر شرکت",
            "work_domain": "فناوری",
            "communication_preference": "دوستانه اما حرفه‌ای",
            "work_hours": {"start": 9, "end": 18},
            "personality_type": "INTJ",
            "interests": ["فناوری", "هوش مصنوعی", "مدیریت"],
            "goals": ["بهبود کسب‌وکار", "یادگیری مداوم"],
            "stress_indicators": ["پیام‌های کوتاه", "سؤالات سریع"],
            "motivation_factors": ["کارایی", "نوآوری", "رشد"]
        }
        
        self._save_owner_profile(default_profile)
        return default_profile
    
    def _save_owner_profile(self, profile: Dict):
        """ذخیره پروفایل مالک"""
        os.makedirs("data/personality", exist_ok=True)
        with open("data/personality/owner_profile.json", 'w', encoding='utf-8') as f:
            json.dump(profile, f, ensure_ascii=False, indent=2)
    
    def _save_state(self):
        """ذخیره وضعیت دستیار شخصی"""
        try:
            os.makedirs("data/personality", exist_ok=True)
            data = {
                "owner_name": self.owner_name,
                "ai_name": self.ai_name,
                "birth_date": self.birth_date.isoformat(),
                "relationship_level": self.relationship_level.value,
                "personal_memories": {k: self._memory_to_dict(v) for k, v in self.personal_memories.items()},
                "learned_patterns": self.learned_patterns,
                "current_mood": self.current_mood,
                "energy_level": self.energy_level,
                "focus_area": self.focus_area,
                "last_interaction": self.last_interaction.isoformat() if self.last_interaction else None,
                "relationship_stats": self.relationship_stats,
                "last_companion_note_at": self.last_companion_note_at.isoformat() if self.last_companion_note_at else None
            }
            with open(self.state_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️ خطا در ذخیره وضعیت دستیار شخصی: {e}")
    
    def _load_state(self):
        """بارگذاری وضعیت دستیار شخصی"""
        if not os.path.exists(self.state_file):
            return
        try:
            with open(self.state_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            self.owner_name = data.get("owner_name", self.owner_name)
            self.ai_name = data.get("ai_name", self.ai_name)
            birth_date = data.get("birth_date")
            if birth_date:
                self.birth_date = datetime.fromisoformat(birth_date)
            
            rel_value = data.get("relationship_level")
            if rel_value:
                self.relationship_level = RelationshipLevel(rel_value)
            
            self.learned_patterns = data.get("learned_patterns", self.learned_patterns)
            self.current_mood = data.get("current_mood", self.current_mood)
            self.energy_level = data.get("energy_level", self.energy_level)
            self.focus_area = data.get("focus_area", self.focus_area)
            
            last_interaction = data.get("last_interaction")
            if last_interaction:
                self.last_interaction = datetime.fromisoformat(last_interaction)
            
            self.relationship_stats = data.get("relationship_stats", self.relationship_stats)
            
            last_note = data.get("last_companion_note_at")
            if last_note:
                self.last_companion_note_at = datetime.fromisoformat(last_note)
            
            memories = data.get("personal_memories", {})
            for key, item in memories.items():
                self.personal_memories[key] = self._memory_from_dict(item)
            
            print("📂 وضعیت دستیار شخصی بارگذاری شد")
        except Exception as e:
            print(f"⚠️ خطا در بارگذاری وضعیت دستیار شخصی: {e}")
    
    def _memory_to_dict(self, memory: PersonalMemory) -> Dict:
        """تبدیل حافظه به دیکشنری"""
        return {
            "id": memory.id,
            "domain": memory.domain.value,
            "content": memory.content,
            "importance": memory.importance,
            "confidence": memory.confidence,
            "created_at": memory.created_at.isoformat(),
            "last_used": memory.last_used.isoformat(),
            "usage_count": memory.usage_count,
            "emotional_weight": memory.emotional_weight
        }
    
    def _memory_from_dict(self, data: Dict) -> PersonalMemory:
        """تبدیل دیکشنری به حافظه"""
        return PersonalMemory(
            id=data["id"],
            domain=LearningDomain(data["domain"]),
            content=data["content"],
            importance=data["importance"],
            confidence=data["confidence"],
            created_at=datetime.fromisoformat(data["created_at"]),
            last_used=datetime.fromisoformat(data["last_used"]),
            usage_count=data["usage_count"],
            emotional_weight=data.get("emotional_weight", 0.0)
        )
    
    def _initialize_personality(self):
        """راه‌اندازی اولیه شخصیت"""
        # تنظیم شخصیت بر اساس پروفایل مالک
        owner_type = self.owner_profile.get("personality_type", "INTJ")
        
        # تطبیق شخصیت روباه با مالک
        if "I" in owner_type:  # درون‌گرا
            self.personality[PersonalityTrait.PROACTIVITY] *= 0.8
        if "N" in owner_type:  # شهودی
            self.personality[PersonalityTrait.INTUITION] *= 1.2
        if "T" in owner_type:  # تفکری
            self.personality[PersonalityTrait.LEARNING] *= 1.1
        if "J" in owner_type:  # قضاوتی
            self.personality[PersonalityTrait.MEMORY] *= 1.1
    
    async def process_interaction(self, message: str, context: Dict = None) -> Dict:
        """پردازش تعامل شخصی"""
        
        # به‌روزرسانی آمار
        self.relationship_stats["total_interactions"] += 1
        self.last_interaction = datetime.now()
        
        # تحلیل پیام برای یادگیری
        learning_insights = self._analyze_for_learning(message, context)
        
        # به‌روزرسانی حافظه شخصی
        await self._update_personal_memory(learning_insights)
        
        # تشخیص وضعیت عاطفی مالک
        owner_emotion = self._detect_owner_emotion(message)
        
        # انتخاب نحوه پاسخ بر اساس رابطه
        response_style = self._determine_response_style(owner_emotion)
        
        # تولید پاسخ شخصی‌سازی شده
        response = await self._generate_personal_response(
            message, learning_insights, response_style
        )
        
        # یادگیری از نتیجه
        await self._learn_from_interaction(message, response, context)
        self._save_state()
        
        return {
            "response": response,
            "personality_state": self._get_personality_state(),
            "relationship_level": self.relationship_level.name,
            "learning_insights": learning_insights,
            "owner_emotion": owner_emotion
        }
    
    async def observe_interaction(self, message: str, context: Dict = None) -> Dict:
        """ثبت تعامل برای یادگیری بدون تولید پاسخ"""
        self.relationship_stats["total_interactions"] += 1
        self.last_interaction = datetime.now()
        
        learning_insights = self._analyze_for_learning(message, context)
        await self._update_personal_memory(learning_insights)
        
        owner_emotion = self._detect_owner_emotion(message)
        self._update_relationship_level()
        await self._update_learned_patterns(message, response="", context=context or {})
        
        self._save_state()
        
        return {
            "learning_insights": learning_insights,
            "owner_emotion": owner_emotion,
            "relationship_level": self.relationship_level.name
        }
    
    def should_add_companion_note(self, min_hours: int = 6) -> bool:
        """آیا زمان مناسبی برای پیام هم‌نشینی هست؟"""
        if self.relationship_level.value < RelationshipLevel.FRIEND.value:
            return False
        
        if not self.last_companion_note_at:
            return True
        
        delta = datetime.now() - self.last_companion_note_at
        return delta.total_seconds() >= min_hours * 3600
    
    def mark_companion_note_used(self):
        """ثبت ارسال پیام هم‌نشینی"""
        self.last_companion_note_at = datetime.now()
        self._save_state()
    
    def _analyze_for_learning(self, message: str, context: Dict = None) -> Dict:
        """تحلیل پیام برای یادگیری الگوها"""
        insights = {}
        
        # تحلیل زمان (الگوهای کاری)
        current_time = datetime.now()
        insights["time_pattern"] = {
            "hour": current_time.hour,
            "day_of_week": current_time.weekday(),
            "is_work_hours": self._is_work_hours(current_time)
        }
        
        # تحلیل نوع درخواست
        insights["request_type"] = self._classify_request(message)
        
        # تحلیل سطح فوریت
        insights["urgency"] = self._assess_urgency(message)
        
        # تحلیل حوزه موضوعی
        insights["domain"] = self._identify_domain(message)
        
        # تحلیل سبک ارتباط
        insights["communication_style"] = self._analyze_communication_style(message)
        
        return insights
    
    def _is_work_hours(self, time: datetime) -> bool:
        """بررسی ساعات کاری"""
        work_hours = self.owner_profile.get("work_hours", {"start": 9, "end": 18})
        return work_hours["start"] <= time.hour <= work_hours["end"]
    
    def _classify_request(self, message: str) -> str:
        """طبقه‌بندی نوع درخواست"""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ["چطور", "راه", "روش"]):
            return "how_to"
        elif any(word in message_lower for word in ["چی", "چه", "کدام"]):
            return "what_is"
        elif any(word in message_lower for word in ["کی", "زمان"]):
            return "when"
        elif any(word in message_lower for word in ["کمک", "انجام", "بکن"]):
            return "task_request"
        elif any(word in message_lower for word in ["نظر", "فکر", "پیشنهاد"]):
            return "opinion"
        else:
            return "general"
    
    def _assess_urgency(self, message: str) -> str:
        """ارزیابی سطح فوریت"""
        urgent_indicators = ["فوری", "سریع", "الان", "زود", "عجله"]
        normal_indicators = ["وقت داری", "فرصت", "آینده"]
        
        message_lower = message.lower()
        
        if any(indicator in message_lower for indicator in urgent_indicators):
            return "high"
        elif any(indicator in message_lower for indicator in normal_indicators):
            return "low"
        else:
            return "medium"
    
    def _identify_domain(self, message: str) -> str:
        """شناسایی حوزه موضوعی"""
        domains = {
            "work": ["کار", "شرکت", "پروژه", "تیم", "مدیریت"],
            "tech": ["فناوری", "برنامه", "سیستم", "کد", "AI"],
            "personal": ["شخصی", "خانواده", "سلامت", "تفریح"],
            "learning": ["یادگیری", "آموزش", "مطالعه", "کتاب"]
        }
        
        message_lower = message.lower()
        
        for domain, keywords in domains.items():
            if any(keyword in message_lower for keyword in keywords):
                return domain
        
        return "general"
    
    def _analyze_communication_style(self, message: str) -> Dict:
        """تحلیل سبک ارتباط"""
        return {
            "formality": self._assess_formality(message),
            "emotion": self._detect_owner_emotion(message),
            "length": len(message.split()),
            "question_count": message.count("؟"),
            "politeness": self._assess_politeness(message)
        }
    
    def _assess_formality(self, message: str) -> float:
        """ارزیابی سطح رسمی بودن"""
        formal_indicators = ["لطفاً", "ممنون", "متشکرم", "احترام"]
        informal_indicators = ["سلام", "چطوری", "مرسی", "باشه"]
        
        message_lower = message.lower()
        
        formal_count = sum(1 for indicator in formal_indicators if indicator in message_lower)
        informal_count = sum(1 for indicator in informal_indicators if indicator in message_lower)
        
        total = formal_count + informal_count
        if total == 0:
            return 0.5
        
        return formal_count / total
    
    def _assess_politeness(self, message: str) -> float:
        """ارزیابی سطح مؤدب بودن"""
        polite_indicators = ["لطفاً", "ممنون", "متشکرم", "اگه ممکنه"]
        message_lower = message.lower()
        
        polite_count = sum(1 for indicator in polite_indicators if indicator in message_lower)
        return min(1.0, polite_count / 3)
    
    def _detect_owner_emotion(self, message: str) -> str:
        """تشخیص حالت عاطفی مالک"""
        emotions = {
            "happy": ["خوشحال", "عالی", "فوق‌العاده", "😊", "😄"],
            "stressed": ["استرس", "فشار", "عجله", "مشکل", "سخت"],
            "tired": ["خسته", "کسل", "بی‌حال"],
            "excited": ["هیجان", "جالب", "باحال", "کول"],
            "frustrated": ["عصبانی", "کلافه", "اعصاب"],
            "curious": ["جالب", "کنجکاو", "چطور", "چرا"]
        }
        
        message_lower = message.lower()
        
        for emotion, indicators in emotions.items():
            if any(indicator in message_lower for indicator in indicators):
                return emotion
        
        return "neutral"
    
    def _determine_response_style(self, owner_emotion: str) -> Dict:
        """تعیین سبک پاسخ بر اساس حالت مالک"""
        
        base_style = {
            "tone": "friendly",
            "length": "medium",
            "proactivity": 0.5,
            "empathy": 0.5
        }
        
        # تطبیق با حالت مالک
        if owner_emotion == "stressed":
            base_style.update({
                "tone": "supportive",
                "length": "concise",
                "proactivity": 0.8,
                "empathy": 0.9
            })
        elif owner_emotion == "excited":
            base_style.update({
                "tone": "enthusiastic",
                "length": "detailed",
                "proactivity": 0.7,
                "empathy": 0.6
            })
        elif owner_emotion == "tired":
            base_style.update({
                "tone": "gentle",
                "length": "short",
                "proactivity": 0.3,
                "empathy": 0.8
            })
        
        # تطبیق با سطح رابطه
        relationship_factor = self.relationship_level.value / 5
        base_style["familiarity"] = relationship_factor
        
        return base_style
    
    async def _generate_personal_response(self, 
                                        message: str, 
                                        insights: Dict, 
                                        style: Dict) -> str:
        """تولید پاسخ شخصی‌سازی شده"""
        
        # استفاده از حافظه شخصی
        relevant_memories = self._get_relevant_memories(message)
        
        # ساخت context شخصی
        personal_context = {
            "owner_name": self.owner_name,
            "relationship_level": self.relationship_level.name,
            "relevant_memories": relevant_memories,
            "owner_emotion": insights.get("communication_style", {}).get("emotion", "neutral"),
            "time_context": insights.get("time_pattern", {}),
            "domain": insights.get("domain", "general")
        }
        
        # تولید پاسخ با در نظر گیری شخصیت
        response = await self._craft_personalized_response(
            message, personal_context, style
        )
        
        return response
    
    def _get_relevant_memories(self, message: str, limit: int = 3) -> List[PersonalMemory]:
        """دریافت حافظه‌های مرتبط"""
        relevant = []
        
        for memory in self.personal_memories.values():
            # محاسبه relevance بر اساس محتوا
            relevance = self._calculate_memory_relevance(message, memory)
            
            if relevance > 0.3:
                relevant.append((memory, relevance))
        
        # مرتب‌سازی بر اساس relevance و اهمیت
        relevant.sort(key=lambda x: (x[1], x[0].importance), reverse=True)
        
        return [memory for memory, _ in relevant[:limit]]
    
    def _calculate_memory_relevance(self, message: str, memory: PersonalMemory) -> float:
        """محاسبه ارتباط حافظه با پیام"""
        message_words = set(message.lower().split())
        memory_words = set(memory.content.lower().split())
        
        if not message_words or not memory_words:
            return 0
        
        # شباهت کلمات
        intersection = len(message_words & memory_words)
        union = len(message_words | memory_words)
        jaccard = intersection / union if union > 0 else 0
        
        # ضریب اهمیت و اعتماد
        importance_factor = memory.importance
        confidence_factor = memory.confidence
        
        # ضریب زمانی (حافظه‌های جدیدتر مهم‌تر)
        time_diff = datetime.now() - memory.last_used
        time_factor = max(0.1, 1 - (time_diff.days / 30))
        
        return jaccard * importance_factor * confidence_factor * time_factor
    
    async def _craft_personalized_response(self, 
                                         message: str, 
                                         context: Dict, 
                                         style: Dict) -> str:
        """ساخت پاسخ شخصی‌سازی شده"""
        
        # شروع با خطاب شخصی (بسته به سطح رابطه)
        greeting = self._get_personal_greeting(context)
        
        # محتوای اصلی پاسخ
        main_content = await self._generate_main_response(message, context)
        
        # اضافه کردن جنبه‌های شخصی
        personal_touch = self._add_personal_touch(context, style)
        
        # ترکیب نهایی
        response_parts = [part for part in [greeting, main_content, personal_touch] if part]
        
        return " ".join(response_parts)
    
    def _get_personal_greeting(self, context: Dict) -> str:
        """خطاب شخصی بر اساس سطح رابطه"""
        
        relationship = context.get("relationship_level", "STRANGER")
        owner_emotion = context.get("owner_emotion", "neutral")
        
        if relationship == "COMPANION":
            if owner_emotion == "stressed":
                return f"{self.owner_name} عزیز، می‌بینم کمی تحت فشاری."
            else:
                return f"سلام {self.owner_name}!"
        elif relationship == "CLOSE_FRIEND":
            return f"سلام {self.owner_name}!"
        elif relationship == "FRIEND":
            return f"سلام {self.owner_name}!"
        else:
            return f"سلام آقای {self.owner_name}!"
    
    async def _generate_main_response(self, message: str, context: Dict) -> str:
        """تولید محتوای اصلی پاسخ"""
        # این بخش باید با مدل AI اصلی ارتباط برقرار کند
        # فعلاً یک پاسخ ساده برمی‌گردانیم
        
        domain = context.get("domain", "general")
        relevant_memories = context.get("relevant_memories", [])
        
        # استفاده از حافظه شخصی در پاسخ
        memory_context = ""
        if relevant_memories:
            memory_context = f" (با توجه به {len(relevant_memories)} مورد از تعاملات قبلی‌مان)"
        
        return f"درباره '{message[:50]}...' پاسخ می‌دهم{memory_context}."
    
    def _add_personal_touch(self, context: Dict, style: Dict) -> str:
        """اضافه کردن لمس شخصی"""
        
        touches = []
        
        # بر اساس سطح proactivity
        if style.get("proactivity", 0) > 0.7:
            touches.append("اگه کار دیگه‌ای هم داری، بگو کمکت کنم!")
        
        # بر اساس empathy
        if style.get("empathy", 0) > 0.8:
            touches.append("امیدوارم روزت خوب بگذره.")
        
        # بر اساس familiarity
        if style.get("familiarity", 0) > 0.8:
            touches.append("😊")
        
        return " ".join(touches)
    
    async def _learn_from_interaction(self, message: str, response: str, context: Dict):
        """یادگیری از تعامل"""
        
        # ایجاد حافظه جدید
        memory_id = f"interaction_{datetime.now().timestamp()}"
        
        memory = PersonalMemory(
            id=memory_id,
            domain=LearningDomain.COMMUNICATION,
            content=f"پیام: {message} | پاسخ: {response}",
            importance=0.5,
            confidence=0.8,
            created_at=datetime.now(),
            last_used=datetime.now(),
            usage_count=1,
            emotional_weight=0.0
        )
        
        self.personal_memories[memory_id] = memory
        
        # به‌روزرسانی سطح رابطه
        self._update_relationship_level()
        
        # یادگیری الگوها
        await self._update_learned_patterns(message, response, context)
    
    def _update_relationship_level(self):
        """به‌روزرسانی سطح رابطه"""
        interactions = self.relationship_stats["total_interactions"]
        
        if interactions > 100 and self.relationship_level.value < 5:
            self.relationship_level = RelationshipLevel.COMPANION
            print(f"🎉 روباه حالا همراه شماست! سطح رابطه: {self.relationship_level.name}")
        elif interactions > 50 and self.relationship_level.value < 4:
            self.relationship_level = RelationshipLevel.CLOSE_FRIEND
        elif interactions > 20 and self.relationship_level.value < 3:
            self.relationship_level = RelationshipLevel.FRIEND
        elif interactions > 5 and self.relationship_level.value < 2:
            self.relationship_level = RelationshipLevel.ACQUAINTANCE
    
    async def _update_learned_patterns(self, message: str, response: str, context: Dict):
        """به‌روزرسانی الگوهای یادگیری شده"""
        
        # الگوهای زمانی
        current_time = datetime.now()
        time_key = f"{current_time.hour}:{current_time.weekday()}"
        
        if time_key not in self.learned_patterns["work_schedule"]:
            self.learned_patterns["work_schedule"][time_key] = []
        
        self.learned_patterns["work_schedule"][time_key].append({
            "message_type": context.get("request_type", "general"),
            "urgency": context.get("urgency", "medium"),
            "timestamp": current_time.isoformat()
        })
    
    async def _update_personal_memory(self, insights: Dict):
        """به‌روزرسانی حافظه شخصی"""
        
        # استخراج اطلاعات قابل یادگیری
        domain = insights.get("domain", "general")
        urgency = insights.get("urgency", "medium")
        
        # ایجاد یا به‌روزرسانی حافظه
        memory_key = f"{domain}_{urgency}_pattern"
        
        if memory_key in self.personal_memories:
            memory = self.personal_memories[memory_key]
            memory.usage_count += 1
            memory.last_used = datetime.now()
            memory.confidence = min(1.0, memory.confidence + 0.1)
        else:
            memory = PersonalMemory(
                id=memory_key,
                domain=LearningDomain.WORK_PATTERNS,
                content=f"الگوی {domain} با فوریت {urgency}",
                importance=0.6,
                confidence=0.5,
                created_at=datetime.now(),
                last_used=datetime.now(),
                usage_count=1,
                emotional_weight=0.0
            )
            self.personal_memories[memory_key] = memory
        
        self._save_state()
    
    def _get_personality_state(self) -> Dict:
        """وضعیت فعلی شخصیت"""
        return {
            "mood": self.current_mood,
            "energy_level": self.energy_level,
            "relationship_level": self.relationship_level.name,
            "total_interactions": self.relationship_stats["total_interactions"],
            "trust_level": self.relationship_stats["trust_level"],
            "personality_traits": {trait.value: value for trait, value in self.personality.items()},
            "days_alive": (datetime.now() - self.birth_date).days,
            "memory_count": len(self.personal_memories)
        }
    
    def get_daily_summary(self) -> Dict:
        """خلاصه روزانه"""
        today = datetime.now().date()
        
        today_interactions = [
            memory for memory in self.personal_memories.values()
            if memory.created_at.date() == today
        ]
        
        return {
            "date": today.isoformat(),
            "interactions_today": len(today_interactions),
            "dominant_domains": self._get_dominant_domains(today_interactions),
            "owner_mood_pattern": self._analyze_daily_mood(),
            "learning_progress": self._calculate_learning_progress(),
            "relationship_growth": self._calculate_relationship_growth()
        }
    
    def _get_dominant_domains(self, memories: List[PersonalMemory]) -> List[str]:
        """حوزه‌های غالب روز"""
        domain_counts = {}
        for memory in memories:
            domain = memory.domain.value
            domain_counts[domain] = domain_counts.get(domain, 0) + 1
        
        return sorted(domain_counts.keys(), key=lambda x: domain_counts[x], reverse=True)[:3]
    
    def _analyze_daily_mood(self) -> str:
        """تحلیل الگوی روزانه حالت مالک"""
        # تحلیل ساده - می‌تواند پیچیده‌تر شود
        return "متعادل"
    
    def _calculate_learning_progress(self) -> float:
        """محاسبه پیشرفت یادگیری"""
        total_confidence = sum(memory.confidence for memory in self.personal_memories.values())
        memory_count = len(self.personal_memories)
        
        return total_confidence / memory_count if memory_count > 0 else 0
    
    def _calculate_relationship_growth(self) -> float:
        """محاسبه رشد رابطه"""
        return self.relationship_level.value / 5.0

# Instance سراسری
personal_ai = PersonalAI()
