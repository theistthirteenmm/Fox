"""
Robah API Client
"""

import requests
from typing import Optional
from .config import get_server_url


class RobahClient:
    """کلاینت برای اتصال به سرور روباه"""

    def __init__(self, server_url: Optional[str] = None):
        self.server_url = server_url or get_server_url()
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
        })

    def is_available(self) -> bool:
        """بررسی در دسترس بودن سرور"""
        try:
            response = self.session.get(
                f"{self.server_url}/status",
                timeout=3
            )
            return response.status_code == 200
        except Exception:
            return False

    def chat(self, message: str) -> Optional[str]:
        """ارسال پیام و دریافت پاسخ"""
        try:
            response = self.session.post(
                f"{self.server_url}/chat",
                json={"message": message},
                timeout=60
            )
            if response.status_code == 200:
                data = response.json()
                return data.get("response")
        except Exception:
            pass
        return None

    def get_status(self) -> Optional[dict]:
        """دریافت وضعیت سرور"""
        try:
            response = self.session.get(
                f"{self.server_url}/status",
                timeout=5
            )
            if response.status_code == 200:
                return response.json()
        except Exception:
            pass
        return None

    def speech_to_text(self, audio_path: str) -> Optional[str]:
        """تبدیل صدا به متن"""
        try:
            with open(audio_path, "rb") as f:
                response = self.session.post(
                    f"{self.server_url}/speech/speech-to-text",
                    files={"audio_file": f},
                    timeout=60
                )
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    return data.get("text", "").strip()
        except Exception:
            pass
        return None

    def text_to_speech(self, text: str) -> Optional[bytes]:
        """تبدیل متن به صدا"""
        try:
            response = self.session.post(
                f"{self.server_url}/speech/text-to-speech",
                data={"text": text},
                timeout=60
            )
            if response.status_code == 200:
                return response.content
        except Exception:
            pass
        return None
