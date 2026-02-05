# API Reference

## Base URL

```
http://localhost:8000
```

---

## Endpoints

### GET /status

Get server status.

**Response:**
```json
{
  "status": "active",
  "brain_loaded": true,
  "memory_size": {
    "short_term": 5,
    "conversations": 12
  },
  "model_policy": {
    "current_model": "partai/dorna-llama3:8b-instruct-q8_0",
    "allow_heavy": false
  }
}
```

---

### POST /chat

Send a message and get response.

**Request:**
```json
{
  "message": "سلام"
}
```

**Response:**
```json
{
  "response": "سلام! چطور می‌تونم کمکت کنم؟",
  "timestamp": "2026-02-05T12:00:00.000Z"
}
```

---

### WebSocket /chat

Real-time chat connection.

**Connect:**
```
ws://localhost:8000/chat
```

**Send:**
```json
{
  "message": "سلام"
}
```

**Receive:**
```json
{
  "type": "ai",
  "message": "سلام! خوشحالم که باهام حرف می‌زنی!"
}
```

---

### POST /speech/speech-to-text

Convert audio to text.

**Request:** `multipart/form-data`
- `audio_file`: WAV file

**Response:**
```json
{
  "success": true,
  "text": "سلام روباه"
}
```

---

### POST /speech/text-to-speech

Convert text to audio.

**Request:** `application/x-www-form-urlencoded`
- `text`: Text to convert

**Response:** WAV audio file

---

## Error Responses

```json
{
  "error": "Error message",
  "status": 400
}
```

---

## Example Usage

### Python

```python
import requests

# Chat
response = requests.post(
    "http://localhost:8000/chat",
    json={"message": "سلام"}
)
print(response.json()["response"])
```

### cURL

```bash
# Status
curl http://localhost:8000/status

# Chat
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "سلام"}'
```
