# 🏗️ ساختار پروژه روباه

## 📁 ساختار کلی بهینه

```
robah/
├── 📚 docs/                    # مستندات کامل
│   ├── README.md               # راهنمای اصلی
│   ├── INSTALLATION.md         # راهنمای نصب
│   ├── USAGE_GUIDE.md          # راهنمای استفاده
│   ├── FEATURES.md             # قابلیت‌ها
│   ├── PROJECT_STRUCTURE.md    # ساختار پروژه
│   ├── WEB_SEARCH.md           # جستجوی وب
│   ├── DATASET_SYSTEM.md       # سیستم دیتاست
│   ├── API_REFERENCE.md        # مرجع API
│   └── DEVELOPMENT.md          # راهنمای توسعه
│
├── 🖥️ backend/                 # سرور FastAPI
│   ├── __init__.py
│   └── main.py                 # سرور اصلی
│
├── 🧠 brain/                   # هسته هوش مصنوعی
│   ├── __init__.py
│   ├── core.py                 # هسته اصلی AI
│   ├── memory.py               # سیستم حافظه
│   ├── personality.py          # موتور شخصیت
│   ├── web_search.py           # جستجوی وب
│   └── dataset_manager.py      # مدیر دیتاست
│
├── ⚙️ config/                  # تنظیمات سیستم
│   ├── __init__.py
│   └── settings.py             # تنظیمات اصلی
│
├── 💾 data/                    # داده‌ها و حافظه
│   ├── datasets/               # دیتاست‌های آموزشی
│   │   ├── conversation_patterns.json
│   │   ├── emotion_responses.json
│   │   ├── learning_data.jsonl
│   │   └── topic_knowledge.json
│   ├── learning/               # داده‌های یادگیری
│   │   └── conversations.jsonl
│   ├── memory/                 # حافظه ChromaDB
│   │   └── chroma.sqlite3
│   ├── personality/            # داده‌های شخصیت
│   │   ├── interactions.jsonl
│   │   └── profile.json
│   └── prompts/                # قالب‌های پرامپت
│       └── templates.json
│
├── 🎨 frontend/                # رابط کاربری React
│   ├── public/                 # فایل‌های عمومی
│   │   ├── index.html
│   │   ├── manifest.json
│   │   ├── favicon.ico
│   │   └── favicon.txt
│   ├── src/                    # کد منبع
│   │   ├── components/         # کامپوننت‌های React
│   │   │   ├── ChatInterface.tsx
│   │   │   ├── MessageBubble.tsx
│   │   │   ├── MessageInput.tsx
│   │   │   └── StatusBar.tsx
│   │   ├── App.tsx             # کامپوننت اصلی
│   │   ├── App.css             # استایل‌های اصلی
│   │   ├── index.tsx           # نقطه ورود
│   │   └── index.css           # استایل‌های پایه
│   ├── package.json            # Dependencies
│   ├── craco.config.js         # تنظیمات React
│   └── .env                    # متغیرهای محیطی
│
├── 📝 logs/                    # فایل‌های لاگ
│   └── robah.log               # لاگ اصلی
│
├── 🛠️ scripts/                # اسکریپت‌های کمکی
│   ├── start_robah.bat         # راه‌اندازی Windows
│   ├── start_robah.sh          # راه‌اندازی Linux/Mac
│   ├── run.bat                 # اجرای سریع Windows
│   ├── run.sh                  # اجرای سریع Linux/Mac
│   ├── stop_robah.bat          # توقف Windows
│   └── stop_robah.sh           # توقف Linux/Mac
│
├── 🐍 venv/                    # محیط مجازی Python
│
├── 📋 README.md                # معرفی اصلی
├── 📖 QUICKSTART.md            # راهنمای سریع
├── 🛠️ INSTALL.md               # راهنمای نصب
├── 📜 SCRIPTS.md               # راهنمای اسکریپت‌ها
├── ⚙️ setup.py                 # نصب خودکار
├── 📦 requirements.txt         # Dependencies Python
├── 🚫 .gitignore               # فایل‌های نادیده Git
└── 🔧 .vscode/                 # تنظیمات VS Code
    └── settings.json
```

## 🎯 توضیح ساختار

### 📚 مستندات (`docs/`)
- تمام راهنماها و مستندات فنی
- سازماندهی موضوعی و منطقی
- لینک‌های متقابل برای ناوبری آسان

### 🖥️ Backend (`backend/`)
- سرور FastAPI
- مدیریت WebSocket و API
- ارتباط با سایر ماژول‌ها

### 🧠 Brain (`brain/`)
- هسته هوش مصنوعی
- سیستم حافظه و شخصیت
- جستجوی وب و یادگیری

### ⚙️ Config (`config/`)
- تنظیمات مرکزی
- پیکربندی سیستم

### 💾 Data (`data/`)
- ذخیره‌سازی داده‌ها
- دسته‌بندی بر اساس نوع

### 🎨 Frontend (`frontend/`)
- رابط کاربری React
- کامپوننت‌های مدولار
- استایل‌های مدرن

### 🛠️ Scripts (`scripts/`)
- اسکریپت‌های راه‌اندازی
- ابزارهای کمکی

## 🔄 جریان داده

```
User → Frontend → WebSocket → Backend → Brain → Memory/Personality
                                    ↓
                              Web Search ← Internet
                                    ↓
                              Dataset Manager ← Learning Data
                                    ↓
                              Response → Frontend → User
```

## 📦 Dependencies

### Python:
- FastAPI (سرور)
- ChromaDB (حافظه)
- Requests (HTTP)
- WebSockets (ارتباط)

### Node.js:
- React (رابط کاربری)
- TypeScript (توسعه)
- WebSocket (ارتباط)

## 🎨 Design Patterns

- **MVC**: جداسازی منطق، داده و نمایش
- **Modular**: ماژول‌های مستقل
- **Event-Driven**: ارتباط بر اساس رویداد
- **Layered**: لایه‌بندی منطقی

## 🔒 امنیت

- محیط مجازی Python
- متغیرهای محیطی
- Validation ورودی‌ها
- CORS تنظیم شده