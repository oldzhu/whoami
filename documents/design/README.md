# 设计决策记录 / Architecture Decision Records (ADR)

## 概述 / Overview

本文档记录了数字分身项目的关键架构决策，包含上下文、决策理由、后果和替代方案。

This document records key architectural decisions for the Digital Twin project, including context, rationale, consequences, and alternatives considered.

---

## ADR 格式 / ADR Format

每条 ADR 包含: 状态 (Accepted)、日期、上下文 (Context)、决策 (Decision)、后果 (Consequences)、替代方案 (Alternatives)。

Each ADR includes: Status (Accepted), Date, Context, Decision, Consequences, and Alternatives Considered.

---

## ADR-001: Piper TTS 替代 Coqui XTTS v2

### 状态 / Status

**Accepted** — 2026-06-17

### 上下文 / Context

系统需要文本转语音 (TTS) 功能，支持中文和英文，完全本地运行。初始计划使用 Coqui XTTS v2，因其支持声音克隆和高质量多语言合成。

在 Python 3.12 环境中安装 Coqui XTTS v2 失败 — 其依赖 （TensorFlow/Torch 版本）与 Python 3.12 不兼容。需要寻找替代方案。

### 决策 / Decision

放弃 Coqui XTTS v2，改用 **Piper TTS**。

- **实现**: Python subprocess 调用 Piper 命令行 (`piper --model --output-raw`)
- **模型**: `zh_CN-huayan-medium.onnx` (63MB) + `en_US-lessac-medium.onnx` (63MB)
- **存储**: `models/piper/` 目录
- **类**: `TextToSpeech` (`backend/app/core/voice/tts.py`)
- **方法**: `synthesize(text, language)` → WAV bytes

Piper 通过了 TTS 测试验证（中文 + 英文合成，WAV 格式验证）。

### 后果 / Consequences

**正面 / Positive**:
- 兼容 Python 3.12，零依赖问题
- 模型极小 (63MB vs XTTS 的 2GB+)
- 子进程隔离，不影响主进程稳定性
- 支持中文和英文

**负面 / Negative**:
- 音质不如 Coqui XTTS v2（无声音克隆功能）
- 语速和语调不可控
- 多语言检测需外部逻辑 (`language[:2]` 截取)

**风险 / Risks**:
- Piper 维护不活跃，长期可能缺乏更新
- 如需声音克隆，需额外集成 (如 OpenVoice)

### 替代方案 / Alternatives

| 方案 | 原因放弃 |
|---|---|
| Coqui XTTS v2 | Python 3.12 不兼容 |
| eSpeak-NG | 音质差，机器感强 |
| Edge-TTS | 需要网络 API |
| Bark (Suno) | 模型过大 (>10GB)，CPU 推理极慢 |

---

## ADR-002: 三引擎 LLM 策略 (Ollama + llama.cpp + vLLM)

### 状态 / Status

**Accepted** — 2026-06-17

### 上下文 / Context

系统需要一个硬件灵活、场景适配的 LLM 推理方案。开发阶段需要快速迭代，生产阶段需要高吞吐。不同用户的硬件差异大 (CUDA/ROCm/CANN/CPU)。

### 决策 / Decision

采用三层引擎策略，通过工厂模式自动选择:

1. **Ollama** (开发) — 快速部署，Ollama v0.17.5，支持 7 个模型热切换
2. **llama.cpp** (单用户生产) — 低资源消耗，纯 CPU 可运行
3. **vLLM** (多用户生产) — PagedAttention，7.5 倍并发吞吐

**自动检测**: `create_llm_provider("auto")` 按优先级检测:
- `nvidia-smi` → CUDA
- `rocm-smi` → ROCm
- `/usr/local/Ascend` → CANN
- 否则 → CPU

各引擎通过统一 `LLMProvider` 抽象接口调用 (`chat()`, `stream()`, `models()`)。

### 后果 / Consequences

**正面**:
- 硬件适应性最强，无 GPU 也能运行
- 开发和生产用不同引擎，各取所长
- 失败时自动降级到 `MockAdapter`

**负面**:
- 三套引擎需分别配置和维护
- 行为差异 (Ollama API 与 llama.cpp API 不一致)
- `trust_env=False` 问题 (HTTP_PROXY 拦截 localhost)

**风险**:
- vLLM 配置复杂，需大量内存
- 不同引擎的 tokenizer 行为可能不同

### 替代方案 / Alternatives

| 方案 | 原因放弃 |
|---|---|
| 单一引擎 (如只用 Ollama) | 生产并发不够 |
| OpenAI API | 非本地，违反核心要求 |
| TGI (HuggingFace) | 硬件支持少 (仅 CUDA) |

---

## ADR-003: 混合 RAG (向量 + BM25 + 图谱)

### 状态 / Status

**Accepted** — 2026-06-17

### 上下文 / Context

个人知识库需要准确的检索。纯向量搜索会丢失精确关键词匹配，纯关键词搜索无法理解语义。数字分身需要根据用户的知识回答问题。

### 决策 / Decision

采用三路混合检索:

1. **ChromaDB 向量搜索** — all-minilm:l6-v2 384维嵌入，语义相似度匹配
2. **BM25 关键词评分** — TF归一化关键词命中，补充向量搜索的遗漏
3. **Neo4j 知识图谱访问** — Person/Project/Skill 实体关系检索

`HybridRetriever.search()` 合并三路结果后，经过 `Reranker` 重排序取 top 3，最后由 `ContextBuilder` 构建带身份的第一人称 prompt。

### 后果 / Consequences

**正面**:
- 召回率显著高于单一检索方法
- 关键词匹配确保技术术语不遗漏
- 知识图谱支持关系推理 ("谁参与了这个项目？")

**负面**:
- 检索延迟增加 (三次查询 + 重排序)
- 三套存储需同步维护
- BM25 分数未与向量分数做归一化融合

**风险**:
- 检索质量依赖 chunk 策略 (当前 512 token / 128 overlap)
- Neo4j 无数据时图检索贡献为零

### 替代方案 / Alternatives

| 方案 | 原因放弃 |
|---|---|
| 纯向量搜索 | 遗漏关键词精确匹配 |
| 纯 BM25 | 无语义理解 |
| 纯图检索 | 覆盖率低，构建成本高 |
| 单路搜索 + 重排序 | 不如三路融合鲁棒 |

---

## ADR-004: Qwen3.5 系列模型

### 状态 / Status

**Accepted** — 2026-06-17

### 上下文 / Context

需要一系列本地可运行、中英文兼通、行为一致的 LLM 模型。理想模型族应有多个规格 (小/中/大) 以适配不同场景和硬件。

### 决策 / Decision

选择 **Qwen3.5 系列** 作为主力模型，Qwen2.5 系列作为备选。

**主力模型**:
| 模型 | 用途 | 说明 |
|---|---|---|
| Qwen3.5 2B | 默认 (最快) | ~6s 单 CPU 回复，适合闲聊 |
| Qwen3.5 4B | 平衡 | 中文对话路由目标 |
| Qwen3.5 9B | 最佳质量 | 编程/技术/复杂任务 |

**备选模型**:
| 模型 | 用途 |
|---|---|
| Qwen2.5 1.5B | 快速备用 |
| Qwen2.5 3B | 平衡备用 |
| Qwen2.5 7B | 编程任务 |

全部从 **ModelScope** (阿里云镜像) 下载，无需科学上网。

### 后果 / Consequences

**正面**:
- 全系列行为一致 (tokenizer、system prompt 格式相同)
- 中英文能力优秀
- 最小模型 (2B) 可在 CPU 上实时运行
- ModelScope 镜像下载速度快

**负面**:
- Qwen3.5 9B 在 CPU 上较慢 (20s+)
- 非 Qwen 模型 (如 DeepSeek) 的编程优势未利用

**风险**:
- Qwen3.5 是最新 (2026)，生态可能不如 Qwen2.5 成熟

### 替代方案 / Alternatives

| 方案 | 原因放弃 |
|---|---|
| LLaMA 3.1 8B | 中文能力弱 |
| DeepSeek Coder | 代码强但通用对话弱，模型系列不完整 |
| Mistral | 中文支持不佳 |
| 单一模型 | 无法权衡速度和质量的矛盾需求 |

---

## ADR-005: 本地 SHA256 认证

### 状态 / Status

**Accepted** — 2026-06-17

### 上下文 / Context

所有服务运行在 localhost，无公网暴露。需要一个简单、零依赖的认证方案来保护管理端点和个人数据。

### 决策 / Decision

采用 **SimpleAuth** — SHA256 + 会话 token:

- **密码**: SHA256 hexdigest，存储于 `data/auth.json`
- **会话**: uuid4 token，内存 dict，1 小时 TTL
- **验证**: HTTP Bearer header (`Authorization: Bearer <token>`)
- **类**: `SimpleAuth` (`backend/app/core/auth.py`)

```
注册流程:
  POST /api/auth/setup { username, password }
    → SHA256(password) → 写入 data/auth.json
    → uuid4 token → 内存 sessions dict
    → 返回 token

登录流程:
  POST /api/auth/login { username, password }
    → 读取 data/auth.json → SHA256 比对
    → uuid4 token → 返回 token

验证流程:
  auth_required() dependency
    → 解析 Bearer token
    → 检查 sessions dict → 未过期?
    → 返回 username
```

### 后果 / Consequences

**正面**:
- 零外部依赖 (无需 JWT 库、OAuth 服务)
- 极简实现 (~80 行)
- 适合 localhost 场景

**负面**:
- 无多用户支持 (同一时间只能一个管理员)
- 无 token 撤销机制
- 服务重启后所有会话失效
- 无密码找回功能

**风险**:
- 会话存储在内存，重启丢失
- 密码 hash 无 salt (SHA256 简单加密)

### 替代方案 / Alternatives

| 方案 | 原因放弃 |
|---|---|
| JWT | 需要密钥管理，对 localhost 场景过度设计 |
| OAuth2 | 复杂且需要第三方服务 |
| API Key | 需要密钥轮换和存储 |
| 无认证 | 不安全，个人数据无法保护 |

---

## ADR-006: LocalHost 安全模型

### 状态 / Status

**Accepted** — 2026-06-18

### 上下文 / Context

数字分身存储个人敏感数据 (简历、项目、声音样本)。必须防止未经授权的外部访问，同时允许本地应用 (Web、App、Desktop) 自由调用。

### 决策 / Decision

采用 **LocalOnlyMiddleware** 限制管理端点到 localhost:

```python
LOCAL_IPS = {"127.0.0.1", "::1", "localhost", "testclient"}
PROTECTED_PREFIXES = (
    "/api/auth", "/api/settings", "/api/admin",
    "/api/knowledge", "/api/profile", "/api/evolution",
    "/api/voice/speaker"
)
```

**防护规则**:
- 管理端点: 非 localhost → 403
- 公开端点 `/api/chat`, `/api/profile GET`: 任何来源可访问 (数字分身互动)
- 限速: 30 req/min/IP

### 后果 / Consequences

**正面**:
- 默认安全 (个人数据不会意外暴露)
- 公开和受保护端点清晰分离
- CORS 允许所有来源 (不影响本地应用)

**负面**:
- 远程访问需要通过反向代理 (如 nginx)
- 测试需要特殊处理 (TestClient 需 "testclient" IP)

**风险**:
- `x-forwarded-for` 可伪造，但 localhost-only 场景无影响

### 替代方案 / Alternatives

| 方案 | 原因放弃 |
|---|---|
| 全局认证 | 不允许公开聊天，违背数字分身设计 |
| VPN/隧道 | 使用复杂，不适合本地优先场景 |
| 开放全部端口 | 安全问题 |

---

## ADR-007: ChromaDB + Neo4j 双存储

### 状态 / Status

**Accepted** — 2026-06-17

### 上下文 / Context

系统需要两种不同的数据访问模式：语义搜索 (基于相似度) 和关系探索 (基于图结构)。单一存储无法同时满足。

### 决策 / Decision

采用双存储架构:

| 用途 | 存储 | 容器 | 数据 |
|---|---|---|---|
| 向量搜索 | ChromaDB PersistentClient | `chromadb/chroma:latest` | 文档嵌入 (384维) |
| 知识图谱 | Neo4j 5 Community | `neo4j:5-community` | Person/Project/Skill 节点 |

- ChromaDB: 通过 `VectorStore` 类操作，支持集合管理、增删查
- Neo4j: 通过 `GraphStore` 类操作，Bolt 协议连接，支持 Cypher 查询
- Docker Compose 编排两个容器，分别带数据卷持久化

### 后果 / Consequences

**正面**:
- 检索质量高 (向量语义 + 图关系)
- ChromaDB 简单可靠 (无服务器模式可用)
- Neo4j 功能成熟 (APOC 插件支持)

**负面**:
- 两个数据库需维护和同步
- 数据一致性需要应用层保证
- Docker 依赖 (Neo4j 配置略复杂)

**风险**:
- Neo4j 无数据时拖慢启动时间
- ChromaDB 在并发写入时可能锁

### 替代方案 / Alternatives

| 方案 | 原因放弃 |
|---|---|
| 纯 ChromaDB | 无关系查询能力 |
| 纯 Neo4j | 无语义向量搜索 |
| PostgreSQL + pgvector | 需额外 Postgres 实例，无图查询 |
| SQLite + sqlite-vec | 功能有限 |

---

## ADR-008: 第一人称身份系统 Prompt

### 状态 / Status

**Accepted** — 2026-06-18

### 上下文 / Context

数字分身必须以真实人物身份说话，而不是 "作为一个 AI 助手"。需要让 LLM 理解为用户本人。

### 决策 / Decision

设计两套 system prompt，均使用第一人称:

**有 RAG 上下文时**:
```
You are {name}, {title}. This is your digital twin — you speak in first person
as if you are the real person.

## Your Identity
{profile_summary}

## Context from your knowledge base
{context}

## Important Rules
- Always speak in FIRST PERSON ("I", "me", "my")
- Be natural and conversational
- Match the language of the question
```

**无 RAG 上下文时**: 类似但更简洁。

Profile 数据 (姓名、技能、项目、经历) 通过 `_load_profile_summary()` 动态注入:
```
Name: Zhang San
Role: Software Engineer
Summary: An experienced AI developer...
Skills: Python, FastAPI, Machine Learning, Next.js
Projects: Digital Twin, AI Chatbot
Experience: AI Developer at Self-Employed (2024-now)
```

### 后果 / Consequences

**正面**:
- 对话自然，数字分身的回答听起来像真实人物
- 自动语言匹配 (中文问→中文答)
- 无检索时也能基于 profile 提供基本身份信息

**负面**:
- 回复质量依赖 profile 数据准确性
- Profile 配置前的回答可能泛化
- 第一人称可能使用户误以为是真人

**风险**:
- profile 注入太长可能消耗大量 context window

### 替代方案 / Alternatives

| 方案 | 原因放弃 |
|---|---|
| 第三人称 ("他/她") | 生硬、不自然 |
| 无身份 prompt | LLM 默认以 AI 身份回答 |
| 硬编码身份 | 灵活度不够 |

---

## 决策流程 / Decision Process

1. 问题识别 — 识别需要决策的事项
2. 方案收集 — 收集至少 3 个备选方案
3. 评估 — 评估每个方案的优缺点
4. 决策 — 选择最优方案并记录
5. 实施 — 在代码中实现决策
6. 回顾 — 文档持续更新

---

## 索引 / Index

| ADR | 决策 | 日期 | 状态 |
|---|---|---|---|
| 001 | Piper TTS over Coqui XTTS v2 | 2026-06-17 | Accepted |
| 002 | 三引擎 LLM 策略 | 2026-06-17 | Accepted |
| 003 | 混合 RAG (向量+BM25+图谱) | 2026-06-17 | Accepted |
| 004 | Qwen3.5 系列模型 | 2026-06-17 | Accepted |
| 005 | 本地 SHA256 认证 | 2026-06-17 | Accepted |
| 006 | LocalHost 安全模型 | 2026-06-18 | Accepted |
| 007 | ChromaDB + Neo4j 双存储 | 2026-06-17 | Accepted |
| 008 | 第一人称身份 System Prompt | 2026-06-18 | Accepted |
