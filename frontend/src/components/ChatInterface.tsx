import React, { useRef, useEffect } from 'react';
import styled, { keyframes } from 'styled-components';
import MessageBubble from './MessageBubble.tsx';
import MessageInput from './MessageInput.tsx';

const fadeIn = keyframes`
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
`;

const ChatContainer = styled.div`
  display: flex;
  flex-direction: column;
  height: 100%;
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(20px);
  margin: 1rem;
  border-radius: 25px;
  border: 1px solid rgba(255, 255, 255, 0.15);
  overflow: hidden;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  animation: ${fadeIn} 0.6s ease-out;
  
  @media (max-width: 768px) {
    margin: 0.5rem;
    border-radius: 20px;
  }
`;

const MessagesArea = styled.div`
  flex: 1;
  overflow-y: auto;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  
  &::-webkit-scrollbar {
    width: 8px;
  }
  
  &::-webkit-scrollbar-track {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 4px;
  }
  
  &::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.3);
    border-radius: 4px;
    
    &:hover {
      background: rgba(255, 255, 255, 0.5);
    }
  }
  
  @media (max-width: 768px) {
    padding: 1rem;
  }
`;

const LoadingIndicator = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.8rem;
  color: rgba(255, 255, 255, 0.8);
  font-size: 1rem;
  padding: 1.5rem;
  font-family: 'Vazirmatn', sans-serif;
  
  .dots {
    display: flex;
    gap: 6px;
  }
  
  .dot {
    width: 8px;
    height: 8px;
    background: rgba(255, 255, 255, 0.6);
    border-radius: 50%;
    animation: pulse 1.4s ease-in-out infinite both;
  }
  
  .dot:nth-child(1) { animation-delay: -0.32s; }
  .dot:nth-child(2) { animation-delay: -0.16s; }
  .dot:nth-child(3) { animation-delay: 0s; }
  
  @keyframes pulse {
    0%, 80%, 100% {
      transform: scale(0.8);
      opacity: 0.5;
    }
    40% {
      transform: scale(1.2);
      opacity: 1;
    }
  }
`;

const WelcomeMessage = styled.div`
  text-align: center;
  color: rgba(255, 255, 255, 0.9);
  padding: 3rem 2rem;
  font-family: 'Vazirmatn', sans-serif;
  
  .emoji {
    font-size: 4rem;
    margin-bottom: 1.5rem;
    display: block;
    animation: bounce 2s infinite;
  }
  
  h2 {
    margin-bottom: 1rem;
    font-size: 2rem;
    font-weight: 600;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
  }
  
  p {
    margin-bottom: 0.8rem;
    opacity: 0.8;
    font-size: 1.1rem;
    line-height: 1.6;
  }
  
  .features {
    margin-top: 2rem;
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 1rem;
    text-align: right;
  }
  
  .feature {
    background: rgba(255, 255, 255, 0.1);
    padding: 1rem;
    border-radius: 15px;
    border: 1px solid rgba(255, 255, 255, 0.2);
    
    .feature-icon {
      font-size: 1.5rem;
      margin-bottom: 0.5rem;
      display: block;
    }
    
    .feature-title {
      font-weight: 600;
      margin-bottom: 0.3rem;
      font-size: 0.9rem;
    }
    
    .feature-desc {
      font-size: 0.8rem;
      opacity: 0.7;
    }
  }
  
  @keyframes bounce {
    0%, 20%, 50%, 80%, 100% {
      transform: translateY(0);
    }
    40% {
      transform: translateY(-15px);
    }
    60% {
      transform: translateY(-7px);
    }
  }
  
  @media (max-width: 768px) {
    padding: 2rem 1rem;
    
    .emoji {
      font-size: 3rem;
    }
    
    h2 {
      font-size: 1.5rem;
    }
    
    p {
      font-size: 1rem;
    }
    
    .features {
      grid-template-columns: 1fr;
    }
  }
`;

const ConnectionStatus = styled.div<{ $connected: boolean }>`
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  padding: 1rem;
  background: ${props => props.$connected 
    ? 'rgba(34, 197, 94, 0.2)' 
    : 'rgba(239, 68, 68, 0.2)'
  };
  color: ${props => props.$connected ? '#22c55e' : '#ef4444'};
  font-family: 'Vazirmatn', sans-serif;
  font-weight: 500;
  border-radius: 10px;
  margin: 1rem;
  border: 1px solid ${props => props.$connected 
    ? 'rgba(34, 197, 94, 0.3)' 
    : 'rgba(239, 68, 68, 0.3)'
  };
  
  .status-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: currentColor;
    animation: ${props => props.$connected ? 'pulse 2s infinite' : 'none'};
  }
`;

interface Message {
  id: string;
  type: 'user' | 'ai' | 'system';
  message: string;
  timestamp: string;
}

interface ChatInterfaceProps {
  messages: Message[];
  onSendMessage: (message: string) => void;
  isLoading: boolean;
  isConnected: boolean;
  onPlayAudio?: (text: string) => void; // اضافه کردن callback برای پخش صدا
}

const ChatInterface: React.FC<ChatInterfaceProps> = ({
  messages,
  onSendMessage,
  isLoading,
  isConnected,
  onPlayAudio
}) => {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSendMessage = (message: string) => {
    if (message.trim() && isConnected) {
      onSendMessage(message.trim());
    }
  };

  return (
    <ChatContainer>
      <MessagesArea>
        {!isConnected && (
          <ConnectionStatus $connected={false}>
            <div className="status-dot"></div>
            <span>در حال اتصال به سرور...</span>
          </ConnectionStatus>
        )}
        
        {messages.length === 0 && isConnected ? (
          <WelcomeMessage>
            <span className="emoji">🦊</span>
            <h2>سلام! من روباه هستم</h2>
            <p>دستیار هوش مصنوعی شخصی شما</p>
            <p>آماده‌ام تا با شما رشد کنم و شما را بشناسم</p>
            <p>چیزی بپرسید یا با من حرف بزنید!</p>
            
            <div className="features">
              <div className="feature">
                <span className="feature-icon">🧠</span>
                <div className="feature-title">یادگیری هوشمند</div>
                <div className="feature-desc">از هر مکالمه یاد می‌گیرم</div>
              </div>
              <div className="feature">
                <span className="feature-icon">💾</span>
                <div className="feature-title">حافظه بلندمدت</div>
                <div className="feature-desc">همه چیز را به خاطر می‌سپارم</div>
              </div>
              <div className="feature">
                <span className="feature-icon">🎭</span>
                <div className="feature-title">شخصیت منحصر به فرد</div>
                <div className="feature-desc">با شما رشد می‌کنم</div>
              </div>
              <div className="feature">
                <span className="feature-icon">🇮🇷</span>
                <div className="feature-title">پشتیبانی کامل فارسی</div>
                <div className="feature-desc">به زبان مادری صحبت می‌کنم</div>
              </div>
            </div>
          </WelcomeMessage>
        ) : (
          messages.map((message) => (
            <MessageBubble
              key={message.id}
              type={message.type}
              message={message.message}
              timestamp={message.timestamp}
              onPlayAudio={onPlayAudio}
            />
          ))
        )}
        
        {isLoading && (
          <LoadingIndicator>
            <span>صبور باشید، در حال آماده کردن جواب روباه...</span>
            <div className="dots">
              <div className="dot"></div>
              <div className="dot"></div>
              <div className="dot"></div>
            </div>
          </LoadingIndicator>
        )}
        
        <div ref={messagesEndRef} />
      </MessagesArea>
      
      <MessageInput
        onSendMessage={handleSendMessage}
        disabled={!isConnected || isLoading}
        placeholder={
          !isConnected 
            ? "در حال اتصال..." 
            : isLoading 
            ? "صبر کنید..." 
            : "پیام خود را بنویسید..."
        }
      />
    </ChatContainer>
  );
};

export default ChatInterface;