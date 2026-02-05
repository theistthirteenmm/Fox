"""
Robah CLI Configuration
"""

import os
import json
from pathlib import Path

# پوشه تنظیمات
CONFIG_DIR = Path.home() / ".robah"
CONFIG_FILE = CONFIG_DIR / "config.json"

DEFAULT_CONFIG = {
    "server": "localhost:8000",
    "voice_enabled": False,
    "typing_effect": True,
    "typing_delay": 0.006,
}


def ensure_config_dir():
    """ایجاد پوشه تنظیمات"""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)


def load_config() -> dict:
    """بارگذاری تنظیمات"""
    ensure_config_dir()
    if CONFIG_FILE.exists():
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                config = json.load(f)
                return {**DEFAULT_CONFIG, **config}
        except Exception:
            pass
    return DEFAULT_CONFIG.copy()


def save_config(config: dict):
    """ذخیره تنظیمات"""
    ensure_config_dir()
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)


def get_server_url() -> str:
    """دریافت آدرس سرور"""
    config = load_config()
    server = config.get("server", "localhost:8000")
    if not server.startswith("http"):
        server = f"http://{server}"
    return server
