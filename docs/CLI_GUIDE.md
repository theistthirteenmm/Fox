# Fox CLI Guide

## Installation

```bash
pip install git+https://github.com/theistthirteenmm/Fox.git
```

With audio support:
```bash
pip install "git+https://github.com/theistthirteenmm/Fox.git#egg=fox-ai[audio]"
```

---

## Usage

### Interactive Mode

```bash
fox
```

### Send Message

```bash
fox "سلام"
fox "What is Python?"
```

### Voice Mode

```bash
# Enable voice output
fox --voice

# Record voice (5 seconds)
fox --listen 5
```

---

## Commands

| Command | Alias | Description |
|---------|-------|-------------|
| `/help` | `/h` | Show help |
| `/status` | `/s` | Server status |
| `/voice` | `/v` | Toggle voice |
| `/listen` | `/l` | Voice input |
| `/config` | - | Show config |
| `/server <url>` | - | Set server |
| `/clear` | `/c` | Clear screen |
| `/exit` | `/q` | Exit |

---

## Configuration

Config location: `~/.fox/config.json`

### Set Server

```bash
fox config --server 192.168.1.100:8000
```

### Command Line Options

```bash
fox --server 192.168.1.100:8000  # Set server
fox --voice                       # Enable voice
fox --listen 5                    # Record 5 seconds
fox --version                     # Show version
fox --help                        # Show help
```

---

## Examples

### Basic Chat

```
$ fox

    ╭─────────────────────────────╮
    │        /\_/\               │
    │       (  o.o  )    Fox      │
    │        > ^ <      v1.0     │
    ╰─────────────────────────────╯

Server: localhost:8000
Type /help for commands

You: سلام
🦊: سلام! چطور می‌تونم کمکت کنم؟

You: /exit
Goodbye! 🦊
```

### Quick Message

```bash
$ fox "What is the capital of Iran?"
🦊: The capital of Iran is Tehran.
```

### Voice Chat

```bash
$ fox --voice
# Responses will be spoken aloud

$ fox --listen 5
# Recording for 5 seconds...
# Converting speech to text...
You (voice): سلام روباه
🦊: سلام! چطوری؟
```

---

## Troubleshooting

### Server not available

1. Start the server:
   ```bash
   scripts/start.bat  # Windows
   ./scripts/start.sh # Linux/Mac
   ```

2. Or set correct server address:
   ```bash
   fox config --server YOUR_SERVER:8000
   ```

### Audio not working

Install audio dependencies:
```bash
pip install sounddevice soundfile numpy
```

### Connection error

Check if Ollama is running:
```bash
ollama serve
```
