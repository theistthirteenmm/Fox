"""
🔮 سیستم پیش‌بینی هوشمند روباه
پیش‌بینی نیازها و ارائه کمک پیش‌قدمانه
"""

import json
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import numpy as np
from collections import defaultdict
import pickle
import os

class PredictionType(Enum):
    TASK_REMINDER = "task_reminder"
    MEETING_PREP = "meeting_prep"
    BREAK_SUGGESTION = "break_suggestion"
    RESOURCE_NEED = "resource_need"
    MOOD_SUPPORT = "mood_support"
    WORKFLOW_OPTIMIZATION = "workflow_optimization"

class PredictionConfidence(Enum):
    LOW = 0.3
    MEDIUM = 0.6
    HIGH = 0.8
    VERY_HIGH = 0.9

@dataclass
class Prediction:
    id: str
    type: PredictionType
    description: str
    confidence: float
    suggested_action: str
    timing: datetime
    context: Dict
    importance: float

class PredictiveIntelligence:
    def __init__(self, owner_name: str = "حامد"):
        self.owner_name = owner_name
        self.predictions = {}
        self.pattern_history = defaultdict(list)
        self.behavioral_model = {}
        
        # الگوهای یادگیری شده
        self.learned_patterns = {
            "daily_routine": {},
            "work_cycles": {},
            "stress_indicators": {},
            "productivity_patterns": {},
            "communication_patterns": {}
        }
        
        # پیش‌بینی‌های فعال
        self.active_predictions = []
        self.prediction_accuracy = {}
        
        print("🔮 سیستم پیش‌بینی هوشمند راه‌اندازی شد")
    
    async def analyze_and_predict(self, current_context: Dict) -> List[Prediction]:
        """تحلیل وضعیت فعلی و تولید پیش‌بینی‌ها"""
        
        predictions = []
        current_time = datetime.now()
        
        # 1. پیش‌بینی بر اساس الگوهای زمانی
        time_predictions = await self._predict_from_time_patterns(current_time, current_context)
        predictions.extend(time_predictions)
        
        # 2. پیش‌بینی بر اساس رفتار کاری
        work_predictions = await self._predict_from_work_patterns(current_context)
        predictions.extend(work_predictions)
        
        # 3. پیش‌بینی بر اساس حالت عاطفی
        mood_predictions = await self._predict_from_mood_patterns(current_context)
        predictions.extend(mood_predictions)
        
        # 4. پیش‌بینی بر اساس بهره‌وری
        productivity_predictions = await self._predict_productivity_needs(current_context)
        predictions.extend(productivity_predictions)
        
        # فیلتر و اولویت‌بندی
        filtered_predictions = self._filter_and_prioritize(predictions)
        
        return filtered_predictions
    
    async def _predict_from_time_patterns(self, current_time: datetime, context: Dict) -> List[Prediction]:
        """پیش‌بینی بر اساس الگوهای زمانی"""
        predictions = []
        
        hour = current_time.hour
        weekday = current_time.weekday()
        
        # الگوی صبح (9-11)
        if 9 <= hour <= 11:
            if weekday < 5:  # روزهای کاری
                predictions.append(Prediction(
                    id=f"morning_routine_{current_time.timestamp()}",
                    type=PredictionType.WORKFLOW_OPTIMIZATION,
                    description="شروع روز کاری - بررسی برنامه روزانه",
                    confidence=0.8,
                    suggested_action="آیا می‌خواهید برنامه امروزتان را مرور کنیم؟",
                    timing=current_time,
                    context={"time_pattern": "morning_routine"},
                    importance=0.7
                ))
        
        # الگوی بعدازظهر (14-16)
        elif 14 <= hour <= 16:
            predictions.append(Prediction(
                id=f"afternoon_energy_{current_time.timestamp()}",
                type=PredictionType.BREAK_SUGGESTION,
                description="کاهش انرژی بعدازظهر",
                confidence=0.6,
                suggested_action="وقت استراحت کوتاه یا قهوه؟",
                timing=current_time,
                context={"time_pattern": "afternoon_dip"},
                importance=0.5
            ))
        
        # الگوی پایان روز (17-19)
        elif 17 <= hour <= 19:
            predictions.append(Prediction(
                id=f"end_of_day_{current_time.timestamp()}",
                type=PredictionType.TASK_REMINDER,
                description="جمع‌بندی روز کاری",
                confidence=0.7,
                suggested_action="بررسی کارهای تکمیل شده و برنامه‌ریزی فردا؟",
                timing=current_time,
                context={"time_pattern": "end_of_day"},
                importance=0.6
            ))
        
        return predictions
    
    async def _predict_from_work_patterns(self, context: Dict) -> List[Prediction]:
        """پیش‌بینی بر اساس الگوهای کاری"""
        predictions = []
        
        # تحلیل فعالیت‌های اخیر
        recent_activities = context.get("recent_activities", [])
        current_project = context.get("current_project", None)
        
        # اگر روی پروژه خاصی کار می‌کند
        if current_project:
            predictions.append(Prediction(
                id=f"project_support_{datetime.now().timestamp()}",
                type=PredictionType.RESOURCE_NEED,
                description=f"پشتیبانی پروژه {current_project}",
                confidence=0.7,
                suggested_action="آیا برای این پروژه به اطلاعات یا منابع اضافی نیاز دارید؟",
                timing=datetime.now(),
                context={"project": current_project},
                importance=0.8
            ))
        
        # الگوی جلسات
        if self._is_meeting_time_approaching(context):
            predictions.append(Prediction(
                id=f"meeting_prep_{datetime.now().timestamp()}",
                type=PredictionType.MEETING_PREP,
                description="آماده‌سازی جلسه",
                confidence=0.9,
                suggested_action="جلسه نزدیک است. آیا نیاز به آماده‌سازی دارید؟",
                timing=datetime.now() + timedelta(minutes=15),
                context={"meeting_prep": True},
                importance=0.9
            ))
        
        return predictions
    
    async def _predict_from_mood_patterns(self, context: Dict) -> List[Prediction]:
        """پیش‌بینی بر اساس الگوهای عاطفی"""
        predictions = []
        
        current_mood = context.get("owner_emotion", "neutral")
        stress_level = context.get("stress_level", 0.5)
        
        # تشخیص استرس بالا
        if stress_level > 0.7 or current_mood == "stressed":
            predictions.append(Prediction(
                id=f"stress_support_{datetime.now().timestamp()}",
                type=PredictionType.MOOD_SUPPORT,
                description="پشتیبانی در مواقع استرس",
                confidence=0.8,
                suggested_action="می‌بینم کمی تحت فشار هستید. آیا می‌خواهید کمی استراحت کنید یا درباره مشکل صحبت کنیم؟",
                timing=datetime.now(),
                context={"mood_support": True, "stress_level": stress_level},
                importance=0.9
            ))
        
        # تشخیص خستگی
        elif current_mood == "tired":
            predictions.append(Prediction(
                id=f"energy_boost_{datetime.now().timestamp()}",
                type=PredictionType.BREAK_SUGGESTION,
                description="پیشنهاد تقویت انرژی",
                confidence=0.7,
                suggested_action="به نظر خسته می‌رسید. چطور است کمی قدم بزنید یا یک نوشیدنی انرژی‌زا بنوشید؟",
                timing=datetime.now(),
                context={"energy_boost": True},
                importance=0.6
            ))
        
        return predictions
    
    async def _predict_productivity_needs(self, context: Dict) -> List[Prediction]:
        """پیش‌بینی نیازهای بهره‌وری"""
        predictions = []
        
        # تحلیل الگوی کاری
        work_duration = context.get("continuous_work_time", 0)
        task_complexity = context.get("task_complexity", "medium")
        
        # کار مداوم طولانی
        if work_duration > 120:  # بیش از 2 ساعت
            predictions.append(Prediction(
                id=f"productivity_break_{datetime.now().timestamp()}",
                type=PredictionType.BREAK_SUGGESTION,
                description="استراحت برای حفظ بهره‌وری",
                confidence=0.8,
                suggested_action="بیش از 2 ساعت مداوم کار کرده‌اید. استراحت 10 دقیقه‌ای چطور است؟",
                timing=datetime.now(),
                context={"productivity_break": True, "work_duration": work_duration},
                importance=0.7
            ))
        
        # کار پیچیده
        if task_complexity == "high":
            predictions.append(Prediction(
                id=f"complex_task_support_{datetime.now().timestamp()}",
                type=PredictionType.RESOURCE_NEED,
                description="پشتیبانی کار پیچیده",
                confidence=0.6,
                suggested_action="این کار پیچیده به نظر می‌رسد. آیا نیاز به تحقیق یا منابع اضافی دارید؟",
                timing=datetime.now(),
                context={"complex_task": True},
                importance=0.6
            ))
        
        return predictions
    
    def _is_meeting_time_approaching(self, context: Dict) -> bool:
        """بررسی نزدیک شدن زمان جلسه"""
        # این باید با تقویم ادغام شود
        # فعلاً یک شبیه‌سازی ساده
        current_hour = datetime.now().hour
        
        # ساعات معمول جلسات
        meeting_hours = [10, 14, 16]
        
        for meeting_hour in meeting_hours:
            if abs(current_hour - meeting_hour) <= 0.25:  # 15 دقیقه
                return True
        
        return False
    
    def _filter_and_prioritize(self, predictions: List[Prediction]) -> List[Prediction]:
        """فیلتر و اولویت‌بندی پیش‌بینی‌ها"""
        
        # حذف تکراری‌ها
        unique_predictions = {}
        for pred in predictions:
            key = f"{pred.type.value}_{pred.description[:20]}"
            if key not in unique_predictions or pred.confidence > unique_predictions[key].confidence:
                unique_predictions[key] = pred
        
        # مرتب‌سازی بر اساس اهمیت و اعتماد
        sorted_predictions = sorted(
            unique_predictions.values(),
            key=lambda x: (x.importance * x.confidence),
            reverse=True
        )
        
        # برگرداندن حداکثر 3 پیش‌بینی برتر
        return sorted_predictions[:3]
    
    async def execute_proactive_action(self, prediction: Prediction) -> Dict:
        """اجرای عمل پیش‌قدمانه"""
        
        action_result = {
            "prediction_id": prediction.id,
            "action_taken": prediction.suggested_action,
            "timestamp": datetime.now().isoformat(),
            "success": True
        }
        
        # ثبت در تاریخچه برای یادگیری
        self.prediction_accuracy[prediction.id] = {
            "prediction": prediction,
            "executed_at": datetime.now(),
            "user_response": None  # باید بعداً پر شود
        }
        
        print(f"🎯 اجرای عمل پیش‌قدمانه: {prediction.suggested_action}")
        
        return action_result
    
    def record_user_feedback(self, prediction_id: str, feedback: str, helpful: bool):
        """ثبت بازخورد کاربر برای یادگیری"""
        
        if prediction_id in self.prediction_accuracy:
            self.prediction_accuracy[prediction_id]["user_response"] = feedback
            self.prediction_accuracy[prediction_id]["helpful"] = helpful
            
            # یادگیری از بازخورد
            self._learn_from_feedback(prediction_id, helpful)
    
    def _learn_from_feedback(self, prediction_id: str, helpful: bool):
        """یادگیری از بازخورد کاربر"""
        
        prediction_data = self.prediction_accuracy.get(prediction_id)
        if not prediction_data:
            return
        
        prediction = prediction_data["prediction"]
        
        # تنظیم وزن‌های یادگیری
        if helpful:
            # تقویت الگوهای مشابه
            pattern_key = f"{prediction.type.value}_{prediction.context}"
            if pattern_key not in self.behavioral_model:
                self.behavioral_model[pattern_key] = {"weight": 0.5, "success_count": 0}
            
            self.behavioral_model[pattern_key]["weight"] = min(1.0, 
                self.behavioral_model[pattern_key]["weight"] + 0.1)
            self.behavioral_model[pattern_key]["success_count"] += 1
        else:
            # کاهش وزن الگوهای ناموفق
            pattern_key = f"{prediction.type.value}_{prediction.context}"
            if pattern_key in self.behavioral_model:
                self.behavioral_model[pattern_key]["weight"] = max(0.1,
                    self.behavioral_model[pattern_key]["weight"] - 0.1)
    
    def get_prediction_stats(self) -> Dict:
        """آمار پیش‌بینی‌ها"""
        
        total_predictions = len(self.prediction_accuracy)
        helpful_predictions = sum(1 for p in self.prediction_accuracy.values() 
                                if p.get("helpful", False))
        
        accuracy_rate = helpful_predictions / total_predictions if total_predictions > 0 else 0
        
        return {
            "total_predictions": total_predictions,
            "helpful_predictions": helpful_predictions,
            "accuracy_rate": accuracy_rate,
            "active_predictions": len(self.active_predictions),
            "learned_patterns": len(self.behavioral_model)
        }

# Instance سراسری
predictive_intelligence = PredictiveIntelligence()