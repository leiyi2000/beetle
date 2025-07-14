# Beetle - 文件同步工具

Beetle 是一个基于 FastAPI 和 Tortoise ORM 构建的文件同步工具，用于在不同的 OpenList 路径之间自动同步文件。

## 功能特点

- 支持定时自动同步文件
- 基于文件大小的差异检测
- RESTful API 接口
- 多任务并行处理
- Docker 容器化部署

## 技术栈

- Python 3.13+
- FastAPI - Web 框架
- Tortoise ORM - 数据库 ORM
- Granian - ASGI 服务器
- SQLite - 数据存储
- Docker - 容器化

## 安装

### 环境要求

- Python 3.13 或更高版本
- OpenList API 访问权限

### 本地开发

1. 克隆仓库

```bash
git clone <repository-url>
cd beetle
```

2. 创建并配置环境变量

```bash
cp env.example .env
```

编辑 `.env` 文件，设置以下环境变量：

```
PORT=8000                         # API 服务端口
OPENLIST_HOST=<your-openlist-host> # OpenList API 主机地址
OPENLIST_TOKEN=<your-token>        # OpenList API 访问令牌
```

3. 安装依赖

```bash
pip install uv
uv sync
```

4. 运行开发服务器

```bash
uv run granian --access-log --host 0.0.0.0 --interface asgi beetle.main:app
```

### Docker 部署

1. 启动服务

```bash
docker compose up -d
```

## API 文档

启动服务后，访问 `http://localhost:8000/docs` 查看 Swagger API 文档。

### 主要 API 端点

#### 健康检查

```
GET /health
```

#### 任务管理

- 创建任务：`POST /task/create`
- 更新任务：`POST /task/update`
- 删除任务：`POST /task/delete`
- 查询任务：`POST /task/reads`

## 任务配置

创建任务时需要提供以下参数：

- `src`: 源路径
- `dst`: 目标路径
- `interval`: 同步间隔（秒，最小 300 秒）
- `cleanup`: 是否清理目标路径中不存在于源路径的文件

## 开发

### 项目结构

```
beetle/
├── api/            # API 路由和处理函数
├── models/         # 数据模型
├── constants.py    # 常量定义
├── main.py         # 应用入口
├── schedule.py     # 任务调度
├── sdk.py          # OpenList API 客户端
└── settings.py     # 应用配置
```

## TODO
- web 

## 许可证

[LICENSE](LICENSE)