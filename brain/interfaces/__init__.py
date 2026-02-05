"""Brain Interfaces - Mock implementations"""

from .physical_interface import physical_interface, EmotionExpression, MovementType
from .speech_handler import speech_handler

__all__ = ['physical_interface', 'EmotionExpression', 'MovementType', 'speech_handler']
