import React, { useRef, useEffect, useState } from 'react';
import { useGLTF, Sphere } from '@react-three/drei';
import { useFrame } from '@react-three/fiber';
import * as THREE from 'three';

interface ModelLoaderProps {
  modelPath: string;
  isListening?: boolean;
  isSpeaking?: boolean;
  emotion?: 'happy' | 'sad' | 'surprised' | 'thinking' | 'neutral';
}

// Cache برای نگهداری اطلاعات normalize شده مدل‌ها
const modelNormalizationCache = new Map<string, {
  scale: number;
  position: THREE.Vector3;
}>();

const ModelLoader: React.FC<ModelLoaderProps> = ({ 
  modelPath, 
  isListening = false, 
  isSpeaking = false, 
  emotion = 'neutral' 
}) => {
  const groupRef = useRef<THREE.Group>(null);
  const [isNormalized, setIsNormalized] = useState(false);
  
  // بارگذاری مدل GLB
  const { scene } = useGLTF(`/${modelPath}`);
  
  // استانداردسازی مدل
  useEffect(() => {
    if (!groupRef.current) return;
    
    const model = groupRef.current;
    
    // چک کردن cache
    const cachedData = modelNormalizationCache.get(modelPath);
    if (cachedData) {
      model.scale.setScalar(cachedData.scale);
      model.position.copy(cachedData.position);
      setIsNormalized(true);
      console.log(`📋 مدل ${modelPath} از cache بارگذاری شد`);
      return;
    }
    
    // محاسبه bounding box
    const box = new THREE.Box3().setFromObject(model);
    const size = box.getSize(new THREE.Vector3());
    const center = box.getCenter(new THREE.Vector3());
    
    // تنظیم موقعیت مرکزی
    model.position.sub(center);
    
    // تنظیم اندازه استاندارد (حداکثر 2 واحد)
    const maxDimension = Math.max(size.x, size.y, size.z);
    const targetSize = 2; // اندازه هدف
    const scale = targetSize / maxDimension;
    
    model.scale.setScalar(scale);
    
    // تنظیم موقعیت نهایی (کمی پایین‌تر از مرکز)
    const finalPosition = new THREE.Vector3(0, -0.5, 0);
    model.position.copy(finalPosition);
    
    // ذخیره در cache
    modelNormalizationCache.set(modelPath, {
      scale: scale,
      position: finalPosition.clone()
    });
    
    console.log(`📏 مدل ${modelPath} استاندارد شد:`, {
      originalSize: size,
      scale: scale,
      finalPosition: finalPosition
    });
    
    setIsNormalized(true);
  }, [scene, modelPath]);
  
  // انیمیشن ساده
  useFrame((state) => {
    if (!groupRef.current || !isNormalized) return;
    
    // حرکت آرام (فقط چرخش و حرکت عمودی کم)
    groupRef.current.rotation.y = Math.sin(state.clock.elapsedTime * 0.5) * 0.1;
    
    // حرکت عمودی کم
    const baseY = -0.5;
    groupRef.current.position.y = baseY + Math.sin(state.clock.elapsedTime * 0.8) * 0.05;
    
    // تغییر رنگ بر اساس حالت
    if (isListening) {
      // اضافه کردن نور آبی هنگام گوش دادن
      groupRef.current.traverse((child) => {
        if (child instanceof THREE.Mesh && child.material) {
          const material = child.material as THREE.MeshStandardMaterial;
          if (material.emissive) {
            material.emissive.setHex(0x001122);
            material.emissiveIntensity = Math.sin(state.clock.elapsedTime * 4) * 0.2 + 0.1;
          }
        }
      });
    } else {
      // حالت عادی
      groupRef.current.traverse((child) => {
        if (child instanceof THREE.Mesh && child.material) {
          const material = child.material as THREE.MeshStandardMaterial;
          if (material.emissive) {
            material.emissive.setHex(0x000000);
            material.emissiveIntensity = 0;
          }
        }
      });
    }
  });
  
  return (
    <group ref={groupRef} dispose={null}>
      {!isNormalized && (
        // نمایش loading تا مدل آماده بشه
        <group>
          <Sphere args={[0.1, 8, 8]} position={[0, 0, 0]}>
            <meshStandardMaterial color="#4ECDC4" transparent opacity={0.6} />
          </Sphere>
          <Sphere args={[0.05, 8, 8]} position={[0, 0.2, 0]}>
            <meshStandardMaterial color="#FFE66D" transparent opacity={0.8} />
          </Sphere>
        </group>
      )}
      <primitive object={scene.clone()} visible={isNormalized} />
    </group>
  );
};

export default ModelLoader;