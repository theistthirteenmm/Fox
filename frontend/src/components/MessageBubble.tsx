import React from 'react';
import styled from 'styled-components';
import ReactMarkdown from 'react-markdown';

const BubbleContainer = styled.div<{ $isUser: boolean; $isSystem: boolean }>`
  display: flex;
  justify-content: ${props => props.$isUser ? 'flex-end' : 'flex-start'};
  margin-bottom: 1rem;
  opacity: ${props => props.$isSystem ? 0.8 : 1};
`;

const Bubble = styled.div<{ $isUser: boolean; $isSystem: boolean }>`
  max-width: 75%;
  min-width: 120px;
  padding: 1.2rem 1.8rem;
  border-radius: 20px;
  position: relative;
  word-wrap: break-word;
  word-break: normal;
  overflow-wrap: break-word;
  hyphens: auto;
  white-space: pre-wrap;
  
  ${props => props.$isUser ? `
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-bottom-right-radius: 8px;
  ` : props.$isSystem ? `
    background: rgba(255, 193, 7, 0.2);
    color: rgba(255, 255, 255, 0.9);
    border: 1px solid rgba(255, 193, 7, 0.3);
    text-align: center;
    font-style: italic;
  ` : `
    background: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(10px);
    color: white;
    border: 1px solid rgba(255, 255, 255, 0.2);
    border-bottom-left-radius: 8px;
  `}
  
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  
  @media (max-width: 768px) {
    max-width: 85%;
    padding: 1rem 1.4rem;
  }
`;

const Avatar = styled.div<{ $isUser: boolean }>`
  width: 45px;
  height: 45px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.4rem;
  margin: ${props => props.$isUser ? '0 0 0 1rem' : '0 1rem 0 0'};
  background: ${props => props.$isUser 
    ? 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)'
    : 'linear-gradient(135deg, #fa709a 0%, #fee140 100%)'
  };
  color: white;
  font-weight: bold;
  flex-shrink: 0;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
`;

const MessageContent = styled.div`
  line-height: 1.6;
  font-size: 1rem;
  word-spacing: normal;
  letter-spacing: normal;
  
  p {
    margin: 0 0 0.8rem 0;
    word-wrap: break-word;
    word-break: normal;
    overflow-wrap: break-word;
    white-space: pre-wrap;
    
    &:last-child {
      margin-bottom: 0;
    }
  }
  
  /* فارسی متن برای بهتر نمایش */
  &[dir="rtl"] {
    text-align: right;
    direction: rtl;
  }
  
  code {
    background: rgba(0, 0, 0, 0.2);
    padding: 3px 8px;
    border-radius: 4px;
    font-family: 'Courier New', monospace;
    font-size: 0.9em;
    word-break: break-all;
  }
  
  pre {
    background: rgba(0, 0, 0, 0.3);
    padding: 1rem;
    border-radius: 8px;
    overflow-x: auto;
    margin: 0.8rem 0;
    white-space: pre-wrap;
    word-wrap: break-word;
    
    code {
      background: none;
      padding: 0;
      word-break: normal;
    }
  }
  
  ul, ol {
    margin: 0.8rem 0;
    padding-right: 1.5rem;
  }
  
  li {
    margin-bottom: 0.4rem;
    word-wrap: break-word;
  }
  
  /* جلوگیری از شکستن کلمات فارسی */
  * {
    word-break: normal;
    overflow-wrap: break-word;
    hyphens: auto;
  }
`;

const Timestamp = styled.div<{ $isUser: boolean }>`
  font-size: 0.75rem;
  opacity: 0.6;
  margin-top: 0.5rem;
  text-align: ${props => props.$isUser ? 'left' : 'right'};
`;

const MessageWrapper = styled.div<{ $isUser: boolean }>`
  display: flex;
  align-items: flex-end;
  flex-direction: ${props => props.$isUser ? 'row-reverse' : 'row'};
  max-width: 100%;
`;

const BubbleContent = styled.div`
  flex: 1;
  min-width: 0;
`;

interface MessageBubbleProps {
  type: 'user' | 'ai' | 'system';
  message: string;
  timestamp: string;
}

const MessageBubble: React.FC<MessageBubbleProps> = ({ type, message, timestamp }) => {
  const isUser = type === 'user';
  const isSystem = type === 'system';
  
  const formatTime = (timestamp: string) => {
    try {
      const date = new Date(timestamp);
      return date.toLocaleTimeString('fa-IR', { 
        hour: '2-digit', 
        minute: '2-digit',
        hour12: false 
      });
    } catch {
      return '';
    }
  };

  const getAvatar = () => {
    if (isUser) return '👤';
    if (isSystem) return '🔔';
    return '🦊';
  };

  return (
    <BubbleContainer $isUser={isUser} $isSystem={isSystem}>
      <MessageWrapper $isUser={isUser}>
        {!isSystem && (
          <Avatar $isUser={isUser}>
            {getAvatar()}
          </Avatar>
        )}
        
        <BubbleContent>
          <Bubble $isUser={isUser} $isSystem={isSystem}>
            <MessageContent className="message-content">
              {isSystem ? (
                message
              ) : (
                <ReactMarkdown>{message}</ReactMarkdown>
              )}
            </MessageContent>
            
            {timestamp && (
              <Timestamp $isUser={isUser}>
                {formatTime(timestamp)}
              </Timestamp>
            )}
          </Bubble>
        </BubbleContent>
      </MessageWrapper>
    </BubbleContainer>
  );
};

export default MessageBubble;