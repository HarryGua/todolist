# 待办事项清单 (Todo List)

一个基于React前端和Python FastAPI后端的待办事项Web应用，使用MongoDB作为数据库。

## 项目架构

- **前端**: React + TypeScript + Vite
- **后端**: Python + FastAPI
- **数据库**: MongoDB Atlas

## 环境要求

- Node.js 16+
- Python 3.8+
- MongoDB Atlas账户

## 安装和运行

### 1. 克隆项目
```bash
git clone <repository-url>
cd todolist-1
```

### 2. 后端设置

```bash
cd backend

# 激活虚拟环境
venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 启动后端服务器
python main.py
```

后端将在 `http://localhost:8000` 运行

### 3. 前端设置

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端将在 `http://localhost:5173` 运行

## 数据库配置

项目已配置使用MongoDB Atlas云数据库：
- 连接字符串: `mongodb+srv://huguao777:5kuRgTIaPZlLGKBi@clustertodolist.xhwhgkb.mongodb.net/`
- 数据库名: `todolist`
- 集合名: `todos`

## API端点

- `GET /` - 健康检查
- `GET /todos` - 获取所有待办事项
- `POST /todos` - 创建新待办事项
- `PUT /todos/{id}` - 更新待办事项
- `DELETE /todos/{id}` - 删除待办事项

## 功能特性

- ✅ 添加新的待办事项
- ✅ 标记待办事项为完成/未完成
- ✅ 删除待办事项
- ✅ 实时数据同步
- ✅ 响应式设计
- ✅ 错误处理

## 项目结构

```
todolist-1/
├── frontend/                 # React前端
│   ├── src/
│   │   ├── App.tsx          # 主应用组件
│   │   ├── App.css          # 应用样式
│   │   └── services/
│   │       └── api.ts       # API服务
│   ├── package.json
│   └── vite.config.ts
├── backend/                  # Python后端
│   ├── main.py              # FastAPI主文件
│   ├── requirements.txt     # Python依赖
│   └── venv/                # Python虚拟环境
└── README.md
```

## 技术栈

### 前端
- React 18
- TypeScript
- Vite
- Axios

### 后端
- FastAPI
- Motor (MongoDB异步驱动)
- Pydantic
- Uvicorn

### 数据库
- MongoDB Atlas

## 开发说明

1. 后端使用异步MongoDB驱动，支持高并发
2. 前端使用TypeScript确保类型安全
3. API使用RESTful设计
4. 支持CORS跨域请求
5. 完整的错误处理机制

## 部署

### 后端部署
可以使用以下平台部署后端：
- Heroku
- Railway
- DigitalOcean
- AWS

### 前端部署
可以使用以下平台部署前端：
- Vercel
- Netlify
- GitHub Pages

## 许可证

MIT License 