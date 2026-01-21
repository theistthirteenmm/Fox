"""
تنظیمات پروژه روباه
"""

import os
from pathlib import Path

# مسیرهای پروژه
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"

# تنظیمات AI
AI_CONFIG = {
    "model_name": "partai/dorna-llama3:8b-instruct-q8_0",
    "ollama_url": "http://localhost:11434",
    "max_tokens": 500,
    "temperature": 0.7,
    "top_p": 0.9
}

# تنظیمات حافظه
MEMORY_CONFIG = {
    "short_term_limit": 50,
    "vector_db_path": str(DATA_DIR / "memory"),
    "long_term_path": str(DATA_DIR / "memory" / "long_term"),
    "max_context_items": 5
}

# تنظیمات شخصیت
PERSONALITY_CONFIG = {
    "profile_file": str(DATA_DIR / "personality" / "profile.json"),
    "interactions_file": str(DATA_DIR / "personality" / "interactions.jsonl"),
    "level_up_threshold": 10,  # تعداد تعاملات برای ارتقای سطح
    "max_favorite_topics": 10
}

# تنظیمات سرور
SERVER_CONFIG = {
    "host": "0.0.0.0",
    "port": 8000,
    "reload": True,
    "log_level": "info"
}

# تنظیمات لاگ
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "level": "INFO"
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": str(LOGS_DIR / "robah.log"),
            "formatter": "default",
            "level": "DEBUG",
            "encoding": "utf-8"
        }
    },
    "loggers": {
        "robah": {
            "handlers": ["console", "file"],
            "level": "DEBUG",
            "propagate": False
        }
    }
}

# تنظیمات امنیتی
SECURITY_CONFIG = {
    "allowed_origins": [
        "http://localhost:3000",
        "http://127.0.0.1:3000"
    ],
    "max_message_length": 1000,
    "rate_limit": {
        "messages_per_minute": 30,
        "burst_limit": 5
    }
}

# تنظیمات یادگیری
LEARNING_CONFIG = {
    "auto_save_conversations": True,
    "learning_data_file": str(DATA_DIR / "learning" / "conversations.jsonl"),
    "fine_tune_threshold": 100,  # تعداد مکالمات برای شروع fine-tuning
    "backup_interval": 24 * 60 * 60  # 24 ساعت (ثانیه)
}

# متغیرهای محیطی
def get_env_var(name: str, default=None):
    """دریافت متغیر محیطی با مقدار پیش‌فرض"""
    return os.getenv(name, default)

# تنظیمات قابل تغییر از طریق متغیرهای محیطی
AI_CONFIG["model_name"] = get_env_var("ROBAH_MODEL", AI_CONFIG["model_name"])
AI_CONFIG["ollama_url"] = get_env_var("OLLAMA_URL", AI_CONFIG["ollama_url"])
SERVER_CONFIG["port"] = int(get_env_var("ROBAH_PORT", SERVER_CONFIG["port"]))
SERVER_CONFIG["host"] = get_env_var("ROBAH_HOST", SERVER_CONFIG["host"])

# ایجاد دایرکتوری‌های مورد نیاز
def ensure_directories():
    """اطمینان از وجود دایرکتوری‌های مورد نیاز"""
    directories = [
        DATA_DIR,
        DATA_DIR / "memory",
        DATA_DIR / "personality",
        DATA_DIR / "learning",
        LOGS_DIR
    ]
    
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

# اجرای تابع ایجاد دایرکتوری‌ها
ensure_directories()