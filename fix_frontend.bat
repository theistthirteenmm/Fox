@echo off
echo 🔧 در حال رفع مشکل فرانت...

cd frontend

echo 📦 پاک کردن node_modules...
rmdir /s /q node_modules 2>nul

echo 📦 پاک کردن package-lock.json...
del package-lock.json 2>nul

echo 📦 نصب مجدد dependencies...
npm install

echo 🚀 راه‌اندازی فرانت...
npm start

pause