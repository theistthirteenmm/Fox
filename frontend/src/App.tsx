import React, { useState, useEffect, useRef } from 'react';
import styled, { keyframes } from 'styled-components';
import ChatInterface from './components/ChatInterface.tsx';
import StatusBar from './components/StatusBar.tsx';
import './App.css';

const fadeIn = keyframes`
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
`;

const AppContainer = styled.div`
  display: flex;
  flex-direction: column;
  height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  font-family: 'Vazirmatn', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  direction: rtl;
  animation: ${fadeIn} 0.8s ease-out;
`;

const Header = styled.header`
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(20px);
  padding: 1.5rem 2rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 4px 32px rgba(0, 0, 0, 0.1);
`;

const Title = styled.h1`
  color: white;
  margin: 0;
  font-size: 2.2rem;
  font-weight: 600;
  text-align: center;
  text-shadow: 0 2px 10px rgba(0, 0, 0, 0.2);
  
  .emoji {
    margin-left: 0.8rem;
    font-size: 2.5rem;
    display: inline-block;
    animation: bounce 2s infinite;
  }
  
  @keyframes bounce {
    0%, 20%, 50%, 80%, 100% {
      transform: translateY(0);
    }
    40% {
      transform: translateY(-10px);
    }
    60% {
      transform: translateY(-5px);
    }
  }
  
  @media (max-width: 768px) {
    font-size: 1.8rem;
    
    .emoji {
      font-size: 2rem;
    }
  }
`;

const Subtitle = styled.p`
  color: rgba(255, 255, 255, 0.8);
  margin: 0.5rem 0 0 0;
  font-size: 1rem;
  text-align: center;
  font-weight: 300;
`;

const MainContent = styled.main`
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  position: relative;
`;

const BackgroundPattern = styled.div`
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  opacity: 0.05;
  background-image: 
    radial-gradient(circle at 25% 25%, white 2px, transparent 2px),
    radial-gradient(circle at 75% 75%, white 2px, transparent 2px);
  background-size: 50px 50px;
  background-position: 0 0, 25px 25px;
  pointer-events: none;
`;

interface Message {
  id: string;
  type: 'user' | 'ai' | 'system';
  message: string;
  timestamp: string;
  shouldAutoPlay?: boolean; // برای پخش خودکار
}

interface SystemStatus {
  status: string;
  brain_loaded: boolean;
  memory_size: { short_term: number; conversations: number; knowledge: number };
  personality_level: number;
  timestamp: string;
}

function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isConnected, setIsConnected] = useState(false);
  const [systemStatus, setSystemStatus] = useState<SystemStatus | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [autoPlayEnabled, setAutoPlayEnabled] = useState(false); // حالت پخش خودکار
  const wsRef = useRef<WebSocket | null>(null);
  const reconnectTimeoutRef = useRef<number | null>(null);
  const isConnectingRef = useRef(false);

  useEffect(() => {
    // تأخیر کوتاه برای اطمینان از بارگذاری کامل component
    const initTimeout = setTimeout(() => {
      connectWebSocket();
      fetchSystemStatus();
    }, 100);
    
    // بررسی وضعیت هر 30 ثانیه
    const statusInterval = setInterval(fetchSystemStatus, 30000);
    
    return () => {
      clearTimeout(initTimeout);
      clearInterval(statusInterval);
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current);
      }
      if (wsRef.current) {
        wsRef.current.close();
        wsRef.current = null;
      }
    };
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  const connectWebSocket = () => {
    // جلوگیری از اتصال همزمان چندگانه
    if (isConnectingRef.current || (wsRef.current && wsRef.current.readyState === WebSocket.OPEN)) {
      return;
    }

    isConnectingRef.current = true;

    try {
      const ws = new WebSocket('ws://localhost:8000/chat');
      
      ws.onopen = () => {
        console.log('🔗 اتصال برقرار شد');
        setIsConnected(true);
        isConnectingRef.current = false;
        
        // اضافه کردن پیام خوش‌آمدگویی فقط اگر پیام‌ها خالی باشد
        setMessages(prevMessages => {
          if (prevMessages.length === 0) {
            const welcomeMessage: Message = {
              id: 'welcome-' + Date.now().toString(),
              type: 'system',
              message: 'سلام! من روباه هستم، دستیار هوش مصنوعی شما. آماده‌ام تا با شما رشد کنم!',
              timestamp: new Date().toISOString()
            };
            return [welcomeMessage];
          }
          return prevMessages;
        });
      };
      
      ws.onmessage = (event) => {
        try {
          const data = JSON.parse(event.data);
          const newMessage: Message = {
            id: Date.now().toString(),
            type: data.type,
            message: data.message,
            timestamp: data.timestamp,
            shouldAutoPlay: data.type === 'ai' && autoPlayEnabled // پخش خودکار برای پیام‌های AI
          };
          
          setMessages(prev => [...prev, newMessage]);
          setIsLoading(false);

          // پخش خودکار اگه فعال باشه
          if (newMessage.shouldAutoPlay && newMessage.type === 'ai') {
            setTimeout(() => playTextToSpeech(newMessage.message), 500);
          }
        } catch (error) {
          console.error('خطا در پردازش پیام:', error);
        }
      };
      
      ws.onclose = () => {
        console.log('🔌 اتصال قطع شد');
        setIsConnected(false);
        isConnectingRef.current = false;
        
        // تلاش مجدد برای اتصال بعد از 3 ثانیه (فقط اگر component هنوز mount باشد)
        if (!reconnectTimeoutRef.current) {
          reconnectTimeoutRef.current = setTimeout(() => {
            reconnectTimeoutRef.current = null;
            connectWebSocket();
          }, 3000);
        }
      };
      
      ws.onerror = (error) => {
        console.error('خطای WebSocket:', error);
        setIsConnected(false);
        isConnectingRef.current = false;
      };
      
      wsRef.current = ws;
      
    } catch (error) {
      console.error('خطا در اتصال:', error);
      isConnectingRef.current = false;
      if (!reconnectTimeoutRef.current) {
        reconnectTimeoutRef.current = setTimeout(() => {
          reconnectTimeoutRef.current = null;
          connectWebSocket();
        }, 3000);
      }
    }
  };

  const fetchSystemStatus = async () => {
    try {
      const response = await fetch('http://localhost:8000/status');
      if (response.ok) {
        const status = await response.json();
        setSystemStatus(status);
      }
    } catch (error) {
      console.error('خطا در دریافت وضعیت:', error);
    }
  };

  const playTextToSpeech = async (text: string) => {
    try {
      const formData = new FormData();
      formData.append('text', text);

      const response = await fetch('http://localhost:8000/speech/text-to-speech', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const audioBlob = await response.blob();
        const audioUrl = URL.createObjectURL(audioBlob);
        const audio = new Audio(audioUrl);
        
        audio.onended = () => {
          URL.revokeObjectURL(audioUrl);
        };
        
        await audio.play();
      }
    } catch (error) {
      console.error('خطا در پخش صدا:', error);
    }
  };

  const sendMessage = (message: string) => {
    if (!wsRef.current || wsRef.current.readyState !== WebSocket.OPEN) {
      console.error('اتصال برقرار نیست');
      return;
    }

    // اضافه کردن پیام کاربر
    const userMessage: Message = {
      id: Date.now().toString(),
      type: 'user',
      message: message,
      timestamp: new Date().toISOString()
    };
    
    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    // ارسال به سرور
    wsRef.current.send(JSON.stringify({
      message: message,
      timestamp: new Date().toISOString()
    }));
  };

  return (
    <AppContainer>
      <Header>
        <Title>
          روباه - دستیار هوش مصنوعی
          <span className="emoji">🦊</span>
        </Title>
        <Subtitle>
          دستیار شخصی که با شما رشد می‌کند
        </Subtitle>
      </Header>
      
      <StatusBar 
        isConnected={isConnected}
        systemStatus={systemStatus}
      />
      
      <MainContent>
        <BackgroundPattern />
        <ChatInterface
          messages={messages}
          onSendMessage={sendMessage}
          isLoading={isLoading}
          isConnected={isConnected}
        />
      </MainContent>
    </AppContainer>
  );
}

export default App;