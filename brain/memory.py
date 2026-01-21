"""
سیستم حافظه روباه
مدیریت ذخیره و بازیابی اطلاعات
"""

import chromadb
from chromadb.config import Settings
import json
import os
from datetime import datetime
from typing import List, Dict, Optional
import hashlib

class MemoryManager:
    def __init__(self):
        # راه‌اندازی ChromaDB برای حافظه vector
        self.chroma_client = chromadb.PersistentClient(
            path="data/memory",
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Collection برای مکالمات
        self.conversations = self.chroma_client.get_or_create_collection(
            name="conversations",
            metadata={"description": "تاریخچه مکالمات کاربر"}
        )
        
        # Collection برای دانش کلی
        self.knowledge = self.chroma_client.get_or_create_collection(
            name="knowledge", 
            metadata={"description": "دانش و اطلاعات یادگیری شده"}
        )
        
        # حافظه کوتاه‌مدت (در RAM)
        self.short_term_memory = []
        self.max_short_term = 50
        
        print("🧠 سیستم حافظه راه‌اندازی شد")
    
    def store_conversation(self, role: str, content: str, metadata: Dict = None):
        """ذخیره مکالمه در حافظه"""
        
        timestamp = datetime.now()
        conversation_id = self._generate_id(f"{role}_{content}_{timestamp}")
        
        # ذخیره در حافظه کوتاه‌مدت
        memory_item = {
            "id": conversation_id,
            "role": role,
            "content": content,
            "timestamp": timestamp.isoformat(),
            "metadata": metadata or {}
        }
        
        self.short_term_memory.append(memory_item)
        
        # محدود کردن حافظه کوتاه‌مدت
        if len(self.short_term_memory) > self.max_short_term:
            # انتقال قدیمی‌ترین آیتم به حافظه بلندمدت
            old_item = self.short_term_memory.pop(0)
            self._store_to_long_term(old_item)
        
        # ذخیره مهم‌ترین مکالمات در vector database
        if self._is_important_conversation(content):
            self._store_to_vector_db(memory_item)
        
        print(f"💾 ذخیره شد: {role} - {content[:50]}...")
    
    def get_relevant_context(self, query: str, limit: int = 5) -> List[Dict]:
        """بازیابی context مرتبط برای query"""
        
        relevant_memories = []
        
        # جستجو در حافظه کوتاه‌مدت
        for item in reversed(self.short_term_memory[-10:]):  # آخرین 10 مورد
            relevant_memories.append(item)
        
        # جستجو در vector database با error handling
        try:
            results = self.conversations.query(
                query_texts=[query],
                n_results=min(limit, 10)
            )
            
            if results['documents'] and results['documents'][0]:
                for i, doc in enumerate(results['documents'][0]):
                    metadata = results['metadatas'][0][i] if results['metadatas'] else {}
                    relevant_memories.append({
                        "content": doc,
                        "metadata": metadata,
                        "similarity_score": results['distances'][0][i] if results['distances'] else 0
                    })
        
        except Exception as e:
            print(f"خطا در جستجوی vector: {e}")
            # در صورت خطا، فقط از حافظه کوتاه‌مدت استفاده کن
            print("🔄 استفاده از حافظه کوتاه‌مدت به جای vector search")
        
        return relevant_memories[:limit]
    
    def get_memory_count(self) -> Dict[str, int]:
        """تعداد آیتم‌های حافظه"""
        return {
            "short_term": len(self.short_term_memory),
            "conversations": self.conversations.count(),
            "knowledge": self.knowledge.count()
        }
    
    def _store_to_long_term(self, memory_item: Dict):
        """انتقال به حافظه بلندمدت"""
        os.makedirs("data/memory/long_term", exist_ok=True)
        
        filename = f"data/memory/long_term/{memory_item['timestamp'][:10]}.jsonl"
        with open(filename, "a", encoding="utf-8") as f:
            f.write(json.dumps(memory_item, ensure_ascii=False) + "\n")
    
    def _store_to_vector_db(self, memory_item: Dict):
        """ذخیره در vector database"""
        try:
            self.conversations.add(
                documents=[memory_item["content"]],
                metadatas=[{
                    "role": memory_item["role"],
                    "timestamp": memory_item["timestamp"],
                    **memory_item.get("metadata", {})
                }],
                ids=[memory_item["id"]]
            )
        except Exception as e:
            print(f"خطا در ذخیره vector: {e}")
    
    def _is_important_conversation(self, content: str) -> bool:
        """تشخیص اهمیت مکالمه"""
        important_keywords = [
            "یادگیری", "یاد بگیر", "به خاطر بسپار", "مهم", 
            "نام من", "اسم من", "دوست دارم", "علاقه دارم",
            "کار می‌کنم", "شغل", "خانواده", "سن"
        ]
        
        content_lower = content.lower()
        return any(keyword in content_lower for keyword in important_keywords)
    
    def _generate_id(self, text: str) -> str:
        """تولید ID یکتا"""
        return hashlib.md5(text.encode('utf-8')).hexdigest()
    
    def store_knowledge(self, topic: str, information: str, source: str = "user"):
        """ذخیره دانش جدید"""
        knowledge_id = self._generate_id(f"{topic}_{information}")
        
        try:
            self.knowledge.add(
                documents=[information],
                metadatas=[{
                    "topic": topic,
                    "source": source,
                    "timestamp": datetime.now().isoformat()
                }],
                ids=[knowledge_id]
            )
            print(f"📚 دانش جدید ذخیره شد: {topic}")
        except Exception as e:
            print(f"خطا در ذخیره دانش: {e}")
    
    def search_knowledge(self, query: str, limit: int = 3) -> List[Dict]:
        """جستجو در دانش ذخیره شده"""
        try:
            results = self.knowledge.query(
                query_texts=[query],
                n_results=limit
            )
            
            knowledge_items = []
            if results['documents'] and results['documents'][0]:
                for i, doc in enumerate(results['documents'][0]):
                    metadata = results['metadatas'][0][i] if results['metadatas'] else {}
                    knowledge_items.append({
                        "information": doc,
                        "topic": metadata.get("topic", "نامشخص"),
                        "source": metadata.get("source", "نامشخص"),
                        "timestamp": metadata.get("timestamp", "")
                    })
            
            return knowledge_items
            
        except Exception as e:
            print(f"خطا در جستجوی دانش: {e}")
            return []