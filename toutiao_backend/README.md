# AI头条新闻系统

一个基于 FastAPI 和 SQLAlchemy 构建的现代化新闻系统后端API服务。

## 技术栈

- **后端框架**: FastAPI
- **数据库**: MySQL
- **ORM**: SQLAlchemy (异步)
- **数据库驱动**: aiomysql
- **密码加密**: passlib + bcrypt
- **认证**: JWT (python-jose)

## 功能模块

### 1. 用户管理
- 用户注册
- 用户登录
- 获取用户信息
- 更新用户信息
- 修改密码

### 2. 新闻模块
- 获取新闻分类列表
- 获取新闻列表（支持分页和分类筛选）
- 获取新闻详情（自动增加浏览量）
- 相关新闻推荐

### 3. 收藏模块
- 检查新闻收藏状态
- 添加收藏
- 取消收藏
- 获取收藏列表
- 清空所有收藏

### 4. 浏览历史模块
- 添加浏览记录
- 获取浏览历史列表
- 删除单条浏览记录
- 清空浏览历史

## 安装依赖

```bash
pip install -r requirements.txt
```

## 配置数据库

在 `config/db_config.py` 中修改数据库连接信息：

```python
Async_dbURL="mysql+aiomysql://用户名:密码@localhost:3306/数据库名?charset=utf8"
```

## 运行项目

```bash
uvicorn main:app --reload
```

访问 http://127.0.0.1:8000/docs 查看 API 文档

## 项目结构

```
toutiao_backend/
├── crud/              # 数据访问层
│   ├── favorite.py
│   ├── history.py
│   ├── news.py
│   └── user.py
├── models/            # 数据模型
│   ├── favorite.py
│   ├── history.py
│   ├── news.py
│   └── user.py
├── routers/           # API路由
│   ├── favorite.py
│   ├── history.py
│   ├── news.py
│   └── user.py
├── schemas/           # 数据验证
│   ├── favorite.py
│   ├── history.py
│   ├── news.py
│   └── user.py
├── utils/             # 工具函数
│   ├── auth.py       # JWT认证
│   └── security.py   # 密码加密
├── config/            # 配置文件
│   └── db_config.py
└── main.py           # 应用入口
```

## API 接口说明

### 用户接口
- `POST /api/user/register` - 用户注册
- `POST /api/user/login` - 用户登录
- `GET /api/user/info` - 获取用户信息（需要认证）
- `PUT /api/user/update` - 更新用户信息（需要认证）
- `PUT /api/user/password` - 修改密码（需要认证）

### 新闻接口
- `GET /api/news/categories` - 获取新闻分类
- `GET /api/news/list` - 获取新闻列表
- `GET /api/news/detail` - 获取新闻详情

### 收藏接口（需要认证）
- `GET /api/favorite/check` - 检查收藏状态
- `POST /api/favorite/add` - 添加收藏
- `DELETE /api/favorite/remove` - 取消收藏
- `GET /api/favorite/list` - 获取收藏列表
- `DELETE /api/favorite/clear` - 清空收藏

### 历史接口（需要认证）
- `POST /api/history/add` - 添加浏览记录
- `GET /api/history/list` - 获取浏览历史
- `DELETE /api/history/delete/{id}` - 删除历史记录
- `DELETE /api/history/clear` - 清空历史

## 认证方式

需要在请求头中添加：
```
Authorization: Bearer <token>
```
