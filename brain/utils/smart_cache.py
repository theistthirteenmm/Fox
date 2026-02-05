"""
🧠 سیستم Cache هوشمند روباه
کش کردن پاسخ‌ها و بهینه‌سازی عملکرد
"""

import hashlib
import json
import time
from typing import Dict, Optional, List
from datetime import datetime, timedelta
import redis
import pickle

class SmartCache:
    def __init__(self):
        # Redis برای cache سریع (اختیاری)
        try:
            self.redis_client = redis.Redis(host='localhost', port=6379, db=0)
            self.use_redis = True
            print("🔴 Redis cache فعال شد")
        except:
            self.use_redis = False
            print("💾 استفاده از cache محلی")
        
        # Cache محلی
        self.local_cache = {}
        self.cache_stats = {
            "hits": 0,
            "misses": 0,
            "total_requests": 0
        }
        
        # تنظیمات cache
        self.max_cache_size = 1000
        self.default_ttl = 3600  # 1 ساعت
        self.similarity_threshold = 0.85
        
    def _generate_cache_key(self, message: str, context: List[Dict] = None) -> str:
        """تولید کلید منحصر به فرد برای cache"""
        # نرمال‌سازی پیام
        normalized = message.lower().strip()
        
        # اضافه کردن context اگر مهم باشد
        context_hash = ""
        if context:
            context_str = json.dumps(context, sort_keys=True)
            context_hash = hashlib.md5(context_str.encode()).hexdigest()[:8]
        
        # تولید hash
        full_key = f"{normalized}_{context_hash}"
        return hashlib.sha256(full_key.encode()).hexdigest()[:16]
    
    def get_cached_response(self, message: str, context: List[Dict] = None) -> Optional[Dict]:
        """دریافت پاسخ از cache"""
        self.cache_stats["total_requests"] += 1
        
        cache_key = self._generate_cache_key(message, context)
        
        # جستجو در Redis
        if self.use_redis:
            try:
                cached_data = self.redis_client.get(cache_key)
                if cached_data:
                    result = pickle.loads(cached_data)
                    self.cache_stats["hits"] += 1
                    print(f"🎯 Cache hit: {message[:30]}...")
                    return result
            except Exception as e:
                print(f"خطا در Redis: {e}")
        
        # جستجو در cache محلی
        if cache_key in self.local_cache:
            cached_item = self.local_cache[cache_key]
            
            # بررسی انقضا
            if datetime.now() < cached_item["expires_at"]:
                self.cache_stats["hits"] += 1
                print(f"🎯 Local cache hit: {message[:30]}...")
                return cached_item["data"]
            else:
                # حذف آیتم منقضی شده
                del self.local_cache[cache_key]
        
        # جستجوی similarity-based
        similar_response = self._find_similar_cached_response(message)
        if similar_response:
            self.cache_stats["hits"] += 1
            print(f"🔍 Similar cache hit: {message[:30]}...")
            return similar_response
        
        self.cache_stats["misses"] += 1
        return None
    
    def cache_response(self, message: str, response: Dict, context: List[Dict] = None, ttl: int = None):
        """ذخیره پاسخ در cache"""
        cache_key = self._generate_cache_key(message, context)
        ttl = ttl or self.default_ttl
        
        cache_data = {
            "response": response,
            "timestamp": datetime.now().isoformat(),
            "message": message,
            "context_size": len(context) if context else 0
        }
        
        # ذخیره در Redis
        if self.use_redis:
            try:
                self.redis_client.setex(
                    cache_key, 
                    ttl, 
                    pickle.dumps(cache_data)
                )
            except Exception as e:
                print(f"خطا در ذخیره Redis: {e}")
        
        # ذخیره در cache محلی
        expires_at = datetime.now() + timedelta(seconds=ttl)
        self.local_cache[cache_key] = {
            "data": cache_data,
            "expires_at": expires_at
        }
        
        # مدیریت اندازه cache
        self._manage_cache_size()
        
        print(f"💾 Cached: {message[:30]}...")
    
    def _find_similar_cached_response(self, message: str) -> Optional[Dict]:
        """جستجوی پاسخ مشابه در cache"""
        message_words = set(message.lower().split())
        
        best_match = None
        best_similarity = 0
        
        for cached_item in self.local_cache.values():
            if datetime.now() >= cached_item["expires_at"]:
                continue
                
            cached_message = cached_item["data"]["message"]
            cached_words = set(cached_message.lower().split())
            
            # محاسبه شباهت Jaccard
            intersection = len(message_words & cached_words)
            union = len(message_words | cached_words)
            
            if union > 0:
                similarity = intersection / union
                
                if similarity > best_similarity and similarity >= self.similarity_threshold:
                    best_similarity = similarity
                    best_match = cached_item["data"]
        
        return best_match
    
    def _manage_cache_size(self):
        """مدیریت اندازه cache"""
        if len(self.local_cache) > self.max_cache_size:
            # حذف قدیمی‌ترین آیتم‌ها
            sorted_items = sorted(
                self.local_cache.items(),
                key=lambda x: x[1]["expires_at"]
            )
            
            # حذف 20% قدیمی‌ترین آیتم‌ها
            remove_count = int(self.max_cache_size * 0.2)
            for i in range(remove_count):
                if i < len(sorted_items):
                    del self.local_cache[sorted_items[i][0]]
    
    def get_cache_stats(self) -> Dict:
        """آمار cache"""
        hit_rate = 0
        if self.cache_stats["total_requests"] > 0:
            hit_rate = self.cache_stats["hits"] / self.cache_stats["total_requests"]
        
        return {
            **self.cache_stats,
            "hit_rate": hit_rate,
            "cache_size": len(self.local_cache),
            "redis_enabled": self.use_redis
        }
    
    def clear_cache(self):
        """پاک کردن کامل cache"""
        self.local_cache.clear()
        if self.use_redis:
            try:
                self.redis_client.flushdb()
            except:
                pass
        print("🗑️ Cache پاک شد")

# Instance سراسری
smart_cache = SmartCache()