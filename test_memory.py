#!/usr/bin/env python3
"""
تست سیستم حافظه روباه
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from brain.memory import MemoryManager

def test_memory():
    print("🧠 تست سیستم حافظه...")
    
    try:
        # ایجاد memory manager
        memory = MemoryManager()
        print("✅ MemoryManager ایجاد شد")
        
        # تست ذخیره
        memory.store_conversation("user", "سلام روباه!")
        print("✅ ذخیره مکالمه موفق")
        
        # تست بازیابی
        context = memory.get_relevant_context("سلام")
        print(f"✅ بازیابی context: {len(context)} آیتم")
        
        # تست آمار
        stats = memory.get_memory_count()
        print(f"✅ آمار حافظه: {stats}")
        
        print("🎉 تست حافظه موفق!")
        return True
        
    except Exception as e:
        print(f"❌ خطا در تست حافظه: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_memory()