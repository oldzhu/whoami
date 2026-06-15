export interface AvatarConfig {
  photo_url?: string;
  animation_type: "musetalk" | "sadtalker";
  idle_animation: boolean;
}

export interface AnimationState {
  speaking: boolean;
  expression: string;
  lip_sync_data?: number[];
}

export interface LipSyncData {
  audio_url: string;
  frames: Array<{ time: number; phoneme: string; intensity: number }>;
}
