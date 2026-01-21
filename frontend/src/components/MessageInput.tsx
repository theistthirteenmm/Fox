import React, { useState, useRef, useEffect } from 'react';
import styled from 'styled-components';

const InputContainer = styled.div`
  padding: 1.5rem;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  
  @media (max-width: 768px) {
    padding: 1rem;
  }
`;

const InputWrapper = styled.div`
  display: flex;
  gap: 1rem;
  align-items: flex-end;
  max-width: 100%;
`;

const VoiceButton = styled.button<{ $isRecording?: boolean }>`
  padding: 1rem;
  border: none;
  border-radius: 50%;
  background: ${props => props.$isRecording ? 
    'linear-gradient(135deg, #f44336, #d32f2f)' : 
    'linear-gradient(135deg, #2196F3, #1976D2)'};
  color: white;
  cursor: pointer;
  font-size: 1.5rem;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 60px;
  height: 60px;
  
  &:hover {
    transform: scale(1.05);
    box-shadow: 0 4px 15px ${props => props.$isRecording ? 
      'rgba(244, 67, 54, 0.4)' : 'rgba(33, 150, 243, 0.4)'};
  }
  
  &:disabled {
    opacity: 0.6;
    cursor: not-allowed;
  }
`;

const FileButton = styled.label`
  padding: 1rem;
  border: none;
  border-radius: 50%;
  background: linear-gradient(135deg, #FF9800, #F57C00);
  color: white;
  cursor: pointer;
  font-size: 1.5rem;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 60px;
  height: 60px;
  
  &:hover {
    transform: scale(1.05);
    box-shadow: 0 4px 15px rgba(255, 152, 0, 0.4);
  }
  
  input {
    display: none;
  }
`;

const TextArea = styled.textarea<{ $disabled: boolean }>`
  flex: 1;
  min-height: 80px;
  max-height: 200px;
  padding: 1.2rem 1.5rem;
  border: 2px solid rgba(255, 255, 255, 0.2);
  border-radius: 25px;
  background: rgba(255, 255, 255, 0.1);
  color: white;
  font-size: 1.1rem;
  font-family: inherit;
  line-height: 1.5;
  resize: none;
  outline: none;
  transition: all 0.3s ease;
  word-wrap: break-word;
  word-break: normal;
  overflow-wrap: break-word;
  
  &::placeholder {
    color: rgba(255, 255, 255, 0.5);
    font-size: 1rem;
  }
  
  &:focus {
    border-color: rgba(255, 255, 255, 0.4);
    background: rgba(255, 255, 255, 0.15);
    min-height: 100px;
  }
  
  &:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }
  
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
  }
`;

const SendButton = styled.button<{ $disabled: boolean }>`
  width: 60px;
  height: 60px;
  border: none;
  border-radius: 50%;
  background: ${props => props.$disabled 
    ? 'rgba(255, 255, 255, 0.2)' 
    : 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
  };
  color: white;
  font-size: 1.4rem;
  cursor: ${props => props.$disabled ? 'not-allowed' : 'pointer'};
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  margin-bottom: 10px;
  
  &:hover:not(:disabled) {
    transform: scale(1.05);
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
  }
  
  &:active:not(:disabled) {
    transform: scale(0.95);
  }
  
  &:disabled {
    opacity: 0.5;
  }
`;

const CharCounter = styled.div<{ $isNearLimit: boolean }>`
  position: absolute;
  bottom: 8px;
  left: 16px;
  font-size: 0.75rem;
  color: ${props => props.$isNearLimit ? '#ff6b6b' : 'rgba(255, 255, 255, 0.5)'};
  pointer-events: none;
`;

const InputGroup = styled.div`
  position: relative;
  flex: 1;
`;

const QuickActions = styled.div`
  display: flex;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
  flex-wrap: wrap;
`;

const QuickActionButton = styled.button`
  padding: 0.5rem 1rem;
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 20px;
  background: rgba(255, 255, 255, 0.1);
  color: rgba(255, 255, 255, 0.8);
  font-size: 0.85rem;
  cursor: pointer;
  transition: all 0.2s ease;
  
  &:hover {
    background: rgba(255, 255, 255, 0.2);
    border-color: rgba(255, 255, 255, 0.5);
  }
`;

interface MessageInputProps {
  onSendMessage: (message: string) => void;
  disabled?: boolean;
  placeholder?: string;
  autoPlayEnabled?: boolean;
  onAutoPlayToggle?: (enabled: boolean) => void;
}

const MessageInput: React.FC<MessageInputProps> = ({
  onSendMessage,
  disabled = false,
  placeholder = "پیام خود را بنویسید...",
  autoPlayEnabled = false,
  onAutoPlayToggle
}) => {
  const [message, setMessage] = useState('');
  const [showQuickActions, setShowQuickActions] = useState(true);
  const [isRecording, setIsRecording] = useState(false);
  const [recordingStatus, setRecordingStatus] = useState('');
  const [localAutoPlay, setLocalAutoPlay] = useState(autoPlayEnabled); // حالت محلی
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const mediaRecorder = new MediaRecorder(stream);
      mediaRecorderRef.current = mediaRecorder;
      const audioChunks: Blob[] = [];

      mediaRecorder.ondataavailable = (event) => {
        if (event.data.size > 0) {
          audioChunks.push(event.data);
        }
      };

      mediaRecorder.onstop = async () => {
        const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
        const formData = new FormData();
        formData.append('audio_file', audioBlob, 'recording.wav');

        try {
          const response = await fetch('http://localhost:8000/speech/speech-to-text', {
            method: 'POST',
            body: formData,
          });

          const result = await response.json();
          
          if (result.success && result.text) {
            setMessage(result.text);
            setRecordingStatus('✅ صدا تبدیل شد');
          } else {
            setRecordingStatus('❌ متنی تشخیص داده نشد');
          }
        } catch (error) {
          setRecordingStatus('❌ خطا در تبدیل صدا');
        }

        stream.getTracks().forEach(track => track.stop());
        setTimeout(() => setRecordingStatus(''), 3000);
      };

      mediaRecorder.start();
      setIsRecording(true);
      setRecordingStatus('🎤 در حال ضبط...');

    } catch (error) {
      setRecordingStatus('❌ دسترسی به میکروفون امکان‌پذیر نیست');
      setTimeout(() => setRecordingStatus(''), 3000);
    }
  };

  const stopRecording = () => {
    if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'recording') {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  };

  const handleVoiceClick = () => {
    if (isRecording) {
      stopRecording();
    } else {
      startRecording();
    }
  };

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://localhost:8000/files/upload', {
        method: 'POST',
        body: formData,
      });

      const result = await response.json();
      
      if (result.success) {
        setMessage(`فایل "${result.file_info.filename}" آپلود شد.\n\n${result.content_preview}`);
      }
    } catch (error) {
      console.error('خطا در آپلود فایل:', error);
    }

    event.target.value = '';
  };

  const playTextToSpeech = async (text: string) => {
    if (!text.trim()) return;

    try {
      setRecordingStatus('در حال تولید صدا...');
      
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
        
        audio.onplay = () => setRecordingStatus('🔊 در حال پخش...');
        audio.onended = () => {
          setRecordingStatus('✅ پخش تمام شد');
          URL.revokeObjectURL(audioUrl);
          setTimeout(() => setRecordingStatus(''), 2000);
        };
        
        await audio.play();
      } else {
        setRecordingStatus('❌ خطا در تولید صدا');
        setTimeout(() => setRecordingStatus(''), 3000);
      }
    } catch (error) {
      console.error('خطا در تولید صدا:', error);
      setRecordingStatus('❌ خطا در تولید صدا');
      setTimeout(() => setRecordingStatus(''), 3000);
    }
  };

  const toggleAutoPlay = () => {
    const newState = !localAutoPlay;
    setLocalAutoPlay(newState);
    if (onAutoPlayToggle) {
      onAutoPlayToggle(newState);
    }
    setRecordingStatus(newState ? 
      '🔊 پخش خودکار فعال شد' : 
      '🔇 پخش خودکار غیرفعال شد'
    );
    setTimeout(() => setRecordingStatus(''), 2000);
  };
  
  const maxLength = 1000;
  const isNearLimit = message.length > maxLength * 0.8;
  const canSend = message.trim().length > 0 && !disabled && message.length <= maxLength;

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${textareaRef.current.scrollHeight}px`;
    }
  }, [message]);

  const handleSubmit = () => {
    if (canSend) {
      onSendMessage(message);
      setMessage('');
      setShowQuickActions(true);
      if (textareaRef.current) {
        textareaRef.current.style.height = 'auto';
      }
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    const value = e.target.value;
    if (value.length <= maxLength) {
      setMessage(value);
      setShowQuickActions(value.length === 0);
    }
  };

  const quickActions = [
    "سلام روباه! 👋",
    "حالت چطوره؟ 😊", 
    "چه کاری می‌تونی انجام بدی؟ 🤔",
    "بهم در مورد خودت بگو 🦊",
    "یه چیز جالب بهم بگو! ✨"
  ];

  const handleQuickAction = (action: string) => {
    setMessage(action);
    setShowQuickActions(false);
    textareaRef.current?.focus();
  };

  return (
    <InputContainer>
      {showQuickActions && message.length === 0 && (
        <QuickActions>
          {quickActions.map((action, index) => (
            <QuickActionButton
              key={index}
              onClick={() => handleQuickAction(action)}
              disabled={disabled}
            >
              {action}
            </QuickActionButton>
          ))}
        </QuickActions>
      )}
      
      <InputWrapper>
        <VoiceButton
          $isRecording={isRecording}
          onClick={handleVoiceClick}
          disabled={disabled}
          title={isRecording ? "توقف ضبط" : "شروع ضبط صدا"}
        >
          {isRecording ? '⏹️' : '🎤'}
        </VoiceButton>

        <FileButton>
          📁
          <input
            ref={fileInputRef}
            type="file"
            accept=".pdf,.docx,.txt,.png,.jpg,.jpeg,.wav,.mp3,.m4a"
            onChange={handleFileUpload}
            disabled={disabled}
          />
        </FileButton>

        <VoiceButton
          $isRecording={localAutoPlay}
          onClick={toggleAutoPlay}
          disabled={disabled}
          title={localAutoPlay ? 
            "پخش خودکار فعال - کلیک برای غیرفعال کردن" : 
            "پخش خودکار غیرفعال - کلیک برای فعال کردن"
          }
        >
          {localAutoPlay ? '🔊' : '🔇'}
        </VoiceButton>
        
        <InputGroup>
          <TextArea
            ref={textareaRef}
            value={message}
            onChange={handleInputChange}
            onKeyPress={handleKeyPress}
            placeholder={recordingStatus || placeholder}
            disabled={disabled}
            $disabled={disabled}
            rows={1}
          />
          {message.length > 0 && (
            <CharCounter $isNearLimit={isNearLimit}>
              {message.length}/{maxLength}
            </CharCounter>
          )}
        </InputGroup>
        
        <SendButton
          onClick={handleSubmit}
          disabled={!canSend}
          $disabled={!canSend}
          title={canSend ? "ارسال پیام" : "پیام خود را بنویسید"}
        >
          {disabled ? '⏳' : '📤'}
        </SendButton>
      </InputWrapper>
    </InputContainer>
  );
};

export default MessageInput;