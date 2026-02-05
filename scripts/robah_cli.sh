#!/bin/bash

# تغییر به دایرکتوری پروژه
cd "$(dirname "$0")/.."

echo
echo "🦊 روباه CLI"
echo

# بررسی Python
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "❌ Python نصب نیست!"
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

# نصب کتابخانه‌ها (بی‌صدا)
pip3 install colorama requests > /dev/null 2>&1 || pip install colorama requests > /dev/null 2>&1

# اجرای CLI
$PYTHON_CMD robah_cli.py "$@"