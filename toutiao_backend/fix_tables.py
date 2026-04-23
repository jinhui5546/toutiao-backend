"""
数据库表结构修复脚本
为 history 和 favorite 表添加 created_at 字段
"""
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy import text
from config.db_config import Async_dbURL


async def fix_tables():
    """修复表结构"""
    engine = create_async_engine(Async_dbURL, echo=True)
    
    async with engine.begin() as conn:
        # 检查并添加 history.created_at
        try:
            await conn.execute(text("ALTER TABLE history ADD COLUMN created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '浏览时间'"))
            print("✓ history 表添加 created_at 字段成功")
        except Exception as e:
            if "Duplicate column name" in str(e):
                print("✓ history.created_at 字段已存在")
            else:
                print(f"✗ history 表修复失败: {e}")
        
        # 检查并添加 favorite.created_at（如果还没有的话）
        try:
            await conn.execute(text("ALTER TABLE favorite ADD COLUMN created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '收藏时间'"))
            print("✓ favorite 表添加 created_at 字段成功")
        except Exception as e:
            if "Duplicate column name" in str(e):
                print("✓ favorite.created_at 字段已存在")
            else:
                print(f"✗ favorite 表修复失败: {e}")
    
    print("\n数据库表结构修复完成！")
    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(fix_tables())
