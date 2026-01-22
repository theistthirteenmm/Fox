# 🦊 راه‌اندازی سریع روباه

## مشکل فرانت حل شد! ✅

فرانت رو ساده کردم تا مشکلات styled-components حل بشه.

## راه‌اندازی

### 1. Backend (ترمینال اول)
```bash
python backend/main.py
```

### 2. Frontend (ترمینال دوم)  
```bash
cd frontend
npm start
```

### 3. تست سیستم
```bash
python quick_test.py
```

## دسترسی

- **Frontend**: http://localhost:3000
- **Backend**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## ویژگی‌های فعال

✅ **Thinking Messages** - پیام‌های میانی در پردازش طولانی  
✅ **Speech Debug** - دیباگ کامل سیستم صوتی  
✅ **Auto-play Toggle** - کنترل پخش خودکار  
✅ **File Upload** - آپلود فایل با progress bar  
✅ **Voice Recording** - ضبط صدا و تبدیل به متن  
✅ **Memory System** - حافظه بلندمدت  
✅ **Personality Engine** - شخصیت رشدیافته  
✅ **Web Search** - جستجوی اینترنت  
✅ **Code Analysis** - تحلیل کد برنامه‌نویسی  
✅ **User Profiling** - شناخت کاربر  

## تست میکروفون

اگه میکروفون مشکل داره:

1. برو به: http://localhost:8000/speech/debug
2. console مرورگر رو باز کن (F12)
3. دکمه میکروفون رو بزن
4. لاگ‌ها رو بررسی کن

## مشکلات رایج

### Frontend نمی‌آد بالا
```bash
cd frontend
npm install
npm start
```

### Backend خطا می‌ده
```bash
pip install -r requirements.txt
python backend/main.py
```

### Ollama مدل نداره
```bash
ollama pull partai/dorna-llama3:8b-instruct-q8_0
```

## فایل‌های مهم

- `frontend/src/App.tsx` - فرانت ساده شده
- `backend/main.py` - API و WebSocket
- `brain/core.py` - هسته AI با thinking support
- `brain/speech_handler.py` - سیستم صوتی بهبود یافته

## نکات

- فرانت رو ساده کردم تا مشکلات styled-components حل بشه
- thinking messages حالا کار م��‌کنه
- سیستم دیباگ میکروفون کامل شده
- همه ویژگی‌های قبلی حفظ شده‌اند

🎉 **سیستم آماده است!**