# 🦊 Fox - Persian AI Assistant

<div align="center">

![Fox](https://img.shields.io/badge/Fox-v1.0-orange?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python)
![Ollama](https://img.shields.io/badge/Ollama-Local_AI-green?style=for-the-badge)

**دستیار هوش مصنوعی فارسی با قابلیت یادگیری**

</div>

---

## 📦 Installation

### Quick Install (pip)

```bash
pip install git+https://github.com/theistthirteenmm/Fox.git
```

### With Audio Support

```bash
pip install "git+https://github.com/theistthirteenmm/Fox.git#egg=fox-ai[audio]"
```

---

## 🚀 Usage

### CLI Commands

```bash
# Interactive mode
fox

# Send a message
fox "سلام"

# Configure server
fox config --server 192.168.1.100:8000

# With voice output
fox --voice

# Voice input (5 seconds)
fox --listen 5

# Help
fox --help
```

### Interactive Commands

| Command | Description |
|---------|-------------|
| `/help` | Show help |
| `/status` | Server status |
| `/voice` | Toggle voice output |
| `/listen` | Voice input |
| `/config` | Show config |
| `/server <url>` | Set server |
| `/clear` | Clear screen |
| `/exit` | Exit |

---

## 🖥️ Server Setup

### Start Server

```bash
# Windows
scripts\start.bat

# Linux/Mac
./scripts/start.sh
```

### Stop Server

```bash
# Windows
scripts\stop.bat

# Linux/Mac
./scripts/stop.sh
```

---

## 📁 Project Structure

```
fox/
├── fox_cli/          # CLI package
│   ├── cli.py        # Main CLI
│   ├── client.py     # API client
│   ├── audio.py      # Audio handler
│   └── config.py     # Configuration
├── backend/          # FastAPI server
│   └── main.py
├── brain/            # AI core
│   ├── core/         # Main brain
│   ├── learning/     # Learning systems
│   └── utils/        # Utilities
├── config/           # Settings
├── data/             # Data files
├── scripts/          # Run scripts
└── docs/             # Documentation
```

---

## 🧠 Features

- **Persian Language** - Native Farsi support
- **Local AI** - Runs on your machine (Ollama)
- **Learning** - Learns from conversations
- **Voice** - Speech-to-text and text-to-speech
- **Memory** - Remembers context

### AI Models

| Model | Purpose |
|-------|---------|
| `partai/dorna-llama3:8b` | Persian (default) |
| `deepseek-r1:7b` | Reasoning |
| `deepseek-coder-v2:16b` | Coding |
| `llama3.2:3b` | Fast responses |

---

## ⚙️ Requirements

- Python 3.8+
- [Ollama](https://ollama.ai)
- 8GB RAM (minimum)

### Install Ollama Models

```bash
ollama pull partai/dorna-llama3:8b-instruct-q8_0
```

---

## 📖 Documentation

- [Installation Guide](docs/INSTALLATION.md)
- [CLI Guide](docs/CLI_GUIDE.md)
- [API Reference](docs/API_REFERENCE.md)

---

## 📄 License

MIT License

---

<div align="center">

**Made with ❤️ for Persian speakers**

</div>
