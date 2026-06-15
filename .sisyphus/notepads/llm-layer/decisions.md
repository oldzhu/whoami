# Decisions - LLM Inference Abstraction Layer

## Why Ollama is default for hardware backends (cuda/rocm/cann/cpu)
The factory maps all hardware backends (cuda, rocm, cann, cpu) to OllamaAdapter because Ollama runs on any hardware and manages model loading transparently. llama.cpp and vLLM adapters are only selected when explicitly requested.

## Why separate adapters for llama.cpp and vLLM despite both being OpenAI-compatible
Even though both expose /v1/chat/completions, they may diverge in the future (stream format, model listing, health checks). Keeping separate adapters allows per-backend customization.

## Why PermissionError is caught in hardware detection
On some systems, nvidia-smi or rocm-smi may exist but be unreadable (PermissionError) due to security restrictions. Treating this the same as "not available" provides better UX.
