'use client';
import { useEffect, useState } from 'react';
import { DigitalHuman } from './DigitalHuman';

interface LipSyncAvatarProps {
  audioUrl?: string;
  photoUrl?: string;
  size?: number;
}

export function LipSyncAvatar({ audioUrl, photoUrl, size = 120 }: LipSyncAvatarProps) {
  const [speaking, setSpeaking] = useState(false);
  const [audio, setAudio] = useState<HTMLAudioElement | null>(null);

  useEffect(() => {
    if (audioUrl) {
      const a = new Audio(audioUrl);
      a.onplay = () => setSpeaking(true);
      a.onended = () => setSpeaking(false);
      a.onpause = () => setSpeaking(false);
      setAudio(a);
      return () => { a.pause(); a.src = ''; };
    }
  }, [audioUrl]);

  const play = () => audio?.play();
  const pause = () => audio?.pause();

  return (
    <div className="flex flex-col items-center gap-3">
      <DigitalHuman photoUrl={photoUrl} speaking={speaking} size={size} />
      {audio && (
        <div className="flex gap-2">
          <button onClick={play} className="px-3 py-1 bg-blue-600 text-white rounded text-sm">▶ Play</button>
          <button onClick={pause} className="px-3 py-1 bg-gray-300 rounded text-sm">⏸ Pause</button>
        </div>
      )}
    </div>
  );
}
