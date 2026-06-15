export interface VoiceSession {
  id: string;
  status: "idle" | "listening" | "thinking" | "speaking";
  started_at: string;
}

export interface TTSRequest {
  text: string;
  speaker_id?: string;
  language?: string;
}

export interface TTSResponse {
  audio_url: string;
  duration_ms: number;
}

export interface STTResult {
  text: string;
  language: string;
  confidence: number;
}
