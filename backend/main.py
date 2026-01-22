"""
روباه - دستیار هوش مصنوعی شخصی
Backend اصلی پروژه
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn
import json
from datetime import datetime
import asyncio
import os
import tempfile
from pathlib import Path

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from brain.core import AIBrain
from brain.memory import MemoryManager
from brain.personality import PersonalityEngine
from brain.speech_handler import speech_handler

app = FastAPI(title="روباه AI Assistant", version="1.0.0")

# CORS middleware برای ارتباط با frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize AI components
ai_brain = AIBrain()
memory_manager = MemoryManager()
personality_engine = PersonalityEngine()

# Initialize AI brain on startup
@app.on_event("startup")
async def startup_event():
    """راه‌اندازی اولیه سیستم"""
    print("🚀 در حال راه‌اندازی سیستم روباه...")
    await ai_brain.initialize_model()
    print("✅ سیستم آماده است!")

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        print(f"کاربر جدید متصل شد. تعداد کل: {len(self.active_connections)}")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            print(f"کاربر قطع شد. تعداد باقی‌مانده: {len(self.active_connections)}")

    async def send_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

manager = ConnectionManager()

@app.get("/")
async def root():
    return {"message": "روباه AI Assistant در حال اجرا است!"}

@app.get("/status")
async def get_status():
    return {
        "status": "active",
        "brain_loaded": ai_brain.is_loaded(),
        "memory_size": memory_manager.get_memory_count(),
        "personality_level": personality_engine.get_development_level(),
        "web_search": ai_brain.get_web_status(),
        "timestamp": datetime.now().isoformat()
    }

@app.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    
    try:
        while True:
            # دریافت پیام از کاربر
            data = await websocket.receive_text()
            user_message = json.loads(data)
            
            print(f"پیام دریافتی: {user_message}")
            
            # پردازش پیام توسط AI
            response = await process_user_message(user_message["message"])
            
            # ارسال پاسخ
            ai_response = {
                "type": "ai",
                "message": response,
                "timestamp": datetime.now().isoformat()
            }
            
            await manager.send_message(json.dumps(ai_response, ensure_ascii=False), websocket)
            
    except WebSocketDisconnect:
        manager.disconnect(websocket)

@app.post("/web-search/toggle")
async def toggle_web_search(enabled: bool = None):
    """فعال/غیرفعال کردن جستجوی وب"""
    status = ai_brain.toggle_web_search(enabled)
    return {
        "web_search_enabled": status,
        "message": f"جستجوی وب {'فعال' if status else 'غیرفعال'} شد"
    }

@app.get("/web-search/status")
async def get_web_search_status():
    """وضعیت جستجوی وب"""
    return ai_brain.get_web_status()

@app.get("/dataset/stats")
async def get_dataset_stats():
    """آمار دیتاست و یادگیری"""
    return {
        "dataset_stats": ai_brain.dataset_manager.get_stats(),
        "learning_enabled": True,
        "total_interactions": ai_brain.dataset_manager.get_stats()
    }

# 🎙️ Speech API Endpoints
@app.post("/speech/text-to-speech")
async def text_to_speech(text: str = Form(...)):
    """تبدیل متن به صدا"""
    try:
        # ایجاد فایل موقت
        temp_dir = Path("data/temp/audio")
        temp_dir.mkdir(parents=True, exist_ok=True)
        
        audio_file = temp_dir / f"tts_{datetime.now().strftime('%Y%m%d_%H%M%S')}.wav"
        
        # تولید صدا
        success = await speech_handler.text_to_speech(text, str(audio_file))
        
        if success and audio_file.exists():
            return FileResponse(
                path=str(audio_file),
                media_type="audio/wav",
                filename=f"robah_speech_{datetime.now().strftime('%H%M%S')}.wav"
            )
        else:
            return {"error": "خطا در تولید صدا"}
            
    except Exception as e:
        return {"error": f"خطا در تبدیل متن به صدا: {str(e)}"}

@app.post("/speech/speech-to-text")
async def speech_to_text(audio_file: UploadFile = File(...)):
    """تبدیل صدا به متن"""
    try:
        # بررسی فرمت فایل
        if not speech_handler.is_audio_file(audio_file.filename):
            return {"error": "فرمت فایل صوتی پشتیبانی نمی‌شود"}
        
        # ذخیره موقت فایل
        temp_dir = Path("data/temp/audio")
        temp_dir.mkdir(parents=True, exist_ok=True)
        
        temp_file = temp_dir / f"upload_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{audio_file.filename}"
        
        with open(temp_file, "wb") as f:
            content = await audio_file.read()
            f.write(content)
        
        # تبدیل به متن
        text = await speech_handler.speech_to_text(audio_file=str(temp_file))
        
        # پاک کردن فایل موقت
        if temp_file.exists():
            temp_file.unlink()
        
        if text:
            return {
                "text": text,
                "success": True,
                "message": "صدا با موفقیت به متن تبدیل شد"
            }
        else:
            return {
                "text": "",
                "success": False,
                "message": "متنی در صدا تشخیص داده نشد"
            }
            
    except Exception as e:
        return {"error": f"خطا در تبدیل صدا به متن: {str(e)}"}

@app.get("/speech/status")
async def get_speech_status():
    """وضعیت سیستم صوتی"""
    return speech_handler.get_status()

# 📁 File Management API Endpoints
@app.post("/files/upload")
async def upload_file(file: UploadFile = File(...)):
    """آپلود و تحلیل فایل"""
    try:
        # بررسی فرمت فایل
        allowed_extensions = ['.pdf', '.docx', '.txt', '.png', '.jpg', '.jpeg']
        file_ext = Path(file.filename).suffix.lower()
        
        if file_ext not in allowed_extensions:
            return {"error": f"فرمت {file_ext} پشتیبانی نمی‌شود"}
        
        # ذخیره فایل
        upload_dir = Path("data/uploads")
        upload_dir.mkdir(parents=True, exist_ok=True)
        
        file_path = upload_dir / f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}"
        
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
        
        # تحلیل فایل (پیاده‌سازی ساده)
        file_info = {
            "filename": file.filename,
            "size": len(content),
            "type": file_ext,
            "path": str(file_path),
            "uploaded_at": datetime.now().isoformat()
        }
        
        # استخراج محتوا بر اساس نوع فایل
        extracted_content = ""
        if file_ext == '.txt':
            extracted_content = content.decode('utf-8', errors='ignore')
        elif file_ext in ['.pdf', '.docx']:
            extracted_content = f"فایل {file_ext} آپلود شد - تحلیل در نسخه‌های آینده"
        elif file_ext in ['.png', '.jpg', '.jpeg']:
            extracted_content = "تصویر آپلود شد - OCR در نسخه‌های آینده"
        
        return {
            "success": True,
            "file_info": file_info,
            "content_preview": extracted_content[:200] + "..." if len(extracted_content) > 200 else extracted_content,
            "message": "فایل با موفقیت آپلود شد"
        }
        
    except Exception as e:
        return {"error": f"خطا در آپلود فایل: {str(e)}"}

@app.get("/files/list")
async def list_uploaded_files():
    """لیست فایل‌های آپلود شده"""
    try:
        upload_dir = Path("data/uploads")
        if not upload_dir.exists():
            return {"files": []}
        
        files = []
        for file_path in upload_dir.iterdir():
            if file_path.is_file():
                stat = file_path.stat()
                files.append({
                    "filename": file_path.name,
                    "size": stat.st_size,
                    "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    "path": str(file_path)
                })
        
        return {"files": sorted(files, key=lambda x: x['modified'], reverse=True)}
        
    except Exception as e:
        return {"error": f"خطا در دریافت لیست فایل‌ها: {str(e)}"}

# 📊 Analytics API Endpoints
@app.get("/analytics/conversations")
async def get_conversation_analytics():
    """آمار مکالمات"""
    try:
        # آمار ساده از حافظه
        memory_stats = memory_manager.get_memory_count()
        
        return {
            "total_conversations": memory_stats.get("conversations", 0),
            "total_messages": memory_stats.get("short_term", 0),
            "personality_level": personality_engine.get_development_level(),
            "last_interaction": datetime.now().isoformat(),
            "active_topics": ["برنامه‌نویسی", "هوش مصنوعی", "فارسی"],  # نمونه
            "mood_trend": "مثبت"  # نمونه
        }
        
    except Exception as e:
        return {"error": f"خطا در دریافت آمار: {str(e)}"}

@app.get("/analytics/personality")
async def get_personality_analytics():
    """آمار شخصیت"""
    try:
        personality_data = personality_engine.get_personality_profile()
        
        return {
            "personality_traits": personality_data,
            "development_level": personality_engine.get_development_level(),
            "interaction_count": personality_engine.get_interaction_count(),
            "growth_trend": "رو به رشد",  # نمونه
            "favorite_topics": ["فناوری", "یادگیری", "کمک به دیگران"]  # نمونه
        }
        
    except Exception as e:
        return {"error": f"خطا در دریافت آمار شخصیت: {str(e)}"}

@app.get("/analytics/dashboard")
async def get_dashboard_data():
    """داده‌های کامل داشبورد"""
    try:
        return {
            "overview": {
                "total_conversations": memory_manager.get_memory_count().get("conversations", 0),
                "personality_level": personality_engine.get_development_level(),
                "web_searches": 0,  # نمونه
                "files_processed": len(list(Path("data/uploads").glob("*"))) if Path("data/uploads").exists() else 0
            },
            "recent_activity": [
                {"type": "conversation", "time": "10 دقیقه پیش", "description": "مکالمه درباره برنامه‌نویسی"},
                {"type": "learning", "time": "1 ساعت پیش", "description": "یادگیری الگوی جدید"},
                {"type": "web_search", "time": "2 ساعت پیش", "description": "جستجو درباره هوش مصنوعی"}
            ],
            "personality_growth": [
                {"date": "2026-01-15", "level": 1.2},
                {"date": "2026-01-16", "level": 1.5},
                {"date": "2026-01-17", "level": 1.8},
                {"date": "2026-01-18", "level": 2.1}
            ]
        }
        
    except Exception as e:
        return {"error": f"خطا در دریافت داده‌های داشبورد: {str(e)}"}

# 👤 User Profile API Endpoints
@app.get("/user/profile")
async def get_user_profile():
    """دریافت پروفایل کاربر"""
    try:
        from brain.user_profiler import user_profiler
        
        insights = user_profiler.get_relationship_insights()
        
        return {
            "success": True,
            "profile": insights,
            "message": "پروفایل کاربر دریافت شد"
        }
        
    except Exception as e:
        return {"error": f"خطا در دریافت پروفایل: {str(e)}"}

@app.get("/user/relationship")
async def get_relationship_status():
    """وضعیت رابطه با کاربر"""
    try:
        from brain.user_profiler import user_profiler
        
        insights = user_profiler.get_relationship_insights()
        
        # تعیین وضعیت رابطه
        level = insights["relationship_level"]
        if level < 2:
            status = "تازه آشنا"
            description = "هنوز در حال آشنایی هستیم"
        elif level < 4:
            status = "دوست"
            description = "رابطه دوستانه‌ای داریم"
        elif level < 7:
            status = "دوست نزدیک"
            description = "به هم نزدیک شده‌ایم"
        elif level < 9:
            status = "رفیق خوب"
            description = "رفیق‌های خوبی هستیم"
        else:
            status = "رفیق صمیمی"
            description = "رابطه بسیار صمیمانه‌ای داریم"
        
        return {
            "relationship_status": status,
            "description": description,
            "level": level,
            "trust_score": insights["trust_score"],
            "total_interactions": insights["total_interactions"],
            "favorite_topics": insights["favorite_topics"]
        }
        
    except Exception as e:
        return {"error": f"خطا در دریافت وضعیت رابطه: {str(e)}"}

# 💻 Code Analysis API Endpoints
@app.post("/code/analyze")
async def analyze_code(code: str = Form(...), language: str = Form(None)):
    """تحلیل کد برنامه‌نویسی"""
    try:
        from brain.code_analyzer import code_analyzer
        
        # تحلیل کد
        analysis = code_analyzer.analyze_code(code, f"temp.{language}" if language else None)
        
        return {
            "success": True,
            "analysis": analysis,
            "message": "کد با موفقیت تحلیل شد"
        }
        
    except Exception as e:
        return {"error": f"خطا در تحلیل کد: {str(e)}"}

@app.post("/code/fix")
async def fix_code(code: str = Form(...), language: str = Form(None)):
    """اصلاح خودکار کد"""
    try:
        from brain.code_analyzer import code_analyzer
        
        # تشخیص زبان
        detected_language = code_analyzer.detect_language(code, f"temp.{language}" if language else None)
        
        # اصلاح کد
        fixed_code = code_analyzer.fix_common_issues(code, detected_language)
        
        # تحلیل کد اصلاح شده
        analysis = code_analyzer.analyze_code(fixed_code)
        
        return {
            "success": True,
            "original_code": code,
            "fixed_code": fixed_code,
            "language": detected_language,
            "improvements": analysis.get('general_suggestions', []),
            "message": "کد اصلاح شد"
        }
        
    except Exception as e:
        return {"error": f"خطا در اصلاح کد: {str(e)}"}

@app.get("/code/languages")
async def get_supported_languages():
    """لیست زبان‌های پشتیبانی شده"""
    try:
        from brain.code_analyzer import code_analyzer
        
        return {
            "supported_languages": list(code_analyzer.supported_languages.keys()),
            "extensions": code_analyzer.supported_languages
        }
        
    except Exception as e:
        return {"error": f"خطا در دریافت زبان‌ها: {str(e)}"}

# 🔄 System Management API Endpoints
@app.post("/system/restart")
async def restart_system():
    """ریستارت سیستم روباه"""
    try:
        import os
        import sys
        
        # پیام تأیید
        response = {
            "message": "سیستم در حال ریستارت...",
            "status": "restarting",
            "timestamp": datetime.now().isoformat()
        }
        
        # ریستارت بعد از 2 ثانیه
        import threading
        def restart_after_delay():
            import time
            time.sleep(2)
            os.execv(sys.executable, ['python'] + sys.argv)
        
        thread = threading.Thread(target=restart_after_delay)
        thread.daemon = True
        thread.start()
        
        return response
        
    except Exception as e:
        return {"error": f"خطا در ریستارت سیستم: {str(e)}"}

@app.get("/system/health")
async def system_health():
    """بررسی سلامت سیستم"""
    try:
        # بررسی اجزای مختلف
        health_status = {
            "overall": "healthy",
            "components": {
                "ai_brain": ai_brain.is_loaded(),
                "memory": memory_manager.get_memory_count().get("short_term", 0) >= 0,
                "personality": personality_engine.get_development_level() > 0,
                "speech": speech_handler.get_status()["initialized"],
                "web_search": ai_brain.get_web_status()["web_enabled"]
            },
            "uptime": "running",
            "timestamp": datetime.now().isoformat()
        }
        
        # تعیین وضعیت کلی
        unhealthy_components = [k for k, v in health_status["components"].items() if not v]
        if len(unhealthy_components) > 2:
            health_status["overall"] = "unhealthy"
        elif len(unhealthy_components) > 0:
            health_status["overall"] = "degraded"
        
        health_status["issues"] = unhealthy_components
        
        return health_status
        
    except Exception as e:
        return {
            "overall": "error",
            "error": str(e),
            "timestamp": datetime.now().isoformat()
        }

async def process_user_message(message: str) -> str:
    """پردازش پیام کاربر و تولید پاسخ"""
    try:
        # ذخیره در حافظه
        memory_manager.store_conversation("user", message)
        
        # تحلیل شخصیت و احساسات
        personality_context = personality_engine.analyze_interaction(message)
        
        # تولید پاسخ توسط AI
        response = await ai_brain.generate_response(
            message=message,
            context=memory_manager.get_relevant_context(message),
            personality=personality_context
        )
        
        # ذخیره پاسخ در حافظه
        memory_manager.store_conversation("ai", response)
        
        # به‌روزرسانی شخصیت
        personality_engine.update_from_interaction(message, response)
        
        return response
        
    except Exception as e:
        print(f"خطا در پردازش پیام: {e}")
        return "متأسفم، مشکلی پیش آمده. لطفاً دوباره تلاش کنید."

if __name__ == "__main__":
    print("🚀 در حال راه‌اندازی روباه...")
    uvicorn.run(app, host="0.0.0.0", port=8000)