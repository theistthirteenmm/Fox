#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
?? ????? CLI - ???? ? ????
"""

import asyncio
import sys
import os
import time
import threading
from datetime import datetime
import requests

try:
    from colorama import init as colorama_init, Fore, Style  # type: ignore
    COLORAMA_AVAILABLE = True
except Exception:
    COLORAMA_AVAILABLE = False
    class _NoColor:
        def __getattr__(self, _name):
            return ""
    Fore = _NoColor()
    Style = _NoColor()


def _configure_unicode_io():
    """Best-effort UTF-8 IO on Windows console."""
    if sys.platform != "win32":
        return
    os.environ.setdefault("PYTHONUTF8", "1")
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    try:
        sys.stdin.reconfigure(encoding="utf-8")
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass
    try:
        import ctypes  # type: ignore
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleCP(65001)
        kernel32.SetConsoleOutputCP(65001)
    except Exception:
        pass


# ??? (???????)
try:
    import numpy as np  # type: ignore
    import sounddevice as sd  # type: ignore
    import soundfile as sf  # type: ignore
    AUDIO_AVAILABLE = True
except Exception:
    AUDIO_AVAILABLE = False


# ??????? ? auto-complete (???????)
try:
    import readline  # type: ignore
    READLINE_AVAILABLE = True
except Exception:
    READLINE_AVAILABLE = False


def _configure_colors(is_tty: bool):
    """Enable colors only when a real TTY is attached."""
    global Fore, Style
    if not COLORAMA_AVAILABLE or not is_tty:
        class _NoColorLocal:
            def __getattr__(self, _name):
                return ""
        Fore = _NoColorLocal()
        Style = _NoColorLocal()
        return
    colorama_init(autoreset=True)


_configure_unicode_io()


class SimpleCLI:
    def __init__(self):
        self.is_tty = sys.stdout.isatty() and sys.stdin.isatty()
        _configure_colors(self.is_tty)

        self.backend_url = "http://localhost:8000"
        self.use_backend = False
        self._backend_warning_shown = False
        self.thinking = False
        self.typing_effect = True
        self.typing_delay = 0.006
        self.session = requests.Session()
        self.history_file = os.path.join("data", "cli_history.txt")
        self.audio_dir = os.path.join("data", "cli_audio")
        self.voice_out_enabled = False
        self.voice_in_enabled = False
        self.sample_rate = 16000

        # ??????
        self.fox_color = Fore.CYAN + Style.BRIGHT
        self.user_color = Fore.GREEN
        self.dim_color = Fore.LIGHTBLACK_EX
        self.warn_color = Fore.YELLOW
        self.err_color = Fore.RED

        # ???????
        self.commands = [
            "/help", "/clear", "/exit",
            "/status", "/model", "/heavy on", "/heavy off",
            "/typing on", "/typing off", "/fast", "/slow",
            "/voice on", "/voice off", "/listen on", "/listen off", "/talk",
            "/???", "/???", "/????", "/?????"
        ]
        self.command_handlers = {
            "/help": self._cmd_help,
            "/???": self._cmd_help,
            "/clear": self._cmd_clear,
            "/???": self._cmd_clear,
            "/exit": self._cmd_exit,
            "/????": self._cmd_exit,
            "exit": self._cmd_exit,
            "/status": self._cmd_status,
            "/?????": self._cmd_status,
            "/model": self._cmd_model,
            "/heavy": self._cmd_heavy,
            "/typing": self._cmd_typing,
            "/fast": self._cmd_fast,
            "/slow": self._cmd_slow,
            "/voice": self._cmd_voice,
            "/listen": self._cmd_listen,
            "/talk": self._cmd_talk,
        }

        self._setup_history_and_completion()
        os.makedirs(self.audio_dir, exist_ok=True)
        if not self.is_tty:
            self.typing_effect = False

    def _setup_history_and_completion(self):
        """?????????? history ? auto-complete"""
        if not READLINE_AVAILABLE or not self.is_tty:
            return
        try:
            os.makedirs(os.path.dirname(self.history_file), exist_ok=True)
            if os.path.exists(self.history_file):
                readline.read_history_file(self.history_file)

            def completer(text, state):
                options = [c for c in self.commands if c.startswith(text)]
                return options[state] if state < len(options) else None

            readline.set_completer(completer)
            readline.parse_and_bind("tab: complete")
        except Exception:
            pass

    def _save_history(self):
        if not READLINE_AVAILABLE:
            return
        try:
            readline.write_history_file(self.history_file)
        except Exception:
            pass

    def show_thinking(self):
        """??????? ???? ??? ????"""
        if not self.is_tty:
            return
        chars = ['?', '?', '?', '?', '?', '?', '?', '?', '?', '?']
        self.thinking = True

        def animate():
            i = 0
            while self.thinking:
                print(f"\r{self.fox_color}?? {chars[i % len(chars)]}{Style.RESET_ALL}", end='', flush=True)
                time.sleep(0.1)
                i += 1

        thread = threading.Thread(target=animate, daemon=True)
        thread.start()

    def stop_thinking(self):
        """???? ???????"""
        if not self.is_tty:
            self.thinking = False
            return
        self.thinking = False
        print(f"\r{' ' * 10}\r", end='', flush=True)

    async def check_backend(self):
        """????? backend"""
        try:
            response = self.session.get(f"{self.backend_url}/status", timeout=2)
            return response.status_code == 200
        except Exception:
            return False

    async def chat_backend(self, message):
        """?? ?? backend"""
        try:
            response = self.session.post(
                f"{self.backend_url}/chat",
                json={"message": message},
                timeout=30
            )
            if response.status_code == 200:
                return response.json().get('response', '??? ?? ????')
        except Exception:
            pass
        return None

    async def chat_local(self, message):
        """?? ???? (????)"""
        responses = {
            '????': '????! ?????? ??',
            '?????': '???? ????? ?????! ?? ??????',
            '????': '??????? ?? ????! ?? ???? ??????? ?????',
            '???': '?????! ?? ??????? ??????',
            'bye': '???????! ??'
        }

        lower = message.lower()
        for key, response in responses.items():
            if key in lower:
                return response
        return '?????! ????? ????? ??? ??'

    async def get_response(self, message):
        """?????? ????"""
        if self.use_backend:
            response = await self.chat_backend(message)
            if response:
                return response
            if not self._backend_warning_shown:
                print(f"{self.warn_color}?? Backend ?? ????? ????? ?? ??? ??????? ?? ???? ????.{Style.RESET_ALL}")
                self._backend_warning_shown = True
        return await self.chat_local(message)

    async def fetch_status(self):
        """?????? ????? ?????"""
        try:
            response = self.session.get(f"{self.backend_url}/status", timeout=3)
            if response.status_code == 200:
                return response.json()
        except Exception:
            pass
        return None

    async def toggle_heavy_models(self, enabled: bool):
        """????/??????? ???? ??????? ?????"""
        try:
            response = self.session.post(
                f"{self.backend_url}/models/policy",
                json={"allow_heavy": enabled},
                timeout=3
            )
            if response.status_code == 200:
                return response.json()
        except Exception:
            pass
        return None

    def _audio_guard(self) -> bool:
        if not AUDIO_AVAILABLE:
            print(f"{self.warn_color}?? ???????? ??? ??? ????. ???? ?????????? ???????? ???? ?? ??? ??.{Style.RESET_ALL}")
            print(f"{self.dim_color}???????: pip install -r requirements_cli.txt{Style.RESET_ALL}")
            return False
        if not self.use_backend:
            print(f"{self.warn_color}?? ???? ???? ???? backend ???? ????.{Style.RESET_ALL}")
            return False
        return True

    async def record_voice(self, seconds: int = 7) -> str:
        """??? ??? ? ????? ?? ???? wav"""
        if not self._audio_guard():
            return ""
        try:
            print(f"{self.dim_color}??? ??? ??? ({seconds} ?????)...{Style.RESET_ALL}")
            recording = sd.rec(int(seconds * self.sample_rate), samplerate=self.sample_rate, channels=1, dtype='float32')
            sd.wait()
            filename = os.path.join(self.audio_dir, f"voice_{int(time.time())}.wav")
            sf.write(filename, recording, self.sample_rate)
            return filename
        except Exception as e:
            print(f"{self.err_color}??? ?? ??? ???: {e}{Style.RESET_ALL}")
            return ""

    async def speech_to_text(self, wav_path: str) -> str:
        """????? ??? ?? backend ? ?????? ???"""
        if not wav_path:
            return ""
        try:
            with open(wav_path, "rb") as f:
                files = {"audio_file": f}
                response = self.session.post(
                    f"{self.backend_url}/speech/speech-to-text",
                    files=files,
                    timeout=60
                )
            if response.status_code == 200:
                data = response.json()
                if data.get("success") and data.get("text"):
                    return data["text"].strip()
        except Exception as e:
            print(f"{self.err_color}??? ?? ????? ???: {e}{Style.RESET_ALL}")
        return ""

    async def text_to_speech(self, text: str):
        """????? ??? ?? ??? ? ??? ??"""
        if not self._audio_guard():
            return
        try:
            response = self.session.post(
                f"{self.backend_url}/speech/text-to-speech",
                data={"text": text},
                timeout=60
            )
            if response.status_code == 200:
                audio_path = os.path.join(self.audio_dir, f"tts_{int(time.time())}.wav")
                with open(audio_path, "wb") as f:
                    f.write(response.content)
                data, sr = sf.read(audio_path, dtype='float32')
                sd.play(data, sr)
                sd.wait()
        except Exception as e:
            print(f"{self.err_color}??? ?? ??? ???: {e}{Style.RESET_ALL}")

    def _print_typing(self, text: str):
        """??? ??? ?? ???? ????"""
        if not self.typing_effect or not self.is_tty:
            print(text)
            return
        for ch in text:
            print(ch, end='', flush=True)
            time.sleep(self.typing_delay)
        print()

    def show_fox_art(self):
        """????? ASCII art ?????"""
        fox_art = f"""{self.fox_color}
    ????????????????????????????????????????
    ?                                      ?
    ?           /\_/\                      ?
    ?          (  o.o  )                   ?
    ?           > ^ <                      ?
    ?                                      ?
    ?        ?? ????? CLI ??               ?
    ?      ?????? ?????? ?????             ?
    ?                                      ?
    ????????????????????????????????????????{Style.RESET_ALL}
"""
        print(fox_art)

    def welcome(self):
        """???? ??????"""
        backend_status = "?? ???? ?? ??? ????" if self.use_backend else "?? ???? ????"
        if self.is_tty:
            os.system('cls' if os.name == 'nt' else 'clear')
        self.show_fox_art()
        print(f"""
{self.dim_color}?????: {backend_status}{Style.RESET_ALL}

{self.dim_color}???????: /help /clear /exit /status /model /heavy{Style.RESET_ALL}
""")

    async def _handle_command(self, user_input: str):
        text = user_input.strip()
        if not text.startswith('/'):
            return None
        parts = text.split()
        cmd = parts[0].lower()
        args = parts[1:]
        handler = self.command_handlers.get(cmd)
        if not handler:
            return None
        return await handler(args)

    async def _cmd_exit(self, _args):
        print(f"{self.fox_color}?? ???????! ??{Style.RESET_ALL}")
        self._save_history()
        return "exit"

    async def _cmd_clear(self, _args):
        if self.is_tty:
            os.system('cls' if os.name == 'nt' else 'clear')
        self.welcome()
        return "continue"

    async def _cmd_help(self, _args):
        print(f"""
{self.fox_color}?? ??????:{Style.RESET_ALL}
{self.dim_color}? ??? ?????? ?? ????!
? /clear - ??? ???? ????
? /exit - ????{Style.RESET_ALL}
? /status - ????? ?????
? /model - ????? ??? ????
? /heavy on|off - ??????? ?????
? /typing on|off - ???? ????
? /fast /slow - ???? ????
? /voice on|off - ??? ???? ????
? /listen on|off - ????/??????? ????? ????
? /talk [sec] - ???? ?? ??? (????? /talk 6)
""")
        return "continue"

    async def _cmd_status(self, _args):
        status = await self.fetch_status()
        if status:
            model = status.get("model_policy", {})
            print(f"{self.fox_color}?? ?????:{Style.RESET_ALL}")
            print(f"{self.dim_color}? ???: {'????' if status.get('brain_loaded') else '?? ??? ????????'}")
            print(f"? ?????: {status.get('memory_size', {})}")
            if model:
                print(f"? ??? ????: {model.get('current_model')}")
                print(f"? ??? ?????: {'????' if model.get('allow_heavy') else '???????'}{Style.RESET_ALL}")
            else:
                print(f"{Style.RESET_ALL}", end="")
        else:
            print(f"{self.err_color}? ????? ?????? ????{Style.RESET_ALL}")
        return "continue"

    async def _cmd_model(self, _args):
        status = await self.fetch_status()
        if status and status.get("model_policy"):
            model = status["model_policy"]
            print(f"{self.fox_color}?? ??? ????:{Style.RESET_ALL} {model.get('current_model')}")
            print(f"{self.dim_color}??? ?????: {'????' if model.get('allow_heavy') else '???????'}{Style.RESET_ALL}")
        else:
            print(f"{self.err_color}? ?????? ??? ???? ????{Style.RESET_ALL}")
        return "continue"

    async def _cmd_heavy(self, args):
        if len(args) < 1 or args[0] not in ['on', 'off']:
            print(f"{self.warn_color}???????: /heavy on | /heavy off{Style.RESET_ALL}")
            return "continue"
        if not self.use_backend:
            print(f"{self.warn_color}????? ?? backend ???? ????.{Style.RESET_ALL}")
            return "continue"
        enabled = args[0] == 'on'
        result = await self.toggle_heavy_models(enabled)
        if result and result.get("success", True):
            print(f"{self.fox_color}?? ??? ????? {'????' if enabled else '???????'} ??.{Style.RESET_ALL}")
        else:
            print(f"{self.err_color}? ????? ??? ????? ???{Style.RESET_ALL}")
        return "continue"

    async def _cmd_typing(self, args):
        if len(args) < 1 or args[0] not in ['on', 'off']:
            print(f"{self.warn_color}???????: /typing on | /typing off{Style.RESET_ALL}")
            return "continue"
        self.typing_effect = args[0] == 'on'
        print(f"{self.dim_color}???? ???? {'????' if self.typing_effect else '???????'} ??.{Style.RESET_ALL}")
        return "continue"

    async def _cmd_fast(self, _args):
        self.typing_delay = 0.002
        print(f"{self.dim_color}???? ???? ???? ??.{Style.RESET_ALL}")
        return "continue"

    async def _cmd_slow(self, _args):
        self.typing_delay = 0.01
        print(f"{self.dim_color}???? ???? ????? ??.{Style.RESET_ALL}")
        return "continue"

    async def _cmd_voice(self, args):
        if len(args) < 1 or args[0] not in ['on', 'off']:
            print(f"{self.warn_color}???????: /voice on | /voice off{Style.RESET_ALL}")
            return "continue"
        self.voice_out_enabled = args[0] == 'on'
        print(f"{self.dim_color}??? ???? {'????' if self.voice_out_enabled else '???????'} ??.{Style.RESET_ALL}")
        return "continue"

    async def _cmd_listen(self, args):
        if len(args) < 1 or args[0] not in ['on', 'off']:
            print(f"{self.warn_color}???????: /listen on | /listen off{Style.RESET_ALL}")
            return "continue"
        self.voice_in_enabled = args[0] == 'on'
        print(f"{self.dim_color}????? ???? {'????' if self.voice_in_enabled else '???????'} ??.{Style.RESET_ALL}")
        return "continue"

    async def _cmd_talk(self, args):
        if not self.voice_in_enabled:
            print(f"{self.warn_color}????? ???? ??????? ???. /listen on ?? ???.{Style.RESET_ALL}")
            return "continue"
        seconds = 7
        if len(args) > 0:
            try:
                seconds = max(3, min(20, int(args[0])))
            except Exception:
                seconds = 7
        wav_path = await self.record_voice(seconds)
        text = await self.speech_to_text(wav_path)
        if not text:
            print(f"{self.warn_color}???? ????? ???? ???.{Style.RESET_ALL}")
            return "continue"
        print(f"{self.user_color}??? (???): {Style.RESET_ALL}{text}")
        self.show_thinking()
        response = await self.get_response(text)
        self.stop_thinking()
        prefix = f"{self.fox_color}??: {Style.RESET_ALL}"
        print(prefix, end='')
        self._print_typing(response)
        print()
        if self.voice_out_enabled:
            await self.text_to_speech(response)
        return "continue"

    async def run_interactive(self):
        """???? ??"""
        self.welcome()
        while True:
            try:
                user_input = input(f"{self.user_color}???: {Style.RESET_ALL}").strip()
                if not user_input:
                    continue

                # ???????
                cmd_result = await self._handle_command(user_input)
                if cmd_result == "exit":
                    break
                if cmd_result == "continue":
                    continue

                # ????? ??? ????
                self.show_thinking()

                # ?????? ????
                response = await self.get_response(user_input)

                # ????? ????
                self.stop_thinking()
                prefix = f"{self.fox_color}??: {Style.RESET_ALL}"
                print(prefix, end='')
                self._print_typing(response)
                print()

                if self.voice_out_enabled:
                    await self.text_to_speech(response)

            except KeyboardInterrupt:
                self.stop_thinking()
                print(f"\n{self.fox_color}?? ???????! ??{Style.RESET_ALL}")
                self._save_history()
                break
            except Exception as e:
                self.stop_thinking()
                print(f"{self.err_color}???: {e}{Style.RESET_ALL}")


async def main():
    """???? ????"""
    import argparse

    parser = argparse.ArgumentParser(description='?? ????? CLI')
    parser.add_argument('message', nargs='*', help='???? ??????')
    parser.add_argument('--backend', action='store_true', help='??????? ?? backend')

    args = parser.parse_args()

    cli = SimpleCLI()

    if args.backend:
        backend_ok = await cli.check_backend()
        if not backend_ok:
            print(f"{Fore.RED}? Backend ?? ????? ????. ????? ???? ?? ???? ????.{Style.RESET_ALL}")
            return
        cli.use_backend = True
    else:
        cli.use_backend = await cli.check_backend()

    if not args.message and not cli.is_tty:
        print("? ??? ???? ?????? ????. ????? ???? ?? ?? ???? ?????? ????? ????.")
        return

    if args.message:
        message = ' '.join(args.message)
        cli.show_thinking()
        response = await cli.get_response(message)
        cli.stop_thinking()
        print(f"{cli.fox_color}??: {Style.RESET_ALL}{response}")
    else:
        await cli.run_interactive()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n{Fore.CYAN}?? ???????! ??{Style.RESET_ALL}")
    except Exception as e:
        print(f"{Fore.RED}???: {e}{Style.RESET_ALL}")
