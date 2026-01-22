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
            
            # تعریف thinking callback برای این WebSocket
            async def thinking_callback(message: str):
                thinking_response = {
                    "type": "thinking",
                    "message": message,
                    "timestamp": datetime.now().isoformat()
                }
                try:
                    await websocket.send_text(json.dumps(thinking_response, ensure_ascii=False))
                except:
                    pass  # اگر ارسال ناموفق بود، نادیده بگیر
            
            # پردازش پیام توسط AI
            response = await process_user_message(user_message["message"], thinking_callback)
            
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
        print(f"🎤 دریافت فایل صوتی: {audio_file.filename}")
        print(f"📊 نوع محتوا: {audio_file.content_type}")
        
        # خواندن محتوای فایل
        content = await audio_file.read()
        file_size = len(content)
        print(f"📏 حجم فایل: {file_size} bytes")
        
        if file_size < 100:
            return {
                "text": "",
                "success": False,
                "message": f"فایل صوتی خیلی کوچک است ({file_size} bytes)",
                "debug_info": {
                    "file_size": file_size,
                    "content_type": audio_file.content_type,
                    "filename": audio_file.filename
                }
            }
        
        # بررسی فرمت فایل
        if not speech_handler.is_audio_file(audio_file.filename):
            return {
                "text": "",
                "success": False,
                "message": f"فرمت فایل پشتیبانی نمی‌شود: {audio_file.filename}",
                "debug_info": {
                    "supported_formats": speech_handler.supported_formats,
                    "received_filename": audio_file.filename
                }
            }
        
        # ذخیره موقت فایل
        temp_dir = Path("data/temp/audio")
        temp_dir.mkdir(parents=True, exist_ok=True)
        
        # تشخیص فرمت از content-type
        file_extension = ".wav"  # پیش‌فرض
        if audio_file.content_type:
            if "webm" in audio_file.content_type:
                file_extension = ".webm"
            elif "mp3" in audio_file.content_type:
                file_extension = ".mp3"
            elif "m4a" in audio_file.content_type:
                file_extension = ".m4a"
        
        temp_file = temp_dir / f"upload_{datetime.now().strftime('%Y%m%d_%H%M%S')}{file_extension}"
        
        print(f"💾 ذخیره در: {temp_file}")
        
        with open(temp_file, "wb") as f:
            f.write(content)
        
        # بررسی فایل ذخیره شده
        if not temp_file.exists():
            return {
                "text": "",
                "success": False,
                "message": "خطا در ذخیره فایل موقت"
            }
        
        saved_size = temp_file.stat().st_size
        print(f"✅ فایل ذخیره شد: {saved_size} bytes")
        
        # تبدیل به متن
        print("🔄 شروع تبدیل صدا به متن...")
        text = await speech_handler.speech_to_text(audio_file=str(temp_file))
        
        # پاک کردن فایل موقت
        try:
            if temp_file.exists():
                temp_file.unlink()
                print("🗑️ فایل موقت پاک شد")
        except Exception as cleanup_error:
            print(f"⚠️ خطا در پاک کردن فایل موقت: {cleanup_error}")
        
        if text and text.strip():
            return {
                "text": text.strip(),
                "success": True,
                "message": "صدا با موفقیت به متن تبدیل شد",
                "debug_info": {
                    "original_size": file_size,
                    "saved_size": saved_size,
                    "text_length": len(text.strip()),
                    "temp_file": str(temp_file)
                }
            }
        else:
            return {
                "text": "",
                "success": False,
                "message": "متنی در صدا تشخیص داده نشد - لطفاً واضح‌تر و بلندتر صحبت کنید",
                "debug_info": {
                    "whisper_result": text,
                    "file_processed": True,
                    "file_size": file_size
                }
            }
            
    except Exception as e:
        print(f"❌ خطای کلی در تبدیل صدا به متن: {e}")
        import traceback
        traceback.print_exc()
        
        return {
            "text": "",
            "success": False,
            "message": f"خطا در تبدیل صدا به متن: {str(e)}",
            "debug_info": {
                "error_type": type(e).__name__,
                "error_message": str(e)
            }
        }

@app.get("/speech/debug")
async def debug_speech_system():
    """تست و دیباگ سیستم صوتی"""
    try:
        debug_info = {
            "speech_handler_status": speech_handler.get_status(),
            "temp_directory": str(Path("data/temp/audio")),
            "temp_dir_exists": Path("data/temp/audio").exists(),
            "supported_formats": speech_handler.supported_formats,
            "whisper_model_loaded": speech_handler.whisper_model is not None,
            "tts_engine_ready": speech_handler.tts_engine is not None
        }
        
        # بررسی فایل‌های موقت
        temp_dir = Path("data/temp/audio")
        if temp_dir.exists():
            temp_files = list(temp_dir.glob("*"))
            debug_info["temp_files_count"] = len(temp_files)
            debug_info["temp_files"] = [str(f) for f in temp_files[:5]]  # فقط 5 فایل اول
        else:
            debug_info["temp_files_count"] = 0
            debug_info["temp_files"] = []
        
        # تست ساده TTS
        try:
            test_text = "سلام، این یک تست است"
            temp_tts_file = temp_dir / "test_tts.wav"
            temp_dir.mkdir(parents=True, exist_ok=True)
            
            tts_success = await speech_handler.text_to_speech(test_text, str(temp_tts_file))
            debug_info["tts_test"] = {
                "success": tts_success,
                "test_file_created": temp_tts_file.exists(),
                "test_file_size": temp_tts_file.stat().st_size if temp_tts_file.exists() else 0
            }
            
            # پاک کردن فایل تست
            if temp_tts_file.exists():
                temp_tts_file.unlink()
                
        except Exception as tts_error:
            debug_info["tts_test"] = {
                "success": False,
                "error": str(tts_error)
            }
        
        return {
            "success": True,
            "debug_info": debug_info,
            "message": "اطلاعات دیباگ سیستم صوتی"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": f"خطا در دیباگ سیستم صوتی: {str(e)}"
        }

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

async def process_user_message(message: str, thinking_callback=None) -> str:
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
            personality=personality_context,
            thinking_callback=thinking_callback
        )
        
        # ذخیره پاسخ در حافظه
        memory_manager.store_conversation("ai", response)
        
        # به‌روزرسانی شخصیت
        personality_engine.update_from_interaction(message, response)
        
        return response
        
    except Exception as e:
        print(f"خطا در پردازش پیام: {e}")
        return "متأسفم، مشکلی پیش آمده. لطفاً دوباره تلاش کنید."

async def send_thinking_message(message: str):
    """ارسال پیام میانی به کاربر"""
    try:
        thinking_response = {
            "type": "thinking",
            "message": message,
            "timestamp": datetime.now().isoformat()
        }
        
        # ارسال به تمام کاربران متصل
        for connection in manager.active_connections:
            try:
                await connection.send_text(json.dumps(thinking_response, ensure_ascii=False))
            except:
                pass  # اگر ارسال ناموفق بود، نادیده بگیر
                
    except Exception as e:
        print(f"خطا در ارسال پیام میانی: {e}")

if __name__ == "__main__":
    print("🚀 در حال راه‌اندازی روباه...")
    uvicorn.run(app, host="0.0.0.0", port=8000)