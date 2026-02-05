# Installation Guide

## Requirements

- Python 3.8+
- [Ollama](https://ollama.ai)
- 8GB RAM (minimum)

---

## 1. Install Ollama

### Windows
```cmd
winget install Ollama.Ollama
```

### macOS
```bash
brew install ollama
```

### Linux
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

---

## 2. Download AI Model

```bash
ollama pull partai/dorna-llama3:8b-instruct-q8_0
```

---

## 3. Install Fox CLI

### From GitHub
```bash
pip install git+https://github.com/theist.thirteenmm/Fox.git
```

### With Audio Support
```bash
pip install "git+https://github.com/theist.thirteenmm/Fox.git#egg=fox-ai[audio]"
```

### Local Development
```bash
git clone https://github.com/theist.thirteenmm/Fox.git
cd Fox
pip install -e .
```

---

## 4. Start Server

### Windows
```cmd
scripts\start.bat
```

### Linux/macOS
```bash
./scripts/start.sh
```

---

## 5. Run CLI

```bash
fox
```

---

## Verify Installation

```bash
# Check CLI
fox --version

# Check server
curl http://localhost:8000/status
```

---

## Configuration

Config file: `~/.fox/config.json`

```json
{
  "server": "localhost:8000",
  "voice_enabled": false,
  "typing_effect": true
}
```

Set server address:
```bash
fox config --server 192.168.1.100:8000
```

---

## Troubleshooting

### Ollama not running
```bash
ollama serve
```

### Model not found
```bash
ollama pull partai/dorna-llama3:8b-instruct-q8_0
```

### Connection refused
Check if server is running on correct port.
