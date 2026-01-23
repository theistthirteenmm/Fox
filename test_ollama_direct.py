#!/usr/bin/env python3
"""
تست مستقیم Ollama
"""

import requests
import json

def test_ollama():
    """تست مستقیم Ollama API"""
    
    url = "http://localhost:11434/api/generate"
    
    data = {
        "model": "partai/dorna-llama3:8b-instruct-q8_0",
        "prompt": "سلام، چطوری؟",
        "stream": False,
        "options": {
            "temperature": 0.7,
            "top_p": 0.9,
            "max_tokens": 400
        }
    }
    
    print("🔄 ارسال درخواست به Ollama...")
    print(f"URL: {url}")
    print(f"Model: {data['model']}")
    print(f"Prompt: {data['prompt']}")
    
    try:
        response = requests.post(
            url,
            json=data,
            proxies={'http': None, 'https': None},
            timeout=30
        )
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"📋 Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ پاسخ: {result.get('response', 'پاسخ خالی')}")
        else:
            print(f"❌ خطا: {response.text}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")

if __name__ == "__main__":
    test_ollama()