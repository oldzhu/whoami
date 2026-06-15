const DEFAULT_BASE = 'http://localhost:8000';

export class ApiClient {
  private baseUrl: string;
  
  constructor(baseUrl?: string) {
    this.baseUrl = baseUrl || DEFAULT_BASE;
  }

  private async post(path: string, body: unknown) {
    const res = await fetch(`${this.baseUrl}${path}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
    });
    if (!res.ok) throw new Error(`API ${res.status}: ${path}`);
    return res.json();
  }

  private async get(path: string) {
    const res = await fetch(`${this.baseUrl}${path}`);
    if (!res.ok) throw new Error(`API ${res.status}: ${path}`);
    return res.json();
  }

  chat = {
    send: (message: string, sessionId?: string) =>
      this.post('/api/chat', { message, session_id: sessionId }),
    history: (sessionId: string) =>
      this.get(`/api/chat/history/${sessionId}`),
  };

  knowledge = {
    search: (query: string, topK = 5) =>
      this.get(`/api/knowledge/search?q=${encodeURIComponent(query)}&top_k=${topK}`),
    stats: () => this.get('/api/knowledge/stats'),
  };

  profile = {
    get: () => this.get('/api/profile'),
  };

  voice = {
    status: () => this.get('/api/voice/status'),
  };

  evolution = {
    pending: () => this.get('/api/evolution/pending'),
    approve: (id: string) => this.post(`/api/evolution/approve/${id}`, {}),
    reject: (id: string) => this.post(`/api/evolution/reject/${id}`, {}),
  };
}
