#!/bin/bash

# رنگ‌ها برای خروجی
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# تابع برای نمایش پیام‌های رنگی
print_status() {
    echo -e "${BLUE}🔍 $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${CYAN}💡 $1${NC}"
}

# تابع برای بررسی وجود دستور
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# تابع برای بررسی پورت
check_port() {
    nc -z localhost $1 >/dev/null 2>&1
}

# شروع اسکریپت
clear
echo
echo "==============================================="
echo "🦊 روباه - دستیار هوش مصنوعی شخصی"
echo "==============================================="
echo

# بررسی پیش‌نیازها
print_status "بررسی پیش‌نیازها..."

# بررسی Python
if ! command_exists python3; then
    print_error "Python 3 نصب نیست!"
    echo "لطفاً Python 3.8+ را نصب کنید"
    exit 1
fi

python_version=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)
if [[ $(echo "$python_version < 3.8" | bc -l) -eq 1 ]]; then
    print_error "Python 3.8+ مورد نیاز است. نسخه فعلی: $python_version"
    exit 1
fi

print_success "Python $(python3 --version | cut -d' ' -f2) ✓"

# بررسی Node.js
if ! command_exists node; then
    print_error "Node.js نصب نیست!"
    echo "لطفاً Node.js 16+ را نصب کنید"
    exit 1
fi

node_version=$(node --version | cut -d'v' -f2 | cut -d'.' -f1)
if [[ $node_version -lt 16 ]]; then
    print_error "Node.js 16+ مورد نیاز است. نسخه فعلی: $(node --version)"
    exit 1
fi

print_success "Node.js $(node --version) ✓"

# بررسی npm
if ! command_exists npm; then
    print_error "npm نصب نیست!"
    exit 1
fi

print_success "npm $(npm --version) ✓"

# بررسی فایل‌های پروژه
print_status "بررسی فایل‌های پروژه..."

required_files=("backend/main.py" "frontend/package.json" "requirements.txt")
for file in "${required_files[@]}"; do
    if [[ ! -f "$file" ]]; then
        print_error "فایل $file یافت نشد!"
        exit 1
    fi
done

print_success "فایل‌های پروژه موجود است"

# بررسی Ollama
print_status "بررسی Ollama..."

if ! command_exists ollama; then
    print_warning "Ollama نصب نیست!"
    echo
    echo "برای نصب Ollama:"
    echo "curl -fsSL https://ollama.ai/install.sh | sh"
    echo
    read -p "آیا می‌خواهید ادامه دهید؟ (y/n): " continue_without_ollama
    if [[ $continue_without_ollama != "y" ]]; then
        exit 1
    fi
else
    # بررسی اجرای Ollama
    if ! check_port 11434; then
        print_warning "Ollama در حال اجرا نیست. در حال راه‌اندازی..."
        ollama serve &
        OLLAMA_PID=$!
        sleep 5
        
        if ! check_port 11434; then
            print_error "نتوانستیم Ollama را راه‌اندازی کنیم"
            exit 1
        fi
    fi
    
    print_success "Ollama در حال اجرا است"
    
    # بررسی مدل
    print_status "بررسی مدل AI..."
    if ! ollama list | grep -q "partai/dorna-llama3"; then
        print_warning "مدل فارسی یافت نشد"
        read -p "آیا می‌خواهید مدل فارسی را دانلود کنید؟ (y/n): " download_model
        if [[ $download_model == "y" ]]; then
            print_status "در حال دانلود مدل فارسی..."
            ollama pull partai/dorna-llama3:8b-instruct-q8_0
            if [[ $? -eq 0 ]]; then
                print_success "مدل فارسی دانلود شد"
            else
                print_warning "خطا در دانلود مدل. با مدل پیش‌فرض ادامه می‌دهیم"
            fi
        fi
    else
        print_success "مدل فارسی موجود است"
    fi
fi

echo

# راه‌اندازی Virtual Environment
print_status "راه‌اندازی Python Virtual Environment..."

if [[ ! -d "venv" ]]; then
    print_warning "Virtual Environment یافت نشد. در حال ایجاد..."
    python3 -m venv venv
    if [[ $? -ne 0 ]]; then
        print_error "خطا در ایجاد Virtual Environment"
        exit 1
    fi
fi

# فعال‌سازی Virtual Environment
source venv/bin/activate

# نصب Python Dependencies
print_status "نصب Python Dependencies..."
pip install -r requirements.txt --quiet --disable-pip-version-check
if [[ $? -ne 0 ]]; then
    print_error "خطا در نصب Python packages"
    exit 1
fi

print_success "Python Dependencies نصب شد"

# نصب Node.js Dependencies
print_status "بررسی Node.js Dependencies..."
cd frontend

if [[ ! -d "node_modules" ]]; then
    print_warning "Node modules یافت نشد. در حال نصب..."
    npm install --silent
    if [[ $? -ne 0 ]]; then
        print_error "خطا در نصب npm packages"
        cd ..
        exit 1
    fi
fi

cd ..
print_success "Node.js Dependencies آماده است"

# ایجاد دایرکتوری‌های مورد نیاز
print_status "ایجاد دایرکتوری‌های مورد نیاز..."
mkdir -p data/{memory,personality,learning} logs
print_success "دایرکتوری‌ها ایجاد شد"

echo
echo "==============================================="
echo "🚀 راه‌اندازی سرویس‌ها"
echo "==============================================="
echo

# تابع cleanup برای تمیز کردن فرآیندها
cleanup() {
    echo
    print_info "در حال توقف سرویس‌ها..."
    
    if [[ ! -z $BACKEND_PID ]]; then
        kill $BACKEND_PID 2>/dev/null
    fi
    
    if [[ ! -z $FRONTEND_PID ]]; then
        kill $FRONTEND_PID 2>/dev/null
    fi
    
    if [[ ! -z $OLLAMA_PID ]]; then
        kill $OLLAMA_PID 2>/dev/null
    fi
    
    # کشتن فرآیندهای باقی‌مانده
    pkill -f "python backend/main.py" 2>/dev/null
    pkill -f "npm start" 2>/dev/null
    
    print_success "سرویس‌ها متوقف شدند"
    exit 0
}

# تنظیم signal handler
trap cleanup SIGINT SIGTERM

# راه‌اندازی Backend
print_status "راه‌اندازی Backend..."
export PYTHONPATH="$(pwd)"
source venv/bin/activate
python backend/main.py &
BACKEND_PID=$!

# انتظار برای راه‌اندازی Backend
print_status "صبر برای راه‌اندازی Backend..."
sleep 8

# بررسی Backend
if ! curl -s http://localhost:8000/status >/dev/null 2>&1; then
    print_warning "Backend هنوز آماده نیست. کمی بیشتر صبر کنید..."
    sleep 5
fi

# راه‌اندازی Frontend
print_status "راه‌اندازی Frontend..."
cd frontend
npm start &
FRONTEND_PID=$!
cd ..

# انتظار برای راه‌اندازی Frontend
print_status "صبر برای راه‌اندازی Frontend..."
sleep 10

echo
echo "==============================================="
echo "🎉 روباه آماده است!"
echo "==============================================="
echo
print_success "🌐 رابط وب:     http://localhost:3000"
print_success "🔧 API Backend:  http://localhost:8000"
print_success "📚 مستندات:     http://localhost:8000/docs"
echo
print_info "💡 نکات مهم:"
echo "   • برای توقف سرویس‌ها، Ctrl+C را فشار دهید"
echo "   • اگر مشکلی پیش آمد، فایل logs/robah.log را بررسی کنید"
echo "   • برای راه‌اندازی مجدد، این اسکریپت را دوباره اجرا کنید"
echo

# باز کردن مرورگر (اگر در محیط گرافیکی باشیم)
if [[ -n "$DISPLAY" ]] || [[ "$OSTYPE" == "darwin"* ]]; then
    print_status "باز کردن مرورگر..."
    sleep 3
    
    if command_exists xdg-open; then
        xdg-open http://localhost:3000 >/dev/null 2>&1
    elif command_exists open; then
        open http://localhost:3000 >/dev/null 2>&1
    fi
fi

echo
print_success "✨ لذت ببرید از چت با روباه! 🦊"
echo

# منتظر ماندن برای Ctrl+C
print_info "برای توقف سرویس‌ها، Ctrl+C را فشار دهید..."
wait