# 🔌 مرجع API روباه

## 🌐 Base URL
```
http://localhost:8000
```

## 📡 WebSocket Endpoints

### 💬 Chat WebSocket
```
ws://localhost:8000/chat
```

#### پیام ورودی:
```json
{
  "message": "سلام روباه!",
  "timestamp": "2026-01-18T12:00:00.000Z"
}
```

#### پیام خروجی:
```json
{
  "type": "ai",
  "message": "سلام! خوش آمدی! چطوری؟ 😊",
  "timestamp": "2026-01-18T12:00:01.000Z"
}
```

## 🔗 REST API Endpoints

### 📊 وضعیت سیستم
```http
GET /status
```

#### پاسخ:
```json
{
  "status": "active",
  "brain_loaded": true,
  "memory_size": {
    "short_term": 5,
    "conversations": 12,
    "knowledge": 3
  },
  "personality_level": 2,
  "web_search": {
    "web_enabled": true,
    "internet_connected": true,
    "search_engines": ["duckduckgo", "wikipedia"]
  },
  "timestamp": "2026-01-18T12:00:00.000Z"
}
```

### 🌐 جستجوی وب

#### وضعیت جستجو:
```http
GET /web-search/status
```

#### فعال/غیرفعال کردن:
```http
POST /web-search/toggle
Content-Type: application/json

{
  "enabled": true
}
```

### 📊 آمار دیتاست
```http
GET /dataset/stats
```

#### پاسخ:
```json
{
  "dataset_stats": {
    "conversation_patterns": 1,
    "emotion_types": 3,
    "topics": 1,
    "prompt_templates": 4
  },
  "learning_enabled": true
}
```