# 聊天记录 / Chat Logs

## 概述 / Overview

本文档规范了聊天记录的命名、格式和索引方式。

This document specifies the naming, format, and indexing conventions for chat logs.

---

## 文件命名规范 / File Naming Convention

### 格式 / Format

```
chat-[YYYYMMDD]-[NNN].md
```

| 组成部分 / Part | 说明 / Description | 示例 / Example |
|---|---|---|
| `chat-` | 固定前缀 / Fixed prefix | `chat-` |
| `YYYYMMDD` | 日期 (年月日) / Date | `20260615` |
| `-` | 分隔符 / Separator | `-` |
| `NNN` | 序号 (3位补零) / Sequence (zero-padded 3 digits) | `001` |
| `.md` | 扩展名 / Extension | `.md` |

### 示例 / Examples

```
chat-20260615-001.md    # 2026年6月15日 第1个会话
chat-20260615-002.md    # 2026年6月15日 第2个会话
chat-20260616-001.md    # 2026年6月16日 第1个会话
```

---

## 文件格式 / File Format

### 模板 / Template

```markdown
# 会话 / Session: {主题 / Topic}

## 元数据 / Metadata

| 字段 / Field | 值 / Value |
|---|---|
| 会话 ID / Session ID | `chat-YYYYMMDD-NNN` |
| 日期 / Date | YYYY-MM-DD HH:MM:SS |
| 模型 / Model | [模型名称 / Model name] |
| 标签 / Tags | [标签列表 / Tag list] |
| 摘要 / Summary | [一句话总结 / One-line summary] |

---

## 消息记录 / Message Log

### [序号] 用户 / User (HH:MM:SS)

用户输入的内容。
The user's input message.

### [序号] 助手 / Assistant (HH:MM:SS)

AI 的回复内容。
The AI's response.

---
```

---

## 索引 / Index

### 按日期 / By Date

| 文件 / File | 日期 / Date | 主题 / Topic | 标签 / Tags |
|---|---|---|---|
| [chat-20260615-001.md](./chat-20260615-001.md) | 2026-06-15 | [TBD] | [TBD] |

### 按标签 / By Tags

TODO: 标签分类索引。
Tag-based index.

---

## 目录结构 / Directory Structure

```
documents/chat/
├── README.md                  # 本文件 / This file
├── index.json                 # 结构化索引 / Structured index (可选 / optional)
├── chat-20260615-001.md       # 会话文件 / Session file
└── chat-20260615-002.md       # 会话文件 / Session file
```

---

## 结构化索引 / Structured Index (`index.json`)

```json
{
  "sessions": [
    {
      "id": "chat-20260615-001",
      "date": "2026-06-15T00:00:00Z",
      "topic": "TBD",
      "model": "TBD",
      "tags": [],
      "message_count": 0,
      "summary": "TBD"
    }
  ]
}
```

---

## 维护规则 / Maintenance Rules

1. 每个会话一个文件 / One file per session
2. 文件名序号同日内递增 / Sequence number increments within same day
3. 新会话追加到 `index.json` / New sessions appended to `index.json`
4. 定期归档旧会话 / Periodically archive old sessions
