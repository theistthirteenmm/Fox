# 👨‍💻 راهنمای توسعه

## 🏗️ معماری سیستم

### 🔄 جریان داده:
```
User Input → Frontend → WebSocket → Backend → 
AI Brain → Memory/Personality → Response → 
Frontend → User
```

### 📦 ماژول‌های اصلی:

#### 🖥️ Backend (FastAPI):
- `main.py`: سرور اصلی و WebSocket
- مدیریت session ها
- API endpoints

#### 🧠 Brain:
- `core.py`: هسته AI و تولید پاسخ
- `memory.py`: سیستم حافظه سه‌لایه
- `personality.py`: موتور شخصیت پویا
- `web_search.py`: جستجوی وب خودکار
- `dataset_manager.py`: یادگیری و دیتاست

#### 🎨 Frontend (React):
- `App.tsx`: کامپوننت اصلی
- `components/`: کامپوننت‌های UI
- WebSocket client

## 🛠️ محیط توسعه

### 📋 پیش‌نیازها:
```bash
# Python dependencies
pip install -r requirements.txt

# Node.js dependencies
cd frontend && npm install
```

### 🔧 تنظیمات IDE:
- Python: VS Code + Python extension
- React: VS Code + ES7+ React snippets
- TypeScript: strict mode enabled

### 🧪 تست:
```bash
# Backend tests
pytest

# Frontend tests
cd frontend && npm test
```

## 🔄 Workflow توسعه

### 1️⃣ Feature جدید:
```bash
git checkout -b feature/new-feature
# توسعه
git commit -m "feat: add new feature"
git push origin feature/new-feature
```

### 2️⃣ Bug fix:
```bash
git checkout -b fix/bug-description
# رفع باگ
git commit -m "fix: resolve bug"
```

### 3️⃣ Documentation:
```bash
# به‌روزرسانی docs/
git commit -m "docs: update documentation"
```

## 📊 مانیتورینگ

### 🔍 Debugging:
- Backend logs: `logs/robah.log`
- Frontend: Browser DevTools
- AI responses: Console output

### 📈 Performance:
- Memory usage monitoring
- Response time tracking
- WebSocket connection health