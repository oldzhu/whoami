# API 规格 / API Specification

## 概述 / Overview

- **基础 URL / Base URL**: `http://localhost:8000`
- **协议 / Protocol**: REST over HTTP + WebSocket
- **数据格式 / Data Format**: JSON (请求和响应)
- **版本 / Version**: 0.1.0

所有 API 端点分为公开 (public) 和需认证 (auth required) 两类。认证使用 Bearer Token。管理端点额外受 `LocalOnlyMiddleware` 保护，仅接受 localhost 请求。

All endpoints are either public or auth-required. Authentication uses Bearer Token. Admin endpoints are additionally protected by `LocalOnlyMiddleware` (localhost-only).

---

## 认证 / Authentication

### 方式 / Method

```
Authorization: Bearer <session_token>
```

- **密码存储**: SHA256 hexdigest in `data/auth.json`
- **会话机制**: uuid4 token, 内存存储, 1 小时 TTL
- **获取 token**: `POST /api/auth/login` 或 `POST /api/auth/setup`
- **限速**: 30 请求/分钟/IP (超出返回 429)

---

## 端点总览 / Endpoint Map

| 方法 | 路径 | 说明 | Auth | localhost |
|---|---|---|---|---|
| GET | `/health` | 健康检查 | ❌ | ❌ |
| GET | `/` | API 信息 | ❌ | ❌ |
| GET | `/api/auth/status` | 认证状态 | ❌ | ✅ |
| POST | `/api/auth/setup` | 首次设置 | ❌ | ✅ |
| POST | `/api/auth/login` | 登录 | ❌ | ✅ |
| POST | `/api/auth/reset` | 修改密码 | ✅ | ✅ |
| GET | `/api/profile` | 获取个人资料 | ❌ | ❌ |
| PUT | `/api/profile` | 更新个人资料 | ✅ | ✅ |
| POST | `/api/profile` | 更新个人资料 | ✅ | ✅ |
| POST | `/api/chat` | 发送聊天消息 | ❌ | ❌ |
| WS | `/api/chat/ws` | 实时聊天 | ❌ | ❌ |
| POST | `/api/knowledge/upload` | 上传文档 | ✅ | ✅ |
| GET | `/api/knowledge/stats` | 知识库统计 | ✅ | ✅ |
| GET | `/api/knowledge/documents` | 文档列表 | ✅ | ✅ |
| GET | `/api/knowledge/search` | 搜索知识库 | ✅ | ✅ |
| POST | `/api/knowledge/import-github` | 导入 GitHub | ✅ | ✅ |
| POST | `/api/knowledge/import-url` | 导入 URL | ✅ | ✅ |
| GET | `/api/voice/status` | 语音管道状态 | ❌ | ❌ |
| POST | `/api/voice/speaker` | 注册发音人 | ✅ | ✅ |
| WS | `/api/voice/conversation` | 语音对话 | ❌ | ❌ |
| GET | `/api/evolution/pending` | 待审事实 | ✅ | ✅ |
| POST | `/api/evolution/approve/{fact_id}` | 批准事实 | ✅ | ✅ |
| POST | `/api/evolution/reject/{fact_id}` | 拒绝事实 | ✅ | ✅ |

---

## 详细端点 / Endpoint Details

### 系统 / System

---

#### `GET /health`

健康检查。

```
GET http://localhost:8000/health
```

**Response `200`**:
```json
{
  "status": "ok",
  "version": "0.1.0"
}
```

---

#### `GET /`

API 根路径。

```
GET http://localhost:8000/
```

**Response `200`**:
```json
{
  "message": "Digital Twin API",
  "docs": "/docs"
}
```

---

### 认证 / Auth (`/api/auth`)

---

#### `GET /api/auth/status`

检查系统是否已设置管理员账号。

```
GET http://localhost:8000/api/auth/status
```

**Auth**: ❌ (但限 localhost)

**Response `200`**:
```json
{
  "setup": false
}
```
```json
{
  "setup": true
}
```

---

#### `POST /api/auth/setup`

首次设置管理员用户名和密码。只能调用一次。

```
POST http://localhost:8000/api/auth/setup
Content-Type: application/json

{
  "username": "admin",
  "password": "mypassword123"
}
```

**Auth**: ❌ (但限 localhost)

**Request Body**:

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| `username` | string | 2-64 字符 | 用户名 |
| `password` | string | 4-128 字符 | 密码 |

**Response `200`**:
```json
{
  "token": "550e8400-e29b-41d4-a716-446655440000",
  "username": "admin"
}
```

**Errors**:

| 状态码 | 条件 |
|---|---|
| 400 | 认证已设置 (只能设置一次) |
| 422 | 参数验证失败 (username < 2, password < 4) |

---

#### `POST /api/auth/login`

登录获取会话 token。

```
POST http://localhost:8000/api/auth/login
Content-Type: application/json

{
  "username": "admin",
  "password": "mypassword123"
}
```

**Auth**: ❌ (但限 localhost)

**Request Body**:

| 字段 | 类型 | 说明 |
|---|---|---|
| `username` | string | 用户名 |
| `password` | string | 密码 |

**Response `200`**:
```json
{
  "token": "550e8400-e29b-41d4-a716-446655440000",
  "username": "admin"
}
```

**Errors**:

| 状态码 | 条件 |
|---|---|
| 400 | 认证尚未设置 |
| 401 | 用户名或密码错误 |

---

#### `POST /api/auth/reset`

修改密码。

```
POST http://localhost:8000/api/auth/reset
Authorization: Bearer <token>
Content-Type: application/json

{
  "current_password": "oldpassword",
  "new_password": "newpassword456"
}
```

**Auth**: ✅ Bearer Token

**Request Body**:

| 字段 | 类型 | 约束 | 说明 |
|---|---|---|---|
| `current_password` | string | — | 当前密码 |
| `new_password` | string | 4-128 字符 | 新密码 |

**Response `200`**:
```json
{
  "status": "password_updated"
}
```

**Errors**: 401 (无/无效 token 或密码错误)

---

### 个人资料 / Profile (`/api/profile`)

---

#### `GET /api/profile`

获取公开的个人资料。缺失字段自动用默认值填充。

```
GET http://localhost:8000/api/profile
```

**Auth**: ❌

**Response `200`**:
```json
{
  "name": "Your Name",
  "title": "AI Digital Twin",
  "summary": "A self-evolving AI digital clone powered by local open-source LLMs.",
  "skills": [
    {"name": "Python", "category": "Programming", "level": 5}
  ],
  "projects": [
    {
      "name": "Digital Twin",
      "description": "AI-powered personal clone with multi-modal interaction",
      "technologies": ["Python", "FastAPI", "Next.js", "Ollama", "ChromaDB"]
    }
  ],
  "experience": [
    {
      "company": "Self-Employed",
      "role": "AI Developer",
      "description": "Building next-generation AI applications",
      "start_date": "2024"
    }
  ],
  "education": [
    {
      "institution": "University",
      "degree": "Bachelor",
      "field": "Computer Science",
      "year": 2020
    }
  ]
}
```

---

#### `PUT /api/profile`

更新个人资料。全部覆盖写入 `data/profile.json`。

```
PUT http://localhost:8000/api/profile
Authorization: Bearer <token>
Content-Type: application/json

{
  "name": "My Real Name",
  "title": "Software Engineer",
  "summary": "...",
  "skills": [...],
  "projects": [...],
  "experience": [...],
  "education": [...]
}
```

**Auth**: ✅ Bearer Token (且限 localhost)

**Request Body**: 任意 JSON 对象

**Response `200`**:
```json
{
  "status": "saved",
  "username": "admin"
}
```

---

### 聊天 / Chat (`/api/chat`)

---

#### `POST /api/chat`

发送消息并获取 AI 回复。非流式，一次性返回完整回复。

内部流程: `ModelRouter.route()` → `RAGChain.query()` → 混合检索 → LLM 生成。

```
POST http://localhost:8000/api/chat
Content-Type: application/json

{
  "message": "你好，请介绍一下你自己",
  "session_id": null
}
```

**Auth**: ❌

**Request Body**:

| 字段 | 类型 | 默认 | 说明 |
|---|---|---|---|
| `message` | string | — | 用户消息 |
| `session_id` | string 或 null | null | 会话 ID, null 自动新建 |

**Response `200`**:
```json
{
  "response": "我是您的数字分身...",
  "session_id": "abc-123-def",
  "model": "qwen3.5:4b"
}
```

| 字段 | 说明 |
|---|---|
| `response` | AI 生成的回复 |
| `session_id` | 会话 ID (用于后续对话) |
| `model` | 实际使用的模型名 |

---

#### `WebSocket /api/chat/ws`

实时流式聊天。连接后自动创建会话。

```
ws://localhost:8000/api/chat/ws
```

**客户端 → 服务端**:
```json
{"message": "你好"}
```

**服务端 → 客户端**:

| 消息 | 说明 |
|---|---|
| `{"type": "thinking"}` | LLM 正在处理 |
| `{"type": "token", "content": "..."}` | 逐 token 输出 |
| `{"type": "done", "session_id": "...", "model": "..."}` | 生成完毕 |

---

### 知识库 / Knowledge (`/api/knowledge`)

---

#### `POST /api/knowledge/upload`

上传文档到知识库。支持格式: .pdf, .docx, .md, .txt。

```
POST http://localhost:8000/api/knowledge/upload
Authorization: Bearer <token>
Content-Type: multipart/form-data

file: @/path/to/document.pdf
```

**Auth**: ✅ Bearer Token (且限 localhost)

**处理流程**: 保存文件 → DocumentParser → TextChunker → LocalEmbedder → ChromaDB 持久化

**Response `200`**:
```json
{
  "task_id": "a1b2c3d4",
  "filename": "document.pdf",
  "chunks": 15,
  "status": "completed"
}
```

**Errors**: 400 (不支持的文件类型), 401 (无/无效 token)

---

#### `GET /api/knowledge/stats`

获取知识库统计 (文档数和分块数)。

```
GET http://localhost:8000/api/knowledge/stats
Authorization: Bearer <token>
```

**Auth**: ✅ Bearer Token (且限 localhost)

**Response `200`**:
```json
{
  "total_documents": 5,
  "total_chunks": 120
}
```

---

#### `GET /api/knowledge/documents`

获取文档列表。

```
GET http://localhost:8000/api/knowledge/documents
Authorization: Bearer <token>
```

**Auth**: ✅ Bearer Token (且限 localhost)

**Response `200`**:
```json
{
  "documents": [
    {
      "id": "uuid-1",
      "filename": "document.pdf",
      "chunks": 15,
      "uploaded_at": "2026-06-18T10:30:00"
    }
  ]
}
```

---

#### `GET /api/knowledge/search`

搜索知识库。

```
GET http://localhost:8000/api/knowledge/search?q=Python+RAG&top_k=3
Authorization: Bearer <token>
```

**Auth**: ✅ Bearer Token (且限 localhost)

**Query**: `q` (搜索词), `top_k` (返回数, 默认 5)

**Response `200`**:
```json
{
  "results": [
    {
      "id": "uuid",
      "text": "Python is a programming language...",
      "score": 0.85,
      "metadata": {"source_file": "doc.pdf", "chunk_index": 0}
    }
  ]
}
```

---

#### `POST /api/knowledge/import-github`

导入 GitHub 仓库内容。

```
POST http://localhost:8000/api/knowledge/import-github
Authorization: Bearer <token>
Content-Type: application/json

{
  "url": "https://github.com/user/repo",
  "branch": "main"
}
```

**Auth**: ✅ Bearer Token (且限 localhost)

**Request Body**: `url` (仓库 URL), `branch` (分支, 默认 main)

**Response `200`**:
```json
{
  "status": "completed",
  "repository": "user/repo",
  "files_processed": 10,
  "chunks_added": 45
}
```

---

#### `POST /api/knowledge/import-url`

导入 URL 网页内容。

```
POST http://localhost:8000/api/knowledge/import-url
Authorization: Bearer <token>
Content-Type: application/json

{
  "url": "https://example.com/about",
  "selector": "article"
}
```

**Auth**: ✅ Bearer Token (且限 localhost)

**Request Body**: `url` (目标 URL), `selector` (CSS 选择器, 可选)

**Response `200`**:
```json
{
  "status": "completed",
  "url": "https://example.com/about",
  "chunks_added": 8
}
```

---

### 语音 / Voice (`/api/voice`)

---

#### `GET /api/voice/status`

获取语音管道状态。

```
GET http://localhost:8000/api/voice/status
```

**Auth**: ❌

**Response `200`**:
```json
{
  "stt_ready": true,
  "tts_ready": true,
  "tts_speakers": []
}
```

| 字段 | 说明 |
|---|---|
| `stt_ready` | faster-whisper 是否已加载 |
| `tts_ready` | Piper TTS 是否就绪 |
| `tts_speakers` | 已注册发音人列表 |

---

#### `POST /api/voice/speaker`

上传语音样本注册发音人 (用于未来声音克隆)。

```
POST http://localhost:8000/api/voice/speaker
Authorization: Bearer <token>
Content-Type: multipart/form-data

file: @/path/to/sample.wav
```

**Auth**: ✅ Bearer Token (且限 localhost)

**Response `200`**:
```json
{
  "status": "registered",
  "speaker_id": "speaker-uuid"
}
```

---

#### `WebSocket /api/voice/conversation`

实时语音对话。支持发送二进制音频 (WAV 16kHz 单声道) 和文本消息。

```
ws://localhost:8000/api/voice/conversation
```

**连接**: 服务端返回就绪状态:
```json
{"type": "ready", "stt": true, "tts": true}
```

**服务端 → 客户端状态机**:

```
IDLE → LISTENING → THINKING → SPEAKING → IDLE
```

| 消息 | 说明 |
|---|---|
| `{"type":"state","state":"listening"}` | 正在听 (STT) |
| `{"type":"state","state":"thinking"}` | 正在思考 (LLM) |
| `{"type":"state","state":"speaking"}` | 正在说 (TTS) |
| `{"type":"result","text":"...","status":"complete"}` | 回复完成 |
| `{"type":"error","message":"..."}` | 错误 |

**处理流程**: 音频 → SpeechToText.transcribe() → RAGChain.query() → TextToSpeech.synthesize() → WAV

---

### 进化 / Evolution (`/api/evolution`)

---

#### `GET /api/evolution/pending`

获取待审核事实列表。

```
GET http://localhost:8000/api/evolution/pending
Authorization: Bearer <token>
```

**Auth**: ✅ Bearer Token (且限 localhost)

**Response `200`**:
```json
{
  "facts": [
    {
      "id": "fact-uuid",
      "type": "skill",
      "content": "Expert in FastAPI development",
      "source": "chat-session-abc",
      "confidence": 0.85
    }
  ]
}
```

---

#### `POST /api/evolution/approve/{fact_id}`

批准事实。自动更新 ChromaDB 向量库和 Neo4j 知识图谱。

```
POST http://localhost:8000/api/evolution/approve/fact-uuid
Authorization: Bearer <token>
```

**Auth**: ✅ Bearer Token (且限 localhost)

**Response `200`**:
```json
{
  "status": "approved",
  "fact_id": "fact-uuid"
}
```

---

#### `POST /api/evolution/reject/{fact_id}`

拒绝事实。

```
POST http://localhost:8000/api/evolution/reject/fact-uuid
Authorization: Bearer <token>
```

**Auth**: ✅ Bearer Token (且限 localhost)

**Response `200`**:
```json
{
  "status": "rejected",
  "fact_id": "fact-uuid"
}
```

---

## 错误码 / Error Codes

| 状态码 | 含义 | 说明 |
|---|---|---|
| 200 | OK | 请求成功 |
| 400 | Bad Request | 参数错误或业务逻辑错误 |
| 401 | Unauthorized | 无 token 或 token 无效/过期 |
| 403 | Forbidden | 非 localhost 请求被限制 |
| 422 | Unprocessable Entity | 请求体验证失败 |
| 429 | Too Many Requests | 超出速率限制 (30 req/min/IP) |
| 500 | Internal Server Error | 服务端内部错误 |

### 错误响应格式 / Error Response Format

```json
{
  "detail": "Invalid or expired session"
}
```

---

## 速率限制 / Rate Limiting

- **算法**: 滑动窗口 / Sliding window
- **限制**: 30 请求 / 60 秒 / IP
- **超限响应**: `429 Too Many Requests. Try again later.`
- **实现**: `backend/app/core/rate_limit.py` — RateLimiter 类
