"""
🏢 سیستم هوش محیط کار روباه
مدیریت و بهینه‌سازی محیط کاری
"""

import json
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import os

class WorkspaceType(Enum):
    OFFICE = "office"
    HOME_OFFICE = "home_office"
    MEETING_ROOM = "meeting_room"
    SHARED_SPACE = "shared_space"

class TaskPriority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4
    CRITICAL = 5

class WorkMode(Enum):
    FOCUS = "focus"           # تمرکز عمیق
    COLLABORATION = "collaboration"  # همکاری
    CREATIVE = "creative"     # خلاقیت
    ADMINISTRATIVE = "administrative"  # اداری
    LEARNING = "learning"     # یادگیری

@dataclass
class WorkTask:
    id: str
    title: str
    description: str
    priority: TaskPriority
    estimated_duration: int  # دقیقه
    deadline: Optional[datetime]
    dependencies: List[str]
    status: str
    work_mode: WorkMode
    context: Dict

@dataclass
class WorkSession:
    id: str
    start_time: datetime
    end_time: Optional[datetime]
    work_mode: WorkMode
    tasks_completed: List[str]
    interruptions: int
    productivity_score: float
    notes: str

class WorkplaceIntelligence:
    def __init__(self, owner_name: str = "حامد"):
        self.owner_name = owner_name
        self.current_workspace = WorkspaceType.OFFICE
        self.current_work_mode = WorkMode.FOCUS
        
        # مدیریت کارها
        self.active_tasks = {}
        self.completed_tasks = {}
        self.task_history = []
        
        # جلسات کاری
        self.work_sessions = []
        self.current_session = None
        
        # تحلیل بهره‌وری
        self.productivity_patterns = {
            "peak_hours": [],
            "best_work_modes": {},
            "distraction_patterns": {},
            "optimal_task_sequence": []
        }
        
        # محیط کار
        self.workspace_config = {
            "lighting": "auto",
            "temperature": 22,
            "noise_level": "quiet",
            "desk_setup": "organized"
        }
        
        # تقویم و برنامه‌ریزی
        self.calendar_integration = False
        self.upcoming_meetings = []
        self.daily_schedule = {}
        
        print("🏢 سیستم هوش محیط کار راه‌اندازی شد")
    
    async def start_work_session(self, work_mode: WorkMode, planned_tasks: List[str] = None) -> str:
        """شروع جلسه کاری"""
        
        session_id = f"session_{datetime.now().timestamp()}"
        
        self.current_session = WorkSession(
            id=session_id,
            start_time=datetime.now(),
            end_time=None,
            work_mode=work_mode,
            tasks_completed=[],
            interruptions=0,
            productivity_score=0.0,
            notes=""
        )
        
        self.current_work_mode = work_mode
        
        # تنظیم محیط برای نوع کار
        await self._optimize_workspace_for_mode(work_mode)
        
        # پیشنهاد کارهای مناسب
        if not planned_tasks:
            suggested_tasks = await self._suggest_tasks_for_mode(work_mode)
            print(f"💡 کارهای پیشنهادی برای حالت {work_mode.value}: {suggested_tasks}")
        
        print(f"🚀 جلسه کاری شروع شد - حالت: {work_mode.value}")
        return session_id
    
    async def end_work_session(self, notes: str = "") -> Dict:
        """پایان جلسه کاری"""
        
        if not self.current_session:
            return {"error": "هیچ جلسه فعالی وجود ندارد"}
        
        self.current_session.end_time = datetime.now()
        self.current_session.notes = notes
        
        # محاسبه امتیاز بهره‌وری
        productivity_score = await self._calculate_productivity_score(self.current_session)
        self.current_session.productivity_score = productivity_score
        
        # ذخیره در تاریخچه
        self.work_sessions.append(self.current_session)
        
        # تحلیل و یادگیری
        await self._analyze_work_session(self.current_session)
        
        session_summary = {
            "session_id": self.current_session.id,
            "duration": (self.current_session.end_time - self.current_session.start_time).total_seconds() / 60,
            "tasks_completed": len(self.current_session.tasks_completed),
            "productivity_score": productivity_score,
            "work_mode": self.current_session.work_mode.value
        }
        
        self.current_session = None
        
        print(f"✅ جلسه کاری پایان یافت - امتیاز بهره‌وری: {productivity_score:.1f}")
        return session_summary
    
    async def add_task(self, title: str, description: str, priority: TaskPriority, 
                      estimated_duration: int, deadline: datetime = None,
                      work_mode: WorkMode = WorkMode.FOCUS) -> str:
        """اضافه کردن کار جدید"""
        
        task_id = f"task_{datetime.now().timestamp()}"
        
        task = WorkTask(
            id=task_id,
            title=title,
            description=description,
            priority=priority,
            estimated_duration=estimated_duration,
            deadline=deadline,
            dependencies=[],
            status="pending",
            work_mode=work_mode,
            context={}
        )
        
        self.active_tasks[task_id] = task
        
        # تحلیل و پیشنهاد زمان انجام
        suggested_time = await self._suggest_optimal_time(task)
        
        print(f"📝 کار جدید اضافه شد: {title}")
        print(f"⏰ زمان پیشنهادی: {suggested_time}")
        
        return task_id
    
    async def complete_task(self, task_id: str, actual_duration: int = None, 
                          quality_score: float = 1.0) -> Dict:
        """تکمیل کار"""
        
        if task_id not in self.active_tasks:
            return {"error": "کار یافت نشد"}
        
        task = self.active_tasks[task_id]
        task.status = "completed"
        
        # انتقال به کارهای تکمیل شده
        self.completed_tasks[task_id] = task
        del self.active_tasks[task_id]
        
        # به‌روزرسانی جلسه فعلی
        if self.current_session:
            self.current_session.tasks_completed.append(task_id)
        
        # تحلیل عملکرد
        performance_analysis = {
            "task_id": task_id,
            "estimated_duration": task.estimated_duration,
            "actual_duration": actual_duration or task.estimated_duration,
            "quality_score": quality_score,
            "efficiency": task.estimated_duration / (actual_duration or task.estimated_duration)
        }
        
        # یادگیری از عملکرد
        await self._learn_from_task_completion(task, performance_analysis)
        
        print(f"✅ کار تکمیل شد: {task.title}")
        return performance_analysis
    
    async def get_daily_plan(self, date: datetime = None) -> Dict:
        """برنامه روزانه"""
        
        if not date:
            date = datetime.now()
        
        # کارهای امروز
        today_tasks = [
            task for task in self.active_tasks.values()
            if task.deadline and task.deadline.date() == date.date()
        ]
        
        # مرتب‌سازی بر اساس اولویت
        today_tasks.sort(key=lambda x: x.priority.value, reverse=True)
        
        # تخمین زمان کل
        total_estimated_time = sum(task.estimated_duration for task in today_tasks)
        
        # پیشنهاد برنامه‌ریزی
        schedule = await self._create_optimal_schedule(today_tasks, date)
        
        return {
            "date": date.date().isoformat(),
            "total_tasks": len(today_tasks),
            "estimated_total_time": total_estimated_time,
            "high_priority_tasks": len([t for t in today_tasks if t.priority.value >= 4]),
            "suggested_schedule": schedule,
            "productivity_forecast": await self._forecast_productivity(date)
        }
    
    async def _optimize_workspace_for_mode(self, work_mode: WorkMode):
        """بهینه‌سازی محیط کار برای نوع کار"""
        
        optimizations = {
            WorkMode.FOCUS: {
                "lighting": "bright",
                "noise_level": "silent",
                "notifications": "off",
                "suggestion": "حالت تمرکز عمیق - اعلان‌ها خاموش شد"
            },
            WorkMode.CREATIVE: {
                "lighting": "warm",
                "noise_level": "ambient",
                "notifications": "minimal",
                "suggestion": "حالت خلاقیت - محیط آرام و الهام‌بخش"
            },
            WorkMode.COLLABORATION: {
                "lighting": "natural",
                "noise_level": "normal",
                "notifications": "on",
                "suggestion": "حالت همکاری - آماده برای تعامل"
            }
        }
        
        if work_mode in optimizations:
            config = optimizations[work_mode]
            self.workspace_config.update(config)
            print(f"🔧 {config['suggestion']}")
    
    async def _suggest_tasks_for_mode(self, work_mode: WorkMode) -> List[str]:
        """پیشنهاد کارهای مناسب برای نوع کار"""
        
        suitable_tasks = [
            task.title for task in self.active_tasks.values()
            if task.work_mode == work_mode
        ]
        
        if not suitable_tasks:
            # پیشنهاد بر اساس اولویت
            suitable_tasks = [
                task.title for task in sorted(
                    self.active_tasks.values(),
                    key=lambda x: x.priority.value,
                    reverse=True
                )[:3]
            ]
        
        return suitable_tasks
    
    async def _calculate_productivity_score(self, session: WorkSession) -> float:
        """محاسبه امتیاز بهره‌وری"""
        
        if not session.end_time:
            return 0.0
        
        duration_minutes = (session.end_time - session.start_time).total_seconds() / 60
        
        # امتیاز بر اساس کارهای تکمیل شده
        tasks_score = len(session.tasks_completed) * 0.3
        
        # امتیاز بر اساس مدت زمان
        duration_score = min(1.0, duration_minutes / 120) * 0.3  # حداکثر 2 ساعت
        
        # کسر امتیاز برای وقفه‌ها
        interruption_penalty = session.interruptions * 0.1
        
        # امتیاز نهایی
        final_score = max(0.0, min(10.0, (tasks_score + duration_score - interruption_penalty) * 10))
        
        return final_score
    
    async def _analyze_work_session(self, session: WorkSession):
        """تحلیل جلسه کاری برای یادگیری"""
        
        hour = session.start_time.hour
        work_mode = session.work_mode.value
        
        # یادگیری ساعات پربازده
        if session.productivity_score > 7.0:
            if hour not in self.productivity_patterns["peak_hours"]:
                self.productivity_patterns["peak_hours"].append(hour)
        
        # یادگیری بهترین حالت‌های کاری
        if work_mode not in self.productivity_patterns["best_work_modes"]:
            self.productivity_patterns["best_work_modes"][work_mode] = []
        
        self.productivity_patterns["best_work_modes"][work_mode].append(session.productivity_score)
    
    async def _suggest_optimal_time(self, task: WorkTask) -> str:
        """پیشنهاد بهترین زمان انجام کار"""
        
        # بر اساس ساعات پربازده
        peak_hours = self.productivity_patterns.get("peak_hours", [9, 10, 14])
        
        # بر اساس نوع کار
        if task.work_mode == WorkMode.FOCUS:
            suggested_hour = min(peak_hours) if peak_hours else 9
        elif task.work_mode == WorkMode.CREATIVE:
            suggested_hour = 10  # صبح برای خلاقیت
        else:
            suggested_hour = 14  # بعدازظهر برای کارهای اداری
        
        return f"ساعت {suggested_hour}:00"
    
    async def _create_optimal_schedule(self, tasks: List[WorkTask], date: datetime) -> List[Dict]:
        """ایجاد برنامه بهینه"""
        
        schedule = []
        current_time = date.replace(hour=9, minute=0)  # شروع از 9 صبح
        
        for task in tasks:
            schedule_item = {
                "time": current_time.strftime("%H:%M"),
                "task": task.title,
                "duration": task.estimated_duration,
                "priority": task.priority.name,
                "work_mode": task.work_mode.value
            }
            
            schedule.append(schedule_item)
            current_time += timedelta(minutes=task.estimated_duration + 15)  # 15 دقیقه استراحت
        
        return schedule
    
    async def _forecast_productivity(self, date: datetime) -> Dict:
        """پیش‌بینی بهره‌وری"""
        
        weekday = date.weekday()
        hour = date.hour
        
        # تحلیل تاریخی
        historical_scores = [
            session.productivity_score for session in self.work_sessions
            if session.start_time.weekday() == weekday
        ]
        
        avg_score = sum(historical_scores) / len(historical_scores) if historical_scores else 7.0
        
        return {
            "expected_productivity": avg_score,
            "confidence": min(1.0, len(historical_scores) / 10),
            "factors": {
                "day_of_week": weekday,
                "historical_average": avg_score,
                "sample_size": len(historical_scores)
            }
        }
    
    async def _learn_from_task_completion(self, task: WorkTask, performance: Dict):
        """یادگیری از تکمیل کار"""
        
        # یادگیری دقت تخمین زمان
        efficiency = performance["efficiency"]
        
        if efficiency < 0.8:  # کار بیشتر از حد انتظار طول کشید
            print(f"📊 یادگیری: کارهای نوع {task.work_mode.value} معمولاً بیشتر طول می‌کشند")
        elif efficiency > 1.2:  # کار زودتر تمام شد
            print(f"📊 یادگیری: کارهای نوع {task.work_mode.value} معمولاً زودتر تمام می‌شوند")
    
    def get_workspace_stats(self) -> Dict:
        """آمار محیط کار"""
        
        total_sessions = len(self.work_sessions)
        avg_productivity = sum(s.productivity_score for s in self.work_sessions) / total_sessions if total_sessions > 0 else 0
        
        return {
            "total_work_sessions": total_sessions,
            "average_productivity": avg_productivity,
            "active_tasks": len(self.active_tasks),
            "completed_tasks": len(self.completed_tasks),
            "current_work_mode": self.current_work_mode.value if self.current_work_mode else None,
            "peak_hours": self.productivity_patterns.get("peak_hours", []),
            "workspace_type": self.current_workspace.value
        }
    
    async def handle_interruption(self, interruption_type: str, duration: int):
        """مدیریت وقفه‌ها"""
        
        if self.current_session:
            self.current_session.interruptions += 1
            print(f"⚠️ وقفه ثبت شد: {interruption_type} ({duration} دقیقه)")
            
            # پیشنهاد بازگشت به کار
            if duration > 15:
                print("💡 پیشنهاد: برای بازگشت بهتر به کار، 5 دقیقه مرور کنید که کجا بودید")

# Instance سراسری
workplace_intelligence = WorkplaceIntelligence()