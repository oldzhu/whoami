# 系统架构 / System Architecture

## 概述 / Overview

数字分身 (Digital Twin) 是一个基于本地开源大语言模型的 AI 克隆系统，支持文字、语音多模态交互。所有推理均在本地完成，不依赖任何远程 API。

Digital Twin is a local OSS LLM-based AI clone system supporting text and voice multi-modal interaction. All inference runs locally with zero dependency on remote APIs.

```
┌──────────────────────────────────────────────────────────────────┐
│                   客户端层 / Client Layer                          │
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐        │
│  │ Web (Next.js) │  │ Mobile (RN)  │  │ Desktop (Tauri)  │        │
│  │ :3000         │  │ (Android)    │  │ (Windows/Linux)  │        │
│  └──────┬───────┘  └──────┬───────┘  └────────┬─────────┘        │
│         │                 │                    │                  │
│         └─────────────────┴────────────────────┘                  │
│                           │ HTTP / WebSocket                      │
├───────────────────────────┴──────────────────────────────────────┤
│                    API 层 / API Layer (FastAPI :8000)              │
│                                                                   │
│  ┌─────────┐ ┌─────────┐ ┌──────┐ ┌────────┐ ┌──────┐ ┌───────┐ │
│  │ Auth    │ │ Profile │ │ Chat │ │Knowledge│ │Voice │ │Evolve │ │
│  │ /api/   │ │ /api/   │ │ /api/│ │ /api/   │ │/api/ │ │/api/  │ │
│  │ auth/*  │ │profile/*│ │chat/*│ │knowledge│ │voice/│ │evolve/│ │
│  └────┬────┘ └────┬────┘ └──┬───┘ └────┬───┘ └──┬───┘ └───┬───┘ │
│       │           │         │          │         │          │     │
│       └───────────┴─────────┴──────────┴─────────┴──────────┘     │
│                             │                                     │
│                    LocalOnlyMiddleware + RateLimiter               │
├────────────────────────────┴──────────────────────────────────────┤
│                   核心层 / Core Layer                               │
│                                                                   │
│  ┌──────────────────┐  ┌──────────────────────────────────┐       │
│  │ 多模型路由 Router  │  │     RAG 管道 Pipeline           │       │
│  │ IntentClassifier  │  │  ┌──────────┐ ┌───────────┐     │       │
│  │   code/chinese/   │  │  │Hybrid    │ │ Reranker  │     │       │
│  │   casual/technical│  │  │Retriever │ │           │     │       │
│  │         ↓         │  │  └────┬─────┘ └─────┬─────┘     │       │
│  │ Model Router      │  │       │              │           │       │
│  │  → Qwen3.5 2/4/9B │  │  ┌────▼──────────────▼─────┐     │       │
│  │  → fallback chain │  │  │   ContextBuilder         │     │       │
│  └──────────────────┘  │  │   (first-person prompt)   │     │       │
│                        │  └────────────┬──────────────┘     │       │
│  ┌──────────────────┐                 │                     │       │
│  │ 语音管道 Voice    │                 │                     │       │
│  │ STT (whisper) ↓   │◄────────────────┘                     │       │
│  │ LLM (RAGChain) ↓  │                                       │       │
│  │ TTS (Piper)       │                                       │       │
│  └──────────────────┘                                        │       │
│  ┌──────────────────────────────────────────────────────┐    │       │
│  │ 存储层 / Storage Layer                                │    │       │
│  │                                                       │    │       │
│  │  ┌──────────────┐  ┌────────────┐  ┌──────────────┐  │    │       │
│  │  │ ChromaDB     │  │ Neo4j      │  │ SQLite       │  │    │       │
│  │  │ (向量/Vector) │  │ (知识图谱)  │  │ (会话/Session)│  │    │       │
│  │  │ :8001        │  │ :7687      │  │ 本地文件      │  │    │       │
│  │  └──────────────┘  └────────────┘  └──────────────┘  │    │       │
│  └──────────────────────────────────────────────────────┘    │       │
│                                                              │       │
│  ┌──────────────────────────────────────────────────────┐    │       │
│  │ 自进化引擎 / Evolution Engine                          │    │       │
│  │  FactExtractor → ReviewQueue → KnowledgeUpdater       │    │       │
│  │  → GraphUpdater                                       │    │       │
│  └──────────────────────────────────────────────────────┘    │       │
└──────────────────────────────────────────────────────────────┘       │
                           │ HTTP (trust_env=False, NO_PROXY=localhost)
┌──────────────────────────┴──────────────────────────────────────────┐
│                    LLM 引擎 / LLM Engine (Ollama v0.17.5)           │
│                                                                     │
│   Qwen3.5 2B (默认/最快)  │  Qwen3.5 4B (平衡)  │  Qwen3.5 9B (最佳)│
│   Qwen2.5 1.5B (备用)     │  Qwen2.5 3B (备用)  │  Qwen2.5 7B (编程) │
│                       all-minilm:l6-v2 (Embedding)                  │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 组件 / Components

### 后端 / Backend

- **技术栈** / **Tech Stack**: Python 3.12, FastAPI, ChromaDB, Neo4j 5 Community
- **职责** / **Responsibilities**: API 服务、LLM 调用、RAG 检索、知识管理、语音处理、自我进化
  API serving, LLM invocation, RAG retrieval, knowledge management, voice processing, self-evolution
- **接口** / **Interfaces**: REST API (HTTP), WebSocket (streaming chat & voice)
- **入口** / **Entrypoint**: `backend/app/main.py` — FastAPI app with lifespan manager, CORS, LocalOnlyMiddleware, rate limiter
- **路由模块** / **Route Modules**: 6 modules — auth, profile, chat, knowledge, voice, evolution — lazy-loaded with graceful fallback
- **配置** / **Config**: `config.yaml` — LLM backend, hardware flags, server host/port, data directory

### 前端 / Frontend (Web)

- **技术栈** / **Tech Stack**: Next.js 14 (React 18), TypeScript, Tailwind CSS
- **页面** / **Pages**: Home (`/`), Chat (`/chat`), Voice (`/voice`), Settings (`/settings`), Login (`/login`), About (`/about`)
- **国际化** / **i18n**: 完整中英文切换, 偏好存 localStorage
  Full Chinese/English switching via `web/lib/i18n.tsx` + `web/lib/translations.ts`
- **API 客户端** / **API Client**: `web/lib/api-client.ts` — auth token management

### 移动端 / Mobile

- **技术栈** / **Tech Stack**: React Native (scaffold)
- **状态** / **Status**: 代码骨架就绪，待构建测试 / Code scaffold ready, pending build and test

### 桌面端 / Desktop

- **技术栈** / **Tech Stack**: Tauri (Rust + WebView, scaffold)
- **状态** / **Status**: 配置就绪，待构建 / Config ready, pending build

### LLM 服务 / LLM Service (Ollama)

- **版本** / **Version**: v0.17.5
- **运行** / **Runtime**: 在 tmux 中运行 / Runs in tmux
- **来源** / **Source**: 全部从 ModelScope (阿里云镜像) 下载 / All from ModelScope

| 模型 / Model | 参数 | 世代 | 用途 / Purpose |
|---|---|---|---|
| qwen3.5:2b | 2B | 2026 | **默认** — 最快响应 / Default, fastest (~6s CPU) |
| qwen3.5:4b | 4B | 2026 | 平衡 / Balanced |
| qwen3.5:9b | 9B | 2026 | 最佳质量 / Best quality |
| qwen2.5:1.5b | 1.5B | 2024 | 快速备用 / Fast fallback |
| qwen2.5:3b | 3B | 2024 | 平衡备用 / Balanced fallback |
| qwen2.5:7b | 7B | 2024 | 编程/复杂任务 / Coding |
| all-minilm:l6-v2 | 33M | - | Embedding |

---

## 数据流 / Data Flow

### 文字聊天 / Text Chat

```
用户输入 "你好，介绍一下你自己"
       │
       ▼
POST /api/chat { message: "你好", session_id: null }
       │
       ├── 1. SessionManager: 创建/恢复会话
       │
       ├── 2. ModelRouter.route("你好")
       │     └── IntentClassifier.classify()
       │           └── 检测到中文 (CJK > 20%) → "chinese_chat"
       │                 └── ModelRegistry → qwen3.5:4b
       │
       ├── 3. RAGChain.query("你好")
       │     ├── a. HybridRetriever.search()
       │     │     ├── VectorStore (ChromaDB): 向量语义搜索
       │     │     ├── BM25Scorer: 关键词评分
       │     │     └── GraphStore (Neo4j): 实体关系检索
       │     ├── b. Reranker.rerank(): top 3 重排序
       │     ├── c. ContextBuilder.build():
       │     │     ├── 读取 profile.json → 姓名/技能/项目/经历
       │     │     ├── 构建第一人称身份描述
       │     │     └── 拼接 system prompt + 检索上下文 + 用户问题
       │     └── d. LLMProvider.chat(messages)
       │           └── OllamaAdapter → POST /api/chat (Ollama, trust_env=False)
       │
       └── 4. SessionManager.add_message(session_id, "user", ...)
             SessionManager.add_message(session_id, "assistant", ...)

返回 { response: "我是...", session_id: "xxx", model: "qwen3.5:4b" }
```

### 语音对话 / Voice Conversation (WebSocket)

```
用户录制语音 (16kHz WAV bytes)
       │
       ▼
WebSocket /api/voice/conversation
       │
       ├── 1. VoiceState: idle → LISTENING
       ├── 2. SpeechToText.transcribe_bytes(audio_bytes)
       │     └── faster-whisper base model (CPU, int8)
       │           └── 返回 { text: "你好", language: "zh", segments: [...] }
       │
       ├── 3. VoiceState: LISTENING → THINKING
       ├── 4. RAGChain.query(text)  ← 同文字聊天的 RAG 步骤
       │
       ├── 5. VoiceState: THINKING → SPEAKING
       ├── 6. TextToSpeech.synthesize(text, language="zh")
       │     └── Piper TTS (子进程管道) → WAV bytes
       │
       ├── 7. VoiceState: SPEAKING → IDLE
       └── WebSocket 返回 { type: "result", text: "...", audio: <WAV> }
```

### 知识摄入 / Knowledge Ingestion

三种来源统一处理：

```
来源 1: 文件上传 (.pdf, .docx, .md, .txt)
         POST /api/knowledge/upload
来源 2: GitHub 仓库
         POST /api/knowledge/import-github { url, branch }
来源 3: 通用 URL
         POST /api/knowledge/import-url { url, selector? }
                 │
                 ▼
         IngestionPipeline
                 │
                 ├── DocumentParser: PDFPlumber/pdfminer.six → 文本
                 │                     python-docx / markdown → 文本
                 ├── TextChunker: 512 token 分块, 128 overlap
                 ├── LocalEmbedder: all-minilm:l6-v2 → 384维向量
                 └── VectorStore.add_documents()
                       └── ChromaDB "knowledge_base" 集合持久化
```

---

## 多模型路由 / Multi-Model Routing

`ModelRouter` (`backend/app/core/router/router.py`) 基于 `IntentClassifier` 的意图评分自动选择模型。

| 意图 / Intent | 触发关键词 / Keywords | 路由至 / Route To |
|---|---|---|
| `code` | code, function, python, debug, api, sql, git, docker, react | Qwen3.5 9B / Qwen2.5 7B |
| `chinese` | CJK 字符比例 > 20% | Qwen3.5 4B |
| `casual` | hi, hello, hey, how are you | Qwen3.5 2B (最快) |
| `technical` | llm, ai, neural, embedding, rag, architecture, performance | Qwen3.5 9B |
| 默认 | 其他 | Qwen3.5 2B |

- **模型不可用时降级** → `default_chat` → `chinese_chat` → `english_chat` → `qwen2.5:7b` → `llama3.1:8b`
- **硬件自动检测** → `create_llm_provider()`: nvidia-smi → CUDA, rocm-smi → ROCm, /usr/local/Ascend → CANN, 否则 CPU

---

## 认证与安全 / Auth & Security

```
外网请求
       │
       ▼
LocalOnlyMiddleware
  ├── 路径以 /api/auth, /api/knowledge, /api/evolution, /api/profile, /api/voice/speaker 开头?
  │     └── 是 → client_host ∈ {127.0.0.1, ::1, localhost}?
  │           ├── 否 → HTTP 403 "Access restricted to localhost"
  │           └── 是 → 继续
  └── 否 → 放行 (公开端点)

RateLimiter (30 req/min/IP)
  └── 超过 → HTTP 429

auth_required (需认证的端点)
  ├── 无 Authorization: Bearer <token> → 401
  ├── token 不在会话中 → 401
  ├── token 过期 (>3600s) → 401
  └── token 有效 → 返回 username → 处理请求
```

### 保护矩阵 / Protection Matrix

| 端点 / Endpoint | 公开 | 需 Auth | 限 localhost |
|---|---|---|---|
| `GET /api/auth/status` | ✅ | ❌ | ✅ |
| `POST /api/auth/login` | ✅ | ❌ | ✅ |
| `POST /api/auth/setup` | ✅ | ❌ | ✅ |
| `POST /api/auth/reset` | ❌ | ✅ | ✅ |
| `GET /api/profile` | ✅ | ❌ | ❌ |
| `PUT /api/profile` | ❌ | ✅ | ✅ |
| `POST /api/chat` | ✅ | ❌ | ❌ |
| `POST /api/knowledge/upload` | ❌ | ✅ | ✅ |
| `POST /api/knowledge/import-github` | ❌ | ✅ | ✅ |
| `GET /api/evolution/pending` | ❌ | ✅ | ✅ |
| `GET /api/voice/status` | ✅ | ❌ | ❌ |
| `POST /api/voice/speaker` | ❌ | ✅ | ✅ |
| `GET /health` | ✅ | ❌ | ❌ |

### 认证实现细节 / Auth Implementation Details

- **密码存储**: SHA256 hexdigest, `data/auth.json`
- **会话**: UUID4 token, 内存 dict, 3600s TTL
- **类**: `SimpleAuth` (`backend/app/core/auth.py`), 单例模式
- **限速**: `RateLimiter` (`backend/app/core/rate_limit.py`), 滑动窗口 30req/60s

---

## 存储 / Storage

| 类型 | 技术 | 数据内容 | 位置 |
|---|---|---|---|
| 向量数据库 | ChromaDB PersistentClient | 文档 Embedding (384维) | `data/chroma/` |
| 知识图谱 | Neo4j 5 Community | Person/Project/Skill 节点关系 | `bolt://localhost:7687` |
| 会话记录 | SQLite (内存) | 聊天消息历史 | `/tmp/conversations.db` |
| 配置文件 | JSON | 认证信息、个人资料 | `data/auth.json`, `data/profile.json` |
| 模型配置 | YAML | 模型路由表、参数 | `models/config.yaml` |

### ChromaDB 集合 / Collections

| 集合名 | 用途 |
|---|---|
| `knowledge_base` | 知识库文档向量 |

### Neo4j 节点类型 / Node Types

| 节点标签 | 属性 |
|---|---|
| `Person` | name, title, summary |
| `Project` | name, description, technologies |
| `Skill` | name, category |
| `Technology` | name |

关系: `Person` -[:WORKED_ON]-> `Project`, `Person` -[:HAS_SKILL]-> `Skill`, `Project` -[:USES]-> `Technology`

---

## 自进化引擎 / Self-Evolution Engine

```
聊天记录 (session 消息)
       │
       ▼
FactExtractor.extract(messages)
       │
       ├── 识别结构化事实 (技能提及、项目讨论、关系推断)
       ├── 去重 (检查是否已存在于知识库)
       └── 存入 ReviewQueue (SQLite)
             │
             ▼
ReviewQueue.get_pending()  →  GET /api/evolution/pending
             │
             ├── POST /api/evolution/approve/{fact_id}
             │     ├── KnowledgeUpdater.apply_approved()
             │     │     └── 更新 ChromaDB 向量
             │     └── GraphUpdater.update()
             │           └── 更新 Neo4j 节点/关系
             │
             └── POST /api/evolution/reject/{fact_id}
                   └── 从队列移除
```

### 组件 / Components

| 组件 | 文件 | 职责 |
|---|---|---|
| `FactExtractor` | `core/evolution/extractor.py` | 从对话提取事实 |
| `ReviewQueue` | `core/evolution/review_queue.py` | SQLite 待审队列 |
| `KnowledgeUpdater` | `core/evolution/knowledge_updater.py` | 批准后更新向量库 |
| `GraphUpdater` | `core/evolution/graph_updater.py` | 更新 Neo4j 图谱 |

---

## 部署架构 / Deployment

### Docker Compose (4 服务)

| 服务 | 镜像来源 | 端口 | 健康检查 | 依赖 |
|---|---|---|---|---|
| `backend` | Dockerfile.backend | `8000` | `GET /health` (30s) | neo4j, chromadb |
| `web` | Dockerfile.web | `3000` | — | backend |
| `chromadb` | `chromadb/chroma:latest` | `8001` | — | — |
| `neo4j` | `neo4j:5-community` | `7474:7474`, `7687:7687` | cypher-shell (30s) | — |

### 开发环境 (tmux)

三个 **tmux** 窗口同时运行：

| 窗口 | 启动命令 | 端口 |
|---|---|---|
| Ollama | `ollama serve` | 11434 |
| Backend | `python backend/app/main.py` | 8000 |
| Frontend | `cd web && npm run dev` | 3000 |

**注意**: HTTP_PROXY 拦截 localhost，需 `trust_env=False` 或 `NO_PROXY=localhost`。
**Note**: HTTP_PROXY intercepts localhost; use `trust_env=False` or `NO_PROXY=localhost`.

---

## 技术栈总览 / Tech Stack Overview

| 层次 / Layer | 技术 / Technology | 版本 |
|---|---|---|
| 后端框架 / Backend Framework | Python 3.12 + FastAPI | 0.115+ |
| 前端框架 / Frontend Framework | Next.js 14 + React 18 | 14.2+ |
| 移动端 / Mobile | React Native | scaffold |
| 桌面端 / Desktop | Tauri (Rust + WebView) | scaffold |
| 向量数据库 / Vector DB | ChromaDB | latest |
| 图数据库 / Graph DB | Neo4j 5 Community | 5 |
| LLM 引擎 (开发) / Dev | Ollama | 0.17.5 |
| LLM 引擎 (生产) / Prod | llama.cpp / vLLM | — |
| 语音识别 / STT | faster-whisper (base) | — |
| 语音合成 / TTS | Piper (zh_CN + en_US) | — |
| 认证 / Auth | SHA256 + uuid4 session | — |
| 容器化 / Container | Docker + Compose | — |
