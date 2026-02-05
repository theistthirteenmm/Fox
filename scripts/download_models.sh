#!/bin/bash

# تغییر به دایرکتوری پروژه (یک سطح بالاتر از scripts)
cd "$(dirname "$0")/.."

# رنگ‌ها برای خروجی
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo
echo "==============================================="
echo "🦊 دانلود مدل‌های هوش مصنوعی روباه"
echo "==============================================="
echo

# تنظیم مسیر مدل‌ها
export OLLAMA_MODELS="$(pwd)/models"
echo -e "${BLUE}📁 مسیر مدل‌ها: $OLLAMA_MODELS${NC}"
echo

# ایجاد پوشه مدل‌ها
mkdir -p models

echo "📋 مدل‌های پیشنهادی روباه:"
echo
echo -e "${YELLOW}  🔥 ضروری:${NC}"
echo "  1. partai/dorna-llama3:8b-instruct-q8_0 (فارسی - 8.5GB)"
echo "  2. llama3.2:3b (سریع - 2GB)"
echo
echo -e "${BLUE}  🚀 پیشرفته:${NC}"
echo "  3. deepseek-r1:7b (استدلال - 4GB)"
echo "  4. deepseek-coder-v2:16b (برنامه‌نویسی - 9GB)"
echo "  5. qwen2.5:32b (چندزبانه - 18GB)"
echo
echo -e "${GREEN}  💪 قدرتمند:${NC}"
echo "  6. llama3.3:70b (بهترین - 43GB)"
echo

echo -e "${YELLOW}⚠️  توجه: دانلود ممکن است چندین ساعت طول بکشد${NC}"
echo -e "${YELLOW}💾 فضای کل مورد نیاز: حدود 85 گیگابایت${NC}"
echo

echo "انتخاب کنید:"
echo "1. دانلود مدل‌های ضروری (10.5GB)"
echo "2. دانلود مدل‌های پیشرفته (31.5GB)"
echo "3. دانلود همه مدل‌ها (85GB)"
echo "4. انتخاب دستی"
echo "0. خروج"
echo

read -p "انتخاب شما (0-4): " choice

download_model() {
    local model_name=$1
    local description=$2
    
    echo
    echo "==============================================="
    echo -e "${BLUE}📥 دانلود $description: $model_name${NC}"
    echo "==============================================="
    
    if ollama pull "$model_name"; then
        echo -e "${GREEN}✅ $model_name با موفقیت دانلود شد${NC}"
    else
        echo -e "${RED}❌ خطا در دانلود $model_name${NC}"
    fi
}

case $choice in
    1)
        echo
        echo "🔥 دانلود مدل‌های ضروری..."
        download_model "partai/dorna-llama3:8b-instruct-q8_0" "مدل فارسی اصلی"
        download_model "llama3.2:3b" "مدل سریع"
        ;;
    2)
        echo
        echo "🚀 دانلود مدل‌های پیشرفته..."
        download_model "partai/dorna-llama3:8b-instruct-q8_0" "مدل فارسی اصلی"
        download_model "llama3.2:3b" "مدل سریع"
        download_model "deepseek-r1:7b" "مدل استدلال"
        download_model "deepseek-coder-v2:16b" "مدل برنامه‌نویسی"
        download_model "qwen2.5:32b" "مدل چندزبانه"
        ;;
    3)
        echo
        echo "💪 دانلود همه مدل‌ها..."
        download_model "partai/dorna-llama3:8b-instruct-q8_0" "مدل فارسی اصلی"
        download_model "llama3.2:3b" "مدل سریع"
        download_model "deepseek-r1:7b" "مدل استدلال"
        download_model "deepseek-coder-v2:16b" "مدل برنامه‌نویسی"
        download_model "qwen2.5:32b" "مدل چندزبانه"
        download_model "llama3.3:70b" "مدل قدرتمند"
        ;;
    4)
        echo
        echo "🎯 انتخاب دستی مدل‌ها:"
        while true; do
            echo
            read -p "نام مدل (مثال: llama3.2:3b): " model_name
            if [[ -z "$model_name" ]]; then
                break
            fi
            download_model "$model_name" "مدل انتخابی"
            echo
            read -p "مدل دیگری دانلود کنید؟ (y/n): " continue_download
            if [[ $continue_download != [yY] ]]; then
                break
            fi
        done
        ;;
    0)
        echo "خروج..."
        exit 0
        ;;
    *)
        echo "انتخاب نامعتبر"
        exit 1
        ;;
esac

echo
echo "==============================================="
echo "🎉 دانلود کامل شد!"
echo "==============================================="
echo

echo "📋 بررسی مدل‌های نصب شده:"
ollama list

echo
echo -e "${GREEN}✅ مدل‌ها در $(pwd)/models ذخیره شدند!${NC}"
echo -e "${GREEN}🦊 حالا می‌توانید روباه را استفاده کنید${NC}"
echo

echo "💡 برای تست مدل‌ها: ./scripts/test.bat"
echo "💡 برای راه‌اندازی روباه: ./start.sh"
echo