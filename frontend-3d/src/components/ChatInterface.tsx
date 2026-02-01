import React, { useState, useRef, useEffect } from 'react';
import './ChatInterface.css';

interface ChatInterfaceProps {
  onListeningChange: (listening: boolean) => void;
  onSpeakingChange: (speaking: boolean) => void;
  onEmotionChange: (emotion: string) => void;
}

interface Message {
  id: string;
  text: string;
  sender: 'user' | 'fox';
  timestamp: Date;
}

const ChatInterface: React.FC<ChatInterfaceProps> = ({
  onListeningChange,
  onSpeakingChange,
  onEmotionChange
}) => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      text: 'سلام! من روباه هستم 🦊 چطور می‌تونم کمکت کنم؟',
      sender: 'fox',
      timestamp: new Date()
    }
  ]);
  const [inputText, setInputText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isMinimized, setIsMinimized] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async () => {
    if (!inputText.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      text: inputText,
      sender: 'user',
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputText('');
    setIsLoading(true);
    onSpeakingChange(true);
    onEmotionChange('thinking');

    try {
      const response = await fetch('http://localhost:8000/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          message: inputText,
          user_id: 'web-user'
        }),
      });

      if (response.ok) {
        const data = await response.json();
        const foxMessage: Message = {
          id: (Date.now() + 1).toString(),
          text: data.response || 'متأسفم، نتونستم پاسخ بدم.',
          sender: 'fox',
          timestamp: new Date()
        };
        setMessages(prev => [...prev, foxMessage]);
        onEmotionChange('happy');
      } else {
        throw new Error('خطا در ارتباط با سرور');
      }
    } catch (error) {
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        text: 'متأسفم، مشکلی پیش اومده. لطفاً دوباره تلاش کن.',
        sender: 'fox',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
      onEmotionChange('sad');
    } finally {
      setIsLoading(false);
      onSpeakingChange(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  const clearChat = () => {
    setMessages([{
      id: '1',
      text: 'چت پاک شد! چطور می‌تونم کمکت کنم؟ 🦊',
      sender: 'fox',
      timestamp: new Date()
    }]);
  };

  return (
    <div className={`chat-interface ${isMinimized ? 'minimized' : ''}`}>
      {/* هدر */}
      <div className="chat-header">
        <div className="chat-title">
          <span className="fox-icon">🦊</span>
          <span>چت با روباه</span>
          <div className={`status-indicator ${isLoading ? 'thinking' : 'online'}`}></div>
        </div>
        <div className="chat-controls">
          <button onClick={clearChat} className="control-btn" title="پاک کردن چت">
            🗑️
          </button>
          <button 
            onClick={() => setIsMinimized(!isMinimized)} 
            className="control-btn"
            title={isMinimized ? 'بزرگ کردن' : 'کوچک کردن'}
          >
            {isMinimized ? '⬆️' : '⬇️'}
          </button>
        </div>
      </div>

      {/* پیام‌ها */}
      <div className="messages-container">
        {messages.map((message) => (
          <div key={message.id} className={`message ${message.sender}`}>
            <div className="message-content">
              <div className="message-text">{message.text}</div>
              <div className="message-time">
                {message.timestamp.toLocaleTimeString('fa-IR', { 
                  hour: '2-digit', 
                  minute: '2-digit' 
                })}
              </div>
            </div>
            {message.sender === 'fox' && (
              <div className="message-avatar">🦊</div>
            )}
          </div>
        ))}
        
        {isLoading && (
          <div className="message fox">
            <div className="message-content">
              <div className="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
            <div className="message-avatar">🦊</div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {/* ورودی */}
      <div className="input-container">
        <div className="input-wrapper">
          <textarea
            value={inputText}
            onChange={(e) => setInputText(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="پیامت رو اینجا بنویس..."
            className="message-input"
            rows={1}
            disabled={isLoading}
          />
          <button 
            onClick={sendMessage} 
            className={`send-button ${isLoading ? 'loading' : ''}`}
            disabled={isLoading || !inputText.trim()}
          >
            {isLoading ? '⏳' : '🚀'}
          </button>
        </div>
        
        <div className="input-hints">
          <span>Enter: ارسال</span>
          <span>Shift+Enter: خط جدید</span>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;