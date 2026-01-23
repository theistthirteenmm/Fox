"""
🤖 رابط سخت‌افزار فیزیکی روباه
آماده‌سازی برای پیاده‌سازی روی ربات متحرک
"""

import asyncio
import json
from datetime import datetime
from typing import Dict, List, Optional, Tuple
from enum import Enum
from dataclasses import dataclass
import math

class MovementType(Enum):
    WALK = "walk"
    TURN = "turn"
    STOP = "stop"
    GESTURE = "gesture"
    HEAD_MOVE = "head_move"
    APPROACH = "approach"
    RETREAT = "retreat"

class EmotionExpression(Enum):
    HAPPY = "happy"
    CURIOUS = "curious"
    THINKING = "thinking"
    CONCERNED = "concerned"
    EXCITED = "excited"
    CALM = "calm"
    FOCUSED = "focused"

class SensorType(Enum):
    CAMERA = "camera"
    MICROPHONE = "microphone"
    PROXIMITY = "proximity"
    TOUCH = "touch"
    TEMPERATURE = "temperature"
    LIGHT = "light"
    MOTION = "motion"

@dataclass
class PhysicalAction:
    """عمل فیزیکی"""
    action_type: MovementType
    parameters: Dict
    duration: float
    priority: int
    emotion: Optional[EmotionExpression] = None

@dataclass
class SensorData:
    """داده حسگر"""
    sensor_type: SensorType
    value: any
    timestamp: datetime
    confidence: float

class PhysicalInterface:
    def __init__(self):
        self.is_physical_mode = False  # فعلاً در حالت شبیه‌سازی
        self.current_position = {"x": 0, "y": 0, "rotation": 0}
        self.current_emotion = EmotionExpression.CALM
        self.battery_level = 1.0
        self.is_moving = False
        
        # صف اعمال فیزیکی
        self.action_queue = asyncio.Queue()
        self.current_action = None
        
        # داده‌های حسگرها
        self.sensor_data = {}
        self.environmental_awareness = {
            "room_map": {},
            "known_objects": {},
            "owner_location": None,
            "obstacles": []
        }
        
        # رفتارهای شخصیتی فیزیکی
        self.physical_personality = {
            "movement_speed": 0.7,      # سرعت حرکت (0-1)
            "gesture_frequency": 0.5,   # تکرار حرکات (0-1)
            "personal_space": 1.0,      # فاصله شخصی (متر)
            "eye_contact_level": 0.8,   # سطح تماس چشمی (0-1)
            "expressiveness": 0.7       # بیان احساسات (0-1)
        }
        
        print("🤖 رابط سخت‌افزار فیزیکی آماده شد (حالت شبیه‌سازی)")
    
    async def express_emotion(self, emotion: EmotionExpression, intensity: float = 1.0):
        """بیان احساسات از طریق حرکات فیزیکی"""
        
        self.current_emotion = emotion
        
        # تعریف حرکات برای هر احساس
        emotion_actions = {
            EmotionExpression.HAPPY: [
                PhysicalAction(MovementType.GESTURE, {"type": "wave"}, 2.0, 1),
                PhysicalAction(MovementType.HEAD_MOVE, {"direction": "nod"}, 1.0, 2)
            ],
            EmotionExpression.CURIOUS: [
                PhysicalAction(MovementType.HEAD_MOVE, {"direction": "tilt"}, 1.5, 1),
                PhysicalAction(MovementType.APPROACH, {"distance": 0.3}, 2.0, 2)
            ],
            EmotionExpression.THINKING: [
                PhysicalAction(MovementType.HEAD_MOVE, {"direction": "look_up"}, 2.0, 1),
                PhysicalAction(MovementType.GESTURE, {"type": "chin_touch"}, 3.0, 2)
            ],
            EmotionExpression.CONCERNED: [
                PhysicalAction(MovementType.HEAD_MOVE, {"direction": "shake"}, 1.0, 1),
                PhysicalAction(MovementType.APPROACH, {"distance": 0.5}, 1.5, 2)
            ]
        }
        
        if emotion in emotion_actions:
            for action in emotion_actions[emotion]:
                action.emotion = emotion
                await self.action_queue.put(action)
        
        print(f"🎭 بیان احساس: {emotion.value} با شدت {intensity}")
    
    async def move_to_owner(self, urgency: float = 0.5):
        """حرکت به سمت مالک"""
        
        if not self.environmental_awareness["owner_location"]:
            # جستجوی مالک
            await self.search_for_owner()
            return
        
        owner_pos = self.environmental_awareness["owner_location"]
        
        # محاسبه مسیر
        path = self._calculate_path_to_position(owner_pos)
        
        # تعیین فاصله مناسب (احترام به فضای شخصی)
        approach_distance = self.physical_personality["personal_space"]
        
        # ایجاد عمل حرکت
        move_action = PhysicalAction(
            action_type=MovementType.APPROACH,
            parameters={
                "target": owner_pos,
                "stop_distance": approach_distance,
                "path": path,
                "speed": min(1.0, urgency + 0.3)
            },
            duration=self._estimate_movement_time(path),
            priority=int(urgency * 10),
            emotion=EmotionExpression.FOCUSED
        )
        
        await self.action_queue.put(move_action)
        print(f"🚶 حرکت به سمت مالک با فوریت {urgency}")
    
    async def search_for_owner(self):
        """جستجوی مالک در محیط"""
        
        search_action = PhysicalAction(
            action_type=MovementType.TURN,
            parameters={
                "angle": 360,
                "speed": 0.3,
                "scan_mode": True
            },
            duration=10.0,
            priority=8,
            emotion=EmotionExpression.CURIOUS
        )
        
        await self.action_queue.put(search_action)
        print("🔍 جستجوی مالک...")
    
    async def respond_to_call(self, call_location: Tuple[float, float]):
        """پاسخ به صدا زدن مالک"""
        
        # چرخش به سمت صدا
        turn_angle = self._calculate_turn_angle(call_location)
        
        turn_action = PhysicalAction(
            action_type=MovementType.TURN,
            parameters={"angle": turn_angle, "speed": 0.8},
            duration=abs(turn_angle) / 90,  # زمان بر اساس زاویه
            priority=9,
            emotion=EmotionExpression.EXCITED
        )
        
        await self.action_queue.put(turn_action)
        
        # حرکت به سمت مالک
        await self.move_to_owner(urgency=0.8)
        
        print(f"📞 پاسخ به صدای مالک از موقعیت {call_location}")
    
    async def perform_task_gesture(self, task_type: str):
        """انجام حرکت مرتبط با نوع کار"""
        
        task_gestures = {
            "presentation": [
                PhysicalAction(MovementType.GESTURE, {"type": "point"}, 2.0, 5),
                PhysicalAction(MovementType.HEAD_MOVE, {"direction": "look_at_screen"}, 1.0, 4)
            ],
            "explanation": [
                PhysicalAction(MovementType.GESTURE, {"type": "open_hands"}, 1.5, 5),
                PhysicalAction(MovementType.HEAD_MOVE, {"direction": "face_owner"}, 1.0, 6)
            ],
            "thinking": [
                PhysicalAction(MovementType.HEAD_MOVE, {"direction": "look_up"}, 2.0, 3),
                PhysicalAction(MovementType.GESTURE, {"type": "chin_touch"}, 3.0, 2)
            ],
            "agreement": [
                PhysicalAction(MovementType.HEAD_MOVE, {"direction": "nod"}, 1.0, 7),
                PhysicalAction(MovementType.GESTURE, {"type": "thumbs_up"}, 1.5, 6)
            ]
        }
        
        if task_type in task_gestures:
            for gesture in task_gestures[task_type]:
                await self.action_queue.put(gesture)
        
        print(f"👋 انجام حرکت برای: {task_type}")
    
    async def maintain_attention(self):
        """حفظ توجه و حضور فعال"""
        
        # حرکات ظریف برای نشان دادن زنده بودن
        subtle_actions = [
            PhysicalAction(MovementType.HEAD_MOVE, {"direction": "slight_tilt"}, 0.5, 1),
            PhysicalAction(MovementType.GESTURE, {"type": "micro_adjustment"}, 0.3, 1)
        ]
        
        # انتخاب تصادفی حرکت ظریف
        import random
        action = random.choice(subtle_actions)
        await self.action_queue.put(action)
    
    async def process_sensor_input(self, sensor_type: SensorType, data: any) -> Dict:
        """پردازش ورودی حسگرها"""
        
        sensor_reading = SensorData(
            sensor_type=sensor_type,
            value=data,
            timestamp=datetime.now(),
            confidence=0.8
        )
        
        self.sensor_data[sensor_type.value] = sensor_reading
        
        # تحلیل داده‌های حسگر
        analysis = await self._analyze_sensor_data(sensor_reading)
        
        # واکنش به داده‌های مهم
        if analysis.get("requires_action", False):
            await self._react_to_sensor_data(analysis)
        
        return analysis
    
    async def _analyze_sensor_data(self, sensor_data: SensorData) -> Dict:
        """تحلیل داده‌های حسگر"""
        
        analysis = {"requires_action": False}
        
        if sensor_data.sensor_type == SensorType.PROXIMITY:
            distance = sensor_data.value
            if distance < 0.5:  # خیلی نزدیک
                analysis.update({
                    "requires_action": True,
                    "action_type": "retreat",
                    "reason": "too_close"
                })
            elif distance > 3.0:  # خیلی دور
                analysis.update({
                    "requires_action": True,
                    "action_type": "approach",
                    "reason": "too_far"
                })
        
        elif sensor_data.sensor_type == SensorType.MOTION:
            if sensor_data.value:  # حرکت تشخیص داده شد
                analysis.update({
                    "requires_action": True,
                    "action_type": "attention",
                    "reason": "motion_detected"
                })
        
        return analysis
    
    async def _react_to_sensor_data(self, analysis: Dict):
        """واکنش به داده‌های حسگر"""
        
        action_type = analysis.get("action_type")
        
        if action_type == "retreat":
            retreat_action = PhysicalAction(
                action_type=MovementType.RETREAT,
                parameters={"distance": 0.5},
                duration=2.0,
                priority=7,
                emotion=EmotionExpression.CONCERNED
            )
            await self.action_queue.put(retreat_action)
        
        elif action_type == "approach":
            approach_action = PhysicalAction(
                action_type=MovementType.APPROACH,
                parameters={"distance": 0.3},
                duration=3.0,
                priority=5,
                emotion=EmotionExpression.CURIOUS
            )
            await self.action_queue.put(approach_action)
        
        elif action_type == "attention":
            await self.express_emotion(EmotionExpression.CURIOUS, 0.7)
    
    def _calculate_path_to_position(self, target_pos: Tuple[float, float]) -> List[Tuple[float, float]]:
        """محاسبه مسیر به موقعیت هدف"""
        
        current_pos = (self.current_position["x"], self.current_position["y"])
        
        # مسیر ساده (خط مستقیم) - می‌تواند پیچیده‌تر شود
        path = [current_pos, target_pos]
        
        # در آینده: obstacle avoidance, path optimization
        
        return path
    
    def _estimate_movement_time(self, path: List[Tuple[float, float]]) -> float:
        """تخمین زمان حرکت"""
        
        total_distance = 0
        for i in range(len(path) - 1):
            dx = path[i+1][0] - path[i][0]
            dy = path[i+1][1] - path[i][1]
            distance = math.sqrt(dx*dx + dy*dy)
            total_distance += distance
        
        speed = self.physical_personality["movement_speed"]
        return total_distance / (speed * 0.5)  # 0.5 m/s base speed
    
    def _calculate_turn_angle(self, target_pos: Tuple[float, float]) -> float:
        """محاسبه زاویه چرخش"""
        
        current_pos = (self.current_position["x"], self.current_position["y"])
        current_rotation = self.current_position["rotation"]
        
        dx = target_pos[0] - current_pos[0]
        dy = target_pos[1] - current_pos[1]
        
        target_angle = math.degrees(math.atan2(dy, dx))
        turn_angle = target_angle - current_rotation
        
        # نرمال‌سازی زاویه
        while turn_angle > 180:
            turn_angle -= 360
        while turn_angle < -180:
            turn_angle += 360
        
        return turn_angle
    
    async def start_physical_loop(self):
        """شروع حلقه اصلی فیزیکی"""
        
        print("🔄 شروع حلقه فیزیکی روباه")
        
        while True:
            try:
                # پردازش صف اعمال
                if not self.action_queue.empty():
                    action = await self.action_queue.get()
                    await self._execute_physical_action(action)
                
                # حفظ توجه (هر 30 ثانیه)
                if not self.is_moving:
                    await asyncio.sleep(30)
                    await self.maintain_attention()
                
                await asyncio.sleep(0.1)  # 10 FPS
                
            except Exception as e:
                print(f"خطا در حلقه فیزیکی: {e}")
                await asyncio.sleep(1)
    
    async def _execute_physical_action(self, action: PhysicalAction):
        """اجرای عمل فیزیکی"""
        
        self.current_action = action
        self.is_moving = True
        
        print(f"🎬 اجرای عمل: {action.action_type.value} - {action.parameters}")
        
        # شبیه‌سازی اجرای عمل
        await asyncio.sleep(action.duration)
        
        # به‌روزرسانی وضعیت
        if action.action_type == MovementType.TURN:
            self.current_position["rotation"] += action.parameters.get("angle", 0)
        elif action.action_type in [MovementType.APPROACH, MovementType.WALK]:
            # به‌روزرسانی موقعیت (ساده‌سازی شده)
            pass
        
        self.is_moving = False
        self.current_action = None
        
        print(f"✅ عمل تکمیل شد: {action.action_type.value}")
    
    def get_physical_status(self) -> Dict:
        """وضعیت فیزیکی فعلی"""
        
        return {
            "position": self.current_position,
            "emotion": self.current_emotion.value,
            "battery_level": self.battery_level,
            "is_moving": self.is_moving,
            "current_action": self.current_action.action_type.value if self.current_action else None,
            "queue_size": self.action_queue.qsize(),
            "sensor_count": len(self.sensor_data),
            "physical_mode": self.is_physical_mode
        }
    
    def enable_physical_mode(self):
        """فعال‌سازی حالت فیزیکی واقعی"""
        self.is_physical_mode = True
        print("🤖 حالت فیزیکی واقعی فعال شد!")
    
    def disable_physical_mode(self):
        """غیرفعال‌سازی حالت فیزیکی"""
        self.is_physical_mode = False
        print("💻 بازگشت به حالت شبیه‌سازی")

# Instance سراسری
physical_interface = PhysicalInterface()