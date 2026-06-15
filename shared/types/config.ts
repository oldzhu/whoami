export interface ModelConfig {
  name: string;
  provider: "ollama" | "llamacpp" | "vllm";
  type: "chat" | "embedding" | "reranker";
  quant: string;
  size_gb: number;
  languages: string[];
  tags: string[];
}

export type HardwareBackend = "cuda" | "rocm" | "cann" | "cpu" | "auto";

export interface LLMProvider {
  backend: HardwareBackend;
  models: ModelConfig[];
  base_url: string;
  api_type: "openai" | "ollama" | "custom";
}
