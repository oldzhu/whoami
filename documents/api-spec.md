# API 规格 / API Specification

## 概述 / Overview

TODO: 描述 API 整体设计理念、版本策略、基础 URL。
Describe API design philosophy, versioning strategy, and base URL.

- **基础 URL / Base URL**: `http://localhost:{port}/api/v1`
- **协议 / Protocol**: REST over HTTP, WebSocket
- **数据格式 / Data Format**: JSON

---

## 认证 / Authentication

### 认证方式 / Auth Methods

TODO: 描述认证机制 (JWT / API Key / OAuth2)。
Describe authentication mechanisms.

```
Authorization: Bearer <token>
```

### 接口 / Endpoints

| 方法 / Method | 路径 / Path | 说明 / Description |
|---|---|---|
| POST | `/auth/login` | 登录 / Login |
| POST | `/auth/refresh` | 刷新令牌 / Refresh token |
| POST | `/auth/logout` | 登出 / Logout |

---

## 请求/响应格式 / Request/Response Format

### 标准响应体 / Standard Response Body

```json
{
  "code": 0,
  "message": "success",
  "data": {}
}
```

### 分页响应 / Paginated Response

```json
{
  "code": 0,
  "message": "success",
  "data": {
    "items": [],
    "total": 100,
    "page": 1,
    "page_size": 20
  }
}
```

---

## 核心接口 / Core Endpoints

### 聊天 / Chat

| 方法 / Method | 路径 / Path | 说明 / Description |
|---|---|---|
| POST | `/chat/completions` | 发送消息 / Send message |
| GET | `/chat/history` | 获取历史 / Get history |
| DELETE | `/chat/history/{id}` | 删除会话 / Delete session |

### 模型管理 / Model Management

| 方法 / Method | 路径 / Path | 说明 / Description |
|---|---|---|
| GET | `/models` | 模型列表 / List models |
| POST | `/models/load` | 加载模型 / Load model |
| POST | `/models/unload` | 卸载模型 / Unload model |

### 系统 / System

| 方法 / Method | 路径 / Path | 说明 / Description |
|---|---|---|
| GET | `/system/health` | 健康检查 / Health check |
| GET | `/system/info` | 系统信息 / System info |
| GET | `/system/metrics` | 监控指标 / Metrics |

---

## 错误码 / Error Codes

| 错误码 / Code | 说明 / Description |
|---|---|
| 0 | 成功 / Success |
| 1001 | 参数错误 / Invalid parameters |
| 1002 | 未认证 / Unauthorized |
| 1003 | 无权限 / Forbidden |
| 1004 | 资源不存在 / Not found |
| 2001 | 模型加载失败 / Model load failed |
| 2002 | 推理超时 / Inference timeout |
| 5000 | 服务器内部错误 / Internal server error |

---

## WebSocket 事件 / WebSocket Events

### 连接 / Connection

```
ws://localhost:{port}/ws/chat
```

### 客户端→服务端 / Client→Server

| 事件 / Event | 载荷 / Payload | 说明 / Description |
|---|---|---|
| `message.send` | `{ "content": "..." }` | 发送消息 / Send message |
| `message.cancel` | `{ "id": "..." }` | 取消生成 / Cancel generation |

### 服务端→客户端 / Server→Client

| 事件 / Event | 载荷 / Payload | 说明 / Description |
|---|---|---|
| `message.chunk` | `{ "content": "..." }` | 流式输出 / Streaming chunk |
| `message.done` | `{ "id": "..." }` | 生成完成 / Generation done |
| `message.error` | `{ "code": 2002 }` | 错误 / Error |

---

## 版本历史 / Changelog

| 版本 / Version | 日期 / Date | 变更 / Changes |
|---|---|---|
| v1.0.0 | TBD | 初始版本 / Initial release |
