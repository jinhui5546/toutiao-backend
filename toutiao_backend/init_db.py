"""
数据库初始化脚本
运行此脚本将创建所有必需的数据表
"""
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from config.db_config import Async_dbURL
from models.news import Base  # 所有模型现在共享同一个Base


async def init_database():
    """初始化数据库，创建所有表"""
    engine = create_async_engine(Async_dbURL, echo=True)
    
    # 创建所有表（所有模型共享同一个Base.metadata）
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    print("数据库表创建成功！")
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(init_database())
