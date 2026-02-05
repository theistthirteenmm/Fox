# Robah + Nginx (Windows)

## Overview
This project is configured to run everything behind Nginx on port 8080:
- Main UI: http://localhost:8080
- 3D UI: http://localhost:8080/3d/
- Backend API: http://localhost:8000
- Backend Docs: http://localhost:8000/docs

Nginx proxies:
- `/` ? Frontend (port 3000)
- `/3d/` ? Frontend-3D (port 3001)
- `/api/` ? Backend (port 8000)
- `/chat` ? WebSocket (Backend)

## Prerequisites
- Python 3.8+
- Node.js 16+
- Nginx (Windows)
- Ollama (optional but recommended)

## Nginx Install (Windows)
Installed via winget:
```
winget install --id nginxinc.nginx -e --source winget
```
If `nginx` is not recognized right away, close and re-open your terminal.

## Run Everything
From project root:
```
start.bat
```
This runs:
- Backend
- Frontend
- Frontend-3D
- Nginx

## Optional Audio (Windows)
Audio input/output uses PyAudio, which requires Visual C++ Build Tools.
If you need audio features, install the build tools and then:
```
pip install pyaudio
```

## Stop Everything
```
stop.bat
```

## Nginx Config Location
- `config/nginx/robah.conf`

Logs:
- `logs/nginx/`
