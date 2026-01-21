# راهنمای نصب روباه 🦊

## پیش‌نیازها

### 1. Python 3.8+
```bash
# بررسی نسخه Python
python --version
```

### 2. Node.js 16+
```bash
# بررسی نسخه Node.js
node --version
npm --version
```

### 3. Ollama (هسته هوش مصنوعی)

#### Windows:
1. از [ollama.ai](https://ollama.ai) دانلود کنید
2. فایل نصب را اجرا کنید
3. مدل مورد نیاز را دانلود کنید:
```cmd
ollama pull llama3.2:3b
```

#### Linux/Mac:
```bash
# نصب Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# دانلود مدل
ollama pull llama3.2:3b
```

## نصب خودکار

### روش ساده (توصیه شده):
```bash
python setup.py
```

این اسکریپت تمام مراحل نصب را خودکار انجام می‌دهد.

## نصب دستی

### 1. Backend (Python)
```bash
# ایجاد virtual environment
python -m venv venv

# فعال‌سازی (Windows)
venv\Scripts\activate

# فعال‌سازی (Linux/Mac)
source venv/bin/activate

# نصب dependencies
pip install -r requirements.txt
```

### 2. Frontend (React)
```bash
cd frontend
npm install
```

### 3. ایجاد دایرکتوری‌های مورد نیاز
```bash
mkdir -p data/memory
mkdir -p data/personality
mkdir -p data/learning
mkdir -p logs
```

## راه‌اندازی

### 1. شروع Ollama
```bash
ollama serve
```

### 2. شروع Backend
```bash
# فعال‌سازی virtual environment
source venv/bin/activate  # Linux/Mac
# یا
venv\Scripts\activate     # Windows

# اجرای سرور
python backend/main.py
```

### 3. شروع Frontend
```bash
cd frontend
npm start
```

### راه‌اندازی خودکار
بعد از نصب، می‌توانید از اسکریپت‌های آماده استفاده کنید:

**Windows:**
```cmd
start_robah.bat
```

**Linux/Mac:**
```bash
./start_robah.sh
```

## دسترسی

- **رابط وب**: http://localhost:3000
- **API Backend**: http://localhost:8000
- **مستندات API**: http://localhost:8000/docs

## تنظیمات

### متغیرهای محیطی
```bash
# مدل AI (اختیاری)
export ROBAH_MODEL="llama3.2:3b"

# آدرس Ollama (اختیاری)
export OLLAMA_URL="http://localhost:11434"

# پورت سرور (اختیاری)
export ROBAH_PORT=8000
```

### فایل تنظیمات
تنظیمات در `config/settings.py` قابل تغییر است.

## عیب‌یابی

### مشکلات رایج

#### 1. Ollama در دسترس نیست
```bash
# بررسی وضعیت Ollama
curl http://localhost:11434/api/tags

# راه‌اندازی مجدد
ollama serve
```

#### 2. مدل دانلود نشده
```bash
# دانلود مدل
ollama pull llama3.2:3b

# بررسی مدل‌های نصب شده
ollama list
```

#### 3. خطای پورت
```bash
# تغییر پورت backend
export ROBAH_PORT=8001
python backend/main.py
```

#### 4. مشکل حافظه
```bash
# پاک کردن حافظه (اختیاری)
rm -rf data/memory/*
```

### لاگ‌ها
لاگ‌های سیستم در `logs/robah.log` ذخیره می‌شوند.

## به‌روزرسانی

```bash
# به‌روزرسانی dependencies
pip install -r requirements.txt --upgrade
cd frontend && npm update
```

## پشتیبانی

در صورت مشکل:
1. لاگ‌ها را بررسی کنید
2. مراحل نصب را دوباره انجام دهید
3. مطمئن شوید تمام پیش‌نیازها نصب شده‌اند

---

🦊 **روباه آماده است تا با شما رشد کند!**