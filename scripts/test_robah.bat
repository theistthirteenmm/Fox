@echo off
chcp 65001 >nul
title 🧪 تست روباه

echo.
echo ===============================================
echo 🧪 تست کامل سیستم روباه
echo ===============================================
echo.

cd ..
python scripts\test_robah.py

echo.
pause