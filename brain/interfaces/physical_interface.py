"""
Physical Interface - Mock Implementation
For future robot/hardware integration
"""

from enum import Enum


class EmotionExpression(Enum):
    HAPPY = "happy"
    SAD = "sad"
    SURPRISED = "surprised"
    THINKING = "thinking"
    NEUTRAL = "neutral"
    CONCERNED = "concerned"
    CURIOUS = "curious"
    EXCITED = "excited"


class MovementType(Enum):
    NOD = "nod"
    SHAKE = "shake"
    TILT = "tilt"
    WAVE = "wave"


class PhysicalInterface:
    """Mock physical interface for future hardware"""

    def __init__(self):
        self.current_emotion = EmotionExpression.NEUTRAL
        self.is_moving = False

    async def express_emotion(self, emotion: EmotionExpression, intensity: float = 0.5):
        """Express emotion (mock)"""
        self.current_emotion = emotion

    async def move_to_owner(self, urgency: float = 0.5):
        """Move to owner (mock)"""
        pass

    async def perform_task_gesture(self, gesture: str):
        """Perform gesture (mock)"""
        pass

    def get_physical_status(self) -> dict:
        """Get current status"""
        return {
            "emotion": self.current_emotion.value,
            "is_moving": self.is_moving,
            "hardware": "mock"
        }


# Singleton instance
physical_interface = PhysicalInterface()
