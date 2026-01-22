import React, { useState, useEffect, useRef } from 'react';
import './App.css';

interface Message {
  id: string;
  type: 'user' | 'ai' | 'system' | 'thinking';
  message: string;
  timestamp: string;
}

function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isConnected, setIsConnected] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const [inputMessage, setInputMessage] = useState('');
  const wsRef = useRef<WebSocket | null>(null);

  useEffect(() => {
    connectWebSocket();
    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, []);

  const connectWebSocket = () => {
    try {
      const ws = new WebSocket('ws://localhost:8000/chat');
      
      ws.onopen = () => {
        console.log('🔗 اتصال برقرار شد');
        setIsConnected(true);
      };
      
      ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          
          if (data.type === 'thinking') {
            // برای پیام‌های thinking، آخرین پیام thinking را جایگزین کن
            setMessages(prev => {
              const filtered = prev.filter(msg => msg.type !== 'thinking');
              const newMessage: Message = {
                id: 'thinking-' + Date.now().toString(),
                type: 'thinking',
                message: data.message,
                timestamp: data.timestamp
              };
              return [...filtered, newMessage];
            });
          } else {
            // برای پیام‌های عادی، پیام‌های thinking را حذف کن و پیام جدید اضافه کن
            setMessages(prev => {
              const filtered = prev.filter(msg => msg.type !== 'thinking');
              const newMessage: Message = {
                id: Date.now().toString(),
                type: data.type,
                message: data.message,
                timestamp: data.timestamp
              };
              return [...filtered, newMessage];
            });
            
            setIsLoading(false);
          }
        } catch (error) {
          console.error('خطا در پردازش پیام:', error);
        }
      };
      
      ws.onclose = () => {
        console.log('🔌 اتصال قطع شد');
        setIsConnected(false);
        setTimeout(() => connectWebSocket(), 3000);
      };
      
      ws.onerror = (error) => {
        console.error('خطای WebSocket:', error);
        setIsConnected(false);
      };
      
      wsRef.current = ws;
      
    } catch (error) {
      console.error('خطا در اتصال:', error);
      setTimeout(() => connectWebSocket(), 3000);
    }
  };

  const sendMessage = () => {
    if (!wsRef.current || wsRef.current.readyState !== WebSocket.OPEN || !inputMessage.trim()) {
      return;
    }

    // اضافه کردن پیام کاربر
    const userMessage: Message = {
      id: Date.now().toString(),
      type: 'user',
      message: inputMessage,
      timestamp: new Date().toISOString()
    };
    
    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    // ارسال به سرور
    wsRef.current.send(JSON.stringify({
      message: inputMessage,
      timestamp: new Date().toISOString()
    }));

    setInputMessage('');
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>🦊 روباه - دستیار هوش مصنوعی</h1>
        <p>دستیار شخصی که با شما رشد می‌کند</p>
      </header>
      
      <div className="status-bar">
        <span className={`status ${isConnected ? 'connected' : 'disconnected'}`}>
          {isConnected ? '🟢 متصل' : '🔴 قطع'}
        </span>
      </div>
      
      <main className="chat-container">
        <div className="messages-area">
          {messages.length === 0 && isConnected ? (
            <div className="welcome-message">
              <span className="emoji">🦊</span>
              <h2>سلام! من روباه هستم</h2>
              <p>دستیار هوش مصنوعی شخصی شما</p>
              <p>چیزی بپرسید یا با من حرف بزنید!</p>
            </div>
          ) : (
            messages.map((message) => (
              <div key={message.id} className={`message ${message.type}`}>
                {message.type === 'thinking' ? (
                  <div className="thinking-message">
                    <span>🦊</span>
                    <span>{message.message}</span>
                    <div className="thinking-dots">
                      <div className="dot"></div>
                      <div className="dot"></div>
                      <div className="dot"></div>
                    </div>
                  </div>
                ) : (
                  <>
                    <div className="message-content">{message.message}</div>
                    <div className="message-time">
                      {new Date(message.timestamp).toLocaleTimeString('fa-IR')}
                    </div>
                  </>
                )}
              </div>
            ))
          )}
          
          {isLoading && (
            <div className="loading">
              <span>🦊 روباه در حال فکر کردن</span>
              <div className="dots">
                <div className="dot"></div>
                <div className="dot"></div>
                <div className="dot"></div>
              </div>
            </div>
          )}
        </div>
        
        <div className="input-area">
          <textarea
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder={
              !isConnected 
                ? "در حال اتصال..." 
                : isLoading 
                ? "صبر کنید..." 
                : "پیام خود را بنویسید..."
            }
            disabled={!isConnected || isLoading}
            rows={3}
          />
          <button 
            onClick={sendMessage}
            disabled={!isConnected || isLoading || !inputMessage.trim()}
          >
            📤 ارسال
          </button>
        </div>
      </main>
    </div>
  );
}

export default App;