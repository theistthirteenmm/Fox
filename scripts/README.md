# 🛠️ اسکریپت‌های روباه

این پوشه شامل تمام اسکریپت‌های راه‌اندازی و مدیریت روباه است.

## 📋 فهرست اسکریپت‌ها

### 🚀 راه‌اندازی سیستم
- `start_robah.bat` / `start_robah.sh` - راه‌اندازی کامل روباه
- `run.bat` / `run.sh` - راه‌اندازی سریع
- `stop_robah.bat` / `stop_robah.sh` - توقف سرویس‌ها

### 🤖 مدیریت مدل‌ها
- `download_models.bat` / `download_models.sh` - دانلود همه مدل‌ها
- `migrate_models.bat` - انتقال مدل‌ها از C به پروژه
- `setup_models_path.bat` - تنظیم مسیر مدل‌ها
- `cleanup_old_models.bat` - پاک‌سازی مدل‌های قدیمی

## 🎯 استفاده

### راه‌اندازی اولیه:
```bash
# Windows
scripts\start_robah.bat

# Linux/Mac
./scripts/start_robah.sh
```

### دانلود مدل‌ها:
```bash
# Windows
scripts\download_models.bat

# Linux/Mac  
./scripts/download_models.sh
```

### انتقال مدل‌ها (Windows):
```bash
# انتقال از C:\Users\[user]\.ollama\models به پروژه
scripts\migrate_models.bat

# پاک‌سازی مدل‌های قدیمی (بعد از اطمینان)
scripts\cleanup_old_models.bat
```

## 📊 مدل‌های پشتیبانی شده

| مدل | اندازه | کاربرد | دستور |
|-----|--------|---------|--------|
| `partai/dorna-llama3:8b-instruct-q8_0` | 8.5GB | فارسی | نصب شده |
| `llama4:scout` | 50GB | قدرتمند | `scripts\download_models.bat` |
| `codellama:13b` | 7GB | کد | `scripts\download_models.bat` |
| `llama4:scout-q4` | 10GB | سریع | `scripts\download_models.bat` |

## 🔧 سفارشی‌سازی

متغیرهای محیطی قابل تنظیم:

```bash
# مسیر مدل‌ها
OLLAMA_MODELS=D:\fox\models

# پورت‌ها
ROBAH_PORT=8000
FRONTEND_PORT=3000

# آدرس Ollama
OLLAMA_URL="http://localhost:11434"
```