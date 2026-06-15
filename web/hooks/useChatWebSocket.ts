'use client';
import { useState, useRef, useCallback } from 'react';

export function useChatWebSocket() {
  const [messages, setMessages] = useState<Array<{role: string; content: string}>>([]);
  const [isStreaming, setIsStreaming] = useState(false);
  const wsRef = useRef<WebSocket | null>(null);

  const connect = useCallback((sessionId?: string) => {
    const baseUrl = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';
    const wsUrl = baseUrl.replace('http', 'ws') + '/api/chat/ws';
    const ws = new WebSocket(wsUrl);
    wsRef.current = ws;

    ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === 'token') {
        setMessages(prev => {
          const last = prev[prev.length - 1];
          if (last?.role === 'assistant' && !last._done) {
            return [...prev.slice(0, -1), { ...last, content: last.content + data.content }];
          }
          return [...prev, { role: 'assistant', content: data.content, _done: false }];
        });
        setIsStreaming(true);
      } else if (data.type === 'done') {
        setMessages(prev => {
          const last = prev[prev.length - 1];
          if (last) return [...prev.slice(0, -1), { ...last, _done: true }];
          return prev;
        });
        setIsStreaming(false);
      }
    };

    ws.onclose = () => setIsStreaming(false);
    return ws;
  }, []);

  const sendMessage = useCallback((text: string) => {
    if (!wsRef.current || wsRef.current.readyState !== WebSocket.OPEN) {
      connect();
    }
    setMessages(prev => [...prev, { role: 'user', content: text }]);
    wsRef.current?.send(JSON.stringify({ message: text }));
  }, [connect]);

  return { messages, sendMessage, isStreaming, connect };
}
