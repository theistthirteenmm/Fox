import React, { useRef, useState } from 'react';
import { useFrame } from '@react-three/fiber';
import { Sphere, Box, Cone, Cylinder } from '@react-three/drei';
import * as THREE from 'three';

interface FoxAvatarProps {
  isListening?: boolean;
  isSpeaking?: boolean;
  emotion?: 'happy' | 'sad' | 'surprised' | 'thinking' | 'neutral';
}

const FoxAvatar: React.FC<FoxAvatarProps> = ({ 
  isListening = false, 
  isSpeaking = false, 
  emotion = 'neutral' 
}) => {
  const groupRef = useRef<THREE.Group>(null);
  const headRef = useRef<THREE.Mesh>(null);
  const leftEyeRef = useRef<THREE.Mesh>(null);
  const rightEyeRef = useRef<THREE.Mesh>(null);
  const mouthRef = useRef<THREE.Mesh>(null);
  const leftEarRef = useRef<THREE.Mesh>(null);
  const rightEarRef = useRef<THREE.Mesh>(null);
  const tailRef = useRef<THREE.Group>(null);
  const leftArmRef = useRef<THREE.Group>(null);
  const rightArmRef = useRef<THREE.Group>(null);
  const leftLegRef = useRef<THREE.Group>(null);
  const rightLegRef = useRef<THREE.Group>(null);
  
  const [blinkTimer, setBlinkTimer] = useState(0);
  const [isBlinking, setIsBlinking] = useState(false);
  const [mouthScale, setMouthScale] = useState(1);

  // انیمیشن اصلی
  useFrame((state, delta) => {
    if (!groupRef.current) return;

    // حرکت آرام کل بدن (مثل ModelLoader)
    groupRef.current.rotation.y = Math.sin(state.clock.elapsedTime * 0.5) * 0.1;
    
    // حرکت عمودی کم (مثل ModelLoader)
    const baseY = -0.5;
    groupRef.current.position.y = baseY + Math.sin(state.clock.elapsedTime * 0.8) * 0.05;

    // حرکت سر
    if (headRef.current) {
      headRef.current.rotation.x = Math.sin(state.clock.elapsedTime * 0.7) * 0.05;
      headRef.current.rotation.y = Math.sin(state.clock.elapsedTime * 0.3) * 0.1;
    }

    // حرکت گوش‌ها
    if (leftEarRef.current && rightEarRef.current) {
      const earMovement = Math.sin(state.clock.elapsedTime * 2) * 0.1;
      leftEarRef.current.rotation.z = earMovement;
      rightEarRef.current.rotation.z = -earMovement;
    }

    // حرکت دم
    if (tailRef.current) {
      tailRef.current.rotation.x = 0.3 + Math.sin(state.clock.elapsedTime * 1.5) * 0.2;
      tailRef.current.rotation.z = Math.sin(state.clock.elapsedTime * 1.2) * 0.3;
      tailRef.current.rotation.y = Math.sin(state.clock.elapsedTime * 0.8) * 0.1;
    }

    // انیمیشن دست‌ها
    if (leftArmRef.current && rightArmRef.current) {
      const armMovement = Math.sin(state.clock.elapsedTime * 1.5) * 0.2;
      leftArmRef.current.rotation.z = armMovement;
      rightArmRef.current.rotation.z = -armMovement;
    }

    // انیمیشن پاها
    if (leftLegRef.current && rightLegRef.current) {
      const legMovement = Math.sin(state.clock.elapsedTime * 1.8) * 0.1;
      leftLegRef.current.rotation.x = legMovement;
      rightLegRef.current.rotation.x = -legMovement;
    }

    // انیمیشن چشم‌ها (پلک زدن)
    setBlinkTimer(prev => prev + delta);
    if (blinkTimer > 3 && !isBlinking) {
      setIsBlinking(true);
      setBlinkTimer(0);
      setTimeout(() => setIsBlinking(false), 150);
    }

    // انیمیشن دهن هنگام صحبت
    if (isSpeaking) {
      const mouthMovement = Math.sin(state.clock.elapsedTime * 8) * 0.3 + 1;
      setMouthScale(mouthMovement);
    } else {
      setMouthScale(1);
    }

    // تغییر رنگ بر اساس حالت
    if (isListening && headRef.current) {
      const material = headRef.current.material as THREE.MeshStandardMaterial;
      material.emissive.setHex(0x001122);
      material.emissiveIntensity = Math.sin(state.clock.elapsedTime * 4) * 0.2 + 0.1;
    }
  });

  // رنگ‌های مختلف بر اساس احساسات
  const getEmotionColors = () => {
    switch (emotion) {
      case 'happy':
        return { body: '#ff8c42', accent: '#ff6b35', dark: '#d63031' };
      case 'sad':
        return { body: '#6c5ce7', accent: '#5f3dc4', dark: '#4834d4' };
      case 'surprised':
        return { body: '#00cec9', accent: '#00b894', dark: '#00a085' };
      case 'thinking':
        return { body: '#fdcb6e', accent: '#e17055', dark: '#d63031' };
      default:
        return { body: '#ff7675', accent: '#d63031', dark: '#b71c1c' };
    }
  };

  const colors = getEmotionColors();

  return (
    <group ref={groupRef} position={[0, -0.5, 0]} scale={0.6}>
      {/* بدن اصلی */}
      <Sphere args={[0.8, 32, 32]} position={[0, -0.5, 0]}>
        <meshStandardMaterial 
          color={colors.body} 
          roughness={0.3}
          metalness={0.1}
        />
      </Sphere>

      {/* سر */}
      <Sphere ref={headRef} args={[0.6, 32, 32]} position={[0, 0.3, 0]}>
        <meshStandardMaterial 
          color={colors.body} 
          roughness={0.3}
          metalness={0.1}
        />
      </Sphere>

      {/* پوزه */}
      <Sphere args={[0.25, 16, 16]} position={[0, 0.1, 0.5]}>
        <meshStandardMaterial color={colors.accent} />
      </Sphere>

      {/* گوش چپ */}
      <Cone 
        ref={leftEarRef}
        args={[0.2, 0.6, 8]} 
        position={[-0.35, 0.7, 0.1]}
        rotation={[0, 0, -0.3]}
      >
        <meshStandardMaterial color={colors.accent} />
      </Cone>

      {/* داخل گوش چپ */}
      <Cone args={[0.12, 0.4, 8]} position={[-0.35, 0.7, 0.1]} rotation={[0, 0, -0.3]}>
        <meshStandardMaterial color="#ffb3ba" />
      </Cone>

      {/* گوش راست */}
      <Cone 
        ref={rightEarRef}
        args={[0.2, 0.6, 8]} 
        position={[0.35, 0.7, 0.1]}
        rotation={[0, 0, 0.3]}
      >
        <meshStandardMaterial color={colors.accent} />
      </Cone>

      {/* داخل گوش راست */}
      <Cone args={[0.12, 0.4, 8]} position={[0.35, 0.7, 0.1]} rotation={[0, 0, 0.3]}>
        <meshStandardMaterial color="#ffb3ba" />
      </Cone>

      {/* چشم چپ */}
      <Sphere 
        ref={leftEyeRef} 
        args={[0.12, 16, 16]} 
        position={[-0.2, 0.4, 0.45]}
        scale={[1, isBlinking ? 0.1 : 1, 1]}
      >
        <meshStandardMaterial color="white" />
      </Sphere>
      
      {/* مردمک چپ */}
      <Sphere args={[0.06, 16, 16]} position={[-0.2, 0.4, 0.52]}>
        <meshStandardMaterial color="black" />
      </Sphere>

      {/* چشم راست */}
      <Sphere 
        ref={rightEyeRef} 
        args={[0.12, 16, 16]} 
        position={[0.2, 0.4, 0.45]}
        scale={[1, isBlinking ? 0.1 : 1, 1]}
      >
        <meshStandardMaterial color="white" />
      </Sphere>
      
      {/* مردمک راست */}
      <Sphere args={[0.06, 16, 16]} position={[0.2, 0.4, 0.52]}>
        <meshStandardMaterial color="black" />
      </Sphere>

      {/* بینی */}
      <Sphere args={[0.04, 16, 16]} position={[0, 0.15, 0.65]}>
        <meshStandardMaterial color="black" />
      </Sphere>

      {/* دهن */}
      <Box 
        ref={mouthRef}
        args={[0.2, 0.08, 0.08]} 
        position={[0, 0.05, 0.6]}
        scale={[mouthScale, mouthScale, 1]}
      >
        <meshStandardMaterial color="black" />
      </Box>

      {/* دست چپ */}
      <group ref={leftArmRef} position={[-0.7, -0.2, 0]}>
        {/* بازو */}
        <Cylinder args={[0.08, 0.1, 0.5, 8]} position={[0, -0.25, 0]}>
          <meshStandardMaterial color={colors.body} />
        </Cylinder>
        {/* ساعد */}
        <Cylinder args={[0.06, 0.08, 0.4, 8]} position={[0, -0.7, 0]}>
          <meshStandardMaterial color={colors.accent} />
        </Cylinder>
        {/* دست */}
        <Sphere args={[0.1, 16, 16]} position={[0, -0.95, 0]}>
          <meshStandardMaterial color={colors.dark} />
        </Sphere>
      </group>

      {/* دست راست */}
      <group ref={rightArmRef} position={[0.7, -0.2, 0]}>
        {/* بازو */}
        <Cylinder args={[0.08, 0.1, 0.5, 8]} position={[0, -0.25, 0]}>
          <meshStandardMaterial color={colors.body} />
        </Cylinder>
        {/* ساعد */}
        <Cylinder args={[0.06, 0.08, 0.4, 8]} position={[0, -0.7, 0]}>
          <meshStandardMaterial color={colors.accent} />
        </Cylinder>
        {/* دست */}
        <Sphere args={[0.1, 16, 16]} position={[0, -0.95, 0]}>
          <meshStandardMaterial color={colors.dark} />
        </Sphere>
      </group>

      {/* پای چپ */}
      <group ref={leftLegRef} position={[-0.3, -1.2, 0]}>
        {/* ران */}
        <Cylinder args={[0.1, 0.12, 0.6, 8]} position={[0, -0.3, 0]}>
          <meshStandardMaterial color={colors.body} />
        </Cylinder>
        {/* ساق */}
        <Cylinder args={[0.08, 0.1, 0.5, 8]} position={[0, -0.75, 0]}>
          <meshStandardMaterial color={colors.accent} />
        </Cylinder>
        {/* پا */}
        <Sphere args={[0.12, 16, 16]} position={[0, -1.05, 0.1]}>
          <meshStandardMaterial color={colors.dark} />
        </Sphere>
      </group>

      {/* پای راست */}
      <group ref={rightLegRef} position={[0.3, -1.2, 0]}>
        {/* ران */}
        <Cylinder args={[0.1, 0.12, 0.6, 8]} position={[0, -0.3, 0]}>
          <meshStandardMaterial color={colors.body} />
        </Cylinder>
        {/* ساق */}
        <Cylinder args={[0.08, 0.1, 0.5, 8]} position={[0, -0.75, 0]}>
          <meshStandardMaterial color={colors.accent} />
        </Cylinder>
        {/* پا */}
        <Sphere args={[0.12, 16, 16]} position={[0, -1.05, 0.1]}>
          <meshStandardMaterial color={colors.dark} />
        </Sphere>
      </group>

      {/* دم - قسمت اول (پایه) */}
      <group ref={tailRef} position={[0, -0.3, -0.6]} rotation={[0.3, 0, 0]}>
        <Sphere args={[0.08, 16, 16]} position={[0, 0, 0]}>
          <meshStandardMaterial color={colors.accent} />
        </Sphere>
        <Sphere args={[0.1, 16, 16]} position={[0, 0.08, -0.15]}>
          <meshStandardMaterial color={colors.accent} />
        </Sphere>
        <Sphere args={[0.12, 16, 16]} position={[0, 0.18, -0.3]}>
          <meshStandardMaterial color={colors.accent} />
        </Sphere>
        <Sphere args={[0.13, 16, 16]} position={[0, 0.3, -0.45]}>
          <meshStandardMaterial color={colors.accent} />
        </Sphere>
        <Sphere args={[0.12, 16, 16]} position={[0, 0.45, -0.6]}>
          <meshStandardMaterial color={colors.accent} />
        </Sphere>
        <Sphere args={[0.1, 16, 16]} position={[0, 0.6, -0.75]}>
          <meshStandardMaterial color={colors.accent} />
        </Sphere>
        
        {/* نوک دم سفید */}
        <Sphere args={[0.08, 16, 16]} position={[0, 0.75, -0.9]}>
          <meshStandardMaterial color="white" />
        </Sphere>
        
        {/* خطوط سفید روی دم */}
        <Sphere args={[0.05, 16, 16]} position={[0, 0.2, -0.35]}>
          <meshStandardMaterial color="white" />
        </Sphere>
        <Sphere args={[0.06, 16, 16]} position={[0, 0.5, -0.65]}>
          <meshStandardMaterial color="white" />
        </Sphere>
      </group>

      {/* سایه */}
      <Sphere args={[1.5, 32, 32]} position={[0, -2.2, 0]} rotation={[-Math.PI / 2, 0, 0]}>
        <meshStandardMaterial 
          color="black" 
          transparent 
          opacity={0.2}
          roughness={1}
        />
      </Sphere>
    </group>
  );
};

export default FoxAvatar;