# 开发指南 / Development Guide

## 概述 / Overview

TODO: 描述开发环境要求和整体工作流。
Describe development environment requirements and overall workflow.

---

## 环境搭建 / Setup

### 前置要求 / Prerequisites

| 工具 / Tool | 版本 / Version | 说明 / Notes |
|---|---|---|
| [Python] | [TBD] | 后端开发 / Backend |
| [Node.js] | [TBD] | 前端开发 / Frontend |
| [Rust] | [TBD] | 桌面端开发 / Desktop |
| [Docker] | [TBD] | 容器化运行 / Containerized run |
| [Git] | [TBD] | 版本控制 / Version control |

### 快速启动 / Quick Start

```bash
# 克隆仓库 / Clone repository
git clone <repo-url>
cd <project-dir>

# 安装依赖 / Install dependencies
# TODO: 添加具体命令 / Add specific commands

# 启动开发服务器 / Start dev server
# TODO: 添加具体命令 / Add specific commands
```

### 项目结构 / Project Structure

```
project-root/
├── backend/          # 后端服务 / Backend service
├── web/              # Web 前端 / Web frontend
├── mobile/           # 移动端 / Mobile app
├── desktop/          # 桌面端 / Desktop app
├── models/           # 模型文件 / Model files
├── data/             # 数据存储 / Data storage
├── documents/        # 项目文档 / Documentation
└── .sisyphus/        # 项目管理 / Project management
```

---

## 编码规范 / Coding Standards

### 通用规范 / General

TODO: 描述通用编码规范。
Describe general coding standards.

- 命名规范 / Naming conventions: [TBD]
- 注释语言 / Comment language: 中英双语 / Bilingual
- 代码审查 / Code review: [TBD]

### 后端 / Backend

TODO: 描述后端编码规范 (语言特定)。
Describe backend coding standards (language-specific).

### 前端 / Frontend

TODO: 描述前端编码规范。
Describe frontend coding standards.

### 移动端 / Mobile

TODO: 描述移动端编码规范。
Describe mobile coding standards.

### 桌面端 / Desktop

TODO: 描述桌面端编码规范。
Describe desktop coding standards.

---

## Git 工作流 / Git Workflow

### 分支策略 / Branching Strategy

| 分支 / Branch | 用途 / Purpose |
|---|---|
| `main` | 稳定发布 / Stable releases |
| `develop` | 开发主线 / Development mainline |
| `feature/*` | 功能开发 / Feature development |
| `bugfix/*` | 问题修复 / Bug fixes |
| `release/*` | 发布准备 / Release preparation |

### 提交规范 / Commit Conventions

```
<type>(<scope>): <中文描述 / English description>

[可选的详细描述 / Optional body]
```

**类型 / Types**: `feat` | `fix` | `docs` | `refactor` | `test` | `chore` | `perf`

### Pull Request 流程 / Pull Request Process

1. 从 `develop` 创建功能分支 / Create feature branch from `develop`
2. 开发和本地测试 / Develop and test locally
3. 提交 PR 并填写描述 / Submit PR with description
4. 通过代码审查 / Pass code review
5. 合并到 `develop` / Merge to `develop`

---

## 测试策略 / Testing Strategy

### 测试层级 / Test Levels

| 层级 / Level | 工具 / Tool | 覆盖要求 / Coverage |
|---|---|---|
| 单元测试 / Unit | [TBD] | >= 80% |
| 集成测试 / Integration | [TBD] | 核心流程 / Core flows |
| 端到端测试 / E2E | [TBD] | 关键路径 / Critical paths |

### 运行测试 / Running Tests

```bash
# 后端测试 / Backend tests
# TODO: 添加命令 / Add commands

# 前端测试 / Frontend tests
# TODO: 添加命令 / Add commands

# 所有测试 / All tests
# TODO: 添加命令 / Add commands
```

---

## 常见问题 / FAQ

TODO: 添加开发过程中常见问题和解决方案。
Add common development issues and solutions.
