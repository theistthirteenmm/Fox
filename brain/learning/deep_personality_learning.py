"""
🧬 سیستم یادگیری عمیق شخصیت روباه
تحلیل و یادگیری عمیق از رفتار و ترجیحات مالک
"""

import json
import asyncio
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from enum import Enum
import numpy as np
from collections import defaultdict, Counter
import re

class PersonalityDimension(Enum):
    COMMUNICATION_STYLE = "communication_style"
    DECISION_MAKING = "decision_making"
    STRESS_RESPONSE = "stress_response"
    LEARNING_PREFERENCE = "learning_preference"
    WORK_STYLE = "work_style"
    SOCIAL_INTERACTION = "social_interaction"
    PROBLEM_SOLVING = "problem_solving"
    TIME_MANAGEMENT = "time_management"

class LearningConfidence(Enum):
    UNCERTAIN = 0.2
    LOW = 0.4
    MEDIUM = 0.6
    HIGH = 0.8
    VERY_HIGH = 0.9

@dataclass
class PersonalityInsight:
    dimension: PersonalityDimension
    insight: str
    confidence: float
    evidence: List[str]
    discovered_at: datetime
    reinforcement_count: int
    last_observed: datetime

@dataclass
class BehaviorPattern:
    pattern_id: str
    description: str
    triggers: List[str]
    responses: List[str]
    frequency: int
    reliability: float
    context: Dict[str, Any]

class DeepPersonalityLearning:
    def __init__(self, owner_name: str = "حامد"):
        self.owner_name = owner_name
        self.state_file = "data/personality/deep_personality.json"
        
        # بینش‌های شخصیتی
        self.personality_insights = {}
        self.behavior_patterns = {}
        self.preference_map = defaultdict(dict)
        
        # تحلیل زبان و ارتباط
        self.communication_analysis = {
            "vocabulary_preferences": Counter(),
            "sentence_patterns": [],
            "emotional_expressions": {},
            "formality_levels": [],
            "response_preferences": {}
        }
        
        # الگوهای تصمیم‌گیری
        self.decision_patterns = {
            "decision_speed": [],  # سریع یا آهسته
            "information_need": [],  # کم یا زیاد اطلاعات
            "risk_tolerance": [],  # محافظه‌کار یا ریسک‌پذیر
            "consultation_tendency": []  # مستقل یا مشورتی
        }
        
        # الگوهای یادگیری
        self.learning_patterns = {
            "preferred_formats": Counter(),  # متن، صوت، تصویر
            "detail_level": [],  # خلاصه یا تفصیلی
            "example_preference": [],  # نظری یا عملی
            "feedback_style": []  # مستقیم یا غیرمستقیم
        }
        
        # تحلیل استرس و احساسات
        self.emotional_patterns = {
            "stress_indicators": [],
            "motivation_factors": [],
            "energy_cycles": {},
            "mood_triggers": {}
        }
        
        self._load_state()
        print("🧬 سیستم یادگیری عمیق شخصیت راه‌اندازی شد")
    
    async def analyze_interaction(self, message: str, context: Dict, response: str) -> Dict:
        """تحلیل عمیق تعامل"""
        
        analysis_results = {}
        
        # 1. تحلیل سبک ارتباط
        comm_analysis = await self._analyze_communication_style(message, context)
        analysis_results["communication"] = comm_analysis
        
        # 2. تحلیل الگوهای تصمیم‌گیری
        decision_analysis = await self._analyze_decision_patterns(message, context)
        analysis_results["decision_making"] = decision_analysis
        
        # 3. تحلیل ترجیحات یادگیری
        learning_analysis = await self._analyze_learning_preferences(message, response)
        analysis_results["learning"] = learning_analysis
        
        # 4. تحلیل وضعیت عاطفی
        emotional_analysis = await self._analyze_emotional_state(message, context)
        analysis_results["emotional"] = emotional_analysis
        
        # 5. شناسایی الگوهای رفتاری جدید
        new_patterns = await self._identify_behavior_patterns(message, context, response)
        analysis_results["new_patterns"] = new_patterns
        
        # 6. به‌روزرسانی بینش‌های شخصیتی
        await self._update_personality_insights(analysis_results)
        self._save_state()
        
        return analysis_results
    
    def _save_state(self):
        """ذخیره وضعیت یادگیری عمیق"""
        try:
            os.makedirs("data/personality", exist_ok=True)
            data = {
                "owner_name": self.owner_name,
                "personality_insights": self._serialize_insights(),
                "behavior_patterns": self._serialize_patterns(),
                "communication_analysis": self.communication_analysis,
                "decision_patterns": self.decision_patterns,
                "learning_patterns": self.learning_patterns,
                "emotional_patterns": self.emotional_patterns
            }
            with open(self.state_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2, default=str)
        except Exception as e:
            print(f"⚠️ خطا در ذخیره وضعیت یادگیری عمیق: {e}")
    
    def _load_state(self):
        """بارگذاری وضعیت یادگیری عمیق"""
        if not os.path.exists(self.state_file):
            return
        try:
            with open(self.state_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            
            self.owner_name = data.get("owner_name", self.owner_name)
            self.communication_analysis = data.get("communication_analysis", self.communication_analysis)
            self.decision_patterns = data.get("decision_patterns", self.decision_patterns)
            self.learning_patterns = data.get("learning_patterns", self.learning_patterns)
            self.emotional_patterns = data.get("emotional_patterns", self.emotional_patterns)
            
            # بازسازی insights
            insights = data.get("personality_insights", {})
            for key, item in insights.items():
                self.personality_insights[key] = PersonalityInsight(
                    dimension=PersonalityDimension(item["dimension"]),
                    insight=item["insight"],
                    confidence=item["confidence"],
                    evidence=item["evidence"],
                    discovered_at=datetime.fromisoformat(item["discovered_at"]),
                    reinforcement_count=item["reinforcement_count"],
                    last_observed=datetime.fromisoformat(item["last_observed"])
                )
            
            # بازسازی patterns
            patterns = data.get("behavior_patterns", {})
            for key, item in patterns.items():
                self.behavior_patterns[key] = BehaviorPattern(
                    pattern_id=item["pattern_id"],
                    description=item["description"],
                    triggers=item["triggers"],
                    responses=item["responses"],
                    frequency=item["frequency"],
                    reliability=item["reliability"],
                    context=item["context"]
                )
            
            print("📂 وضعیت یادگیری عمیق بارگذاری شد")
        except Exception as e:
            print(f"⚠️ خطا در بارگذاری یادگیری عمیق: {e}")
    
    def _serialize_insights(self) -> Dict:
        """سریال‌سازی بینش‌ها"""
        result = {}
        for key, insight in self.personality_insights.items():
            result[key] = {
                "dimension": insight.dimension.value,
                "insight": insight.insight,
                "confidence": insight.confidence,
                "evidence": insight.evidence,
                "discovered_at": insight.discovered_at.isoformat(),
                "reinforcement_count": insight.reinforcement_count,
                "last_observed": insight.last_observed.isoformat()
            }
        return result
    
    def _serialize_patterns(self) -> Dict:
        """سریال‌سازی الگوهای رفتاری"""
        result = {}
        for key, pattern in self.behavior_patterns.items():
            result[key] = {
                "pattern_id": pattern.pattern_id,
                "description": pattern.description,
                "triggers": pattern.triggers,
                "responses": pattern.responses,
                "frequency": pattern.frequency,
                "reliability": pattern.reliability,
                "context": pattern.context
            }
        return result
    
    async def _analyze_communication_style(self, message: str, context: Dict) -> Dict:
        """تحلیل سبک ارتباط"""
        
        analysis = {}
        
        # تحلیل طول پیام
        word_count = len(message.split())
        analysis["message_length"] = "short" if word_count < 10 else "medium" if word_count < 30 else "long"
        
        # تحلیل رسمی بودن
        formal_indicators = ["لطفاً", "ممنون", "متشکرم", "احترام", "سپاس"]
        informal_indicators = ["سلام", "چطوری", "مرسی", "باشه", "اوکی"]
        
        formal_count = sum(1 for indicator in formal_indicators if indicator in message.lower())
        informal_count = sum(1 for indicator in informal_indicators if indicator in message.lower())
        
        if formal_count > informal_count:
            analysis["formality"] = "formal"
        elif informal_count > formal_count:
            analysis["formality"] = "informal"
        else:
            analysis["formality"] = "neutral"
        
        # تحلیل مستقیم بودن
        direct_indicators = ["بگو", "انجام بده", "می‌خوام", "باید"]
        indirect_indicators = ["ممکنه", "اگه میشه", "بهتره", "چطور است"]
        
        direct_count = sum(1 for indicator in direct_indicators if indicator in message.lower())
        indirect_count = sum(1 for indicator in indirect_indicators if indicator in message.lower())
        
        analysis["directness"] = "direct" if direct_count > indirect_count else "indirect"
        
        # تحلیل احساسات در ارتباط
        emotional_words = {
            "positive": ["خوب", "عالی", "فوق‌العاده", "خوشحال", "راضی"],
            "negative": ["بد", "ناراحت", "عصبانی", "مشکل", "سخت"],
            "neutral": ["معمولی", "متوسط", "نرمال"]
        }
        
        for emotion_type, words in emotional_words.items():
            if any(word in message.lower() for word in words):
                analysis["emotional_tone"] = emotion_type
                break
        else:
            analysis["emotional_tone"] = "neutral"
        
        # به‌روزرسانی آمار
        self.communication_analysis["formality_levels"].append(analysis["formality"])
        
        return analysis
    
    async def _analyze_decision_patterns(self, message: str, context: Dict) -> Dict:
        """تحلیل الگوهای تصمیم‌گیری"""
        
        analysis = {}
        
        # تشخیص درخواست تصمیم‌گیری
        decision_indicators = ["انتخاب", "تصمیم", "کدام", "بهتر", "پیشنهاد", "نظر"]
        
        if any(indicator in message.lower() for indicator in decision_indicators):
            analysis["involves_decision"] = True
            
            # تحلیل سرعت تصمیم‌گیری
            urgency_indicators = ["سریع", "فوری", "الان", "زود"]
            deliberation_indicators = ["فکر", "بررسی", "مطالعه", "زمان"]
            
            if any(indicator in message.lower() for indicator in urgency_indicators):
                analysis["decision_speed"] = "fast"
            elif any(indicator in message.lower() for indicator in deliberation_indicators):
                analysis["decision_speed"] = "deliberate"
            else:
                analysis["decision_speed"] = "normal"
            
            # تحلیل نیاز به اطلاعات
            info_request_indicators = ["جزئیات", "اطلاعات", "توضیح", "چطور", "چرا"]
            
            if any(indicator in message.lower() for indicator in info_request_indicators):
                analysis["information_need"] = "high"
            else:
                analysis["information_need"] = "low"
            
            # به‌روزرسانی الگوها
            self.decision_patterns["decision_speed"].append(analysis.get("decision_speed", "normal"))
            self.decision_patterns["information_need"].append(analysis.get("information_need", "medium"))
        
        else:
            analysis["involves_decision"] = False
        
        return analysis
    
    async def _analyze_learning_preferences(self, message: str, response: str) -> Dict:
        """تحلیل ترجیحات یادگیری"""
        
        analysis = {}
        
        # تشخیص درخواست یادگیری
        learning_indicators = ["یاد بده", "توضیح", "چطور", "راه", "روش", "آموزش"]
        
        if any(indicator in message.lower() for indicator in learning_indicators):
            analysis["is_learning_request"] = True
            
            # تحلیل سطح جزئیات مورد نیاز
            detail_indicators = ["جزئیات", "کامل", "دقیق", "همه چیز"]
            summary_indicators = ["خلاصه", "سریع", "مختصر", "کلی"]
            
            if any(indicator in message.lower() for indicator in detail_indicators):
                analysis["detail_preference"] = "detailed"
            elif any(indicator in message.lower() for indicator in summary_indicators):
                analysis["detail_preference"] = "summary"
            else:
                analysis["detail_preference"] = "medium"
            
            # تحلیل ترجیح مثال
            example_indicators = ["مثال", "نمونه", "عملی", "واقعی"]
            theory_indicators = ["تئوری", "نظری", "اصول", "مفهوم"]
            
            if any(indicator in message.lower() for indicator in example_indicators):
                analysis["example_preference"] = "practical"
            elif any(indicator in message.lower() for indicator in theory_indicators):
                analysis["example_preference"] = "theoretical"
            else:
                analysis["example_preference"] = "balanced"
            
            # به‌روزرسانی الگوها
            self.learning_patterns["detail_level"].append(analysis.get("detail_preference", "medium"))
            self.learning_patterns["example_preference"].append(analysis.get("example_preference", "balanced"))
        
        else:
            analysis["is_learning_request"] = False
        
        return analysis
    
    async def _analyze_emotional_state(self, message: str, context: Dict) -> Dict:
        """تحلیل وضعیت عاطفی"""
        
        analysis = {}
        
        # تشخیص نشانه‌های استرس
        stress_indicators = [
            "استرس", "فشار", "عجله", "مشکل", "سخت", "خسته", 
            "کلافه", "اعصاب", "نگران", "ضرب‌الاجل"
        ]
        
        stress_score = sum(1 for indicator in stress_indicators if indicator in message.lower())
        analysis["stress_level"] = min(1.0, stress_score / 3)
        
        # تشخیص انگیزه
        motivation_indicators = {
            "high": ["هیجان", "علاقه", "عاشق", "دوست دارم", "جالب"],
            "low": ["مجبور", "باید", "ناچار", "کسل", "بی‌حوصله"]
        }
        
        for level, indicators in motivation_indicators.items():
            if any(indicator in message.lower() for indicator in indicators):
                analysis["motivation_level"] = level
                break
        else:
            analysis["motivation_level"] = "medium"
        
        # تشخیص سطح انرژی
        energy_indicators = {
            "high": ["پرانرژی", "فعال", "آماده", "بیا بریم"],
            "low": ["خسته", "کسل", "بی‌حال", "کم انرژی"]
        }
        
        for level, indicators in energy_indicators.items():
            if any(indicator in message.lower() for indicator in indicators):
                analysis["energy_level"] = level
                break
        else:
            analysis["energy_level"] = "medium"
        
        # به‌روزرسانی الگوهای عاطفی
        if analysis["stress_level"] > 0.5:
            self.emotional_patterns["stress_indicators"].append({
                "timestamp": datetime.now(),
                "message": message[:50],
                "stress_level": analysis["stress_level"]
            })
        
        return analysis
    
    async def _identify_behavior_patterns(self, message: str, context: Dict, response: str) -> List[BehaviorPattern]:
        """شناسایی الگوهای رفتاری جدید"""
        
        new_patterns = []
        
        # الگوی زمانی
        current_hour = datetime.now().hour
        message_type = self._classify_message_type(message)
        
        pattern_key = f"time_{current_hour}_{message_type}"
        
        if pattern_key not in self.behavior_patterns:
            pattern = BehaviorPattern(
                pattern_id=pattern_key,
                description=f"فعالیت {message_type} در ساعت {current_hour}",
                triggers=[f"hour_{current_hour}"],
                responses=[message_type],
                frequency=1,
                reliability=0.5,
                context={"hour": current_hour, "type": message_type}
            )
            
            self.behavior_patterns[pattern_key] = pattern
            new_patterns.append(pattern)
        else:
            # تقویت الگوی موجود
            self.behavior_patterns[pattern_key].frequency += 1
            self.behavior_patterns[pattern_key].reliability = min(1.0, 
                self.behavior_patterns[pattern_key].reliability + 0.1)
        
        return new_patterns
    
    def _classify_message_type(self, message: str) -> str:
        """طبقه‌بندی نوع پیام"""
        
        message_lower = message.lower()
        
        if any(word in message_lower for word in ["سلام", "درود", "صبح بخیر"]):
            return "greeting"
        elif "؟" in message:
            return "question"
        elif any(word in message_lower for word in ["کمک", "انجام", "بکن"]):
            return "request"
        elif any(word in message_lower for word in ["ممنون", "مرسی", "متشکر"]):
            return "gratitude"
        else:
            return "general"
    
    async def _update_personality_insights(self, analysis_results: Dict):
        """به‌روزرسانی بینش‌های شخصیتی"""
        
        # تحلیل سبک ارتباط
        comm_analysis = analysis_results.get("communication", {})
        if comm_analysis:
            await self._update_communication_insights(comm_analysis)
        
        # تحلیل تصمیم‌گیری
        decision_analysis = analysis_results.get("decision_making", {})
        if decision_analysis.get("involves_decision"):
            await self._update_decision_insights(decision_analysis)
        
        # تحلیل یادگیری
        learning_analysis = analysis_results.get("learning", {})
        if learning_analysis.get("is_learning_request"):
            await self._update_learning_insights(learning_analysis)
    
    async def _update_communication_insights(self, comm_analysis: Dict):
        """به‌روزرسانی بینش‌های ارتباطی"""
        
        # تحلیل رسمی بودن
        formality_pattern = Counter(self.communication_analysis["formality_levels"])
        most_common_formality = formality_pattern.most_common(1)[0][0] if formality_pattern else "neutral"
        
        insight_key = "communication_formality"
        if insight_key not in self.personality_insights:
            self.personality_insights[insight_key] = PersonalityInsight(
                dimension=PersonalityDimension.COMMUNICATION_STYLE,
                insight=f"ترجیح به ارتباط {most_common_formality}",
                confidence=0.6,
                evidence=[f"در {len(self.communication_analysis['formality_levels'])} تعامل"],
                discovered_at=datetime.now(),
                reinforcement_count=1,
                last_observed=datetime.now()
            )
        else:
            # تقویت بینش موجود
            self.personality_insights[insight_key].reinforcement_count += 1
            self.personality_insights[insight_key].last_observed = datetime.now()
            self.personality_insights[insight_key].confidence = min(0.95, 
                self.personality_insights[insight_key].confidence + 0.05)
    
    async def _update_decision_insights(self, decision_analysis: Dict):
        """به‌روزرسانی بینش‌های تصمیم‌گیری"""
        
        decision_speed = decision_analysis.get("decision_speed", "normal")
        info_need = decision_analysis.get("information_need", "medium")
        
        # الگوی سرعت تصمیم‌گیری
        speed_pattern = Counter(self.decision_patterns["decision_speed"])
        dominant_speed = speed_pattern.most_common(1)[0][0] if speed_pattern else "normal"
        
        insight_key = "decision_speed_preference"
        if insight_key not in self.personality_insights:
            self.personality_insights[insight_key] = PersonalityInsight(
                dimension=PersonalityDimension.DECISION_MAKING,
                insight=f"تمایل به تصمیم‌گیری {dominant_speed}",
                confidence=0.5,
                evidence=[f"در {len(self.decision_patterns['decision_speed'])} تصمیم"],
                discovered_at=datetime.now(),
                reinforcement_count=1,
                last_observed=datetime.now()
            )
    
    async def _update_learning_insights(self, learning_analysis: Dict):
        """به‌روزرسانی بینش‌های یادگیری"""
        
        detail_pref = learning_analysis.get("detail_preference", "medium")
        example_pref = learning_analysis.get("example_preference", "balanced")
        
        # الگوی سطح جزئیات
        detail_pattern = Counter(self.learning_patterns["detail_level"])
        dominant_detail = detail_pattern.most_common(1)[0][0] if detail_pattern else "medium"
        
        insight_key = "learning_detail_preference"
        if insight_key not in self.personality_insights:
            self.personality_insights[insight_key] = PersonalityInsight(
                dimension=PersonalityDimension.LEARNING_PREFERENCE,
                insight=f"ترجیح به یادگیری {dominant_detail}",
                confidence=0.6,
                evidence=[f"در {len(self.learning_patterns['detail_level'])} درخواست یادگیری"],
                discovered_at=datetime.now(),
                reinforcement_count=1,
                last_observed=datetime.now()
            )
    
    def get_personality_profile(self) -> Dict:
        """پروفایل کامل شخصیت"""
        
        profile = {
            "owner": self.owner_name,
            "total_insights": len(self.personality_insights),
            "behavior_patterns": len(self.behavior_patterns),
            "confidence_distribution": {},
            "key_insights": {},
            "learning_summary": {}
        }
        
        # توزیع اعتماد
        confidence_levels = [insight.confidence for insight in self.personality_insights.values()]
        if confidence_levels:
            profile["confidence_distribution"] = {
                "average": sum(confidence_levels) / len(confidence_levels),
                "high_confidence_insights": len([c for c in confidence_levels if c > 0.8]),
                "total_insights": len(confidence_levels)
            }
        
        # بینش‌های کلیدی
        for dimension in PersonalityDimension:
            dimension_insights = [
                insight for insight in self.personality_insights.values()
                if insight.dimension == dimension
            ]
            
            if dimension_insights:
                best_insight = max(dimension_insights, key=lambda x: x.confidence)
                profile["key_insights"][dimension.value] = {
                    "insight": best_insight.insight,
                    "confidence": best_insight.confidence,
                    "reinforcements": best_insight.reinforcement_count
                }
        
        # خلاصه یادگیری
        profile["learning_summary"] = {
            "communication_interactions": len(self.communication_analysis["formality_levels"]),
            "decision_points": len(self.decision_patterns["decision_speed"]),
            "learning_requests": len(self.learning_patterns["detail_level"]),
            "stress_episodes": len(self.emotional_patterns["stress_indicators"])
        }
        
        return profile
    
    def get_recommendations(self) -> List[str]:
        """توصیه‌های بر اساس شخصیت شناخته شده"""
        
        recommendations = []
        
        # توصیه‌های ارتباطی
        formality_pattern = Counter(self.communication_analysis["formality_levels"])
        if formality_pattern:
            most_common = formality_pattern.most_common(1)[0][0]
            if most_common == "formal":
                recommendations.append("استفاده از زبان رسمی‌تر در پاسخ‌ها")
            elif most_common == "informal":
                recommendations.append("استفاده از زبان دوستانه‌تر و صمیمی‌تر")
        
        # توصیه‌های یادگیری
        detail_pattern = Counter(self.learning_patterns["detail_level"])
        if detail_pattern:
            most_common = detail_pattern.most_common(1)[0][0]
            if most_common == "detailed":
                recommendations.append("ارائه توضیحات جزئی‌تر و کامل‌تر")
            elif most_common == "summary":
                recommendations.append("ارائه خلاصه‌های مختصر و مفید")
        
        # توصیه‌های مدیریت استرس
        if len(self.emotional_patterns["stress_indicators"]) > 5:
            recommendations.append("پیشنهاد استراحت و مدیریت استرس در مواقع لزوم")
        
        return recommendations

# Instance سراسری
deep_personality_learning = DeepPersonalityLearning()
