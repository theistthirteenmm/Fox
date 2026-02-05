"""
Speech Handler - Mock Implementation
"""


class SpeechHandler:
    """Mock speech handler"""

    def __init__(self):
        self.is_listening = False
        self.voice_enabled = False
        self.initialized = False

    async def initialize(self):
        """Initialize speech handler"""
        self.initialized = True

    async def speech_to_text(self, audio_path: str) -> str:
        """Convert speech to text (mock)"""
        return ""

    async def text_to_speech(self, text: str) -> bytes:
        """Convert text to speech (mock)"""
        return b""

    def is_available(self) -> bool:
        """Check if speech is available"""
        return False

    def get_status(self) -> dict:
        """Get status"""
        return {
            "initialized": self.initialized,
            "available": False
        }


# Singleton
speech_handler = SpeechHandler()
