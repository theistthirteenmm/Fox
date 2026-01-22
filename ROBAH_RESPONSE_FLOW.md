# 🦊 فرایند پاسخ‌دهی روباه - گراف کامل

## مراحل کلی فرایند

```
کاربر پیام می‌فرسته → Frontend → WebSocket → Backend → AI Brain → پاسخ برمی‌گرده
```

## گراف تفصیلی فرایند

### 1️⃣ **Frontend - دریافت پیام کاربر**
```
MessageInput.tsx
    ↓
کاربر پیام می‌نویسه/صدا ضبط می‌کنه
    ↓
handleSendMessage() فراخوانی می‌شه
    ↓
App.tsx - sendMessage()
    ↓
WebSocket.send() - ارسال به backend
```

### 2️⃣ **Backend - دریافت و پردازش اولیه**
```
backend/main.py - websocket_endpoint()
    ↓
ws.receive_text() - دریافت پیام
    ↓
JSON.parse() - تبدیل به object
    ↓
thinking_callback تعریف می‌شه
    ↓
process_user_message() فراخوانی می‌شه
```

### 3️⃣ **Memory Management - ذخیره پیام**
```
process_user_message()
    ↓
memory_manager.store_conversation("user", message)
    ↓
brain/memory.py - MemoryManager.store_conversation()
    ↓
- ذخیره در short_term_memory (RAM)
- اگر مهم باشه → ذخیره در ChromaDB
```

### 4️⃣ **Personality Analysis - تحلیل شخصیت**
```
process_user_message()
    ↓
personality_engine.analyze_interaction(message)
    ↓
brain/personality.py - PersonalityEngine
    ↓
- تحلیل احساسات پیام
- به‌روزرسانی سطح شخصیت
- تعیین mood فعلی
```

### 5️⃣ **AI Brain - تولید پاسخ اصلی**
```
ai_brain.generate_response()
    ↓
brain/core.py - AIBrain.generate_response()
    ↓
thinking_callback("صبور باشید، در حال آماده کردن جواب روباه...")
```

### 6️⃣ **Code Analysis - تشخیص کد (اختیاری)**
```
analyze_user_code(message)
    ↓
detect_code_in_message() - آیا کد داره؟
    ↓
اگر کد داشت:
    ↓
brain/code_analyzer.py
    ↓
- تحلیل syntax
- پیدا کردن مشکلات
- پیشنهاد بهبود
```

### 7️⃣ **User Profiling - تحلیل کاربر**
```
user_profiler.analyze_message(message)
    ↓
brain/user_profiler.py
    ↓
- تحلیل علایق کاربر
- به‌روزرسانی پروفایل
- استخراج اطلاعات شخصی
```

### 8️⃣ **Dataset Analysis - تحلیل پیام**
```
dataset_manager.analyze_user_message(message, context)
    ↓
brain/dataset_manager.py
    ↓
- تشخیص emotion (happy, sad, curious, neutral)
- تشخیص topic (programming, general, etc.)
- تشخیص intent (conversation, question, definition)
- تشخیص complexity (simple, medium, complex)
- پیدا کردن patterns (greeting, etc.)
```

### 9️⃣ **Dataset Response Check - بررسی پاسخ آماده**
```
dataset_manager.get_suggested_response(analysis)
    ↓
شرایط بررسی:
- complexity نباشه complex/technical
- topic نباشه تخصصی
- intent باشه conversation
    ↓
اگر شرایط OK:
    ↓
پاسخ از دیتاست برمی‌گرده
    ↓
FINISH - پایان فرایند
```

### 🔟 **Web Search Check - بررسی نیاز به جستجو**
```
web_search.should_search_web(message, context)
    ↓
brain/web_search.py
    ↓
شرایط جستجو:
- سؤالات آب و هوا
- اخبار جدید
- اطلاعات به‌روز
    ↓
اگر نیاز باشه:
    ↓
web_search.search_and_summarize(message)
    ↓
- جستجو در موتورهای مختلف
- خلاصه‌سازی نتایج
```

### 1️⃣1️⃣ **Prompt Building - ساخت پرامپت**
```
_build_prompt(message, context, personality, web_info)
    ↓
ساخت prompt شامل:
- System prompt (معرفی روباه)
- Context از حافظه (آخرین 2 مکالمه)
- اطلاعات وب (اگر موجود باشه)
- پیام کاربر
```

### 1️⃣2️⃣ **AI Model Generation - تولید پاسخ**
```
_generate_raw(prompt, thinking_callback)
    ↓
ارسال به Ollama API:
- Model: partai/dorna-llama3:8b-instruct-q8_0
- Temperature: 0.7
- Max tokens: 150
- Timeout: 30 seconds
    ↓
2 تلاش برای دریافت پاسخ
    ↓
اگر موفق: پاسخ برمی‌گرده
اگر ناموفق: fallback response
```

### 1️⃣3️⃣ **Fallback Response - پاسخ جایگزین**
```
_generate_fallback_response(message, web_info)
    ↓
اولویت‌ها:
1. اگر web_info داره → اطلاعات وب
2. اگر سؤال آب و هوا → پیشنهاد سایت هواشناسی
3. اگر سؤال عمومی → "مشکل فنی دارم"
4. اگر سلام → پاسخ دوستانه
```

### 1️⃣4️⃣ **Learning & Storage - یادگیری و ذخیره**
```
dataset_manager.learn_from_interaction(message, response)
    ↓
- ذخیره در learning_data.jsonl
- اگر پاسخ خوب بود → اضافه به patterns
    ↓
memory_manager.store_conversation("ai", response)
    ↓
personality_engine.update_from_interaction(message, response)
```

### 1️⃣5️⃣ **Response Delivery - ارسال پاسخ**
```
Backend - process_user_message() پاسخ برمی‌گردونه
    ↓
websocket_endpoint() - ساخت JSON response
    ↓
WebSocket.send() - ارسال به frontend
    ↓
Frontend - App.tsx - ws.onmessage()
    ↓
setMessages() - اضافه کردن به لیست پیام‌ها
    ↓
ChatInterface.tsx - نمایش پیام
```

## 🔄 حالات مختلف فرایند

### ✅ **حالت عادی (Happy Path)**
```
پیام → تحلیل → دیتاست ندارد → AI مدل → پاسخ موفق → نمایش
```

### 🎯 **حالت دیتاست (Dataset Response)**
```
پیام → تحلیل → دیتاست دارد → پاسخ آماده → نمایش
```

### 🌐 **حالت جستجوی وب (Web Search)**
```
پیام → تحلیل → نیاز به وب → جستجو → AI مدل با اطلاعات وب → پاسخ
```

### ⚠️ **حالت خطا (Error/Timeout)**
```
پیام → تحلیل → AI مدل → Timeout → Fallback Response → نمایش
```

### 💻 **حالت تحلیل کد (Code Analysis)**
```
پیام → تشخیص کد → تحلیل کد → AI مدل با تحلیل → پاسخ تخصصی
```

## ⏱️ زمان‌بندی فرایند

1. **Frontend → Backend**: ~10ms
2. **Memory Storage**: ~50ms
3. **Analysis & Profiling**: ~100ms
4. **Dataset Check**: ~20ms
5. **Web Search** (اختیاری): ~2-5 seconds
6. **AI Model Generation**: ~5-30 seconds
7. **Response Delivery**: ~10ms

**کل زمان**: 5-35 ثانیه (بسته به پیچیدگی)

## 🧠 اجزای دخیل در فرایند

- **Frontend**: React + WebSocket
- **Backend**: FastAPI + WebSocket
- **Memory**: ChromaDB + RAM
- **AI Model**: Ollama + Dorna-Llama3
- **Web Search**: Multiple search engines
- **Storage**: JSON files + SQLite