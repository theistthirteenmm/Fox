"""
سیستم جستجوی وب روباه
قابلیت جستجو و دریافت اطلاعات از اینترنت
"""

import requests
import json
from typing import List, Dict, Optional
from datetime import datetime
import re
from urllib.parse import quote_plus
import time

class WebSearchEngine:
    def __init__(self):
        self.search_engines = {
            "duckduckgo": "https://api.duckduckgo.com/",
            "wikipedia": "https://fa.wikipedia.org/api/rest_v1/page/summary/",
            "google_custom": None  # می‌تونیم بعداً اضافه کنیم
        }
        
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        print("🌐 سیستم جستجوی وب راه‌اندازی شد")
    
    def should_search_web(self, query: str, context: List[Dict] = None) -> bool:
        """تشخیص اینکه آیا نیاز به جستجوی وب هست یا نه"""
        
        # پیام‌های ساده که نیاز به جستجوی وب ندارن
        simple_greetings = [
            "سلام", "درود", "صبح بخیر", "عصر بخیر", "شب بخیر",
            "چطوری", "حالت چطوره", "خوبی", "چه خبر",
            "hello", "hi", "how are you", "good morning"
        ]
        
        query_lower = query.lower().strip()
        
        # اگر پیام ساده سلام و احوال‌پرسی باشه، جستجو نکن
        if any(greeting in query_lower for greeting in simple_greetings):
            return False
        
        # اگر پیام خیلی کوتاه باشه (کمتر از 5 کلمه)
        if len(query.split()) < 5:
            return False
        
        # کلمات کلیدی که نشان‌دهنده نیاز به اطلاعات جدید هستند
        web_indicators = [
            "آخرین", "جدیدترین", "امروز", "الان", "فعلی", "اخبار",
            "قیمت", "نرخ", "ارز", "بورس", "هوا", "آب و هوا",
            "چه خبر", "چه اتفاقی", "وضعیت", "آمار", "تاریخ",
            "کی", "کجا", "چطور", "چرا", "چیست", "تعریف",
            "latest", "current", "today", "now", "news", "price"
        ]
        
        # اگر شامل کلمات کلیدی باشد
        if any(indicator in query_lower for indicator in web_indicators):
            return True
        
        # اگر سؤال پیچیده باشد و در context جواب نباشد
        if "؟" in query and len(query.split()) > 8 and (not context or len(context) == 0):
            return True
        
        # پیش‌فرض: جستجو نکن
        return False
        specific_requests = [
            "بگو", "توضیح بده", "شرح بده", "اطلاعات", "جزئیات"
        ]
        
        if any(req in query_lower for req in specific_requests):
            return True
        
        return False
    
    async def search_and_summarize(self, query: str) -> Optional[Dict]:
        """جستجو و خلاصه‌سازی نتایج"""
        
        print(f"🔍 جستجوی وب برای: {query}")
        
        # جستجو در منابع مختلف
        results = []
        
        # جستجو در ویکی‌پدیا فارسی
        wiki_result = await self._search_wikipedia_fa(query)
        if wiki_result:
            results.append(wiki_result)
        
        # جستجو در DuckDuckGo
        ddg_result = await self._search_duckduckgo(query)
        if ddg_result:
            results.extend(ddg_result)
        
        if not results:
            return None
        
        # خلاصه‌سازی نتایج
        summary = self._summarize_results(results, query)
        
        return {
            "query": query,
            "timestamp": datetime.now().isoformat(),
            "sources": len(results),
            "summary": summary,
            "raw_results": results[:3]  # فقط 3 نتیجه اول
        }
    
    async def _search_wikipedia_fa(self, query: str) -> Optional[Dict]:
        """جستجو در ویکی‌پدیا فارسی"""
        try:
            # ابتدا جستجو کنیم
            search_url = "https://fa.wikipedia.org/w/api.php"
            search_params = {
                'action': 'query',
                'format': 'json',
                'list': 'search',
                'srsearch': query.replace("؟", "").strip(),
                'srlimit': 1
            }
            
            search_response = requests.get(search_url, params=search_params, headers=self.headers, timeout=10)
            
            if search_response.status_code == 200:
                search_data = search_response.json()
                
                if search_data.get('query', {}).get('search'):
                    page_title = search_data['query']['search'][0]['title']
                    
                    # حالا محتوای صفحه را بگیریم
                    content_params = {
                        'action': 'query',
                        'format': 'json',
                        'titles': page_title,
                        'prop': 'extracts',
                        'exintro': True,
                        'explaintext': True,
                        'exsectionformat': 'plain'
                    }
                    
                    content_response = requests.get(search_url, params=content_params, headers=self.headers, timeout=10)
                    
                    if content_response.status_code == 200:
                        content_data = content_response.json()
                        pages = content_data.get('query', {}).get('pages', {})
                        
                        for page_id, page_data in pages.items():
                            if page_data.get('extract'):
                                return {
                                    "source": "ویکی‌پدیا فارسی",
                                    "title": page_data.get('title', ''),
                                    "content": page_data.get('extract', ''),
                                    "url": f"https://fa.wikipedia.org/wiki/{page_title.replace(' ', '_')}",
                                    "type": "encyclopedia"
                                }
        
        except Exception as e:
            print(f"خطا در جستجوی ویکی‌پدیا: {e}")
        
        return None
    
    async def _search_duckduckgo(self, query: str) -> List[Dict]:
        """جستجو در DuckDuckGo"""
        try:
            # DuckDuckGo Instant Answer API
            params = {
                'q': query,
                'format': 'json',
                'no_html': '1',
                'skip_disambig': '1'
            }
            
            response = requests.get(
                "https://api.duckduckgo.com/",
                params=params,
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                results = []
                
                # Abstract (خلاصه اصلی)
                if data.get('Abstract'):
                    results.append({
                        "source": "DuckDuckGo",
                        "title": data.get('AbstractText', ''),
                        "content": data.get('Abstract', ''),
                        "url": data.get('AbstractURL', ''),
                        "type": "abstract"
                    })
                
                # Definition (تعریف)
                if data.get('Definition'):
                    results.append({
                        "source": "تعریف",
                        "title": "تعریف",
                        "content": data.get('Definition', ''),
                        "url": data.get('DefinitionURL', ''),
                        "type": "definition"
                    })
                
                # Answer (پاسخ مستقیم)
                if data.get('Answer'):
                    results.append({
                        "source": "پاسخ مستقیم",
                        "title": "پاسخ",
                        "content": data.get('Answer', ''),
                        "url": "",
                        "type": "direct_answer"
                    })
                
                # اگر نتیجه‌ای نیافتیم، یک پاسخ عمومی بدهیم
                if not results:
                    results.append({
                        "source": "سیستم",
                        "title": "اطلاعات عمومی",
                        "content": f"متأسفانه اطلاعات دقیقی درباره '{query}' در دسترس نیست، اما می‌توانم بر اساس دانش عمومی‌ام کمکتان کنم.",
                        "url": "",
                        "type": "fallback"
                    })
                
                return results
        
        except Exception as e:
            print(f"خطا در جستجوی DuckDuckGo: {e}")
        
        return []
    
    def _summarize_results(self, results: List[Dict], original_query: str) -> str:
        """خلاصه‌سازی نتایج جستجو"""
        
        if not results:
            return "متأسفانه اطلاعات مرتبطی پیدا نکردم."
        
        summary_parts = []
        
        for result in results[:3]:  # فقط 3 نتیجه اول
            content = result.get('content', '').strip()
            source = result.get('source', 'منبع نامشخص')
            
            if content:
                # محدود کردن طول محتوا
                if len(content) > 200:
                    content = content[:200] + "..."
                
                summary_parts.append(f"📌 {source}: {content}")
        
        if summary_parts:
            summary = "\n\n".join(summary_parts)
            summary += f"\n\n🔍 این اطلاعات از جستجوی اینترنت برای سؤال شما دریافت شد."
            return summary
        
        return "اطلاعاتی پیدا شد اما قابل خلاصه‌سازی نبود."
    
    def is_online(self) -> bool:
        """بررسی اتصال به اینترنت"""
        try:
            response = requests.get("https://www.google.com", timeout=5)
            return response.status_code == 200
        except:
            return False