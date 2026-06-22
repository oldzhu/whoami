# 数字分身 — 本次会话工作记录

## Session: 2026-06-17 ~ 2026-06-18

---

## 🔐 安全加固 (Security Hardening)

| 提交 | 内容 |
|------|------|
| `04527b5` | `.env.production` 从 git 历史彻底清除 |
| `4582209` | evolution approve/reject 加 auth 保护 |
| `17d4ddd` | chat history, knowledge documents/stats, evolution pending 加 auth |
| `14efa4f` | 文件上传路径穿越修复 + session TTL + 限速器 |
| `b3bee34` | 所有 admin 端点 localhost 限制 |

### 安全架构
```
公网 → ❌ (无公网暴露)
localhost → /api/auth, /api/knowledge, /api/profile, /api/evolution  → 需登录
localhost → /api/chat, /api/profile (GET)  → 公开 (数字分身对话)
限速: 30 req/min/IP | 会话: 1小时 TTL | 密码: SHA256
```

---

## 🌐 国际化 (i18n)

| 提交 | 内容 |
|------|------|
| `355208c` | 中英文切换系统，6个页面全部支持 |

- `web/lib/i18n.tsx` — I18nProvider context
- `web/lib/translations.ts` — 中英文翻译表
- 语言切换按钮在导航栏
- 偏好存 localStorage

---

## ⚙️ 数据管理后台

| 提交 | 内容 |
|------|------|
| `355208c` | 认证系统 + Settings 页面 |

### 认证
- `POST /api/auth/setup` — 首次设置密码
- `POST /api/auth/login` — 登录获取 token
- `POST /api/auth/reset` — 修改密码
- SHA256 哈希存储

### Settings 页面 (`/settings`)
- 📝 Profile 标签 — 编辑姓名/技能/项目/经历
- 📄 Documents 标签 — 上传文档
- 🎤 Voice 标签 — 录制语音样本
- 🔑 Password 标签 — 修改密码

---

## 🤖 LLM 模型

| 模型 | 大小 | 世代 | 用途 |
|------|------|------|------|
| qwen2.5:1.5b | 1.1GB | 2024 | 快速备用 |
| qwen2.5:3b | 2.1GB | 2024 | 平衡备用 |
| qwen2.5:7b | 4.7GB | 2024 | 编程/复杂任务 |
| qwen3.5:2b | 1.3GB | 2026 | **默认** (最快) |
| qwen3.5:4b | 2.7GB | 2026 | 平衡 |
| qwen3.5:9b | 5.6GB | 2026 | 最佳质量 |
| all-minilm:l6-v2 | 45MB | - | Embedding |

全部从 ModelScope 下载，支持模型热切换。

---

## 📚 知识摄入 (Knowledge Ingestion)

| 提交 | 端点 | 功能 |
|------|------|------|
| `3057a0c` | `POST /api/knowledge/import-github` | 导入 GitHub 项目 (README + 技术栈) |
| `b7bf641` | `POST /api/knowledge/import-url` | 导入任意 URL 内容 |
| - | `POST /api/knowledge/upload` | 上传文件 (.docx/.pdf/.md) |

### System Prompt 优化 (`aac8a74`)
- 数字分身以第一人称说话 ("我", "我的")
- 自动加载 profile 数据构建身份
- 有/无检索上下文两套 prompt

---

## 🐛 修复

| 问题 | 修复 |
|------|------|
| `/` 首页 `profile.projects.map` undefined | `(profile.projects \|\| []).map` 安全访问 |
| Profile API 部分字段缺失 | 合并默认值 |
| `/settings` hydration warning | Suspense 包裹 + i18n mounted 标志 |
| Ollama adapter 代理超时 | `trust_env=False` |
| Embedding API 路径错误 | `/api/embeddings` → `/api/embed` |
| Embedding 模型缺失 | pull all-minilm:l6-v2 |

---

## 📁 当前文件结构

```
backend/app/
  api/          auth, chat, evolution, knowledge, profile, voice
  core/
    auth.py           SHA256 认证 + session
    rate_limit.py     限速器 (30 req/min)
    llm/              Ollama/llama.cpp/vLLM adapters + mock
    router/           多模型路由
    rag/              RAG pipeline + context builder
    ingestion/        文档解析 + GitHub/URL 导入
    storage/          ChromaDB + Neo4j
    conversation/     会话管理
    voice/            STT + TTS (代码就绪，待测试)
    evolution/        自进化引擎
  middleware.py       localhost 限制 + auth_required

web/
  app/
    page.tsx          首页 (i18n)
    layout.tsx        布局 + 语言切换
    login/            登录页
    settings/         数据管理 (4标签)
    chat/             文字聊天
    voice/            语音对话
    about/            关于
  lib/
    i18n.tsx          国际化
    translations.ts   中英文翻译表
    api-client.ts     API 客户端

mobile/               React Native (代码就绪)
desktop/              Tauri (代码就绪)
deploy/               Docker + vLLM
models/               模型配置
```

## Git 历史
```
b3bee34 security: extend localhost restriction to all admin endpoints
b7bf641 feat: generic URL content importer
aac8a74 feat: authentic system prompt - first person
3057a0c feat: GitHub project importer
17d4ddd security: protect admin-only GET endpoints
14efa4f security: path traversal fix, session TTL, rate limiter
4582209 security: add auth protection to evolution/knowledge
04527b5 security: remove .env.production from tracking
355208c feat: auth system, i18n, settings page, embedding fix, mock LLM
8bf1c9e feat: complete digital twin implementation - all 31 tasks
b167820 chore: initialize project structure and dev environment
```
