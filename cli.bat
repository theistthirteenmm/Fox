@echo off
:: Robah CLI - simple and fast
chcp 65001 > nul
set PYTHONUTF8=1
set PYTHONIOENCODING=utf-8
python robah_cli.py %*
