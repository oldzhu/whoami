# 开发指南 / Development Guide

## 概述 / Overview

本文档指导你在本地搭建数字分身开发环境。

This guide walks you through setting up the Digital Twin development environment locally.

---

## 环境搭建 / Setup

### 前置要求 / Prerequisites

| 工具 / Tool | 版本 / Version | 用途 / Purpose |
|---|---|---|
| Python | 3.12+ | 后端 / Backend |
| Node.js | 20+ | 前端 / Frontend |
| Ollama | 0.17.5+ | LLM 推理 / LLM Inference |
| Git | — | 版本控制 / Version control |

### 快速启动 / Quick Start

```bash
# 1. 克隆仓库 / Clone
git clone https://github.com/oldzhu/whoami.git
cd whoami

# 2. 后端依赖 / Backend deps
python3 -m venv venv
source venv/bin/activate
pip install -e ".[dev]"

# 3. 前端依赖 / Frontend deps
cd web && npm install && cd ..

# 4. Ollama + 模型 / Models
ollama serve
ollama pull qwen3.5:2b
ollama pull qwen3.5:4b
ollama pull qwen3.5:9b
ollama pull all-minilm:l6-v2

# 5. 启动 (三个终端) / Start (3 terminals)
# Terminal 1: Ollama
NO_PROXY=localhost ollama serve

# Terminal 2: Backend
source venv/bin/activate
NO_PROXY=localhost python backend/app/main.py

# Terminal 3: Frontend
cd web && npm run dev
```

---

## 项目结构 / Project Structure

```
whoami/
├── backend/
│   ├── app/
│   │   ├── main.py                 # FastAPI 入口 / App entrypoint
│   │   ├── middleware.py           # LocalOnlyMiddleware + auth dependency
│   │   ├── config.py               # 配置加载 / Config loader
│   │   ├── api/                    # API 路由 / Route modules
│   │   │   ├── auth.py             # /api/auth/*
│   │   │   ├── profile.py          # /api/profile/*
│   │   │   ├── chat.py             # /api/chat/* (REST + WS)
│   │   │   ├── knowledge.py        # /api/knowledge/*
│   │   │   ├── voice.py            # /api/voice/* (REST + WS)
│   │   │   └── evolution.py        # /api/evolution/*
│   │   └── core/                   # 核心模块 / Core modules
│   │       ├── auth.py             # SHA256 认证 / SimpleAuth
│   │       ├── rate_limit.py       # 限速器 / RateLimiter
│   │       ├── model_manager.py    # 模型注册表 / ModelRegistry
│   │       ├── llm/                # LLM 适配器 / Adapters (Ollama/llama.cpp/vLLM/mock)
│   │       ├── router/             # 多模型路由 / Model routing (IntentClassifier)
│   │       ├── rag/                # RAG 管道 / Pipeline (HybridRetriever, Reranker, ContextBuilder)
│   │       ├── voice/              # 语音 / STT + TTS + Orchestrator
│   │       ├── evolution/          # 自进化 / FactExtractor, ReviewQueue, Updaters
│   │       ├── storage/            # 存储 / VectorStore (ChromaDB) + GraphStore (Neo4j)
│   │       ├── conversation/       # 会话管理 / SessionManager, ConversationMemory
│   │       └── ingestion/          # 知识摄入 / Parser, Chunker, Embedder, Pipeline
│   ├── requirements.txt
│   └── ...
├── web/
│   ├── app/                        # Next.js 页面 / Pages
│   │   ├── page.tsx                # 首页 / Home
│   │   ├── layout.tsx              # 布局 + 语言切换 / Layout with i18n switcher
│   │   ├── login/page.tsx          # 登录 / Login (auto-detect setup mode)
│   │   ├── settings/page.tsx       # 设置 / Settings (4 tabs)
│   │   ├── chat/page.tsx           # 文字聊天 / Text Chat
│   │   ├── voice/page.tsx          # 语音对话 / Voice Conversation
│   │   └── about/page.tsx          # 关于 / About
│   ├── lib/
│   │   ├── i18n.tsx                # 国际化上下文 / i18n Provider
│   │   ├── translations.ts         # 中英文翻译表 / Translation strings
│   │   └── api-client.ts           # API 客户端 / API client with token management
│   └── ...
├── mobile/                         # React Native (scaffold)
├── desktop/                        # Tauri (scaffold)
├── tests/                          # 自动化测试 / Automated tests
│   ├── conftest.py                 # 共享 fixtures (rate_limit reset)
│   ├── test_text_chat.py           # 27 个测试 / Auth/Chat/Knowledge/Evolution/Router/RAG/LLM
│   └── test_voice.py               # 10 个测试 / STT/TTS pipeline
├── models/                         # LLM 模型 / Model files
│   ├── config.yaml                 # 模型配置 + 路由表
│   ├── piper/                      # Piper TTS 模型 (zh_CN + en_US)
│   └── whisper/                    # faster-whisper 缓存
├── data/                           # 运行时数据 / Runtime data
│   ├── auth.json                   # 认证信息 (SHA256)
│   ├── profile.json                # 个人资料
│   ├── uploads/                    # 上传文件
│   ├── chroma/                     # ChromaDB 持久化
│   ├── neo4j/                      # Neo4j 数据
│   └── voice/                      # 声音样本
├── documents/                      # 项目文档 / Documentation
├── config.yaml                     # 系统配置 / System config
├── docker-compose.yml              # Docker 编排 / Docker Compose
├── Dockerfile.backend              # 后端容器 / Backend container
├── Dockerfile.web                  # 前端容器 / Frontend container
└── pyproject.toml                  # Python 项目配置
```

---

## 后端开发 / Backend Development

### 依赖安装 / Dependencies

```bash
# 核心依赖 (自动安装)
pip install -e ".[dev]"

# 可选: 语音功能
pip install -e ".[voice]"

# 查看所有依赖
pip list | grep -E "fastapi|uvicorn|chromadb|neo4j|faster-whisper"
```

**核心依赖** (来自 `pyproject.toml`):

| 包 | 版本 | 用途 |
|---|---|---|
| fastapi | >=0.115.0 | Web 框架 |
| uvicorn | >=0.30.0 | ASGI 服务器 |
| chromadb | >=0.5.0 | 向量数据库 |
| neo4j | >=5.0.0 | 图数据库驱动 |
| pyyaml | >=6.0 | YAML 配置 |
| pydantic | >=2.0 | 数据验证 |
| python-multipart | >=0.0.9 | 文件上传 |
| websockets | >=12.0 | WebSocket |

### 启动 / Run

```bash
source venv/bin/activate

# 开发模式 (热重载)
uvicorn backend.app.main:app --reload --port 8000

# 或直接运行
NO_PROXY=localhost python backend/app/main.py

# 访问
# API: http://localhost:8000
# Swagger 文档: http://localhost:8000/docs
```

### 代码规范 / Coding Style

- 命名: `snake_case` (Python), `camelCase` (TypeScript)
- 类型注解: 所有函数必须有类型注解
- 错误处理: 使用 FastAPI `HTTPException`，不抛裸异常
- 单例模式: 使用 lazy getter 函数 (`_get_*()`)，非模块级初始化
- 注释: 中英文双语 (中文在前，英文在后)

---

## 前端开发 / Frontend Development

### 技术栈 / Tech Stack

| 技术 | 版本 |
|---|---|
| Next.js | 16.2.9 |
| React | 19.2.4 |
| TypeScript | 5.x |
| Tailwind CSS | 4.x |

### 启动 / Run

```bash
cd web
npm install    # 首次
npm run dev    # 开发 (localhost:3000, Turbopack)
npm run build  # 生产构建
```

### 国际化 / i18n

- 文件: `web/lib/i18n.tsx` (I18nProvider), `web/lib/translations.ts` (翻译表)
- 用法: `useI18n()` hook 返回 `{ t: (key) => string, locale, setLocale }`
- 切换: 导航栏右上角语言按钮，偏好存 localStorage
- 翻译键: 所有页面共用翻译表，支持中英文

### 页面路由 / Pages

| 路径 | 页面 | 说明 |
|---|---|---|
| `/` | 首页 | 欢迎页，显示 profile 信息 |
| `/chat` | 文字聊天 | POST /api/chat 交互 |
| `/voice` | 语音对话 | WebSocket 语音交互 |
| `/settings` | 设置 (4 标签) | Profile/Documents/Voice/Password |
| `/login` | 登录 | 自动检测 setup vs login 模式 |
| `/about` | 关于 | 项目说明 |

---

## 测试 / Testing

### 运行测试 / Run Tests

```bash
source venv/bin/activate

# 全部测试 (37 个)
python -m pytest tests/ -v

# 仅文本测试
python -m pytest tests/test_text_chat.py -v

# 仅语音测试
python -m pytest tests/test_voice.py -v

# 含输出
python -m pytest tests/ -v --tb=short
```

### 测试结构 / Test Structure

```
tests/
├── conftest.py              # autouse: rate_limit.reset() per test
│                            # fixtures: api_base, test_text
├── test_text_chat.py        # 27 tests
│   ├── Auth: setup, login, reset, wrong password
│   ├── Profile: GET public, PUT auth-protected
│   ├── Chat: POST, session, history auth
│   ├── Knowledge: upload, search, stats/documents auth
│   ├── Evolution: pending, approve/reject auth
│   ├── Router: Chinese/code intent detection
│   ├── RAG: query, stream, context builder
│   └── LLM: provider creation, mock adapter
│
└── test_voice.py            # 10 tests
    ├── STT: model loading (lazy init)
    ├── TTS: zh synthesis, en synthesis, WAV validation
    ├── Fallback: unknown language → zh
    └── Speaker: register
```

### 测试注意事项 / Testing Notes

- **LocalOnlyMiddleware**: TestClient 的 host 不是 `127.0.0.1`，必须在 `LOCAL_IPS` 中包含 `"testclient"` (已在 `middleware.py` 中处理)
- **Rate Limiter**: 每个测试结束后会自动 `limiter.reset()` (通过 `conftest.py` 的 `autouse` fixture)
- **速率**: 整个测试套约 30 秒，37 个测试全部通过
- **异步**: pytest-asyncio 已配置 `asyncio_mode = auto`，测试函数直接使用 `async def`
- **配置**: `pytest.ini` 指定 testpaths 和文件匹配规则

---

## Git 工作流 / Git Workflow

### 分支策略 / Branching Strategy

| 分支 | 用途 |
|---|---|
| `master` | 主分支，保持可部署状态 |

### 提交规范 / Commit Conventions

```
<type>: <description>

# 类型 / Types:
# feat     — 新功能 / New feature
# fix      — 修复 / Bug fix
# docs     — 文档 / Documentation
# security — 安全 / Security fix
# test     — 测试 / Test addition/change
# chore    — 维护 / Maintenance
# refactor — 重构 / Refactoring
```

### 当前提交历史 / Recent Commit History

```
5c4ea9b test: comprehensive automated tests - 37/37 passing
592b8e9 fix: voice pipeline - Piper TTS subprocess, STT cpu path
7c058a6 docs: comprehensive changelog for 2026-06-17~18 session
b3bee34 security: extend localhost restriction to all admin endpoints
b7bf641 feat: generic URL content importer for digital twin knowledge
aac8a74 feat: authentic system prompt - digital twin speaks in first person
3057a0c feat: GitHub project importer for digital twin knowledge
17d4ddd security: protect admin-only GET endpoints
14efa4f security: path traversal fix, session TTL, rate limiter
4582209 security: add auth protection to evolution and knowledge write endpoints
04527b5 security: remove .env.production from tracking
f136e45 feat: auth system, i18n, settings page, embedding fix, mock LLM
8bf1c9e feat: complete digital twin implementation - all 31 tasks
b167820 chore: initialize project structure and dev environment
```

---

## 编码规范 / Coding Standards

### 通用 / General

- 注释: 中英文双语 (`# 中文注释 / English comment`)
- 行宽: 不超过 120 字符
- 类型注解: 强制 (Python 后端 + TypeScript 前端)
- 不要写不必要的注释 — 代码本身应可读

### 后端规范 / Backend

- 路由函数: 使用 `Depends(auth_required)` 保护，`APIRouter(prefix=...)` 组织
- 单例: 使用 lazy getter 模式，不要在模块级别创建有状态对象
- 错误: 使用 `HTTPException(status_code=, detail=)`
- 配置: 从 `config.yaml` 加载，通过 `app.state.config` 访问

### 前端规范 / Frontend

- 组件: 函数式组件 + TypeScript
- 状态: React hooks (useState, useEffect)
- 样式: Tailwind CSS (v4)
- API: 使用 `web/lib/api-client.ts` 封装的 fetch

---

## 已知问题 / Known Issues

| 问题 | 状态 |
|---|---|
| Settings 页面 hydration warning (Next.js 16.2 + Turbopack) | 不影响生产 |
| HTTP_PROXY 拦截 localhost → `trust_env=False` | 已在 OllamaAdapter 中处理 |
| TestClient 与 LocalOnlyMiddleware | "testclient" 已加入白名单 |
| Neo4j 需要 Docker 运行 | `docker compose up -d neo4j` |
| Piper TTS 音质不如商业方案 | 可后续集成 OpenVoice |
