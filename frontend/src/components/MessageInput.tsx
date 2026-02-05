import React, { useState, useRef, useEffect } from 'react';
import styled from 'styled-components';

const isDirectDev = window.location.port === '3000' || window.location.port === '3001';
const API_BASE = isDirectDev ? 'http://localhost:8000' : '/api';

const InputContainer = styled.div`
  padding: 1.5rem;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  
  @media (max-width: 768px) {
    padding: 1rem;
  }
`;

const ProgressBar = styled.div<{ $progress: number }>`
  width: 100%;
  height: 6px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 3px;
  overflow: hidden;
  margin: 0.5rem 0;
  
  &::after {
    content: '';
    display: block;
    width: ${props => props.$progress}%;
    height: 100%;
    background: linear-gradient(90deg, #4CAF50, #8BC34A, #CDDC39);
    border-radius: 3px;
    transition: width 0.3s ease;
    box-shadow: 0 0 10px rgba(76, 175, 80, 0.5);
  }
`;

const UploadStatus = styled.div<{ $isUploading: boolean }>`
  display: ${props => props.$isUploading ? 'flex' : 'none'};
  align-items: center;
  justify-content: space-between;
  gap: 0.5rem;
  padding: 0.75rem 1rem;
  background: rgba(76, 175, 80, 0.1);
  border: 1px solid rgba(76, 175, 80, 0.3);
  border-radius: 12px;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
  color: #4CAF50;
  
  .upload-info {
    display: flex;
    align-items: center;
    gap: 0.5rem;
  }
  
  .spinner {
    width: 18px;
    height: 18px;
    border: 2px solid rgba(76, 175, 80, 0.3);
    border-top: 2px solid #4CAF50;
    border-radius: 50%;
    animation: spin 1s linear infinite;
  }
  
  .progress-text {
    font-weight: bold;
    color: #2E7D32;
  }
  
  @keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
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

const FileButton = styled.label<{ $isUploading?: boolean }>`
  padding: 1rem;
  border: none;
  border-radius: 50%;
  background: ${props => props.$isUploading ? 
    'linear-gradient(135deg, #9E9E9E, #757575)' : 
    'linear-gradient(135deg, #FF9800, #F57C00)'};
  color: white;
  cursor: ${props => props.$isUploading ? 'not-allowed' : 'pointer'};
  opacity: ${props => props.$isUploading ? 0.6 : 1};
  font-size: 1.5rem;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  min-width: 60px;
  height: 60px;
  
  &:hover:not([aria-disabled="true"]) {
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
  const [localAutoPlay, setLocalAutoPlay] = useState(autoPlayEnabled);
  const [isUploading, setIsUploading] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [uploadStatus, setUploadStatus] = useState('');
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);

  const formatFileSize = (bytes: number): string => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file || isUploading) return;

    setIsUploading(true);
    setUploadProgress(0);
    
    const fileSize = file.size;
    const fileSizeFormatted = formatFileSize(fileSize);
    setUploadStatus(`آپلود ${file.name} (${fileSizeFormatted})`);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const startTime = Date.now();
      let progress = 0;
      
      // شبیه‌سازی progress با نمایش سرعت
      const progressInterval = setInterval(() => {
        progress += Math.random() * 8 + 3; // افزایش 3-11%
        if (progress > 85) progress = 85; // توقف در 85% تا response بیاد
        
        const elapsed = Math.max((Date.now() - startTime) / 1000, 0.1);
        const uploadedBytes = (fileSize * progress / 100);
        const speed = uploadedBytes / elapsed;
        const speedFormatted = formatFileSize(speed);
        
        setUploadProgress(Math.min(progress, 85));
        setUploadStatus(`آپلود ${file.name} - ${speedFormatted}/s`);
      }, 150);

      const response = await fetch(`${API_BASE}/files/upload`, {
        method: 'POST',
        body: formData,
      });

      clearInterval(progressInterval);
      setUploadProgress(100);

      const result = await response.json();
      
      if (result.success) {
        setUploadStatus(`✅ ${file.name} آپلود شد!`);
        setMessage(`فایل "${result.file_info.filename}" آپلود شد.\n\n${result.content_preview}`);
        
        setTimeout(() => {
          setUploadStatus('');
        }, 2000);
      } else {
        setUploadStatus('❌ خطا در آپلود فایل');
        setTimeout(() => {
          setUploadStatus('');
        }, 3000);
      }
    } catch (error) {
      console.error('خطا در آپلود فایل:', error);
      setUploadStatus('❌ خطا در ارتباط با سرور');
      setTimeout(() => {
        setUploadStatus('');
      }, 3000);
    } finally {
      setIsUploading(false);
      setTimeout(() => {
        setUploadProgress(0);
        setUploadStatus('');
      }, 2000);
    }

    event.target.value = '';
  };
  // باقی توابع (startRecording, stopRecording, etc.) مثل قبل...
  const startRecording = async () => {
    try {
      console.log('🎤 درخواست دسترسی به میکروفون...');
      
      const stream = await navigator.mediaDevices.getUserMedia({ 
        audio: {
          echoCancellation: true,
          noiseSuppression: true,
          sampleRate: 44100
        } 
      });
      
      console.log('✅ دسترسی به میکروفون موفق');
      
      const mediaRecorder = new MediaRecorder(stream, {
        mimeType: 'audio/webm;codecs=opus'
      });
      
      mediaRecorderRef.current = mediaRecorder;
      const audioChunks: Blob[] = [];

      mediaRecorder.ondataavailable = (event) => {
        console.log('📊 داده صوتی دریافت شد:', event.data.size, 'bytes');
        if (event.data.size > 0) {
          audioChunks.push(event.data);
        }
      };

      mediaRecorder.onstop = async () => {
        console.log('⏹️ ضبط متوقف شد. تعداد chunks:', audioChunks.length);
        
        if (audioChunks.length === 0) {
          setRecordingStatus('❌ هیچ صدایی ضبط نشد');
          setTimeout(() => setRecordingStatus(''), 3000);
          return;
        }
        
        const audioBlob = new Blob(audioChunks, { type: 'audio/webm;codecs=opus' });
        console.log('🎵 فایل صوتی ساخته شد:', audioBlob.size, 'bytes');
        
        if (audioBlob.size < 1000) {
          setRecordingStatus('❌ فایل صوتی خیلی کوچک است');
          setTimeout(() => setRecordingStatus(''), 3000);
          return;
        }
        
        const formData = new FormData();
        formData.append('audio_file', audioBlob, 'recording.webm');

        try {
          setRecordingStatus('🔄 در حال تبدیل صدا به متن...');
          
          const response = await fetch(`${API_BASE}/speech/speech-to-text`, {
            method: 'POST',
            body: formData,
          });

          console.log('📡 پاسخ سرور:', response.status);
          const result = await response.json();
          console.log('📝 نتیجه:', result);
          
          if (result.success && result.text && result.text.trim()) {
            setMessage(result.text);
            setRecordingStatus('✅ صدا تبدیل شد');
          } else {
            setRecordingStatus('❌ متنی تشخیص داده نشد - لطفاً واضح‌تر صحبت کنید');
          }
        } catch (error) {
          console.error('❌ خطا در تبدیل صدا:', error);
          setRecordingStatus('❌ خطا در تبدیل صدا به متن');
        }

        stream.getTracks().forEach(track => track.stop());
        setTimeout(() => setRecordingStatus(''), 5000);
      };

      mediaRecorder.onerror = (event) => {
        console.error('❌ خطا در ضبط:', event);
        setRecordingStatus('❌ خطا در ضبط صدا');
        setTimeout(() => setRecordingStatus(''), 3000);
      };

      mediaRecorder.start(1000); // ضبط هر 1 ثانیه یک chunk
      setIsRecording(true);
      setRecordingStatus('🎤 در حال ضبط... (حداکثر 10 ثانیه)');
      
      // توقف خودکار بعد از 10 ثانیه
      setTimeout(() => {
        if (mediaRecorderRef.current && mediaRecorderRef.current.state === 'recording') {
          stopRecording();
        }
      }, 10000);

    } catch (error) {
      console.error('❌ خطا در دسترسی به میکروفون:', error);
      
      if (error.name === 'NotAllowedError') {
        setRecordingStatus('❌ دسترسی به میکروفون رد شد - لطفاً مجوز دهید');
      } else if (error.name === 'NotFoundError') {
        setRecordingStatus('❌ میکروفون یافت نشد');
      } else if (error.name === 'NotSupportedError') {
        setRecordingStatus('❌ مرورگر از ضبط صدا پشتیبانی نمی‌کند');
      } else {
        setRecordingStatus('❌ خطا در دسترسی به میکروفون: ' + error.message);
      }
      
      setTimeout(() => setRecordingStatus(''), 5000);
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
      {/* نمایش وضعیت آپلود با progress bar */}
      <UploadStatus $isUploading={isUploading}>
        <div className="upload-info">
          <div className="spinner"></div>
          <span>{uploadStatus}</span>
        </div>
        <div className="progress-text">
          {uploadProgress > 0 && `${Math.round(uploadProgress)}%`}
        </div>
      </UploadStatus>
      
      {/* Progress Bar */}
      {isUploading && <ProgressBar $progress={uploadProgress} />}
      
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

        <FileButton $isUploading={isUploading}>
          {isUploading ? '⏳' : '📁'}
          <input
            ref={fileInputRef}
            type="file"
            accept=".pdf,.docx,.txt,.png,.jpg,.jpeg,.wav,.mp3,.m4a"
            onChange={handleFileUpload}
            disabled={disabled || isUploading}
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
