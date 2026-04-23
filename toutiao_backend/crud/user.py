from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from models.user import User
from schemas.user import UserRequest
from utils.security import get_hash_password, verify_password


async def get_username(username: str, db: AsyncSession):
    """根据用户名获取用户"""
    stmt = select(User).where(User.username == username)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def get_user_by_id(user_id: int, db: AsyncSession):
    """根据ID获取用户"""
    stmt = select(User).where(User.id == user_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def create_user(db: AsyncSession, user: UserRequest):
    """创建新用户"""
    pwd_hash = get_hash_password(user.password)
    new_user = User(username=user.username, password=pwd_hash)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def update_user_info(db: AsyncSession, user_id: int, update_data: dict):
    """更新用户信息"""
    # 过滤掉None值
    update_data = {k: v for k, v in update_data.items() if v is not None}
    if not update_data:
        return None
    
    stmt = update(User).where(User.id == user_id).values(**update_data)
    result = await db.execute(stmt)
    await db.commit()
    
    # 返回更新后的用户
    return await get_user_by_id(user_id, db)


async def verify_user_password(plain_password: str, hashed_password: str) -> bool:
    """验证用户密码"""
    return verify_password(plain_password, hashed_password)

