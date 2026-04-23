# 数据库设置指南

## 前置要求

1. 确保已安装 MySQL 8.0+ 
2. 确保 MySQL 服务正在运行

## 快速导入数据库

### 方法一：使用命令行导入（推荐）

打开命令提示符或终端，执行以下命令：

```bash
mysql -u root -p < "D:\BaiduNetdiskDownload\项目物料\02-数据库sql文件\database.sql"
```

输入MySQL密码后，将自动创建数据库并导入所有数据。

### 方法二：使用MySQL Workbench

1. 打开 MySQL Workbench
2. 连接到本地 MySQL 服务器
3. 点击 File → Open SQL Script
4. 选择 `D:\BaiduNetdiskDownload\项目物料\02-数据库sql文件\database.sql`
5. 点击执行按钮（⚡图标）

### 方法三：手动执行SQL

1. 登录 MySQL：
   ```bash
   mysql -u root -p
   ```

2. 执行SQL文件：
   ```sql
   source D:\BaiduNetdiskDownload\项目物料\02-数据库sql文件\database.sql
   ```

## 验证导入

导入完成后，可以执行以下SQL语句验证：

```sql
-- 查看数据库
SHOW DATABASES;

-- 切换到 news_app 数据库
USE news_app;

-- 查看所有表
SHOW TABLES;

-- 查看新闻分类
SELECT * FROM news_category;

-- 查看新闻数量
SELECT COUNT(*) FROM news;

-- 查看用户表结构
DESCRIBE user;
```

## 数据库结构

### 主要数据表

1. **user** - 用户信息表
2. **user_token** - 用户令牌表
3. **news_category** - 新闻分类表
4. **news** - 新闻表
5. **related_news** - 相关新闻关联表
6. **favorite** - 收藏表
7. **history** - 浏览历史表
8. **ai_chat** - AI聊天记录表

### 初始数据

SQL文件包含以下初始数据：
- 8个新闻分类（头条、社会、国内、国际、娱乐、体育、科技、财经）
- 300+条新闻数据
- 涵盖多个类别的真实新闻内容

## 配置后端连接

在 `config/db_config.py` 中确认数据库连接配置：

```python
Async_dbURL="mysql+aiomysql://root:你的密码@localhost:3306/news_app?charset=utf8"
```

**重要：** 请将 `你的密码` 替换为实际的MySQL root密码。

## 常见问题

### 问题1：权限不足

如果遇到权限错误，请以管理员身份运行命令提示符。

### 问题2：数据库已存在

如果 `news_app` 数据库已存在，SQL文件会自动使用该数据库。如需重新创建：

```sql
DROP DATABASE IF EXISTS news_app;
```

然后重新执行导入命令。

### 问题3：字符集问题

确保MySQL使用UTF-8字符集：

```sql
SHOW VARIABLES LIKE 'character_set%';
```

### 问题4：文件大小限制

如果导入时遇到文件大小限制，修改MySQL配置：

```ini
# my.ini 或 my.cnf
[mysqld]
max_allowed_packet=500M
```

## 测试连接

导入完成后，运行以下Python代码测试数据库连接：

```python
import asyncio
from config.db_config import get_db

async def test_connection():
    async for db in get_db():
        result = await db.execute("SELECT 1")
        print("数据库连接成功！")
        break

asyncio.run(test_connection())
```

## 下一步

数据库设置完成后，可以启动后端服务：

```bash
cd D:\Python\toutiao_backend
python -m uvicorn main:app --reload
```

访问 http://127.0.0.1:8000/docs 查看API文档。
