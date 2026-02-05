"""
🦊 روباه - دستیار هوش مصنوعی شخصی
Personal AI Assistant that grows with you

Version: 1.0.0
Author: Robah Team
License: MIT
"""

__version__ = "1.0.0"
__author__ = "Robah Team"
__description__ = "دستیار هوش مصنوعی شخصی که با شما رشد می‌کند"

# اطلاعات پروژه
PROJECT_NAME = "روباه"
PROJECT_NAME_EN = "Robah"
PROJECT_DESCRIPTION = "Personal AI Assistant with Persian Language Support"

# ماژول‌های اصلی
MODULES = [
    "backend",      # سرور FastAPI
    "brain",        # هسته هوش مصنوعی
    "config",       # تنظیمات
    "frontend",     # رابط کاربری
]

# قابلیت‌های اصلی
FEATURES = [
    "🧠 هوش مصنوعی پیشرفته",
    "💾 حافظه هوشمند",
    "🎭 شخصیت پویا",
    "🌐 جستجوی وب",
    "📊 یادگیری مستمر",
    "🎨 رابط زیبا",
]

def get_info():
    """اطلاعات پروژه"""
    return {
        "name": PROJECT_NAME,
        "name_en": PROJECT_NAME_EN,
        "version": __version__,
        "description": PROJECT_DESCRIPTION,
        "author": __author__,
        "modules": MODULES,
        "features": FEATURES
    }