"""
Fox CLI - Main Interface
"""

import sys
import os
import time
import threading
import argparse

from .config import load_config, save_config, get_server_url
from .client import FoxClient
from .audio import AudioHandler, AUDIO_AVAILABLE

# رنگ‌ها
try:
    from colorama import init as colorama_init, Fore, Style
    colorama_init(autoreset=True)
except ImportError:
    class _NoColor:
        def __getattr__(self, _):
            return ""
    Fore = Style = _NoColor()


class FoxCLI:
    """رابط خط فرمان"""

    def __init__(self):
        self.config = load_config()
        self.client = FoxClient()
        self.audio = AudioHandler()
        self.thinking = False
        self.is_tty = sys.stdout.isatty()

        # رنگ‌ها
        self.fox = f"{Fore.CYAN}{Style.BRIGHT}"
        self.user = Fore.GREEN
        self.dim = Fore.LIGHTBLACK_EX
        self.warn = Fore.YELLOW
        self.err = Fore.RED
        self.ok = Fore.GREEN
        self.reset = Style.RESET_ALL

    def banner(self):
        """نمایش بنر"""
        print(f"""
{self.fox}
    ╭─────────────────────────────╮
    │                             │
    │        /\\_/\\               │
    │       (  o.o  )    Fox      │
    │        > ^ <      v1.0     │
    │                             │
    ╰─────────────────────────────╯
{self.reset}""")

    def show_thinking(self):
        """نمایش انیمیشن فکر کردن"""
        if not self.is_tty:
            return
        chars = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        self.thinking = True

        def animate():
            i = 0
            while self.thinking:
                print(f"\r{self.fox}🦊 {chars[i % len(chars)]}{self.reset}", end='', flush=True)
                time.sleep(0.1)
                i += 1

        thread = threading.Thread(target=animate, daemon=True)
        thread.start()

    def stop_thinking(self):
        """توقف انیمیشن"""
        self.thinking = False
        if self.is_tty:
            print(f"\r{' ' * 10}\r", end='', flush=True)

    def type_text(self, text: str):
        """نمایش متن با افکت تایپ"""
        if not self.is_tty or not self.config.get("typing_effect", True):
            print(text)
            return

        delay = self.config.get("typing_delay", 0.006)
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()

    def chat(self, message: str) -> str:
        """ارسال پیام و دریافت پاسخ"""
        self.show_thinking()
        response = self.client.chat(message)
        self.stop_thinking()

        if response is None:
            return "Connection error"
        return response

    def cmd_help(self):
        """نمایش راهنما"""
        print(f"""
{self.fox}Commands:{self.reset}

{self.dim}Connection:{self.reset}
  /server <url>  - Set server address
  /ping          - Test server connection
  /reconnect     - Reconnect to server
  /status, /s    - Server status

{self.dim}Testing:{self.reset}
  /test          - Full system test
  /models        - List available AI models

{self.dim}Audio:{self.reset}
  /voice, /v     - Toggle voice output
  /listen, /l    - Voice input (speak)

{self.dim}Other:{self.reset}
  /config        - Show config
  /clear, /c     - Clear screen
  /help, /h      - Show this help
  /exit, /q      - Exit
""")

    def cmd_status(self):
        """نمایش وضعیت"""
        status = self.client.get_status()
        if status:
            print(f"{self.fox}Server Status:{self.reset}")
            print(f"{self.dim}  Brain: {self.ok}Loaded{self.reset}" if status.get('brain_loaded') else f"{self.dim}  Brain: {self.err}Not loaded{self.reset}")
            print(f"{self.dim}  Memory: {status.get('memory_size', {})}")
            if status.get('model_policy'):
                print(f"  Model: {status['model_policy'].get('current_model')}")
                print(f"  Heavy models: {'Enabled' if status['model_policy'].get('allow_heavy') else 'Disabled'}{self.reset}")
        else:
            print(f"{self.err}Server not available{self.reset}")

    def cmd_config(self):
        """نمایش تنظیمات"""
        print(f"{self.fox}Config:{self.reset}")
        print(f"{self.dim}  Server: {self.config.get('server')}")
        print(f"  Voice: {'On' if self.config.get('voice_enabled') else 'Off'}")
        print(f"  Typing effect: {'On' if self.config.get('typing_effect') else 'Off'}{self.reset}")

    def cmd_server(self, url: str):
        """تنظیم آدرس سرور"""
        self.config["server"] = url
        save_config(self.config)
        self.client = FoxClient(f"http://{url}")
        print(f"{self.ok}Server set to: {url}{self.reset}")
        # تست اتصال
        self.cmd_ping()

    def cmd_ping(self):
        """تست اتصال به سرور"""
        print(f"{self.dim}Pinging server...{self.reset}")
        start = time.time()
        if self.client.is_available():
            elapsed = (time.time() - start) * 1000
            print(f"{self.ok}✓ Server is online ({elapsed:.0f}ms){self.reset}")
        else:
            print(f"{self.err}✗ Server not available{self.reset}")

    def cmd_reconnect(self):
        """اتصال مجدد به سرور"""
        print(f"{self.dim}Reconnecting...{self.reset}")
        self.client = FoxClient()
        self.cmd_ping()

    def cmd_test(self):
        """تست کامل سیستم"""
        print(f"{self.fox}System Test:{self.reset}")
        print()

        # 1. تست اتصال
        print(f"{self.dim}[1/4] Testing connection...{self.reset}")
        if self.client.is_available():
            print(f"  {self.ok}✓ Server connected{self.reset}")
        else:
            print(f"  {self.err}✗ Server not available{self.reset}")
            return

        # 2. تست وضعیت
        print(f"{self.dim}[2/4] Checking brain...{self.reset}")
        status = self.client.get_status()
        if status and status.get('brain_loaded'):
            print(f"  {self.ok}✓ Brain loaded{self.reset}")
        else:
            print(f"  {self.err}✗ Brain not loaded{self.reset}")
            return

        # 3. تست حافظه
        print(f"{self.dim}[3/4] Checking memory...{self.reset}")
        if status and status.get('memory_size'):
            mem = status.get('memory_size', {})
            print(f"  {self.ok}✓ Memory OK (short: {mem.get('short_term', 0)}, conv: {mem.get('conversations', 0)}){self.reset}")
        else:
            print(f"  {self.warn}? Memory status unknown{self.reset}")

        # 4. تست پاسخ
        print(f"{self.dim}[4/4] Testing AI response...{self.reset}")
        response = self.client.chat("سلام")
        if response:
            print(f"  {self.ok}✓ AI responding{self.reset}")
        else:
            print(f"  {self.err}✗ AI not responding{self.reset}")

        print()
        print(f"{self.ok}All tests passed!{self.reset}")

    def cmd_models(self):
        """نمایش مدل‌های موجود"""
        status = self.client.get_status()
        if status and status.get('model_policy'):
            policy = status['model_policy']
            print(f"{self.fox}AI Models:{self.reset}")
            print(f"{self.dim}  Current: {policy.get('current_model', 'Unknown')}")
            print(f"  Heavy models: {'Enabled' if policy.get('allow_heavy') else 'Disabled'}{self.reset}")
            print()
            print(f"{self.dim}Available models:{self.reset}")
            print(f"  - partai/dorna-llama3:8b (Persian)")
            print(f"  - deepseek-r1:7b (Reasoning)")
            print(f"  - deepseek-coder-v2:16b (Code)")
            print(f"  - llama3.2:3b (Fast)")
        else:
            print(f"{self.err}Cannot get model info{self.reset}")

    def cmd_voice_toggle(self):
        """تغییر وضعیت صدا"""
        if not AUDIO_AVAILABLE:
            print(f"{self.warn}Audio not available. Install: pip install sounddevice soundfile numpy{self.reset}")
            return

        self.config["voice_enabled"] = not self.config.get("voice_enabled", False)
        save_config(self.config)
        status = "On" if self.config["voice_enabled"] else "Off"
        print(f"{self.dim}Voice output: {status}{self.reset}")

    def cmd_listen(self, seconds: int = 5):
        """ضبط صدا و ارسال"""
        if not AUDIO_AVAILABLE:
            print(f"{self.warn}Audio not available. Install: pip install sounddevice soundfile numpy{self.reset}")
            return

        # ضبط
        audio_path = self.audio.record(seconds)
        if not audio_path:
            print(f"{self.err}Recording failed{self.reset}")
            return

        # تبدیل به متن
        print(f"{self.dim}Converting speech to text...{self.reset}")
        text = self.client.speech_to_text(audio_path)
        if not text:
            print(f"{self.err}Speech recognition failed{self.reset}")
            return

        print(f"{self.user}You (voice): {self.reset}{text}")

        # پردازش
        response = self.chat(text)
        print(f"{self.fox}🦊: {self.reset}", end='')
        self.type_text(response)

        # پخش صدا
        if self.config.get("voice_enabled"):
            audio_data = self.client.text_to_speech(response)
            if audio_data:
                self.audio.play(audio_data)

    def handle_command(self, text: str) -> bool:
        """پردازش دستورات"""
        parts = text.strip().split()
        cmd = parts[0].lower()
        args = parts[1:]

        if cmd in ['/help', '/h', '/کمک']:
            self.cmd_help()
        elif cmd in ['/status', '/s', '/وضعیت']:
            self.cmd_status()
        elif cmd in ['/config']:
            self.cmd_config()
        elif cmd in ['/server']:
            if args:
                self.cmd_server(args[0])
            else:
                print(f"{self.warn}Usage: /server <host:port>{self.reset}")
        elif cmd in ['/ping']:
            self.cmd_ping()
        elif cmd in ['/reconnect', '/rc']:
            self.cmd_reconnect()
        elif cmd in ['/test']:
            self.cmd_test()
        elif cmd in ['/models', '/model']:
            self.cmd_models()
        elif cmd in ['/voice', '/v', '/صدا']:
            self.cmd_voice_toggle()
        elif cmd in ['/listen', '/l', '/گوش']:
            seconds = int(args[0]) if args else 5
            self.cmd_listen(seconds)
        elif cmd in ['/clear', '/c', '/پاک']:
            os.system('cls' if os.name == 'nt' else 'clear')
            self.banner()
        elif cmd in ['/exit', '/q', '/quit', '/خروج', 'exit', 'quit']:
            print(f"{self.fox}Goodbye! 🦊{self.reset}")
            return False
        else:
            print(f"{self.warn}Unknown command. Type /help{self.reset}")

        return True

    def run_interactive(self):
        """اجرای حالت تعاملی"""
        # بررسی سرور
        if not self.client.is_available():
            print(f"{self.warn}Server not available at {get_server_url()}")
            print(f"Start server or set address with: /server <host:port>{self.reset}")
            print()

        self.banner()
        print(f"{self.dim}Server: {self.config.get('server')}")
        print(f"Type /help for commands{self.reset}")
        print()

        while True:
            try:
                user_input = input(f"{self.user}You: {self.reset}").strip()
                if not user_input:
                    continue

                # دستورات
                if user_input.startswith('/') or user_input.lower() in ['exit', 'quit']:
                    if not self.handle_command(user_input):
                        break
                    continue

                # چت
                response = self.chat(user_input)
                print(f"{self.fox}🦊: {self.reset}", end='')
                self.type_text(response)
                print()

                # پخش صدا
                if self.config.get("voice_enabled"):
                    audio_data = self.client.text_to_speech(response)
                    if audio_data:
                        self.audio.play(audio_data)

            except KeyboardInterrupt:
                print(f"\n{self.fox}Goodbye! 🦊{self.reset}")
                break
            except Exception as e:
                print(f"{self.err}Error: {e}{self.reset}")

    def run_single(self, message: str):
        """اجرای یک پیام"""
        if not self.client.is_available():
            print(f"{self.err}Server not available{self.reset}")
            return

        response = self.chat(message)
        print(f"{self.fox}🦊: {self.reset}{response}")


def main():
    """نقطه ورود اصلی"""
    parser = argparse.ArgumentParser(
        description="Fox - Persian AI Assistant",
        prog="fox"
    )
    parser.add_argument(
        "message",
        nargs="*",
        help="Message to send (optional, starts interactive mode if empty)"
    )
    parser.add_argument(
        "--server", "-s",
        help="Server address (host:port)"
    )
    parser.add_argument(
        "--voice", "-v",
        action="store_true",
        help="Enable voice output"
    )
    parser.add_argument(
        "--listen", "-l",
        type=int,
        metavar="SEC",
        help="Record voice for SEC seconds"
    )
    parser.add_argument(
        "--version",
        action="version",
        version="Fox CLI v1.0.0"
    )

    # زیردستورات
    subparsers = parser.add_subparsers(dest="command")

    # config
    config_parser = subparsers.add_parser("config", help="Configure Fox")
    config_parser.add_argument("--server", help="Set server address")
    config_parser.add_argument("--show", action="store_true", help="Show config")

    args = parser.parse_args()

    # تنظیم سرور
    if args.server:
        config = load_config()
        config["server"] = args.server
        save_config(config)

    # صدا
    if args.voice:
        config = load_config()
        config["voice_enabled"] = True
        save_config(config)

    cli = FoxCLI()

    # زیردستور config
    if args.command == "config":
        if args.server:
            cli.cmd_server(args.server)
        else:
            cli.cmd_config()
        return

    # ضبط صدا
    if args.listen:
        cli.cmd_listen(args.listen)
        return

    # پیام مستقیم
    if args.message:
        message = " ".join(args.message)
        cli.run_single(message)
        return

    # حالت تعاملی
    cli.run_interactive()


if __name__ == "__main__":
    main()
