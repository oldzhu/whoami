'use client';
import { useState, useRef, useEffect } from 'react';
import { MessageBubble } from '@/components/Chat/MessageBubble';
import { DigitalHuman } from '@/components/Avatar/DigitalHuman';
import { useChatWebSocket } from '@/hooks/useChatWebSocket';

export default function ChatPage() {
  const { messages, sendMessage, isStreaming, connect } = useChatWebSocket();
  const [input, setInput] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);

  useEffect(() => {
    const ws = connect();
    return () => ws?.close();
  }, [connect]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const handleSend = () => {
    if (!input.trim()) return;
    sendMessage(input.trim());
    setInput('');
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); handleSend(); }
  };

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const recorder = new MediaRecorder(stream);
      const chunks: Blob[] = [];
      recorder.ondataavailable = (e) => chunks.push(e.data);
      recorder.onstop = async () => {
        const blob = new Blob(chunks);
        const ws = new WebSocket((process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000').replace('http','ws') + '/api/voice/conversation');
        ws.onopen = () => ws.send(blob);
        ws.onmessage = (e) => {
          const data = JSON.parse(e.data);
          if (data.type === 'result' && data.text) {
            setInput(data.text);
          }
        };
      };
      recorder.start();
      mediaRecorderRef.current = recorder;
      setIsRecording(true);
    } catch (err) { console.error('Mic error:', err); }
  };

  const stopRecording = () => {
    mediaRecorderRef.current?.stop();
    setIsRecording(false);
  };

  const speakLastMessage = async () => {
    const lastMsg = messages.filter(m => m.role === 'assistant').pop();
    if (!lastMsg) return;
    const res = await fetch((process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000') + '/api/tts', {
      method: 'POST', headers: {'Content-Type':'application/json'},
      body: JSON.stringify({ text: lastMsg.content }),
    });
    if (res.ok) {
      const blob = await res.blob();
      const audio = new Audio(URL.createObjectURL(blob));
      audio.play();
    }
  };

  return (
    <div className="flex flex-col h-[calc(100vh-120px)]">
      <h2 className="text-2xl font-bold mb-4">Chat with Digital Twin 数字分身对话</h2>

      <div className="flex justify-center mb-4">
        <DigitalHuman size={80} />
      </div>

      <div className="flex-1 overflow-y-auto mb-4 space-y-1">
        {messages.length === 0 && (
          <div className="text-center text-gray-400 py-20">
            Start a conversation! 开始对话吧！
          </div>
        )}
        {messages.map((m, i) => <MessageBubble key={i} role={m.role} content={m.content} />)}
        {isStreaming && <div className="text-gray-400 text-sm">Thinking...</div>}
        <div ref={messagesEndRef} />
      </div>

      <div className="flex gap-2 items-end">
        <button
          onClick={isRecording ? stopRecording : startRecording}
          className={`p-3 rounded-lg ${isRecording ? 'bg-red-500' : 'bg-gray-200'} hover:opacity-80`}
          title={isRecording ? 'Stop recording' : 'Voice input'}
        >
          🎤
        </button>
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Type a message... / 输入消息..."
          className="flex-1 border rounded-lg p-3 resize-none focus:outline-none focus:ring-2 focus:ring-blue-500"
          rows={2}
        />
        <button onClick={handleSend} disabled={!input.trim()} className="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 disabled:opacity-50">
          Send
        </button>
        <button onClick={speakLastMessage} className="p-3 rounded-lg bg-gray-200 hover:opacity-80" title="Read aloud">
          🔊
        </button>
      </div>
    </div>
  );
}
