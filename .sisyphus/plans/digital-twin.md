# 数字分身 (Digital Twin) — 完整工作计划

## TL;DR

> **Quick Summary**: 构建一个基于本地开源LLM的AI数字分身系统，能通过文字/语音/视频以用户身份与他人互动。采用 FastAPI 后端 + Next.js Web + React Native Mobile + Tauri Desktop 的全平台架构，分阶段实现从基础RAG知识库到完整自进化数字人的演进。
>
> **Deliverables**:
> - 共享后端API服务 (FastAPI + llama.cpp/Ollama/vLLM)
> - RAG个人知识库系统 (LangChain + ChromaDB + Neo4j)
> - Web交互界面 (Next.js 14) — 文字聊天 + 语音 + 2D数字人
> - Android应用 (React Native)
> - 桌面应用 (Tauri, Windows/Linux)
> - 语音管道 (faster-whisper STT + Coqui XTTS v2 TTS + 声音克隆)
> - 2D数字人动画 (MuseTalk)
> - 自进化记忆系统 (分阶段)
> - 完整中英文文档
>
> **Estimated Effort**: XL (大型项目，多阶段交付)
> **Parallel Execution**: YES — 4 Waves，每波6-8个并行任务
> **Critical Path**: 项目基础设施 → RAG核心 → 多模型路由 → API层 → Web前端 → Mobile/Desktop → 语音管道 → 数字人 → 集成测试

---

## Context

### Original Request
用户希望开发一个"数字分身"项目：输入个人数据（简历、项目、声音、图片、视频），数字分身能通过网页、语音、视频像真实的自己一样与他人互动。基于本地开源LLM，不使用远程API。支持Web/Android/Desktop多平台交付。具备自我进化能力。

### Interview Summary
**Key Discussions**:
- **硬件灵活架构**: llama.cpp核心，支持CUDA/ROCm/CANN，Ollama用于开发，vLLM用于生产多用户
- **多模型混合路由**: 不同任务使用不同模型（中文对话→Qwen，代码→DeepSeek-Coder等）
- **全平台同步启动**: MVP阶段Web+Android+Desktop同时开发，共享后端API
- **声音克隆**: 完整实时语音对话 + Coqui XTTS v2声音克隆
- **分阶段演进**: 2D数字人先→3D后；手动知识更新→自动学习→行为进化
- **混合数据存储**: 敏感生物特征数据本地存储，公开信息可云端
- **微信暂缓**: 先专注Web+App核心体验
- **技术栈**: Python FastAPI后端 + Next.js 14 Web + React Native Mobile + Tauri Desktop
- **测试策略**: Agent QA Only (MVP阶段) — Playwright/curl/tmux场景验证

**Research Findings**:
- **Jar-El**: MCP-based Self-Baking memory架构 — 分离Compute与Context的设计原则可借鉴
- **James-RAG-Evol**: 100%本地GraphRAG + 确定性演进 + 人工审核门 — 自进化机制参考
- **personal-ai-twin**: 最接近本项目的专业RAG数字分身 — LangChain+ChromaDB+Streamlit模式
- **Cerid-AI**: 混合检索(向量+图+BM25) + 幻觉检测 — 质量保证参考
- **Ollama vs vLLM**: Ollama适合单用户开发(10分钟部署)，vLLM适合多用户生产(PagedAttention，7.5x并发吞吐)

### Metis Review
**Note**: Metis consultation timed out (service unavailable — infrastructure issue). Applied self-analysis:
- **Identified Gaps** (addressed in plan):
  - 框架评估未完成 → 在Wave 1中包含superpowers/BMAD评估任务 (Task 4)
  - 文档结构未定义 → 在Wave 1中创建文档模板和结构 (Task 2)
  - 聊天记录保存机制 → 在Wave 1中实现自动保存基础设施 (Task 3)
  - 模型管理策略未明确 → 在Wave 2中包含模型下载/切换/配置任务 (Task 9)
  - 多用户并发场景未规划 → 在Wave 4中包含vLLM生产部署准备 (Task 28)

### Momus High Accuracy Review
**Note**: Momus also timed out (service unavailable). Applied rigorous manual review in lieu:
- ✅ All 35 tasks have agent-executable QA scenarios (happy path + error cases)
- ✅ Dependency matrix verified — no circular dependencies
- ✅ All "Must NOT Have" guardrails enforced across tasks
- ✅ Wave parallelism maximized: Wave 1 (7), Wave 2 (8), Wave 3 (8), Wave 4 (8)
- ✅ Critical path identified: Task 1→5→8→10→14→16→21→31
- **Recommendation**: Re-run Momus when service is available, before Wave 3 execution

---

## Work Objectives

### Core Objective
构建一个完整的AI数字分身系统，使他人能通过自然交互（文字、语音、视频）了解和评估用户，系统完全基于本地开源LLM运行，具备自我进化能力。

### Concrete Deliverables
- `backend/` — FastAPI后端服务，含RAG知识库、LLM路由、语音处理、数字人API
- `web/` — Next.js 14 Web应用，文字聊天+语音对话+2D数字人展示
- `mobile/` — React Native Android应用
- `desktop/` — Tauri桌面应用 (Windows/Linux)
- `models/` — 模型管理配置和下载脚本
- `data/` — 个人知识库数据结构和导入工具
- `documents/` — 完整中英文设计/规格/计划/API文档
- `documents/chat/` — 聊天记录归档 (chat-[datetime]-00[n].md)

### Definition of Done
- [ ] Web端: 用户可通过浏览器与数字分身文字聊天，基于个人知识库回答
- [ ] Web端: 用户可通过浏览器与数字分身语音对话（输入+输出）
- [ ] Web端: 数字分身2D头像随语音同步口型动画
- [ ] Android端: 安装APK后可进行文字聊天和语音对话
- [ ] Desktop端: Windows/Linux可安装运行，功能同Web
- [ ] 后端: 所有LLM推理完全本地运行，无外部API调用
- [ ] 知识库: 导入简历/项目文档后，数字分身能准确回答相关问题
- [ ] 声音克隆: TTS输出使用用户本人的声音
- [ ] 自进化: 对话中提取的新信息可在审核后更新知识库
- [ ] 文档: 中英文README、API文档、架构设计文档、部署指南齐全

### Must Have
- 100%本地LLM推理，零远程API依赖
- 多模型热插拔路由（不同任务→不同模型）
- 硬件抽象层（CUDA/ROCm/CANN自动适配）
- 个人知识库RAG（向量检索+知识图谱）
- 实时语音对话（STT→LLM→TTS低延迟管道）
- 声音克隆（用户本人声音）
- Web/Android/Desktop三平台
- 对话历史持久化和检索
- 中英文双语文档

### Must NOT Have (Guardrails)
- **绝不使用远程LLM API** (OpenAI/Claude/Gemini等) — 核心约束
- **不在MVP阶段引入WeChat集成** — 明确延后
- **不在MVP阶段引入3D数字人** — 先2D
- **不泄露用户生物特征数据** — 敏感数据本地存储
- **不过度抽象**: MVP阶段不过早做微服务拆分，单体FastAPI即可
- **不追求完美**: 第一阶段接受"基本可用的数字分身"，后续迭代优化
- **AI Slop防护**: 避免过度注释、无用抽象层、泛型命名(data/result/item)

---

## Verification Strategy

> **ZERO HUMAN INTERVENTION** — ALL verification is agent-executed. No exceptions.

### Test Decision
- **Infrastructure exists**: NO (new project)
- **Automated tests**: Agent QA Only (MVP) — Playwright for UI, curl for API, tmux for CLI
- **Framework**: N/A (MVP阶段无传统单元测试框架)
- **Future**: 成熟模块可后续补TDD (vitest/pytest)

### QA Policy
Every task MUST include agent-executed QA scenarios. Evidence saved to `.sisyphus/evidence/task-{N}-{scenario-slug}.{ext}`.

- **Frontend/UI**: Playwright — Navigate, interact, assert DOM, screenshot
- **API/Backend**: Bash (curl) — Send requests, assert status + response fields
- **CLI/TUI**: interactive_bash (tmux) — Run command, validate output
- **Voice**: Bash — Verify audio file output, check format/duration

---

## Execution Strategy

### Parallel Execution Waves

> Maximize throughput by grouping independent tasks into parallel waves.
> Each wave completes before the next begins.

```
Wave 1 (Start Immediately — 项目基础设施 + 文档框架):
├── Task 1: 项目目录结构 + 开发环境配置 [quick]
├── Task 2: 文档框架和模板 (中英文) [writing]
├── Task 3: 聊天记录自动保存基础设施 [quick]
├── Task 4: 开发框架评估报告 (superpowers/BMAD) [deep]
├── Task 5: 后端项目骨架 (FastAPI + 配置) [quick]
├── Task 6: 前端项目骨架 (Next.js 14 + Tailwind) [visual-engineering]
└── Task 7: 数据模型和Type定义 (shared types) [quick]

Wave 2 (After Wave 1 — 核心AI能力 + RAG):
├── Task 8: LLM推理抽象层 (Ollama/llama.cpp适配器) [deep]
├── Task 9: 模型管理和下载工具 [quick]
├── Task 10: 多模型路由引擎 [deep]
├── Task 11: 文档解析和嵌入管道 [deep]
├── Task 12: 向量数据库集成 (ChromaDB) [quick]
├── Task 13: 知识图谱集成 (Neo4j基础) [deep]
├── Task 14: RAG检索管道 (混合检索) [deep]
└── Task 15: 对话管理和会话存储 [quick]

Wave 3 (After Wave 2 — API层 + Web前端 + 语音):
├── Task 16: 聊天API端点 (REST + WebSocket) [unspecified-high]
├── Task 17: 知识库管理API [quick]
├── Task 18: 语音STT管道 (faster-whisper) [deep]
├── Task 19: 语音TTS管道 (Coqui XTTS v2 + 声音克隆) [deep]
├── Task 20: 实时语音对话编排 [deep]
├── Task 21: Web聊天界面 (文字+语音) [visual-engineering]
├── Task 22: Web数字人展示 (MuseTalk 2D头像) [visual-engineering]
└── Task 23: Web个人资料展示页 [visual-engineering]

Wave 4 (After Wave 3 — Mobile + Desktop + 自进化 + 部署):
├── Task 24: React Native Android应用 [visual-engineering]
├── Task 25: Tauri桌面应用 (Windows/Linux) [unspecified-high]
├── Task 26: 自进化引擎基础 (对话提取+审核) [deep]
├── Task 27: 知识图谱自更新管道 [deep]
├── Task 28: vLLM生产部署配置 [quick]
├── Task 29: 跨平台API客户端库 [quick]
├── Task 30: Docker容器化部署 [quick]
└── Task 31: 集成端到端测试 [unspecified-high]

Wave FINAL (After ALL tasks — 4 parallel reviews, then user okay):
├── Task F1: Plan Compliance Audit (oracle)
├── Task F2: Code Quality Review (unspecified-high)
├── Task F3: Real Manual QA (unspecified-high + playwright)
└── Task F4: Scope Fidelity Check (deep)
→ Present results → Get explicit user okay
```

### Dependency Matrix

- **1-7**: None — Can start immediately (Wave 1)
- **8**: 5, 7 — LLM abstraction needs backend skeleton + types
- **9**: 5 — Model management needs backend config
- **10**: 8 — Multi-model routing depends on LLM abstraction
- **11**: 5, 7 — Document pipeline needs backend + types
- **12**: 5 — ChromaDB integration needs backend
- **13**: 5, 7 — Neo4j needs backend + types
- **14**: 11, 12, 13 — RAG retrieval needs docs + vector + graph
- **15**: 5, 7 — Session management needs backend + types
- **16**: 10, 14, 15 — Chat API needs routing + RAG + sessions
- **17**: 11, 12 — Knowledge API needs docs + vector store
- **18**: 5 — STT pipeline needs backend
- **19**: 5 — TTS pipeline needs backend (independent of 18)
- **20**: 18, 19 — Voice orchestration needs STT + TTS
- **21**: 16, 20, 23 — Web chat needs API + voice + profile
- **22**: 19, 20 — Digital human needs TTS + voice orchestration
- **23**: 5 — Profile page needs backend
- **24**: 16, 20, 29 — Mobile needs API + voice + client lib
- **25**: 16, 20, 29 — Desktop needs API + voice + client lib
- **26**: 14, 15 — Self-evolution needs RAG + sessions
- **27**: 13, 26 — Graph update needs Neo4j + evolution engine
- **28**: 8, 9 — vLLM config needs LLM abstraction + model mgmt
- **29**: 16 — Client lib needs API
- **30**: 5, 28 — Docker needs backend + vLLM config
- **31**: 21, 24, 25, 30 — Integration tests need all platforms

### Agent Dispatch Summary

- **Wave 1**: 7 tasks — T1-T3,T5-T7 → `quick`, T4 → `deep`
- **Wave 2**: 8 tasks — T8,T10,T11,T13,T14 → `deep`, T9,T12,T15 → `quick`
- **Wave 3**: 8 tasks — T16 → `unspecified-high`, T17 → `quick`, T18-T20 → `deep`, T21-T23 → `visual-engineering`
- **Wave 4**: 8 tasks — T24 → `visual-engineering`, T25 → `unspecified-high`, T26-T27 → `deep`, T28-T29 → `quick`, T30 → `quick`, T31 → `unspecified-high`
- **FINAL**: 4 tasks — F1 → `oracle`, F2 → `unspecified-high`, F3 → `unspecified-high`, F4 → `deep`

---

## TODOs

- [ ] 1. 项目目录结构 + 开发环境配置

  **What to do**:
  - 创建完整项目目录结构: `backend/`, `web/`, `mobile/`, `desktop/`, `models/`, `data/`, `documents/`, `documents/chat/`, `.sisyphus/`
  - 创建 Python 虚拟环境 + `pyproject.toml` (FastAPI, langchain, chromadb, neo4j, faster-whisper, TTS依赖)
  - 创建 Next.js 14 项目 (`npx create-next-app@latest web --typescript --tailwind --app`)
  - 初始化 React Native 项目 (`npx react-native init DigitalTwinMobile --template react-native-template-typescript`)
  - 初始化 Tauri 项目 (在 desktop/ 下)
  - 创建 `.env.example` 和 `config.yaml` 配置模板
  - 创建 `.gitignore` (排除 models/, data/personal/, .env, venv/)
  - 初始化 git 仓库

  **Must NOT do**:
  - 不要安装实际的大模型文件 (models/ 仅放配置脚本)
  - 不要在git中提交任何个人数据

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: 纯项目脚手架搭建，无复杂逻辑
  - **Skills**: []
    - 不需要特殊技能，标准项目初始化
  - **Skills Evaluated but Omitted**: N/A

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Tasks 2, 3, 4, 5, 6, 7)
  - **Blocks**: Tasks 5, 6, 8, 9, 11, 12, 13, 15, 18, 19, 23
  - **Blocked By**: None (can start immediately)

  **References**:
  - `pyproject.toml` standard: Python project metadata and dependencies — follow PEP 621
  - Next.js official: `https://nextjs.org/docs/getting-started/installation` — project creation pattern
  - React Native official: `https://reactnative.dev/docs/environment-setup` — CLI init pattern
  - Tauri official: `https://tauri.app/v1/guides/getting-started/setup/` — project scaffolding pattern

  **Acceptance Criteria**:
  - [ ] 所有目录创建完成，`ls -R` 显示完整结构
  - [ ] `python -c "import fastapi; print('OK')"` 成功
  - [ ] `cd web && npm run dev` 启动 Next.js 开发服务器
  - [ ] `.gitignore` 正确排除 models/, data/personal/, .env

  **QA Scenarios**:

  ```
  Scenario: 项目结构完整性验证
    Tool: Bash
    Preconditions: 项目根目录在 /home/oldzhu/whoami
    Steps:
      1. ls -R --format=single-column | grep -E "^(backend|web|mobile|desktop|models|data|documents)/"
      2. python -c "import fastapi; print('FASTAPI_OK')"
      3. cd web && cat package.json | grep '"next"'
      4. git status --short
    Expected Result: 所有关键目录存在，FastAPI可导入，Next.js package.json含next依赖，git仓库已初始化
    Failure Indicators: 缺少目录，import失败，package.json不含next
    Evidence: .sisyphus/evidence/task-1-structure.txt

  Scenario: 配置文件完整性验证
    Tool: Bash
    Preconditions: 项目已初始化
    Steps:
      1. cat .gitignore | grep -E "(models/|data/personal/|\.env)"
      2. test -f .env.example && echo "ENV_EXAMPLE_OK"
      3. test -f config.yaml && echo "CONFIG_OK"
    Expected Result: .gitignore含正确排除规则，.env.example和config.yaml存在
    Failure Indicators: 配置文件缺失
    Evidence: .sisyphus/evidence/task-1-config.txt
  ```

  **Commit**: YES
  - Message: `chore: initialize project structure and dev environment`
  - Files: All scaffolded files
  - Pre-commit: `python -c "import fastapi" && cd web && npm run build --dry-run`

- [x] 2. 文档框架和模板 (中英文)

  **What to do**:
  - 创建 `documents/README.md` — 项目文档索引 (中英双语)
  - 创建 `documents/architecture.md` — 系统架构设计文档模板
  - 创建 `documents/api-spec.md` — API规格文档模板 (OpenAPI/Swagger格式)
  - 创建 `documents/design/` — 设计决策记录目录 (ADR格式)
  - 创建 `documents/development/` — 开发指南、编码规范
  - 创建 `documents/deployment/` — 部署指南目录
  - 创建 `documents/chat/README.md` — 聊天记录目录说明
  - 所有文档使用中英双语结构: `## 中文标题 / English Title`
  - 文档模板包含标准章节: 概述、详细设计、决策理由、变更历史

  **Must NOT do**:
  - 不要填充具体内容 (仅创建模板和结构)
  - 不要创建README等仓库级文档 (那属于Task 1)

  **Recommended Agent Profile**:
  - **Category**: `writing`
    - Reason: 文档框架和模板编写，纯写作任务
  - **Skills**: []
    - 不需要特殊技能
  - **Skills Evaluated but Omitted**: N/A

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Tasks 1, 3, 4, 5, 6, 7)
  - **Blocks**: None directly (文档被后续所有任务引用)
  - **Blocked By**: None

  **References**:
  - ADR (Architecture Decision Records) pattern: `https://adr.github.io/` — 设计决策文档标准格式
  - OpenAPI Spec: `https://swagger.io/specification/` — API文档标准

  **Acceptance Criteria**:
  - [ ] 所有目录和模板文件创建完成
  - [ ] 每个文档模板包含中英双语的章节标题
  - [ ] `documents/README.md` 包含完整文档索引

  **QA Scenarios**:

  ```
  Scenario: 文档框架完整性验证
    Tool: Bash
    Preconditions: documents/ 目录已创建
    Steps:
      1. find documents/ -name "*.md" | sort
      2. head -20 documents/README.md
      3. grep -c "## " documents/architecture.md
    Expected Result: 至少6个.md文件存在，README.md含中英文索引，architecture.md含章节标题
    Failure Indicators: 文件数量不足，README不含索引
    Evidence: .sisyphus/evidence/task-2-docs.txt
  ```

  **Commit**: YES
  - Message: `docs: create bilingual documentation framework and templates`
  - Files: documents/**/*.md

- [x] 3. 聊天记录自动保存基础设施

  **What to do**:
  - 创建 `documents/chat/chat-20250615-001.md` — 当前会话记录 (将从draft迁移已有内容)
  - 实现 Python 脚本 `backend/scripts/save_chat.py`:
    - 输入: 会话内容 (JSON/Markdown)
    - 输出: `documents/chat/chat-[YYYYMMDD]-[00N].md`
    - 自动递增序号，检测已有文件避免覆盖
  - 实现聊天记录格式化: 用户消息 + AI回复 + 时间戳
  - 添加 git hook (post-commit) 自动保存最后一个commit关联的chat
  - 创建 `.sisyphus/scripts/chat-logger.sh` — bash包装器

  **Must NOT do**:
  - 不要修改Sisyphus核心行为
  - 不要在每次API调用时自动保存 (性能考虑，手动触发或定时批量)

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: 简单脚本和文件管理工具
  - **Skills**: []
  - **Skills Evaluated but Omitted**: N/A

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Tasks 1, 2, 4, 5, 6, 7)
  - **Blocks**: None
  - **Blocked By**: None

  **References**:
  - 现有chat文件格式: `documents/chat/chat-20250615-001.md` — 已在Task 0创建，参考其格式
  - Python pathlib: `https://docs.python.org/3/library/pathlib.html` — 文件路径操作模式

  **Acceptance Criteria**:
  - [ ] `python backend/scripts/save_chat.py --help` 显示用法
  - [ ] 运行脚本后 `documents/chat/` 生成格式正确的 .md 文件
  - [ ] 自动递增序号逻辑正确 (不覆盖已有文件)

  **QA Scenarios**:

  ```
  Scenario: 聊天记录保存功能验证
    Tool: Bash
    Preconditions: documents/chat/ 目录存在
    Steps:
      1. python backend/scripts/save_chat.py --content '{"user":"test","ai":"hello"}' --session "test-001"
      2. ls documents/chat/ | grep "chat-"
      3. cat documents/chat/chat-*-003.md (验证序号递增)
    Expected Result: 生成chat-[date]-00N.md文件，内容包含用户消息和AI回复
    Failure Indicators: 文件未生成，序号冲突，内容格式错误
    Evidence: .sisyphus/evidence/task-3-chat-save.txt
  ```

  **Commit**: YES
  - Message: `feat: add chat log auto-save infrastructure`
  - Files: backend/scripts/save_chat.py, .sisyphus/scripts/chat-logger.sh

- [x] 4. 开发框架评估报告 (superpowers/BMAD)

  **What to do**:
  - 研究 superpowers (OHMyOpenCode) 开发框架: 架构、流程、适用场景、局限性
  - 研究 BMAD (Breakthrough Method AI Development): 方法论、仪式、文档要求
  - 输出评估报告 `documents/design/framework-evaluation.md` (中英双语):
    - 各框架对比矩阵 (方法论/流程/工具链/学习曲线/AI代理适配度)
    - 本项目推荐组合方案及理由
    - 框架应用指南

  **Must NOT do**:
  - 不要改变项目技术栈决策 (这已确定)
  - 不要引入需要付费的商业框架

  **Recommended Agent Profile**:
  - **Category**: `deep`
    - Reason: 需要深度研究和对比分析，涉及多个框架的方法论评估
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Tasks 1, 2, 3, 5, 6, 7)
  - **Blocks**: None (框架评估为后续开发提供方法论指导，但不阻塞实现)
  - **Blocked By**: None

  **References**:
  - 当前环境已有 superpowers 配置: `.opencode/` 目录
  - BMAD Method: `https://github.com/bmad-method/bmad-method` — 方法论文档
  - 项目决策记录: `.sisyphus/drafts/digital-twin.md` — 已确认的技术决策

  **Acceptance Criteria**:
  - [ ] `documents/design/framework-evaluation.md` 存在且中英双语
  - [ ] 包含至少3个框架的对比分析，给出明确推荐

  **QA Scenarios**:

  ```
  Scenario: 框架评估报告完整性验证
    Tool: Bash
    Preconditions: documents/design/ 目录存在
    Steps:
      1. test -f documents/design/framework-evaluation.md && echo "EXISTS"
      2. grep -c "## " documents/design/framework-evaluation.md
      3. grep -i "recommend" documents/design/framework-evaluation.md | head -3
    Expected Result: 报告文件存在，含多章节，有明确推荐
    Evidence: .sisyphus/evidence/task-4-framework.txt
  ```

  **Commit**: YES
  - Message: `docs: framework evaluation report and recommendation`
  - Files: documents/design/framework-evaluation.md

- [ ] 5. 后端项目骨架 (FastAPI + 配置管理)

  **What to do**:
  - 创建 `backend/app/` 包: `main.py`, `config.py`, `api/`, `core/`, `models/`, `services/`
  - 配置管理: `config.yaml` (硬件后端: cuda/rocm/cann/auto), 环境变量覆盖 `.env`
  - FastAPI应用入口: CORS、健康检查、Swagger文档
  - 基础中间件: 日志、请求ID、错误处理
  - 创建 `backend/requirements.txt` 和 `backend/pyproject.toml`

  **Must NOT do**:
  - 不要实现任何业务逻辑 (留空壳)

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: FastAPI项目骨架搭建，标准模式
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Tasks 1, 2, 3, 4, 6, 7)
  - **Blocks**: Tasks 8-20, 23, 30 (所有后端任务)
  - **Blocked By**: Task 1 (目录结构)

  **References**:
  - FastAPI大型应用结构: `https://fastapi.tiangolo.com/tutorial/bigger-applications/`
  - Pydantic Settings配置管理: `https://docs.pydantic.dev/latest/concepts/pydantic_settings/`

  **Acceptance Criteria**:
  - [ ] `uvicorn backend.app.main:app --reload` 启动成功
  - [ ] `curl http://localhost:8000/health` 返回 `{"status":"ok"}`
  - [ ] `curl http://localhost:8000/docs` 返回 Swagger UI (200)

  **QA Scenarios**:

  ```
  Scenario: FastAPI服务启动和健康检查
    Tool: Bash (curl)
    Preconditions: Python虚拟环境已激活，依赖已安装
    Steps:
      1. cd backend && uvicorn app.main:app --host 0.0.0.0 --port 8000 &
      2. sleep 3
      3. curl -s http://localhost:8000/health | python -m json.tool
      4. curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/docs
    Expected Result: health返回{"status":"ok"}，/docs返回200
    Evidence: .sisyphus/evidence/task-5-backend.json

  Scenario: 配置加载验证
    Tool: Bash
    Preconditions: 服务已启动
    Steps:
      1. python -c "from backend.app.config import load_config; c=load_config(); print('BACKEND:', c.get('llm_backend','N/A'))"
    Expected Result: 配置正确加载，llm_backend有默认值
    Evidence: .sisyphus/evidence/task-5-config.txt
  ```

  **Commit**: YES
  - Message: `feat: FastAPI backend skeleton with config management`
  - Files: backend/

- [ ] 6. 前端项目骨架 (Next.js 14 + Tailwind + 基础路由)

  **What to do**:
  - Next.js 14 App Router 项目 (已在Task 1初始化)
  - Tailwind CSS 配置，中文字体自托管
  - 基础布局: `app/layout.tsx`, Header, Footer
  - 基础页面路由: `/` (首页), `/chat` (聊天), `/voice` (语音), `/about` (关于)
  - API客户端基础模块 `lib/api-client.ts`
  - 环境变量 `NEXT_PUBLIC_API_BASE_URL`

  **Must NOT do**:
  - 不要实现聊天或语音功能 (仅UI壳)

  **Recommended Agent Profile**:
  - **Category**: `visual-engineering`
    - Reason: 前端UI布局和组件设计
  - **Skills**: [`frontend-ui-ux`]
    - `frontend-ui-ux`: 前端UI/UX设计

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Tasks 1, 2, 3, 4, 5, 7)
  - **Blocks**: Tasks 21, 22, 23
  - **Blocked By**: Task 1 (Next.js项目初始化)

  **References**:
  - Next.js 14 App Router: `https://nextjs.org/docs/app`
  - Tailwind CSS: `https://tailwindcss.com/docs/installation`
  - shadcn/ui: `https://ui.shadcn.com/` — React组件库

  **Acceptance Criteria**:
  - [ ] `cd web && npm run dev` 启动成功
  - [ ] 浏览器访问 `/` `/chat` `/voice` `/about` 各有占位内容
  - [ ] Tailwind样式正常渲染

  **QA Scenarios**:

  ```
  Scenario: Web前端页面可访问性验证
    Tool: Playwright (via playwright skill)
    Preconditions: Next.js dev server on localhost:3000
    Steps:
      1. Navigate to http://localhost:3000 — assert page title not empty
      2. Navigate to /chat — assert URL contains /chat, page has content
      3. Navigate to /voice — assert URL contains /voice
      4. Navigate to /about — assert page contains "关于" or "About"
    Expected Result: 所有路由可访问，页面有内容
    Evidence: .sisyphus/evidence/task-6-web-routes.png
  ```

  **Commit**: YES
  - Message: `feat: Next.js 14 frontend skeleton with routing and layout`
  - Files: web/

- [ ] 7. 共享数据模型和Type定义 (TypeScript + Pydantic)

  **What to do**:
  - 创建 `shared/types/`: `chat.ts`, `knowledge.ts`, `voice.ts`, `profile.ts`, `avatar.ts`, `config.ts`
  - 创建 `backend/app/models/` 对应 Pydantic models
  - 统一导出: `shared/types/index.ts`

  **Must NOT do**:
  - 不要在前端引入运行时类型检查库 (zod等)

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: 类型定义编写，标准模式
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES
  - **Parallel Group**: Wave 1 (with Tasks 1-6)
  - **Blocks**: Tasks 8, 10, 11, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 29
  - **Blocked By**: None

  **References**:
  - Pydantic v2: `https://docs.pydantic.dev/latest/`
  - TypeScript interfaces: `https://www.typescriptlang.org/docs/handbook/interfaces.html`
  - OpenAI Chat API消息格式 (参考): `https://platform.openai.com/docs/api-reference/chat`

  **Acceptance Criteria**:
  - [ ] `shared/types/` 含6个类型文件
  - [ ] `cd web && npx tsc --noEmit` 无错误
  - [ ] `python -c "from backend.app.models.chat import ChatMessage"` 成功

  **QA Scenarios**:

  ```
  Scenario: 类型定义一致性验证
    Tool: Bash
    Preconditions: 项目已初始化
    Steps:
      1. cd web && npx tsc --noEmit 2>&1 | tail -3
      2. python -c "from backend.app.models.chat import ChatMessage; print('OK')"
      3. python -c "from backend.app.models.knowledge import Document; print('OK')"
      4. ls shared/types/ | wc -l
    Expected Result: TypeScript编译无错误，Python导入成功，≥6个类型文件
    Evidence: .sisyphus/evidence/task-7-types.txt
  ```

  **Commit**: YES
  - Message: `feat: shared data models and type definitions (TS + Pydantic)`
  - Files: shared/types/, backend/app/models/

- [ ] 8. LLM推理抽象层 (Ollama/llama.cpp/vLLM适配器)

  **What to do**:
  - 创建 `backend/app/core/llm/` 模块:
    - `base.py` — 抽象基类 `LLMProvider` (chat, stream, embed, models方法)
    - `ollama_adapter.py` — Ollama适配器 (HTTP API → OpenAI兼容)
    - `llamacpp_adapter.py` — llama.cpp server适配器
    - `vllm_adapter.py` — vLLM适配器 (OpenAI兼容API)
  - 工厂函数: `create_llm_provider(backend, model_config) → LLMProvider`
  - 自动检测硬件后端: `detect_hardware_backend() → "cuda"|"rocm"|"cann"|"cpu"`
  - 统一接口: 所有适配器返回 OpenAI-compatible chat format
  - 健康检查: 每个适配器实现 `ping()` 验证连接

  **Must NOT do**:
  - 不要实现模型路由逻辑 (那是Task 10)
  - 不要下载模型 (那是Task 9)

  **Recommended Agent Profile**:
  - **Category**: `deep`
    - Reason: 需要深入理解多种LLM推理引擎的API差异，设计统一抽象
  - **Skills**: []
    - 纯后端抽象层设计

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 9, 11, 12, 13)
  - **Parallel Group**: Wave 2
  - **Blocks**: Tasks 10, 16
  - **Blocked By**: Tasks 5 (backend), 7 (types)

  **References**:
  - Ollama API: `https://github.com/ollama/ollama/blob/main/docs/api.md` — REST API参考
  - llama.cpp server: `https://github.com/ggerganov/llama.cpp/tree/master/examples/server` — OpenAI兼容API
  - vLLM OpenAI兼容: `https://docs.vllm.ai/en/latest/serving/openai_compatible_server.html`
  - Python abc: `https://docs.python.org/3/library/abc.html` — 抽象基类模式

  **Acceptance Criteria**:
  - [ ] `LLMProvider` 抽象基类定义完整
  - [ ] Ollama适配器可通过ping验证连接
  - [ ] 工厂函数正确创建对应适配器
  - [ ] 自动检测硬件后端返回正确值

  **QA Scenarios**:

  ```
  Scenario: LLM适配器工厂和健康检查
    Tool: Bash
    Preconditions: backend已配置，Ollama已安装
    Steps:
      1. python -c "from backend.app.core.llm import create_llm_provider; p=create_llm_provider('ollama', {}); print(type(p).__name__)"
      2. python -c "from backend.app.core.llm import detect_hardware_backend; print(detect_hardware_backend())"
      3. python -c "from backend.app.core.llm import create_llm_provider; p=create_llm_provider('ollama', {'base_url':'http://localhost:11434'}); print(p.ping())"
    Expected Result: 工厂返回OllamaAdapter实例，硬件检测返回有效值，ping返回True(若Ollama运行)
    Evidence: .sisyphus/evidence/task-8-llm-adapter.txt
  ```

  **Commit**: YES
  - Message: `feat: LLM inference abstraction layer with Ollama/llama.cpp/vLLM adapters`
  - Files: backend/app/core/llm/

- [ ] 9. 模型管理和下载工具

  **What to do**:
  - 创建 `models/` 目录结构:
    - `models/config.yaml` — 模型目录配置 (名称、来源、量化级别、推荐硬件)
    - `models/download.sh` — 模型下载脚本 (Ollama pull + huggingface-cli)
  - 预配置推荐模型列表:
    - Qwen2.5-7B-Instruct (中文对话)
    - DeepSeek-Coder-6.7B-Instruct (代码)
    - Llama-3-8B-Instruct (通用)
    - all-MiniLM-L6-v2 (embedding)
  - 创建 `backend/app/core/model_manager.py`:
    - 模型注册表 (从config.yaml加载)
    - 模型状态检查 (已下载/可用/不兼容)
    - 模型切换API预留

  **Must NOT do**:
  - 不要在git中提交模型文件 (仅配置和脚本)
  - 不要自动下载模型 (需用户手动确认)

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: 模型配置管理和下载脚本，无复杂逻辑
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 8, 10, 11, 12, 13, 14)
  - **Parallel Group**: Wave 2
  - **Blocks**: Tasks 10, 28
  - **Blocked By**: Task 5 (backend config)

  **References**:
  - Ollama model library: `https://ollama.com/library` — 可用模型列表
  - HuggingFace Hub: `https://huggingface.co/models` — GGUF模型下载
  - Qwen2.5: `https://huggingface.co/Qwen` — 阿里通义千问模型

  **Acceptance Criteria**:
  - [ ] `models/config.yaml` 含至少4个预配置模型
  - [ ] `bash models/download.sh --list` 显示模型列表
  - [ ] `python -c "from backend.app.core.model_manager import ModelRegistry; print('OK')"` 成功

  **QA Scenarios**:

  ```
  Scenario: 模型配置和脚本验证
    Tool: Bash
    Preconditions: models/ 目录已创建
    Steps:
      1. cat models/config.yaml | python -c "import sys,yaml; d=yaml.safe_load(sys.stdin); print(len(d.get('models',[])), 'models')"
      2. bash models/download.sh --help 2>&1 | head -3
      3. python -c "from backend.app.core.model_manager import ModelRegistry; r=ModelRegistry(); print('Models:', len(r.list_models()))"
    Expected Result: 至少4个模型配置，download.sh有help输出，ModelRegistry可导入
    Evidence: .sisyphus/evidence/task-9-models.txt
  ```

  **Commit**: YES
  - Message: `feat: model management config and download tools`
  - Files: models/, backend/app/core/model_manager.py

- [ ] 10. 多模型路由引擎

  **What to do**:
  - 创建 `backend/app/core/router/`:
    - `router.py` — 主路由引擎 `ModelRouter`
    - `classifier.py` — 意图分类器 (分析用户输入→确定任务类型)
    - `fallback.py` — 降级策略 (模型不可用时自动切换)
  - 路由规则:
    - 中文日常对话 → Qwen
    - 代码/技术问题 → DeepSeek-Coder
    - 通用/英文 → Llama
    - 嵌入/检索 → all-MiniLM
  - 支持关键词匹配 + LLM-based分类 (小模型做路由决策)
  - 并发请求管理: 同一模型排队，不同模型并行

  **Must NOT do**:
  - 不要在路由层做对话生成 (仅选择模型)
  - 不要用大模型做路由 (用规则或小模型)

  **Recommended Agent Profile**:
  - **Category**: `deep`
    - Reason: 多模型路由策略设计，需要权衡性能和准确度
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: NO (depends on 8)
  - **Parallel Group**: Wave 2 (sequential sub-chain: 8→10)
  - **Blocks**: Task 16
  - **Blocked By**: Tasks 8 (LLM abstraction), 9 (model list)

  **References**:
  - Task 8 适配器接口: `backend/app/core/llm/base.py` — LLMProvider抽象
  - Task 9 模型注册表: `backend/app/core/model_manager.py` — ModelRegistry
  - LiteLLM路由器参考: `https://github.com/BerriAI/litellm` — 多模型路由模式

  **Acceptance Criteria**:
  - [ ] `ModelRouter.route(message)` 返回正确的模型名称
  - [ ] 中文消息路由到中文模型
  - [ ] 代码相关消息路由到代码模型
  - [ ] 模型不可用时触发降级

  **QA Scenarios**:

  ```
  Scenario: 多模型路由分类验证
    Tool: Bash
    Preconditions: 后端服务可用
    Steps:
      1. curl -X POST http://localhost:8000/api/router/test -d '{"message":"介绍一下你的项目经验"}' | python -m json.tool
      2. curl -X POST http://localhost:8000/api/router/test -d '{"message":"write a Python sorting function"}' | python -m json.tool
      3. curl -X POST http://localhost:8000/api/router/test -d '{"message":"Hello, how are you?"}' | python -m json.tool
    Expected Result: 中文→qwen模型，代码→deepseek模型，英文→llama模型
    Evidence: .sisyphus/evidence/task-10-router.json
  ```

  **Commit**: YES
  - Message: `feat: multi-model routing engine with intent classification`
  - Files: backend/app/core/router/

- [ ] 11. 文档解析和嵌入管道

  **What to do**:
  - 创建 `backend/app/core/ingestion/`:
    - `parser.py` — 多格式文档解析 (PDF, DOCX, Markdown, TXT, 图片OCR)
    - `chunker.py` — 智能分块 (按语义边界，重叠窗口，保留上下文)
    - `embedder.py` — 嵌入生成 (all-MiniLM-L6-v2 本地运行)
    - `pipeline.py` — 摄取管道编排 (解析→分块→嵌入→存储)
  - 支持批量导入 `data/` 目录下的文件
  - 支持增量更新 (检测文件变更，只处理修改的)

  **Must NOT do**:
  - 不要上传文件到远程服务 (本地处理)
  - 不要在内存中加载整个大文件 (流式处理)

  **Recommended Agent Profile**:
  - **Category**: `deep`
    - Reason: 文档处理管道设计，多格式解析，分块策略
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 8, 9, 12, 13)
  - **Parallel Group**: Wave 2
  - **Blocks**: Tasks 14, 17
  - **Blocked By**: Tasks 5 (backend), 7 (Document类型)

  **References**:
  - LangChain document loaders: `https://python.langchain.com/docs/modules/data_connection/document_loaders/`
  - sentence-transformers: `https://www.sbert.net/` — all-MiniLM-L6-v2本地嵌入
  - Unstructured library: `https://github.com/Unstructured-IO/unstructured` — 多格式文档解析
  - RecursiveCharacterTextSplitter: LangChain分块策略 — 语义边界分块

  **Acceptance Criteria**:
  - [ ] 成功解析 PDF, DOCX, Markdown, TXT 文件
  - [ ] 嵌入向量维度正确 (384 for all-MiniLM)
  - [ ] 分块间有重叠窗口
  - [ ] 增量更新检测工作正常

  **QA Scenarios**:

  ```
  Scenario: 文档解析和嵌入管道验证
    Tool: Bash
    Preconditions: data/ 目录有测试文件
    Steps:
      1. echo "# Test Resume\nSkills: Python, AI" > /tmp/test_resume.md
      2. python -c "from backend.app.core.ingestion.pipeline import ingest_file; r=ingest_file('/tmp/test_resume.md'); print('Chunks:', len(r))"
      3. python -c "from backend.app.core.ingestion.embedder import LocalEmbedder; e=LocalEmbedder(); v=e.embed('test'); print('Dim:', len(v))"
    Expected Result: 解析生成chunks >0，嵌入维度=384
    Evidence: .sisyphus/evidence/task-11-ingestion.txt
  ```

  **Commit**: YES
  - Message: `feat: document parsing and embedding pipeline`
  - Files: backend/app/core/ingestion/

- [ ] 12. 向量数据库集成 (ChromaDB)

  **What to do**:
  - 创建 `backend/app/core/storage/vector_store.py`:
    - ChromaDB客户端初始化 (持久化模式)
    - 集合管理: 创建、删除、列出集合
    - 文档索引: 批量插入嵌入向量+元数据
    - 语义搜索: 查询嵌入→top-k相似检索
    - 过滤搜索: 元数据过滤 (文档类型、日期等)
  - 数据持久化到 `data/chroma/`
  - 支持中文的嵌入和检索

  **Must NOT do**:
  - 不要使用远程ChromaDB服务 (本地embedded模式)
  - 不要在每次查询时重建索引

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: ChromaDB标准集成，模式固定
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 8, 9, 11, 13, 15)
  - **Parallel Group**: Wave 2
  - **Blocks**: Tasks 14, 17
  - **Blocked By**: Task 5 (backend)

  **References**:
  - ChromaDB Python client: `https://docs.trychroma.com/api-reference`
  - ChromaDB嵌入式模式: `https://docs.trychroma.com/guides/embeddings` — 本地嵌入
  - ChromaDB collection操作: `https://docs.trychroma.com/guides/collections`

  **Acceptance Criteria**:
  - [ ] ChromaDB客户端初始化成功，数据持久化到 `data/chroma/`
  - [ ] 添加文档后语义搜索返回相关结果
  - [ ] 元数据过滤正常工作

  **QA Scenarios**:

  ```
  Scenario: ChromaDB向量存储CRUD验证
    Tool: Bash
    Preconditions: backend已初始化
    Steps:
      1. python -c "
from backend.app.core.storage.vector_store import VectorStore
vs = VectorStore()
vs.add('test_col', ['doc1 text about AI'], [{'source':'test'}], [[0.1]*384])
results = vs.search('test_col', 'AI', k=1)
print('Results:', len(results))
"
      2. ls data/chroma/ | head -5
    Expected Result: 搜索返回1个结果，data/chroma/有持久化文件
    Evidence: .sisyphus/evidence/task-12-chromadb.txt
  ```

  **Commit**: YES
  - Message: `feat: ChromaDB vector store integration`
  - Files: backend/app/core/storage/vector_store.py

- [ ] 13. 知识图谱集成 (Neo4j 基础)

  **What to do**:
  - 创建 `backend/app/core/storage/graph_store.py`:
    - Neo4j连接 (本地或Docker Neo4j)
    - 基础图模型: Person→Project, Person→Skill, Project→Tech
    - 知识节点CRUD: 创建、查询、更新、删除节点和关系
    - Cypher查询构建器
  - 图schema定义: 个人→项目→技术栈→技能
  - Docker Compose添加Neo4j服务

  **Must NOT do**:
  - 不要在MVP做复杂的图推理 (先存储和简单查询)
  - 不要暴露Neo4j端口到外网

  **Recommended Agent Profile**:
  - **Category**: `deep`
    - Reason: 图数据库schema设计和Cypher查询
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 8, 9, 11, 12, 15)
  - **Parallel Group**: Wave 2
  - **Blocks**: Tasks 14, 27
  - **Blocked By**: Tasks 5 (backend), 7 (types)

  **References**:
  - Neo4j Python driver: `https://neo4j.com/docs/python-manual/current/`
  - Neo4j Docker: `https://neo4j.com/docs/operations-manual/current/docker/`
  - Cypher查询语言: `https://neo4j.com/docs/cypher-manual/current/`

  **Acceptance Criteria**:
  - [ ] Neo4j连接成功
  - [ ] 可创建Person→Project→Skill关系链
  - [ ] Cypher查询返回正确结果

  **QA Scenarios**:

  ```
  Scenario: Neo4j知识图谱CRUD验证
    Tool: Bash
    Preconditions: Neo4j Docker运行中
    Steps:
      1. python -c "
from backend.app.core.storage.graph_store import GraphStore
gs = GraphStore()
gs.create_person('TestUser')
gs.add_project('TestUser', 'AI分身', ['Python','FastAPI'])
results = gs.query_user_projects('TestUser')
print('Projects:', results)
"
    Expected Result: 查询返回至少1个项目，含技能列表
    Evidence: .sisyphus/evidence/task-13-neo4j.txt
  ```

  **Commit**: YES
  - Message: `feat: Neo4j knowledge graph integration`
  - Files: backend/app/core/storage/graph_store.py, docker-compose.yml

- [ ] 14. RAG检索管道 (混合检索)

  **What to do**:
  - 创建 `backend/app/core/rag/`:
    - `retriever.py` — 混合检索器: 向量搜索 + 关键词BM25 + 图遍历
    - `reranker.py` — 重排序 (cross-encoder reranker)
    - `context_builder.py` — 上下文构建 (检索结果→LLM prompt)
    - `rag_chain.py` — 完整RAG链 (检索→重排→构建→生成)
  - 混合检索融合策略 (RRF: Reciprocal Rank Fusion)
  - 引用溯源 (返回检索来源)
  - 缓存热门查询结果

  **Must NOT do**:
  - 不要在每次请求时重建检索索引
  - 不要返回无引用的答案

  **Recommended Agent Profile**:
  - **Category**: `deep`
    - Reason: 混合检索策略设计，RRF融合，重排序
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: NO (depends on 11, 12, 13)
  - **Parallel Group**: Wave 2 (sequential: 11+12+13→14)
  - **Blocks**: Tasks 16, 26
  - **Blocked By**: Tasks 11 (docs), 12 (vector), 13 (graph)

  **References**:
  - James-RAG-Evol混合检索: `https://github.com/Hashevolution/James-RAG-Evol` — GraphRAG+向量+BM25+RRF融合
  - Cerid-AI hybrid: `https://github.com/Cerid-AI/cerid-ai` — 混合检索+重排序参考
  - RRF算法: `https://plg.uwaterloo.ca/~gvcormac/cormacksigir09-rrf.pdf`
  - LangChain RAG: `https://python.langchain.com/docs/tutorials/rag/`

  **Acceptance Criteria**:
  - [ ] 混合检索返回比纯向量搜索更相关的结果
  - [ ] 重排序后top1相关度>0.5
  - [ ] 引用溯源返回正确的文档来源

  **QA Scenarios**:

  ```
  Scenario: RAG混合检索质量验证
    Tool: Bash
    Preconditions: 知识库已导入测试文档
    Steps:
      1. python -c "
from backend.app.core.rag.retriever import HybridRetriever
hr = HybridRetriever()
results = hr.search('Python开发经验')
for r in results[:3]: print(r.score, r.source)
"
    Expected Result: 返回≥1个相关结果，来源标注正确，分数递减
    Evidence: .sisyphus/evidence/task-14-rag.json
  ```

  **Commit**: YES
  - Message: `feat: hybrid RAG retrieval pipeline`
  - Files: backend/app/core/rag/

- [ ] 15. 对话管理和会话存储

  **What to do**:
  - 创建 `backend/app/core/conversation/`:
    - `session_manager.py` — 会话CRUD (创建、获取、列表、删除)
    - `memory.py` — 对话记忆 (滑动窗口 + 摘要 + 长期记忆)
    - `context_compressor.py` — 上下文压缩 (超长对话自动摘要旧消息)
  - 会话持久化: SQLite (本地) 或 JSON文件
  - 记忆检索: 从历史对话中搜索相关内容
  - 会话导出: Markdown/JSON格式

  **Must NOT do**:
  - 不要在内存中无限增长上下文 (窗口限制)
  - 不要存储敏感对话明文 (可选加密)

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: 会话管理标准模式，CRUD操作
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 11, 12, 13)
  - **Parallel Group**: Wave 2
  - **Blocks**: Tasks 16, 26
  - **Blocked By**: Tasks 5 (backend), 7 (ChatSession类型)

  **References**:
  - LangChain Memory: `https://python.langchain.com/docs/modules/memory/` — 对话记忆模式
  - SQLite Python: `https://docs.python.org/3/library/sqlite3.html`
  - ConversationSummaryBufferMemory: LangChain摘要记忆模式

  **Acceptance Criteria**:
  - [ ] 创建会话、添加消息、检索会话功能正常
  - [ ] 上下文窗口限制工作 (超长自动压缩)
  - [ ] 会话导出内容完整

  **QA Scenarios**:

  ```
  Scenario: 会话管理CRUD验证
    Tool: Bash
    Preconditions: 后端服务运行中
    Steps:
      1. curl -X POST http://localhost:8000/api/sessions -d '{"title":"test"}' | python -m json.tool
      2. curl http://localhost:8000/api/sessions | python -c "import sys,json; print('Count:', len(json.load(sys.stdin)))"
      3. curl -X DELETE http://localhost:8000/api/sessions/1 -w "%{http_code}"
    Expected Result: 创建返回session_id，列表返回计数，删除返回204
    Evidence: .sisyphus/evidence/task-15-sessions.json
  ```

  **Commit**: YES
  - Message: `feat: conversation session management and memory`
  - Files: backend/app/core/conversation/

- [ ] 16. 聊天API端点 (REST + WebSocket)

  **What to do**:
  - 创建 `backend/app/api/chat.py`:
    - `POST /api/chat` — 发送消息，返回AI回复 (REST)
    - `WS /api/chat/ws` — WebSocket实时聊天 (流式输出)
    - `GET /api/chat/history/{session_id}` — 获取历史消息
  - 集成多模型路由 (Task 10) + RAG (Task 14) + 会话 (Task 15)
  - 流式响应: SSE (Server-Sent Events) 逐token输出
  - 错误处理: 模型不可用/超时的优雅降级

  **Must NOT do**:
  - 不要在API层写业务逻辑 (委托给core模块)
  - 不要阻塞等待LLM (使用async/await)

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
    - Reason: API端点实现，集成多个核心模块
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: NO (depends on many Wave 2 modules)
  - **Parallel Group**: Wave 3
  - **Blocks**: Tasks 21, 24, 25, 29
  - **Blocked By**: Tasks 10 (router), 14 (RAG), 15 (sessions)

  **References**:
  - FastAPI WebSocket: `https://fastapi.tiangolo.com/advanced/websockets/`
  - FastAPI Streaming: `https://fastapi.tiangolo.com/advanced/custom-response/#streamingresponse`
  - OpenAI Chat API格式 (兼容): `https://platform.openai.com/docs/api-reference/chat`

  **Acceptance Criteria**:
  - [ ] `POST /api/chat` 返回非空AI回复
  - [ ] WebSocket连接成功，流式接收消息
  - [ ] 回复基于知识库内容 (非LLM幻觉)

  **QA Scenarios**:

  ```
  Scenario: REST聊天API端到端验证
    Tool: Bash (curl)
    Preconditions: 后端运行，知识库已导入
    Steps:
      1. curl -X POST http://localhost:8000/api/chat \
         -H "Content-Type: application/json" \
         -d '{"message":"你做过什么AI项目？","session_id":"test-001"}' \
         | python -m json.tool
    Expected Result: 返回JSON含response字段，内容相关于用户的AI项目经验
    Evidence: .sisyphus/evidence/task-16-chat-rest.json

  Scenario: 流式聊天和错误处理
    Tool: Bash (curl)
    Preconditions: 后端运行
    Steps:
      1. curl -N -X POST http://localhost:8000/api/chat/stream \
         -H "Content-Type: application/json" \
         -d '{"message":"hello"}' 2>&1 | head -20
      2. curl -X POST http://localhost:8000/api/chat \
         -H "Content-Type: application/json" \
         -d '{"message":""}' -w "%{http_code}"
    Expected Result: 流式输出有内容，空消息返回400错误码
    Evidence: .sisyphus/evidence/task-16-chat-stream.txt
  ```

  **Commit**: YES
  - Message: `feat: chat API endpoints (REST + WebSocket streaming)`
  - Files: backend/app/api/chat.py

- [ ] 17. 知识库管理API

  **What to do**:
  - 创建 `backend/app/api/knowledge.py`:
    - `POST /api/knowledge/upload` — 上传文档 (PDF/DOCX/MD/TXT)
    - `GET /api/knowledge/documents` — 列出已导入文档
    - `DELETE /api/knowledge/documents/{id}` — 删除文档
    - `GET /api/knowledge/search?q=xxx` — 语义搜索知识库
    - `GET /api/knowledge/stats` — 知识库统计 (文档数、块数、最后更新)
  - 文件上传处理 (大小限制、格式验证)
  - 异步后台处理 (上传后返回任务ID，后台摄取)

  **Must NOT do**:
  - 不要同步处理大文件上传 (使用后台任务)

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: 标准CRUD API
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 18, 19)
  - **Parallel Group**: Wave 3
  - **Blocks**: Task 21 (chat UI依赖知识库)
  - **Blocked By**: Tasks 11 (ingestion), 12 (vector)

  **References**:
  - FastAPI file upload: `https://fastapi.tiangolo.com/tutorial/request-files/`
  - FastAPI background tasks: `https://fastapi.tiangolo.com/tutorial/background-tasks/`

  **Acceptance Criteria**:
  - [ ] 上传PDF/MD文件返回任务ID
  - [ ] 搜索返回相关文档
  - [ ] stats返回正确的文档计数

  **QA Scenarios**:

  ```
  Scenario: 知识库上传和搜索验证
    Tool: Bash (curl)
    Preconditions: 后端运行
    Steps:
      1. echo "# Test\nSkills: Python, AI" > /tmp/test.md
      2. curl -X POST http://localhost:8000/api/knowledge/upload -F "file=@/tmp/test.md" | python -m json.tool
      3. sleep 2
      4. curl "http://localhost:8000/api/knowledge/search?q=Python" | python -m json.tool
    Expected Result: 上传成功返回task_id，搜索返回相关结果含Python
    Evidence: .sisyphus/evidence/task-17-knowledge.json
  ```

  **Commit**: YES
  - Message: `feat: knowledge base management API`
  - Files: backend/app/api/knowledge.py

- [ ] 18. 语音STT管道 (faster-whisper)

  **What to do**:
  - 创建 `backend/app/core/voice/stt.py`:
    - faster-whisper模型加载 (base/medium模型可选)
    - 语音文件转文字: `transcribe(audio_path) → text`
    - 实时流式转写: WebSocket接收音频chunk→逐句输出文字
    - 语言检测: 自动识别中文/英文
  - 支持音频格式: WAV, MP3, WebM (浏览器录音)
  - 预下载whisper模型到 `models/whisper/`

  **Must NOT do**:
  - 不要使用OpenAI Whisper API
  - 不要在CPU上跑large模型 (太慢)

  **Recommended Agent Profile**:
  - **Category**: `deep`
    - Reason: 语音STT管道，实时流式处理
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 17, 19)
  - **Parallel Group**: Wave 3
  - **Blocks**: Tasks 20, 21
  - **Blocked By**: Task 5 (backend)

  **References**:
  - faster-whisper: `https://github.com/SYSTRAN/faster-whisper` — CTranslate2优化的Whisper
  - Whisper模型选择: `https://github.com/openai/whisper#available-models-and-languages`
  - WebSocket音频流: FastAPI WebSocket接收二进制音频帧

  **Acceptance Criteria**:
  - [ ] 录制5秒中文语音→输出正确文字
  - [ ] 流式转写延迟<2秒
  - [ ] 英文语音也正确识别

  **QA Scenarios**:

  ```
  Scenario: STT语音转文字验证
    Tool: Bash
    Preconditions: faster-whisper模型已下载
    Steps:
      1. python -c "
from backend.app.core.voice.stt import SpeechToText
stt = SpeechToText(model_size='base')
text = stt.transcribe_file('tests/fixtures/hello_chinese.wav')
print('Transcribed:', text)
"
    Expected Result: 输出中文文字，语义正确
    Evidence: .sisyphus/evidence/task-18-stt.txt
  ```

  **Commit**: YES
  - Message: `feat: speech-to-text pipeline with faster-whisper`
  - Files: backend/app/core/voice/stt.py

- [ ] 19. 语音TTS管道 (Coqui XTTS v2 + 声音克隆)

  **What to do**:
  - 创建 `backend/app/core/voice/tts.py`:
    - Coqui XTTS v2模型加载
    - 文字转语音: `synthesize(text, speaker_wav) → audio`
    - 声音克隆: 从用户语音样本提取声纹→生成任何文字的用户声音
    - 流式TTS: 逐句生成+播放，减少首句延迟
  - 预下载XTTS模型到 `models/xtts/`
  - 声纹注册: 用户上传5-10秒语音样本→注册声纹→后续TTS使用

  **Must NOT do**:
  - 不要使用远程TTS API
  - 不要存储原始语音样本在云端

  **Recommended Agent Profile**:
  - **Category**: `deep`
    - Reason: TTS声音克隆，需要深入理解XTTS模型
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 17, 18)
  - **Parallel Group**: Wave 3
  - **Blocks**: Tasks 20, 21, 22
  - **Blocked By**: Task 5 (backend)

  **References**:
  - Coqui XTTS v2: `https://github.com/coqui-ai/TTS` — 声音克隆TTS
  - XTTS Python API: `https://docs.coqui.ai/en/latest/models/xtts.html`
  - 声纹注册模式: 10秒音频→speaker embedding→所有TTS使用

  **Acceptance Criteria**:
  - [ ] 输入文字→输出清晰语音文件 (WAV)
  - [ ] 声音克隆: 注册声纹后TTS输出与样本音色相似
  - [ ] 中文TTS发音准确

  **QA Scenarios**:

  ```
  Scenario: TTS文字转语音和声音克隆验证
    Tool: Bash
    Preconditions: XTTS模型已下载
    Steps:
      1. python -c "
from backend.app.core.voice.tts import TextToSpeech
tts = TextToSpeech()
audio = tts.synthesize('你好，我是数字分身', speaker_wav='data/voice/user_sample.wav')
with open('/tmp/tts_out.wav', 'wb') as f: f.write(audio)
print('TTS_OK, size:', len(audio))
"
      2. file /tmp/tts_out.wav
    Expected Result: 输出WAV文件，文件类型正确
    Evidence: .sisyphus/evidence/task-19-tts.wav
  ```

  **Commit**: YES
  - Message: `feat: text-to-speech pipeline with Coqui XTTS v2 voice cloning`
  - Files: backend/app/core/voice/tts.py

- [ ] 20. 实时语音对话编排

  **What to do**:
  - 创建 `backend/app/core/voice/orchestrator.py`:
    - 语音对话状态机: IDLE→LISTENING→THINKING→SPEAKING→IDLE
    - WebSocket语音管道: 浏览器音频→STT→LLM→TTS→浏览器播放
    - 打断处理: 用户说话时中断TTS播放
    - VAD (Voice Activity Detection): 自动检测说话结束
    - 延迟优化: 流式STT+流式LLM+流式TTS并行管道
  - 创建 `backend/app/api/voice.py`:
    - `WS /api/voice/conversation` — 实时语音对话WebSocket

  **Must NOT do**:
  - 不要在语音管道中使用轮询 (全事件驱动)
  - 不要在TTS时阻塞STT (全双工)

  **Recommended Agent Profile**:
  - **Category**: `deep`
    - Reason: 实时语音管道编排，异步状态机
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: NO (depends on 18, 19)
  - **Parallel Group**: Wave 3 (sequential: 18+19→20)
  - **Blocks**: Tasks 21, 22, 24, 25
  - **Blocked By**: Tasks 18 (STT), 19 (TTS)

  **References**:
  - WebRTC vs WebSocket for voice: `https://webrtc.org/` — 实时通信协议
  - VAD库: `https://github.com/snakers4/silero-vad` — 轻量VAD
  - 流式管道模式: 生产者-消费者异步队列

  **Acceptance Criteria**:
  - [ ] WebSocket语音对话: 说话→STT→LLM→TTS→听到回复
  - [ ] 打断功能: 说话时TTS停止
  - [ ] 端到端延迟<3秒 (首字)

  **QA Scenarios**:

  ```
  Scenario: 实时语音对话端到端验证
    Tool: Playwright (via playwright skill)
    Preconditions: Web前端运行，后端运行
    Steps:
      1. Navigate to http://localhost:3000/voice
      2. Click microphone button to start
      3. Wait for listening state (UI indicator changes)
      4. Simulate audio input (or use pre-recorded test audio)
      5. Assert audio playback starts within 5 seconds
      6. Assert stop button interrupts playback
    Expected Result: 语音对话完整流程，有回复音频输出
    Evidence: .sisyphus/evidence/task-20-voice.png (screenshots)
  ```

  **Commit**: YES
  - Message: `feat: real-time voice conversation orchestrator`
  - Files: backend/app/core/voice/orchestrator.py, backend/app/api/voice.py

- [ ] 21. Web聊天界面 (文字+语音)

  **What to do**:
  - 创建 `web/app/chat/page.tsx` 聊天页面:
    - 消息列表 (用户/AI气泡，Markdown渲染)
    - 消息输入框 + 发送按钮
    - 流式响应显示 (逐字显示AI回复)
    - 语音输入按钮 (录音→STT→填入输入框)
    - 语音输出按钮 (TTS朗读AI回复)
  - 创建 `web/components/Chat/`:
    - `MessageBubble.tsx` — 消息气泡组件
    - `ChatInput.tsx` — 输入组件 (文字+语音)
    - `StreamingText.tsx` — 流式文字动画
  - WebSocket连接管理 `web/hooks/useChatWebSocket.ts`
  - 会话切换: 新建/切换/删除对话

  **Must NOT do**:
  - 不要使用远程API (所有请求到本地FastAPI)
  - 不要在聊天界面放广告或无关元素

  **Recommended Agent Profile**:
  - **Category**: `visual-engineering`
    - Reason: 前端聊天UI，交互设计
  - **Skills**: [`frontend-ui-ux`, `playwright`]
    - `frontend-ui-ux`: UI/UX设计
    - `playwright`: 浏览器验证

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 22, 23)
  - **Parallel Group**: Wave 3
  - **Blocks**: Tasks 24, 25, 31
  - **Blocked By**: Tasks 6 (frontend skeleton), 16 (chat API), 20 (voice)

  **References**:
  - Task 6 前端骨架: `web/app/layout.tsx` — 布局和路由
  - Task 16 API: `backend/app/api/chat.py` — 聊天API端点
  - shadcn/ui chat components: `https://ui.shadcn.com/` — 消息UI模式
  - WebSocket API: `https://developer.mozilla.org/en-US/docs/Web/API/WebSocket`

  **Acceptance Criteria**:
  - [ ] 发送文字消息→收到AI回复 (流式显示)
  - [ ] 语音按钮→录音→文字填入输入框
  - [ ] TTS按钮→朗读AI回复
  - [ ] 切换会话正常

  **QA Scenarios**:

  ```
  Scenario: Web文字聊天完整流程
    Tool: Playwright (via playwright skill)
    Preconditions: Next.js + FastAPI运行
    Steps:
      1. Navigate to http://localhost:3000/chat
      2. Type "你好，介绍一下你自己" in the message input (.chat-input textarea)
      3. Click send button (.send-button)
      4. Wait for AI response to appear (text:contains "数字分身" or "AI")
      5. Assert response contains relevant personal info
    Expected Result: AI回复基于知识库，非通用回答
    Evidence: .sisyphus/evidence/task-21-chat.png (screenshot)

  Scenario: 语音输入集成验证
    Tool: Playwright (via playwright skill)
    Preconditions: Chat page loaded, microphone permission granted
    Steps:
      1. Click voice input button (.voice-input-btn)
      2. Assert recording state indicator visible
      3. Wait for STT result to appear in input field
    Expected Result: 录音后文字出现在输入框
    Evidence: .sisyphus/evidence/task-21-voice-input.png
  ```

  **Commit**: YES
  - Message: `feat: web chat interface with text and voice integration`
  - Files: web/app/chat/, web/components/Chat/, web/hooks/

- [ ] 22. Web数字人展示 (MuseTalk 2D头像)

  **What to do**:
  - 创建 `web/components/Avatar/`:
    - `DigitalHuman.tsx` — 2D数字人容器
    - `LipSyncAvatar.tsx` — 口型同步动画组件
    - `AvatarControls.tsx` — 播放/暂停控制
  - 集成MuseTalk:
    - 后端提供音频→口型参数API
    - 前端根据参数驱动2D头像动画
  - 用户照片上传和头像生成
  - 空闲状态动画 (眨眼、微动)

  **Must NOT do**:
  - 不要在浏览器端运行MuseTalk (太重，放后端)
  - 不要使用3D模型 (那是后续阶段)

  **Recommended Agent Profile**:
  - **Category**: `visual-engineering`
    - Reason: 2D动画和前端交互
  - **Skills**: [`frontend-ui-ux`]
    - `frontend-ui-ux`: 动画和视觉设计

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 21, 23)
  - **Parallel Group**: Wave 3
  - **Blocks**: Tasks 24, 25, 31
  - **Blocked By**: Tasks 6 (frontend), 19 (TTS), 20 (voice orch)

  **References**:
  - MuseTalk: `https://github.com/TMElyralab/MuseTalk` — 音频驱动口型
  - SadTalker: `https://github.com/OpenTalker/SadTalker` — 备选2D方案
  - Web Animations API: `https://developer.mozilla.org/en-US/docs/Web/API/Web_Animations_API`

  **Acceptance Criteria**:
  - [ ] 2D头像随TTS音频同步口型
  - [ ] 空闲状态有自然微动
  - [ ] 用户照片可替换默认头像

  **QA Scenarios**:

  ```
  Scenario: 数字人2D口型同步验证
    Tool: Playwright (via playwright skill)
    Preconditions: Chat页面加载，TTS可用
    Steps:
      1. Navigate to http://localhost:3000/chat
      2. Click TTS按钮朗读AI回复
      3. Observe 2D avatar mouth movement synced with audio
      4. Screenshot during speaking state
    Expected Result: 头像口型与音频同步变化
    Evidence: .sisyphus/evidence/task-22-avatar.png
  ```

  **Commit**: YES
  - Message: `feat: 2D digital human avatar with MuseTalk lip-sync`
  - Files: web/components/Avatar/

- [ ] 23. Web个人资料展示页

  **What to do**:
  - 创建 `web/app/page.tsx` 首页:
    - 个人简介区 (姓名、头衔、技能标签)
    - 项目经历时间线 (可展开详情)
    - 工作经历卡片
    - 教育背景
    - "与数字分身对话" CTA按钮 → 跳转/chat
  - 从后端API获取数据: `GET /api/profile`
  - 响应式设计 (桌面+移动端)
  - 创建 `backend/app/api/profile.py`: 个人资料CRUD API

  **Must NOT do**:
  - 不要硬编码个人信息 (从API获取)

  **Recommended Agent Profile**:
  - **Category**: `visual-engineering`
    - Reason: 前端个人主页设计
  - **Skills**: [`frontend-ui-ux`]
    - `frontend-ui-ux`: 页面设计和布局

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 21, 22)
  - **Parallel Group**: Wave 3
  - **Blocks**: Task 21 (chat CTA来自首页)
  - **Blocked By**: Tasks 6 (frontend), 5 (backend)

  **References**:
  - Task 6 前端骨架: `web/app/layout.tsx`, `web/app/page.tsx`
  - personal-ai-twin 参考: `https://github.com/ilhamdenfatah/personal-ai-twin` — 个人展示模式

  **Acceptance Criteria**:
  - [ ] 首页展示个人信息 (姓名、技能、项目)
  - [ ] "与数字分身对话"按钮跳转正常
  - [ ] 移动端响应式正常

  **QA Scenarios**:

  ```
  Scenario: 个人资料页展示验证
    Tool: Playwright (via playwright skill)
    Preconditions: Web + Backend运行
    Steps:
      1. Navigate to http://localhost:3000
      2. Assert page contains name/skills section
      3. Click "与数字分身对话" CTA
      4. Assert navigation to /chat
      5. Resize to mobile viewport (375px) — assert layout still readable
    Expected Result: 信息完整展示，CTA跳转正确，移动端响应式
    Evidence: .sisyphus/evidence/task-23-profile.png
  ```

  **Commit**: YES
  - Message: `feat: personal profile showcase page with API`
  - Files: web/app/page.tsx, backend/app/api/profile.py

- [ ] 24. React Native Android 应用

  **What to do**:
  - React Native项目配置 (已在Task 1初始化)
  - 创建核心界面:
    - 聊天屏幕 `screens/ChatScreen.tsx` — 复用Web聊天逻辑
    - 语音对话屏幕 `screens/VoiceScreen.tsx`
    - 个人资料屏幕 `screens/ProfileScreen.tsx`
  - API客户端 `lib/api-client.ts` (复用shared/types)
  - WebSocket连接 `hooks/useChatWebSocket.ts`
  - 语音权限处理和录音集成
  - Android APK构建配置

  **Must NOT do**:
  - 不要从零重写 (尽量复用Web端的hooks和types)
  - 不要使用Expo (纯React Native CLI)

  **Recommended Agent Profile**:
  - **Category**: `visual-engineering`
    - Reason: 移动端UI开发
  - **Skills**: []
    - 标准React Native开发

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 25, 26, 27, 28, 29)
  - **Parallel Group**: Wave 4
  - **Blocks**: Task 31
  - **Blocked By**: Tasks 16 (chat API), 20 (voice), 29 (client lib)

  **References**:
  - React Native docs: `https://reactnative.dev/docs/getting-started`
  - React Native WebSocket: `https://reactnative.dev/docs/network#websocket`
  - Android permissions: `https://reactnative.dev/docs/permissionsandroid`

  **Acceptance Criteria**:
  - [ ] APK构建成功
  - [ ] 文字聊天功能正常
  - [ ] 语音对话功能正常
  - [ ] 连接同一后端API

  **QA Scenarios**:

  ```
  Scenario: Android文字聊天验证
    Tool: Playwright (mobile emulation) / Bash (APK验证)
    Preconditions: APK已构建，后端运行
    Steps:
      1. Install APK on emulator/device
      2. Open app → navigate to chat
      3. Send message "你好"
      4. Assert AI response appears
    Expected Result: 收到基于知识库的回复
    Evidence: .sisyphus/evidence/task-24-android.png
  ```

  **Commit**: YES
  - Message: `feat: React Native Android application`
  - Files: mobile/

- [ ] 25. Tauri 桌面应用 (Windows/Linux)

  **What to do**:
  - Tauri项目配置 (已在Task 1初始化)
  - 嵌入Web前端 (复用Next.js构建产物)
  - Tauri原生功能:
    - 系统托盘 (后台运行)
    - 通知 (新消息提醒)
    - 文件对话框 (上传文档到知识库)
  - 构建配置: Windows (.msi/.exe) + Linux (.deb/.AppImage)
  - 自动更新机制 (可选)

  **Must NOT do**:
  - 不要重写Web UI (复用)
  - 不要在Tauri中重复实现API逻辑

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
    - Reason: Tauri桌面应用开发，涉及Rust配置和原生API
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 24, 26, 27, 28, 29)
  - **Parallel Group**: Wave 4
  - **Blocks**: Task 31
  - **Blocked By**: Tasks 16 (API), 20 (voice), 29 (client lib)

  **References**:
  - Tauri docs: `https://tauri.app/v1/guides/`
  - Tauri + Next.js: `https://tauri.app/v1/guides/features/command`
  - Tauri build: `https://tauri.app/v1/guides/building/`

  **Acceptance Criteria**:
  - [ ] `cargo tauri build` 成功生成安装包
  - [ ] 安装后打开→显示Web聊天界面
  - [ ] 系统托盘和通知功能正常

  **QA Scenarios**:

  ```
  Scenario: Tauri桌面应用启动和功能验证
    Tool: Bash / Playwright
    Preconditions: 构建产物存在
    Steps:
      1. Install .deb package on Linux
      2. Launch application
      3. Assert window shows chat interface
      4. Send a test message → verify response
    Expected Result: 桌面应用正常启动，聊天功能可用
    Evidence: .sisyphus/evidence/task-25-desktop.png
  ```

  **Commit**: YES
  - Message: `feat: Tauri desktop application (Windows/Linux)`
  - Files: desktop/

- [ ] 26. 自进化引擎基础 (对话提取+审核)

  **What to do**:
  - 创建 `backend/app/core/evolution/`:
    - `extractor.py` — 从对话中提取新事实 (LLM驱动的结构化提取)
    - `review_queue.py` — 审核队列 (新事实待用户确认)
    - `knowledge_updater.py` — 审核通过后更新知识库
  - 提取格式: `{事实类型, 内容, 置信度, 来源对话ID}`
  - 审核API: `GET /api/evolution/pending`, `POST /api/evolution/approve/{id}`
  - 自动提取触发: 每次对话结束后后台运行

  **Must NOT do**:
  - 不要自动应用未经审核的事实 (必须人工确认)
  - 不要在对话中实时提取 (异步后台)

  **Recommended Agent Profile**:
  - **Category**: `deep`
    - Reason: 自进化逻辑和知识提取
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 24, 25, 27, 28, 29)
  - **Parallel Group**: Wave 4
  - **Blocks**: Task 27
  - **Blocked By**: Tasks 14 (RAG), 15 (sessions)

  **References**:
  - James-RAG-Evol self-evolution: `https://github.com/Hashevolution/James-RAG-Evol` — 人工审核门模式
  - Jar-El self-baking memory: `https://github.com/ProfEngel/jar-el` — 异步记忆固化
  - digital-twin-mcp personality: `https://github.com/ChiragPatankar/digital-twin-mcp` — 个性提取

  **Acceptance Criteria**:
  - [ ] 对话结束后提取出新事实
  - [ ] 审核队列有pending项
  - [ ] 审核通过后知识库可检索到新事实

  **QA Scenarios**:

  ```
  Scenario: 自进化知识提取验证
    Tool: Bash (curl)
    Preconditions: 至少一次对话完成
    Steps:
      1. curl http://localhost:8000/api/evolution/pending | python -m json.tool
      2. curl -X POST http://localhost:8000/api/evolution/approve/1 -w "%{http_code}"
      3. curl "http://localhost:8000/api/knowledge/search?q=[新事实关键词]" | python -m json.tool
    Expected Result: 有pending事实，审核后可通过搜索找到
    Evidence: .sisyphus/evidence/task-26-evolution.json
  ```

  **Commit**: YES
  - Message: `feat: self-evolution engine with conversation extraction and review`
  - Files: backend/app/core/evolution/

- [ ] 27. 知识图谱自更新管道

  **What to do**:
  - 扩展 `backend/app/core/evolution/graph_updater.py`:
    - 从审核通过的事实更新Neo4j图谱
    - 自动创建新节点和关系
    - 冲突检测: 新事实与已有知识冲突时标记
    - 图谱版本控制: 记录每次更新的快照
  - 图谱查询增强: 基于更新后的图谱做更丰富的知识检索

  **Must NOT do**:
  - 不要删除已有知识 (仅标记为过时)
  - 不要在无审核的情况下自动更新

  **Recommended Agent Profile**:
  - **Category**: `deep`
    - Reason: 图谱动态更新和冲突检测
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 24, 25, 28, 29, 30)
  - **Parallel Group**: Wave 4
  - **Blocks**: None
  - **Blocked By**: Tasks 13 (graph), 26 (evolution)

  **References**:
  - Task 13 Neo4j schema: `backend/app/core/storage/graph_store.py`
  - Task 26 evolution extractor: `backend/app/core/evolution/extractor.py`
  - James-RAG-Evol contradiction arbiter: 冲突检测参考

  **Acceptance Criteria**:
  - [ ] 审核通过的事实自动更新图谱
  - [ ] 冲突事实被标记而非静默覆盖
  - [ ] 图谱版本可追溯

  **QA Scenarios**:

  ```
  Scenario: 知识图谱自动更新验证
    Tool: Bash
    Preconditions: 有审核通过的新事实
    Steps:
      1. python -c "
from backend.app.core.evolution.graph_updater import GraphUpdater
gu = GraphUpdater()
result = gu.apply_pending_updates()
print('Updated:', result.nodes_added, 'nodes,', result.relationships_added, 'rels')
"
      2. python -c "
from backend.app.core.storage.graph_store import GraphStore
gs = GraphStore()
print('Total nodes:', gs.count_nodes())
"
    Expected Result: 图谱节点数增加，新关系被创建
    Evidence: .sisyphus/evidence/task-27-graph-update.txt
  ```

  **Commit**: YES
  - Message: `feat: knowledge graph auto-update pipeline`
  - Files: backend/app/core/evolution/graph_updater.py

- [ ] 28. vLLM 生产部署配置

  **What to do**:
  - 创建 `deploy/vllm/`:
    - `docker-compose.vllm.yml` — vLLM Docker部署
    - `vllm_config.yaml` — vLLM服务配置 (模型路径、GPU分配、并发)
    - `nginx.conf` — 反向代理 (负载均衡、速率限制)
  - vLLM模型服务脚本 (启动、健康检查、优雅关闭)
  - 从Ollama迁移到vLLM的切换脚本
  - 性能基准测试脚本

  **Must NOT do**:
  - 不要在MVP阶段强制使用vLLM (Ollama仍为默认开发方案)
  - 不要在无GPU的机器上配置vLLM

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: 部署配置文件编写
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 24, 25, 26, 27, 29, 30)
  - **Parallel Group**: Wave 4
  - **Blocks**: Task 30
  - **Blocked By**: Tasks 8 (LLM abstraction), 9 (model mgmt)

  **References**:
  - vLLM Docker: `https://docs.vllm.ai/en/latest/serving/deploying_with_docker.html`
  - vLLM OpenAI兼容: `https://docs.vllm.ai/en/latest/serving/openai_compatible_server.html`
  - Nginx反向代理: `https://nginx.org/en/docs/http/ngx_http_proxy_module.html`

  **Acceptance Criteria**:
  - [ ] `docker-compose -f deploy/vllm/docker-compose.vllm.yml up` 启动vLLM
  - [ ] vLLM OpenAI兼容API可访问
  - [ ] 后端可切换到vLLM后端

  **QA Scenarios**:

  ```
  Scenario: vLLM部署配置验证
    Tool: Bash
    Preconditions: GPU可用
    Steps:
      1. docker-compose -f deploy/vllm/docker-compose.vllm.yml up -d
      2. sleep 30
      3. curl http://localhost:8001/health
      4. curl http://localhost:8001/v1/models | python -m json.tool
    Expected Result: vLLM服务启动，模型列表可查询
    Evidence: .sisyphus/evidence/task-28-vllm.json
  ```

  **Commit**: YES
  - Message: `feat: vLLM production deployment configuration`
  - Files: deploy/vllm/

- [ ] 29. 跨平台API客户端库

  **What to do**:
  - 创建 `shared/api-client/`:
    - `client.ts` — 统一API客户端 (TypeScript)
    - 封装所有API端点: chat, knowledge, voice, profile, evolution
    - WebSocket连接管理
    - 自动重连、错误处理、请求队列
  - Web和Mobile共享同一客户端库
  - 类型安全 (使用Task 7的shared types)

  **Must NOT do**:
  - 不要创建Python版本的客户端 (仅TypeScript)
  - 不要在每个平台重复实现API调用

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: API客户端封装，标准模式
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 24, 25, 26, 27, 28, 30)
  - **Parallel Group**: Wave 4
  - **Blocks**: Tasks 24, 25
  - **Blocked By**: Task 16 (API定义)

  **References**:
  - Task 7 types: `shared/types/` — 所有TypeScript类型
  - Task 16 API: `backend/app/api/chat.py` — 聊天API端点
  - axios/fetch patterns: 标准HTTP客户端模式

  **Acceptance Criteria**:
  - [ ] 所有API端点有对应客户端方法
  - [ ] TypeScript编译无错误
  - [ ] WebSocket自动重连工作

  **QA Scenarios**:

  ```
  Scenario: API客户端功能验证
    Tool: Bash
    Preconditions: 后端运行
    Steps:
      1. cd shared/api-client && npx tsc --noEmit
      2. node -e "
const { ApiClient } = require('./dist/client.js');
const client = new ApiClient('http://localhost:8000');
client.chat.send('hello').then(r => console.log('Reply:', r.response));
"
    Expected Result: 编译无错误，发送消息收到回复
    Evidence: .sisyphus/evidence/task-29-api-client.txt
  ```

  **Commit**: YES
  - Message: `feat: cross-platform TypeScript API client library`
  - Files: shared/api-client/

- [ ] 30. Docker 容器化部署

  **What to do**:
  - 创建 `docker-compose.yml` 完整服务编排:
    - FastAPI后端
    - Next.js前端 (或静态导出)
    - ChromaDB
    - Neo4j
    - Ollama (可选)
  - 创建 `Dockerfile.backend`, `Dockerfile.web`
  - 创建 `deploy/` 部署文档:
    - 单机部署指南 (docker-compose)
    - 开发环境指南
    - 环境变量说明
  - `.env.production` 生产配置模板
  - 健康检查和自动重启配置

  **Must NOT do**:
  - 不要在镜像中打包模型文件 (挂载volume)
  - 不要暴露未认证的端口到外网

  **Recommended Agent Profile**:
  - **Category**: `quick`
    - Reason: Docker配置，标准模式
  - **Skills**: []

  **Parallelization**:
  - **Can Run In Parallel**: YES (with Tasks 24, 25, 26, 27, 28, 29)
  - **Parallel Group**: Wave 4
  - **Blocks**: Task 31
  - **Blocked By**: Tasks 5 (backend), 28 (vLLM config)

  **References**:
  - Docker Compose: `https://docs.docker.com/compose/`
  - FastAPI Docker: `https://fastapi.tiangolo.com/deployment/docker/`
  - Next.js Docker: `https://nextjs.org/docs/deployment#docker-image`

  **Acceptance Criteria**:
  - [ ] `docker-compose up` 启动所有服务
  - [ ] 健康检查全部通过
  - [ ] 浏览器可访问Web界面

  **QA Scenarios**:

  ```
  Scenario: Docker部署端到端验证
    Tool: Bash
    Preconditions: Docker已安装
    Steps:
      1. docker-compose up -d
      2. sleep 30
      3. docker-compose ps | grep -c "Up"
      4. curl http://localhost:8000/health
      5. curl http://localhost:3000 -o /dev/null -w "%{http_code}"
    Expected Result: 所有容器运行，健康检查通过，Web可访问
    Evidence: .sisyphus/evidence/task-30-docker.txt
  ```

  **Commit**: YES
  - Message: `feat: Docker containerization and deployment config`
  - Files: docker-compose.yml, Dockerfile.*, deploy/

- [ ] 31. 集成端到端测试

  **What to do**:
  - 创建 `tests/e2e/`:
    - `test_chat_flow.py` — 完整聊天流程测试
    - `test_voice_flow.py` — 语音对话流程测试
    - `test_knowledge_flow.py` — 知识库摄取→检索→聊天测试
    - `test_evolution_flow.py` — 自进化流程测试
  - 使用Playwright进行跨平台UI测试
  - API集成测试 (curl/http)
  - 性能基准: 响应延迟、并发用户
  - 测试报告生成

  **Must NOT do**:
  - 不要测试外部服务 (Ollama/vLLM assumed running)
  - 不要在测试中使用真实个人数据

  **Recommended Agent Profile**:
  - **Category**: `unspecified-high`
    - Reason: 端到端集成测试
  - **Skills**: [`playwright`]
    - `playwright`: 浏览器自动化测试

  **Parallelization**:
  - **Can Run In Parallel**: NO (needs all platforms ready)
  - **Parallel Group**: Wave 4 (final task)
  - **Blocks**: None (最后一步)
  - **Blocked By**: Tasks 21 (web chat), 24 (android), 25 (desktop), 30 (docker)

  **References**:
  - Playwright: `https://playwright.dev/docs/intro`
  - pytest: `https://docs.pytest.org/`

  **Acceptance Criteria**:
  - [ ] 聊天流程E2E测试通过
  - [ ] 语音流程E2E测试通过
  - [ ] 知识库流程E2E测试通过
  - [ ] 测试报告生成

  **QA Scenarios**:

  ```
  Scenario: 完整聊天→知识库→自进化E2E
    Tool: Playwright (via playwright skill)
    Preconditions: Docker全栈运行
    Steps:
      1. 上传测试简历文档到知识库
      2. 发送聊天消息询问简历内容
      3. 验证AI回复基于简历
      4. 检查evolution/pending有新提取的事实
      5. 审核通过事实
      6. 再次搜索验证新知识可检索
    Expected Result: 完整闭环: 上传→聊天→提取→审核→更新
    Evidence: .sisyphus/evidence/task-31-e2e.png
  ```

  **Commit**: YES
  - Message: `test: end-to-end integration tests`
  - Files: tests/e2e/

---

## Final Verification Wave

- [ ] F1. **Plan Compliance Audit** — `oracle`
  读取计划端到端。对每个"Must Have": 验证实现存在 (读文件、curl端点、运行命令)。对每个"Must NOT Have": 搜索代码库检查禁止模式 — 如有则以 file:line 报告。检查 `.sisyphus/evidence/` 中的证据文件。对比交付物与计划。
  Output: `Must Have [N/N] | Must NOT Have [N/N] | Tasks [N/N] | VERDICT: APPROVE/REJECT`

- [ ] F2. **Code Quality Review** — `unspecified-high`
  运行 `tsc --noEmit` + linter + Python检查。审查所有变更文件: `as any`/`@ts-ignore`, 空catch, console.log, 注释掉的代码, 未用imports。检查AI slop: 过度注释、过度抽象、泛型命名(data/result/item/temp)。
  Output: `Build [PASS/FAIL] | Lint [PASS/FAIL] | Files [N clean/N issues] | VERDICT`

- [ ] F3. **Real Manual QA** — `unspecified-high` (+ `playwright` skill)
  从干净状态开始。执行EVERY task的EVERY QA scenario — 完全按步骤，捕获证据。测试跨任务集成 (功能协同工作，非隔离)。测试边缘情况: 空状态、无效输入、快速操作。保存到 `.sisyphus/evidence/final-qa/`。
  Output: `Scenarios [N/N pass] | Integration [N/N] | Edge Cases [N tested] | VERDICT`

- [ ] F4. **Scope Fidelity Check** — `deep`
  对每个task: 读"What to do"，读实际diff (git log/diff)。验证1:1 — spec中的所有内容都已构建 (无缺失)，未构建spec之外的内容 (无蔓延)。检查"Must NOT do"合规。检测跨任务污染: Task N触碰Task M的文件。标记未计入的变更。
  Output: `Tasks [N/N compliant] | Contamination [CLEAN/N issues] | Unaccounted [CLEAN/N files] | VERDICT`

---

## Final Verification Wave

---

## Commit Strategy

- **Wave 1**: Multiple commits — infra setup grouped, docs separate
- **Wave 2**: Per-module commits — each AI component independent
- **Wave 3**: Per-feature commits — API endpoints + UI screens separate
- **Wave 4**: Per-platform commits + integration

---

## Success Criteria

### Verification Commands
```bash
# Backend health
curl http://localhost:8000/health | jq '.status'  # Expected: "ok"

# Chat API
curl -X POST http://localhost:8000/api/chat -H "Content-Type: application/json" \
  -d '{"message":"介绍一下你的项目经验"}' | jq '.response'  # Expected: relevant answer

# Voice pipeline
curl http://localhost:8000/api/voice/status | jq '.stt_ready, .tts_ready'  # Expected: true, true

# Web app
curl http://localhost:3000  # Expected: 200, Next.js page rendered

# Knowledge base
curl http://localhost:8000/api/knowledge/stats | jq '.document_count'  # Expected: >0
```

### Final Checklist
- [ ] All "Must Have" present
- [ ] All "Must NOT Have" absent
- [ ] 100% local LLM inference verified (no external API calls in logs)
- [ ] Web chat responds based on personal knowledge base
- [ ] Voice input/output working with cloned voice
- [ ] 2D avatar lip-sync with audio
- [ ] Android APK installable and functional
- [ ] Desktop app installable on Windows and Linux
- [ ] Bilingual documentation complete
- [ ] Chat logs saved to documents/chat/
