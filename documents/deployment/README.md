# 部署指南 / Deployment Guide

## 概述 / Overview

数字分身支持两种运行方式：
1. **Docker Compose** (推荐用于生产) — 4 个容器化服务
2. **本地直接运行** (开发模式) — 在 tmux 中分别启动

Digital Twin supports two deployment modes:
1. **Docker Compose** (recommended for production) — 4 containerized services
2. **Local direct run** (development mode) — separate processes in tmux

---

## 前置要求 / Prerequisites

| 工具 / Tool | 最低版本 / Min Version | 用途 / Purpose |
|---|---|---|
| Docker | 24+ | 容器运行时 / Container runtime |
| Docker Compose | 2.20+ | 多容器编排 / Multi-service orchestration |
| Python | 3.12+ | 后端直接运行 / Backend direct run |
| Node.js | 20+ | 前端直接运行 / Frontend direct run |
| Ollama | 0.17.5 | LLM 推理引擎 / LLM inference (local dev) |
| Git | — | 版本控制 / Version control |

**硬件要求 / Hardware Requirements**:

| 配置 | 最低 | 推荐 |
|---|---|---|
| RAM (CPU 运行) | 8GB | 16GB+ |
| RAM (GPU 运行) | 8GB | 32GB+ |
| 磁盘 | 20GB (含模型) | 50GB+ |
| GPU | 可选 (CUDA/ROCm/CANN) | NVIDIA 8GB+ VRAM |

---

## Docker 部署 / Docker Deployment

### 服务架构 / Service Architecture

```
┌─────────────┐     ┌─────────────┐
│  web:3000   │     │  backend:8000│
│  Next.js    │────▶│  FastAPI     │
└─────────────┘     └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
       ┌──────────┐ ┌──────────┐ ┌──────────┐
       │chromadb  │ │ neo4j    │ │ Ollama   │
       │:8001     │ │:7474     │ │(host)    │
       │(向量)     │ │:7687     │ │:11434    │
       └──────────┘ │(图谱)     │ └──────────┘
                    └──────────┘
```

### docker-compose.yml

项目根目录的 `docker-compose.yml` 定义了 4 个服务:

```yaml
services:
  backend:
    build:
      context: .
      dockerfile: Dockerfile.backend
    ports: ["8000:8000"]
    volumes:
      - ./data:/app/data
      - ./models:/app/models
      - ./config.yaml:/app/config.yaml
    environment:
      - LLM_BACKEND=${LLM_BACKEND:-auto}
      - NEO4J_URI=bolt://neo4j:7687
      - NEO4J_USER=neo4j
      - NEO4J_PASSWORD=${NEO4J_PASSWORD:-password}
    depends_on:
      neo4j: { condition: service_healthy }
      chromadb: { condition: service_started }
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    restart: unless-stopped

  web:
    build:
      context: .
      dockerfile: Dockerfile.web
    ports: ["3000:3000"]
    environment:
      - NEXT_PUBLIC_API_BASE_URL=http://backend:8000
    depends_on: [backend]
    restart: unless-stopped

  chromadb:
    image: chromadb/chroma:latest
    ports: ["8001:8000"]
    volumes:
      - ./data/chroma:/chroma/chroma
    restart: unless-stopped

  neo4j:
    image: neo4j:5-community
    ports:
      - "7474:7474"  # Web UI
      - "7687:7687"  # Bolt protocol
    volumes:
      - ./data/neo4j:/data
    environment:
      - NEO4J_AUTH=neo4j/${NEO4J_PASSWORD:-password}
      - NEO4J_PLUGINS=["apoc"]
    healthcheck:
      test: ["CMD", "cypher-shell", "-u", "neo4j", "-p", "${NEO4J_PASSWORD:-password}", "RETURN 1"]
      interval: 30s
      timeout: 10s
      retries: 5
    restart: unless-stopped
```

### 快速启动 / Quick Start

```bash
# 1. 克隆仓库
git clone https://github.com/oldzhu/whoami.git
cd whoami

# 2. 配置环境变量
cp .env.example .env
# 编辑 .env，设置 NEO4J_PASSWORD 等

# 3. 确保 Ollama 在宿主机运行 (Docker 容器连接宿主机 Ollama)
ollama serve

# 4. 下载模型 (从 ModelScope)
ollama pull qwen3.5:2b
ollama pull qwen3.5:4b
ollama pull qwen3.5:9b
ollama pull all-minilm:l6-v2

# 5. 构建并启动所有服务
docker compose up -d

# 6. 查看日志
docker compose logs -f

# 7. 验证
curl http://localhost:8000/health
curl http://localhost:3000

# 8. 停止
docker compose down
```

### 各服务详情 / Service Details

#### Backend (FastAPI)

| 属性 | 值 |
|---|---|
| Dockerfile | `Dockerfile.backend` (python:3.11-slim) |
| 入口 | `uvicorn app.main:app --host 0.0.0.0 --port 8000` |
| 端口 | `8000` |
| 健康检查 | `GET /health` (30s 间隔, 3 次重试) |
| 数据卷 | `./data:/app/data` — 认证/Profile/上传文件 |
| 模型卷 | `./models:/app/models` — 语音/Piper 模型 |
| 配置卷 | `./config.yaml:/app/config.yaml` |

#### Web (Next.js)

| 属性 | 值 |
|---|---|
| Dockerfile | `Dockerfile.web` (node:20-alpine, 多阶段构建) |
| 端口 | `3000` |
| 环境变量 | `NEXT_PUBLIC_API_BASE_URL=http://backend:8000` |

#### ChromaDB

| 属性 | 值 |
|---|---|
| 镜像 | `chromadb/chroma:latest` |
| 端口 | `8001` (内部 8000) |
| 数据卷 | `./data/chroma:/chroma/chroma` |

#### Neo4j

| 属性 | 值 |
|---|---|
| 镜像 | `neo4j:5-community` |
| 端口 | `7474` (Web UI), `7687` (Bolt) |
| 数据卷 | `./data/neo4j:/data` |
| 插件 | `apoc` (图算法) |
| 健康检查 | cypher-shell RETURN 1 (30s 间隔) |

---

## 本地开发部署 / Local Development

### 环境变量 / Environment Variables

复制 `.env.example` 到 `.env`:

```bash
LLM_BACKEND=auto
API_HOST=0.0.0.0
API_PORT=8000
MODELS_DIR=./models
DATA_DIR=./data
```

### 启动步骤 / Setup Steps

#### 1. Ollama (LLM 引擎)

```bash
# 安装 Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 启动 (注意 HTTP_PROXY)
unset HTTP_PROXY HTTPS_PROXY  # 或设置 NO_PROXY=localhost
ollama serve

# 下载模型 (ModelScope 镜像)
ollama pull qwen3.5:2b
ollama pull qwen3.5:4b
ollama pull qwen3.5:9b
ollama pull all-minilm:l6-v2
```

#### 2. Backend (FastAPI)

```bash
# Python 虚拟环境
python3 -m venv venv
source venv/bin/activate
pip install -e ".[dev]"

# 启动
# 注意: HTTP_PROXY 会拦截 localhost 请求
# 必须设置 trust_env=False 或 NO_PROXY=localhost
NO_PROXY=localhost python backend/app/main.py
# 服务启动在 http://localhost:8000
```

#### 3. Frontend (Next.js)

```bash
cd web
npm install
npm run dev
# 服务启动在 http://localhost:3000
```

### 建议使用 tmux

```bash
# 三个窗口分别运行
tmux new -s ollama 'ollama serve'
tmux new -s backend 'NO_PROXY=localhost python backend/app/main.py'
tmux new -s frontend 'cd web && npm run dev'
```

---

## 生产部署建议 / Production Considerations

### 反向代理 / Reverse Proxy

如需从局域网访问，建议使用 nginx 反向代理:

```nginx
server {
    listen 80;
    server_name digital-twin.local;

    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    location /ws/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }

    location / {
        proxy_pass http://127.0.0.1:3000;
    }
}
```

### GPU 支持 / GPU Support

Docker 中启用 GPU:

```yaml
services:
  backend:
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
```

### 模型存储 / Model Storage

- 模型文件较大 (5-10GB)，建议使用 Docker 命名卷而非绑定挂载
- 首次启动需下载模型，可提前在 Dockerfile 中预下载
- Ollama 模型默认在 `~/.ollama/models/`

### 安全加固 / Security Hardening

- 设置强 `NEO4J_PASSWORD`
- 限制 CORS 来源 (目前为 `*`)
- 考虑 `APP_ENV=production` 时关闭 `/docs` (FastAPI Swagger)
- 用 `fail2ban` 防护 localhost 端口

---

## 健康检查 / Health Checks

| 端点 | 方法 | 预期 |
|---|---|---|
| `http://localhost:8000/health` | GET | `{"status":"ok","version":"0.1.0"}` |
| `http://localhost:3000` | GET | HTML 页面 |
| `http://localhost:8001` | GET | ChromaDB 响应 |
| `bolt://localhost:7687` | Bolt | Neo4j 连接成功 |

---

## 故障排查 / Troubleshooting

| 问题 | 可能原因 | 解决 |
|---|---|---|
| `429 Too Many Requests` | 超速限制 | 等待 60 秒 |
| `403 Access restricted to localhost` | 非本地请求 | 使用 localhost |
| Ollama 超时 | HTTP_PROXY 拦截 | `NO_PROXY=localhost` 或 `trust_env=False` |
| Neo4j 连接失败 | Docker 未启动 | `docker compose up -d neo4j` |
| 模型不存在 | 未下载 | `ollama pull <model>` |
| Embedding 错误 | 模型未加载 | 确保 `all-minilm:l6-v2` 已拉取 |

---

## 配置文件 / Configuration Files

| 文件 | 说明 |
|---|---|
| `config.yaml` | LLM 后端、硬件设置、数据目录 |
| `.env` | Docker 环境变量 |
| `models/config.yaml` | 模型路由表、模型参数 |
| `data/auth.json` | 认证信息 (SHA256 hash) |
| `data/profile.json` | 个人资料 |
| `docker-compose.yml` | Docker 服务编排 |
