"""
Robah Audio Handler
"""

import os
import time
import tempfile
from pathlib import Path
from typing import Optional

# بررسی وجود کتابخانه‌های صوتی
AUDIO_AVAILABLE = False
try:
    import sounddevice as sd
    import soundfile as sf
    import numpy as np
    AUDIO_AVAILABLE = True
except ImportError:
    pass


class AudioHandler:
    """مدیریت ضبط و پخش صدا"""

    def __init__(self):
        self.sample_rate = 16000
        self.temp_dir = Path(tempfile.gettempdir()) / "robah_audio"
        self.temp_dir.mkdir(parents=True, exist_ok=True)

    @property
    def is_available(self) -> bool:
        """آیا صدا در دسترس است؟"""
        return AUDIO_AVAILABLE

    def record(self, seconds: int = 5) -> Optional[str]:
        """ضبط صدا از میکروفون"""
        if not AUDIO_AVAILABLE:
            return None

        try:
            print(f"    Recording for {seconds} seconds...")
            recording = sd.rec(
                int(seconds * self.sample_rate),
                samplerate=self.sample_rate,
                channels=1,
                dtype='float32'
            )
            sd.wait()

            # ذخیره به فایل
            filename = self.temp_dir / f"voice_{int(time.time())}.wav"
            sf.write(str(filename), recording, self.sample_rate)
            return str(filename)

        except Exception as e:
            print(f"    Recording error: {e}")
            return None

    def play(self, audio_data: bytes) -> bool:
        """پخش صدا"""
        if not AUDIO_AVAILABLE:
            return False

        try:
            # ذخیره موقت
            temp_file = self.temp_dir / f"play_{int(time.time())}.wav"
            with open(temp_file, "wb") as f:
                f.write(audio_data)

            # پخش
            data, sr = sf.read(str(temp_file), dtype='float32')
            sd.play(data, sr)
            sd.wait()

            # حذف فایل موقت
            temp_file.unlink(missing_ok=True)
            return True

        except Exception as e:
            print(f"    Playback error: {e}")
            return False

    def play_file(self, filepath: str) -> bool:
        """پخش فایل صوتی"""
        if not AUDIO_AVAILABLE:
            return False

        try:
            data, sr = sf.read(filepath, dtype='float32')
            sd.play(data, sr)
            sd.wait()
            return True
        except Exception as e:
            print(f"    Playback error: {e}")
            return False

    def cleanup(self):
        """پاکسازی فایل‌های موقت"""
        try:
            for f in self.temp_dir.glob("*.wav"):
                f.unlink(missing_ok=True)
        except Exception:
            pass
