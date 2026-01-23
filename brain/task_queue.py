"""
⚡ سیستم Task Queue غیرهمزمان
مدیریت وظایف سنگین و بهینه‌سازی عملکرد
"""

import asyncio
import json
from typing import Dict, List, Callable, Optional, Any
from datetime import datetime
from enum import Enum
import uuid
from dataclasses import dataclass
import logging

class TaskPriority(Enum):
    LOW = 1
    NORMAL = 2
    HIGH = 3
    URGENT = 4

class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

@dataclass
class Task:
    id: str
    name: str
    func: Callable
    args: tuple
    kwargs: dict
    priority: TaskPriority
    created_at: datetime
    status: TaskStatus = TaskStatus.PENDING
    result: Any = None
    error: str = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

class AsyncTaskQueue:
    def __init__(self, max_workers: int = 3):
        self.max_workers = max_workers
        self.tasks = {}
        self.pending_queue = asyncio.PriorityQueue()
        self.running_tasks = {}
        self.completed_tasks = {}
        self.workers = []
        self.is_running = False
        
        # آمار
        self.stats = {
            "total_tasks": 0,
            "completed_tasks": 0,
            "failed_tasks": 0,
            "average_execution_time": 0
        }
        
        print(f"⚡ Task Queue با {max_workers} worker راه‌اندازی شد")
    
    async def start(self):
        """شروع task queue"""
        if self.is_running:
            return
        
        self.is_running = True
        
        # ایجاد worker ها
        for i in range(self.max_workers):
            worker = asyncio.create_task(self._worker(f"worker-{i}"))
            self.workers.append(worker)
        
        print(f"🚀 {len(self.workers)} worker شروع به کار کردند")
    
    async def stop(self):
        """توقف task queue"""
        self.is_running = False
        
        # لغو همه worker ها
        for worker in self.workers:
            worker.cancel()
        
        # انتظار برای تمام شدن worker ها
        await asyncio.gather(*self.workers, return_exceptions=True)
        self.workers.clear()
        
        print("⏹️ Task Queue متوقف شد")
    
    def add_task(self, 
                 name: str, 
                 func: Callable, 
                 *args, 
                 priority: TaskPriority = TaskPriority.NORMAL,
                 **kwargs) -> str:
        """اضافه کردن task جدید"""
        
        task_id = str(uuid.uuid4())[:8]
        
        task = Task(
            id=task_id,
            name=name,
            func=func,
            args=args,
            kwargs=kwargs,
            priority=priority,
            created_at=datetime.now()
        )
        
        self.tasks[task_id] = task
        
        # اضافه کردن به صف با اولویت
        priority_value = -priority.value  # منفی برای ترتیب نزولی
        asyncio.create_task(self.pending_queue.put((priority_value, task_id)))
        
        self.stats["total_tasks"] += 1
        
        print(f"📝 Task اضافه شد: {name} (ID: {task_id})")
        return task_id
    
    async def _worker(self, worker_name: str):
        """Worker برای اجرای task ها"""
        print(f"👷 {worker_name} شروع به کار کرد")
        
        while self.is_running:
            try:
                # دریافت task از صف
                priority, task_id = await asyncio.wait_for(
                    self.pending_queue.get(), 
                    timeout=1.0
                )
                
                if task_id not in self.tasks:
                    continue
                
                task = self.tasks[task_id]
                
                # شروع اجرای task
                task.status = TaskStatus.RUNNING
                task.started_at = datetime.now()
                self.running_tasks[task_id] = task
                
                print(f"🔄 {worker_name} در حال اجرای: {task.name}")
                
                try:
                    # اجرای task
                    if asyncio.iscoroutinefunction(task.func):
                        result = await task.func(*task.args, **task.kwargs)
                    else:
                        result = task.func(*task.args, **task.kwargs)
                    
                    # تکمیل موفق
                    task.result = result
                    task.status = TaskStatus.COMPLETED
                    task.completed_at = datetime.now()
                    
                    self.stats["completed_tasks"] += 1
                    
                    print(f"✅ {worker_name} تکمیل کرد: {task.name}")
                
                except Exception as e:
                    # خطا در اجرا
                    task.error = str(e)
                    task.status = TaskStatus.FAILED
                    task.completed_at = datetime.now()
                    
                    self.stats["failed_tasks"] += 1
                    
                    print(f"❌ {worker_name} خطا در: {task.name} - {e}")
                
                finally:
                    # انتقال از running به completed
                    if task_id in self.running_tasks:
                        del self.running_tasks[task_id]
                    self.completed_tasks[task_id] = task
                    
                    # محاسبه میانگین زمان اجرا
                    if task.started_at and task.completed_at:
                        execution_time = (task.completed_at - task.started_at).total_seconds()
                        self._update_average_execution_time(execution_time)
            
            except asyncio.TimeoutError:
                # timeout عادی برای بررسی is_running
                continue
            except Exception as e:
                print(f"خطا در {worker_name}: {e}")
    
    def _update_average_execution_time(self, execution_time: float):
        """به‌روزرسانی میانگین زمان اجرا"""
        completed = self.stats["completed_tasks"]
        if completed == 1:
            self.stats["average_execution_time"] = execution_time
        else:
            current_avg = self.stats["average_execution_time"]
            self.stats["average_execution_time"] = (
                (current_avg * (completed - 1) + execution_time) / completed
            )
    
    def get_task_status(self, task_id: str) -> Optional[Dict]:
        """دریافت وضعیت task"""
        if task_id not in self.tasks:
            return None
        
        task = self.tasks[task_id]
        
        return {
            "id": task.id,
            "name": task.name,
            "status": task.status.value,
            "priority": task.priority.name,
            "created_at": task.created_at.isoformat(),
            "started_at": task.started_at.isoformat() if task.started_at else None,
            "completed_at": task.completed_at.isoformat() if task.completed_at else None,
            "result": task.result,
            "error": task.error
        }
    
    def get_queue_stats(self) -> Dict:
        """آمار صف"""
        return {
            **self.stats,
            "pending_tasks": self.pending_queue.qsize(),
            "running_tasks": len(self.running_tasks),
            "completed_tasks_stored": len(self.completed_tasks),
            "workers": len(self.workers),
            "is_running": self.is_running
        }
    
    async def wait_for_task(self, task_id: str, timeout: float = 30.0) -> Optional[Any]:
        """انتظار برای تکمیل task"""
        start_time = datetime.now()
        
        while (datetime.now() - start_time).total_seconds() < timeout:
            if task_id in self.completed_tasks:
                task = self.completed_tasks[task_id]
                if task.status == TaskStatus.COMPLETED:
                    return task.result
                elif task.status == TaskStatus.FAILED:
                    raise Exception(f"Task failed: {task.error}")
            
            await asyncio.sleep(0.1)
        
        raise asyncio.TimeoutError(f"Task {task_id} timeout after {timeout}s")

# Instance سراسری
task_queue = AsyncTaskQueue(max_workers=3)