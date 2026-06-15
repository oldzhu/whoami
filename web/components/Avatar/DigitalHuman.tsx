'use client';
import { useState, useEffect } from 'react';

interface DigitalHumanProps {
  photoUrl?: string;
  speaking?: boolean;
  size?: number;
}

export function DigitalHuman({ photoUrl, speaking = false, size = 120 }: DigitalHumanProps) {
  const [blink, setBlink] = useState(false);

  useEffect(() => {
    const interval = setInterval(() => {
      setBlink(true);
      setTimeout(() => setBlink(false), 150);
    }, 3000 + Math.random() * 2000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="flex flex-col items-center">
      <div
        className={`relative rounded-full overflow-hidden border-4 transition-all duration-300 ${
          speaking ? 'border-blue-500 shadow-lg shadow-blue-200 scale-105' : 'border-gray-300'
        }`}
        style={{ width: size, height: size }}
      >
        {photoUrl ? (
          <img src={photoUrl} alt="Digital Twin" className="w-full h-full object-cover" />
        ) : (
          <div className="w-full h-full bg-gradient-to-br from-blue-400 to-purple-500 flex items-center justify-center">
            <span className={`text-4xl ${blink ? 'opacity-50' : 'opacity-100'} transition-opacity`}>
              {blink ? '😑' : '🤖'}
            </span>
          </div>
        )}
        {speaking && (
          <div className="absolute bottom-1 left-1/2 -translate-x-1/2 flex gap-1">
            <span className="w-1.5 h-4 bg-blue-500 rounded animate-pulse" style={{animationDelay:'0ms'}} />
            <span className="w-1.5 h-4 bg-blue-500 rounded animate-pulse" style={{animationDelay:'150ms'}} />
            <span className="w-1.5 h-4 bg-blue-500 rounded animate-pulse" style={{animationDelay:'300ms'}} />
          </div>
        )}
      </div>
      <p className="text-sm text-gray-500 mt-2">
        {speaking ? 'Speaking...' : 'Digital Twin'}
      </p>
    </div>
  );
}
