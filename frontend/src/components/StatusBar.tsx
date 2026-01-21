import React, { useState } from 'react';
import styled from 'styled-components';

const StatusContainer = styled.div`
  background: rgba(0, 0, 0, 0.2);
  padding: 0.5rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.85rem;
  color: rgba(255, 255, 255, 0.8);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
`;

const StatusGroup = styled.div`
  display: flex;
  align-items: center;
  gap: 1.5rem;
`;

const StatusItem = styled.div<{ $status?: 'good' | 'warning' | 'error' }>`
  display: flex;
  align-items: center;
  gap: 0.5rem;
  
  .indicator {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: ${props => {
      switch (props.$status) {
        case 'good': return '#4ade80';
        case 'warning': return '#fbbf24';
        case 'error': return '#ef4444';
        default: return '#6b7280';
      }
    }};
    animation: ${props => props.$status === 'good' ? 'pulse 2s infinite' : 'none'};
  }
  
  @keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
  }
`;

const MemoryInfo = styled.div`
  display: flex;
  align-items: center;
  gap: 1rem;
  font-size: 0.8rem;
`;

const MemoryItem = styled.span`
  display: flex;
  align-items: center;
  gap: 0.25rem;
  
  .count {
    font-weight: bold;
    color: #60a5fa;
  }
`;

const PersonalityLevel = styled.div`
  display: flex;
  align-items: center;
  gap: 0.5rem;
  
  .level {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 2px 8px;
    border-radius: 12px;
    font-size: 0.75rem;
    font-weight: bold;
  }
`;

interface SystemStatus {
  status: string;
  brain_loaded: boolean;
  memory_size: {
    short_term: number;
    conversations: number;
    knowledge: number;
  };
  personality_level: number;
  web_search?: {
    web_enabled: boolean;
    internet_connected: boolean;
    search_engines: string[];
  };
  dataset_stats?: {
    conversation_patterns: number;
    emotion_types: number;
    topics: number;
    prompt_templates: number;
  };
  timestamp: string;
}

interface StatusBarProps {
  isConnected: boolean;
  systemStatus: SystemStatus | null;
  uploadStatus?: {
    isUploading: boolean;
    fileName?: string;
    progress?: number;
  };
}

const StatusBar: React.FC<StatusBarProps> = ({ isConnected, systemStatus, uploadStatus }) => {
  const [isRestarting, setIsRestarting] = useState(false);
  const [restartStatus, setRestartStatus] = useState<string>('');

  const restartSystem = async () => {
    if (isRestarting) return;
    
    const confirmed = window.confirm('آیا مطمئنید که می‌خواهید سیستم را ریستارت کنید؟\n\nاین کار در صورت هنگ کردن سیستم مفید است.');
    if (!confirmed) return;

    try {
      setIsRestarting(true);
      setRestartStatus('🔄 در حال ریستارت...');
      
      const response = await fetch('http://localhost:8000/system/restart', {
        method: 'POST',
      });
      
      if (response.ok) {
        setRestartStatus('✅ ریستارت شد - صفحه تازه می‌شود');
        
        // بعد از 3 ثانیه صفحه رو refresh کن
        setTimeout(() => {
          window.location.reload();
        }, 3000);
      } else {
        setRestartStatus('❌ خطا در ریستارت');
        setTimeout(() => setRestartStatus(''), 3000);
      }
    } catch (error) {
      setRestartStatus('❌ خطا در ارتباط');
      setTimeout(() => setRestartStatus(''), 3000);
    }
    
    setTimeout(() => {
      setIsRestarting(false);
    }, 5000);
  };
  const getConnectionStatus = () => {
    if (!isConnected) return 'error';
    return 'good';
  };

  const getBrainStatus = () => {
    if (!systemStatus) return 'warning';
    return systemStatus.brain_loaded ? 'good' : 'warning';
  };

  const getWebSearchStatus = () => {
    if (!systemStatus?.web_search) return 'warning';
    if (!systemStatus.web_search.web_enabled) return 'warning';
    return systemStatus.web_search.internet_connected ? 'good' : 'error';
  };

  const formatLastUpdate = (timestamp: string) => {
    try {
      const date = new Date(timestamp);
      const now = new Date();
      const diff = Math.floor((now.getTime() - date.getTime()) / 1000);
      
      if (diff < 60) return 'همین الان';
      if (diff < 3600) return `${Math.floor(diff / 60)} دقیقه پیش`;
      return `${Math.floor(diff / 3600)} ساعت پیش`;
    } catch {
      return 'نامشخص';
    }
  };

  return (
    <StatusContainer>
      <StatusGroup>
        <StatusItem $status={getConnectionStatus()}>
          <div className="indicator" />
          <span>
            {isConnected ? 'متصل' : 'قطع شده'}
          </span>
        </StatusItem>
        
        <StatusItem $status={getBrainStatus()}>
          <div className="indicator" />
          <span>
            {systemStatus?.brain_loaded ? 'مغز فعال' : 'در حال بارگذاری'}
          </span>
        </StatusItem>
        
        <StatusItem $status={getWebSearchStatus()}>
          <div className="indicator" />
          <span>
            {systemStatus?.web_search?.web_enabled 
              ? (systemStatus.web_search.internet_connected ? '🌐 آنلاین' : '🌐 آفلاین')
              : '🌐 غیرفعال'
            }
          </span>
        </StatusItem>
        
        {systemStatus && (
          <PersonalityLevel>
            <span>🧠</span>
            <span>سطح:</span>
            <div className="level">
              {systemStatus.personality_level}
            </div>
          </PersonalityLevel>
        )}
      </StatusGroup>
      
      {systemStatus && (
        <StatusGroup>
          <MemoryInfo>
            <MemoryItem>
              <span>💭</span>
              <span>حافظه کوتاه:</span>
              <span className="count">{systemStatus.memory_size.short_term}</span>
            </MemoryItem>
            
            <MemoryItem>
              <span>💬</span>
              <span>مکالمات:</span>
              <span className="count">{systemStatus.memory_size.conversations}</span>
            </MemoryItem>
            
            <MemoryItem>
              <span>📚</span>
              <span>دانش:</span>
              <span className="count">{systemStatus.memory_size.knowledge}</span>
            </MemoryItem>
            
            {systemStatus.dataset_stats && (
              <MemoryItem>
                <span>🧠</span>
                <span>الگوها:</span>
                <span className="count">{systemStatus.dataset_stats.conversation_patterns}</span>
              </MemoryItem>
            )}
          </MemoryInfo>
          
          <StatusItem>
            <span>🕐</span>
            <span>{formatLastUpdate(systemStatus.timestamp)}</span>
          </StatusItem>
          
          {/* دکمه ریستارت */}
          <StatusItem 
            style={{ 
              cursor: 'pointer', 
              opacity: isRestarting ? 0.6 : 1,
              backgroundColor: isRestarting ? 'rgba(255,193,7,0.2)' : 'rgba(220,53,69,0.2)',
              padding: '4px 8px',
              borderRadius: '8px',
              border: '1px solid rgba(220,53,69,0.3)'
            }}
            onClick={restartSystem}
            title="ریستارت سیستم (در صورت هنگ کردن)"
          >
            <span>{isRestarting ? '🔄' : '🔴'}</span>
            <span>{isRestarting ? 'ریستارت...' : 'ریستارت'}</span>
          </StatusItem>
          
          {restartStatus && (
            <StatusItem style={{ color: '#ffc107' }}>
              <span>{restartStatus}</span>
            </StatusItem>
          )}
        </StatusGroup>
      )}
    </StatusContainer>
  );
};

export default StatusBar;