"""
🎯 مدیر Context هوشمند
تحلیل و مدیریت context مکالمه برای پاسخ‌های بهتر
"""

import json
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import re
from collections import defaultdict

class ContextType(Enum):
    CONVERSATION = "conversation"
    TOPIC = "topic"
    EMOTION = "emotion"
    TASK = "task"
    REFERENCE = "reference"

class ContextImportance(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

@dataclass
class ContextItem:
    id: str
    type: ContextType
    content: str
    importance: ContextImportance
    timestamp: datetime
    metadata: Dict
    expires_at: Optional[datetime] = None
    usage_count: int = 0

class ContextManager:
    def __init__(self):
        self.contexts = {}  # Dict[str, ContextItem]
        self.context_history = []  # List[str] - IDs مرتب شده
        self.topic_contexts = defaultdict(list)  # Dict[str, List[str]]
        self.active_contexts = []  # List[str] - context های فعال
        
        # تنظیمات
        self.max_contexts = 100
        self.max_active_contexts = 10
        self.default_context_ttl = timedelta(hours=2)
        
        # الگوهای تشخیص context
        self.context_patterns = {
            "question": [r"\?", r"چی", r"کی", r"کجا", r"چطور", r"چرا"],
            "request": [r"لطفا", r"می‌تونی", r"کمک", r"بگو", r"توضیح"],
            "emotion": [r"خوشحال", r"ناراحت", r"عصبانی", r"خسته", r"هیجان"],
            "reference": [r"این", r"آن", r"همون", r"قبلی", r"گفتی"]
        }
        
        print("🎯 Context Manager راه‌اندازی شد")
    
    def add_context(self, 
                   content: str, 
                   context_type: ContextType,
                   importance: ContextImportance = ContextImportance.MEDIUM,
                   metadata: Dict = None,
                   ttl: timedelta = None) -> str:
        """اضافه کردن context جدید"""
        
        context_id = f"{context_type.value}_{datetime.now().timestamp()}"
        ttl = ttl or self.default_context_ttl
        
        context_item = ContextItem(
            id=context_id,
            type=context_type,
            content=content,
            importance=importance,
            timestamp=datetime.now(),
            metadata=metadata or {},
            expires_at=datetime.now() + ttl
        )
        
        self.contexts[context_id] = context_item
        self.context_history.append(context_id)
        
        # اضافه کردن به topic contexts
        if context_type == ContextType.TOPIC:
            topic = metadata.get("topic", "general")
            self.topic_contexts[topic].append(context_id)
        
        # مدیریت اندازه
        self._manage_context_size()
        
        print(f"📝 Context اضافه شد: {context_type.value} - {content[:50]}...")
        return context_id
    
    def get_relevant_contexts(self, 
                            message: str, 
                            max_contexts: int = 5) -> List[ContextItem]:
        """دریافت context های مرتبط با پیام"""
        
        relevant_contexts = []
        message_lower = message.lower()
        
        # تحلیل پیام برای تشخیص نوع context مورد نیاز
        needed_types = self._analyze_message_context_needs(message)
        
        # جستجو در context های فعال
        for context_id in self.active_contexts:
            if context_id in self.contexts:
                context = self.contexts[context_id]
                
                # بررسی انقضا
                if context.expires_at and datetime.now() > context.expires_at:
                    continue
                
                # محاسبه امتیاز relevance
                relevance_score = self._calculate_relevance(message, context)
                
                if relevance_score > 0.3:  # threshold
                    relevant_contexts.append((context, relevance_score))
        
        # مرتب‌سازی بر اساس امتیاز و اهمیت
        relevant_contexts.sort(
            key=lambda x: (x[1], x[0].importance.value), 
            reverse=True
        )
        
        # برگرداندن بهترین context ها
        result = [ctx for ctx, score in relevant_contexts[:max_contexts]]
        
        # به‌روزرسانی usage_count
        for context in result:
            context.usage_count += 1
        
        return result
    
    def _analyze_message_context_needs(self, message: str) -> List[ContextType]:
        """تحلیل پیام برای تشخیص نیاز به انواع context"""
        needed_types = []
        message_lower = message.lower()
        
        # بررسی الگوها
        for pattern_type, patterns in self.context_patterns.items():
            for pattern in patterns:
                if re.search(pattern, message_lower):
                    if pattern_type == "reference":
                        needed_types.append(ContextType.REFERENCE)
                    elif pattern_type == "emotion":
                        needed_types.append(ContextType.EMOTION)
                    elif pattern_type in ["question", "request"]:
                        needed_types.append(ContextType.CONVERSATION)
                    break
        
        # همیشه conversation context نیاز است
        if ContextType.CONVERSATION not in needed_types:
            needed_types.append(ContextType.CONVERSATION)
        
        return needed_types
    
    def _calculate_relevance(self, message: str, context: ContextItem) -> float:
        """محاسبه امتیاز relevance بین پیام و context"""
        score = 0.0
        message_words = set(message.lower().split())
        context_words = set(context.content.lower().split())
        
        # شباهت کلمات
        if context_words and message_words:
            intersection = len(message_words & context_words)
            union = len(message_words | context_words)
            jaccard_similarity = intersection / union if union > 0 else 0
            score += jaccard_similarity * 0.4
        
        # امتیاز اهمیت
        importance_score = context.importance.value / 4.0
        score += importance_score * 0.3
        
        # امتیاز زمانی (context های جدیدتر امتیاز بیشتر)
        time_diff = datetime.now() - context.timestamp
        time_score = max(0, 1 - (time_diff.total_seconds() / 3600))  # کاهش در 1 ساعت
        score += time_score * 0.2
        
        # امتیاز استفاده (context های پراستفاده امتیاز بیشتر)
        usage_score = min(1.0, context.usage_count / 10.0)
        score += usage_score * 0.1
        
        return min(1.0, score)
    
    def update_active_contexts(self, message: str, response: str):
        """به‌روزرسانی context های فعال بعد از مکالمه"""
        
        # اضافه کردن پیام کاربر
        user_context_id = self.add_context(
            content=message,
            context_type=ContextType.CONVERSATION,
            importance=ContextImportance.MEDIUM,
            metadata={"role": "user"}
        )
        
        # اضافه کردن پاسخ AI
        ai_context_id = self.add_context(
            content=response,
            context_type=ContextType.CONVERSATION,
            importance=ContextImportance.MEDIUM,
            metadata={"role": "assistant"}
        )
        
        # به‌روزرسانی context های فعال
        self.active_contexts.extend([user_context_id, ai_context_id])
        
        # محدود کردن تعداد context های فعال
        if len(self.active_contexts) > self.max_active_contexts:
            # حذف قدیمی‌ترین context ها
            self.active_contexts = self.active_contexts[-self.max_active_contexts:]
        
        # تشخیص و اضافه کردن topic context
        self._extract_and_add_topic_context(message, response)
    
    def _extract_and_add_topic_context(self, message: str, response: str):
        """استخراج و اضافه کردن topic context"""
        
        # کلمات کلیدی برای تشخیص topic
        topic_keywords = {
            "برنامه‌نویسی": ["کد", "برنامه", "python", "javascript", "programming"],
            "هوش مصنوعی": ["ai", "هوش مصنوعی", "machine learning", "مدل"],
            "علم": ["علم", "فیزیک", "شیمی", "ریاضی", "science"],
            "فناوری": ["تکنولوژی", "فناوری", "technology", "کامپیوتر"],
            "سلامت": ["سلامت", "پزشکی", "درمان", "بیماری", "health"]
        }
        
        combined_text = f"{message} {response}".lower()
        
        for topic, keywords in topic_keywords.items():
            if any(keyword in combined_text for keyword in keywords):
                self.add_context(
                    content=f"بحث درباره {topic}: {message[:100]}...",
                    context_type=ContextType.TOPIC,
                    importance=ContextImportance.HIGH,
                    metadata={"topic": topic, "keywords": keywords}
                )
                break
    
    def _manage_context_size(self):
        """مدیریت اندازه context ها"""
        if len(self.contexts) > self.max_contexts:
            # حذف قدیمی‌ترین context ها
            sorted_contexts = sorted(
                self.contexts.items(),
                key=lambda x: (x[1].importance.value, x[1].timestamp),
                reverse=True
            )
            
            # نگه‌داری مهم‌ترین context ها
            keep_count = int(self.max_contexts * 0.8)
            contexts_to_keep = dict(sorted_contexts[:keep_count])
            
            # حذف context های اضافی
            removed_count = len(self.contexts) - len(contexts_to_keep)
            self.contexts = contexts_to_keep
            
            # به‌روزرسانی لیست‌های مرتبط
            self._cleanup_context_references()
            
            print(f"🗑️ {removed_count} context قدیمی حذف شد")
    
    def _cleanup_context_references(self):
        """پاک‌سازی ارجاعات context های حذف شده"""
        valid_ids = set(self.contexts.keys())
        
        # پاک‌سازی context_history
        self.context_history = [
            ctx_id for ctx_id in self.context_history 
            if ctx_id in valid_ids
        ]
        
        # پاک‌سازی active_contexts
        self.active_contexts = [
            ctx_id for ctx_id in self.active_contexts 
            if ctx_id in valid_ids
        ]
        
        # پاک‌سازی topic_contexts
        for topic in list(self.topic_contexts.keys()):
            self.topic_contexts[topic] = [
                ctx_id for ctx_id in self.topic_contexts[topic]
                if ctx_id in valid_ids
            ]
            
            # حذف topic های خالی
            if not self.topic_contexts[topic]:
                del self.topic_contexts[topic]
    
    def get_context_summary(self) -> Dict:
        """خلاصه وضعیت context ها"""
        now = datetime.now()
        
        # شمارش context ها بر اساس نوع
        type_counts = defaultdict(int)
        expired_count = 0
        
        for context in self.contexts.values():
            type_counts[context.type.value] += 1
            if context.expires_at and now > context.expires_at:
                expired_count += 1
        
        return {
            "total_contexts": len(self.contexts),
            "active_contexts": len(self.active_contexts),
            "expired_contexts": expired_count,
            "contexts_by_type": dict(type_counts),
            "topics": list(self.topic_contexts.keys()),
            "memory_usage": f"{len(self.contexts)} / {self.max_contexts}"
        }

# Instance سراسری
context_manager = ContextManager()