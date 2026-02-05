# 🛠️ نصب و راه‌اندازی روباه

## 📋 پیش‌نیازها

### 🐍 Python 3.11+
```bash
python --version
```

### 🦙 Ollama
```bash
# Windows
winget install Ollama.Ollama

# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.ai/install.sh | sh
```

### 📦 Node.js 18+
```bash
node --version
npm --version
```

## 🚀 نصب سریع

### 1️⃣ کلون پروژه:
```bash
git clone https://github.com/your-repo/robah.git
cd robah
```

### 2️⃣ اجرای اسکریپت نصب:

#### Windows:
```cmd
start.bat
```

#### Linux/macOS:
```bash
chmod +x start_robah.sh
./start_robah.sh
```

## 🔧 نصب دستی

### 1️⃣ محیط مجازی Python:
```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate     # Windows
```

### 2️⃣ نصب dependencies:
```bash
pip install -r requirements.txt
```

### 3️⃣ دانلود مدل AI:
```bash
ollama pull partai/dorna-llama3:8b-instruct-q8_0
```

### 4️⃣ نصب frontend:
```bash
cd frontend
npm install
cd ..
```

### 5️⃣ راه‌اندازی:
```bash
# Terminal 1 - Backend
python -m backend.main

# Terminal 2 - Frontend  
cd frontend
npm start
```

## ✅ تست نصب

### 🌐 دسترسی:
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Status: http://localhost:8000/status

### 🧪 تست سریع:
```bash
curl http://localhost:8000/status
```