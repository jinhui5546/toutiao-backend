from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from crud.user import get_username, create_user, verify_user_password, update_user_info, get_user_by_id
from schemas.user import UserRequest, UserUpdateRequest, PasswordChangeRequest, UserInfoResponse, AuthResponse
from config.db_config import get_db
from utils.auth import create_access_token, get_current_user
from models.user import User

router = APIRouter(prefix="/api/user", tags=["users"])


@router.post("/register", response_model=dict)
async def register(user: UserRequest, db: AsyncSession = Depends(get_db)):
    """用户注册"""
    # 检查用户名是否已存在
    exist_user = await get_username(user.username, db)
    if exist_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名已存在"
        )
    
    # 创建新用户
    new_user = await create_user(db, user)
    
    # 生成 token（sub必须是字符串）
    token = create_access_token(data={"sub": str(new_user.id)})
    
    return {
        "code": 200,
        "message": "注册成功",
        "data": {
            "token": token,
            "userInfo": {
                "id": new_user.id,
                "username": new_user.username,
                "nickname": new_user.nickname,
                "avatar": new_user.avatar,
                "gender": new_user.gender,
                "bio": new_user.bio
            }
        }
    }


@router.post("/login", response_model=dict)
async def login(user: UserRequest, db: AsyncSession = Depends(get_db)):
    """用户登录"""
    # 查找用户
    db_user = await get_username(user.username, db)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误"
        )
    
    # 验证密码
    if not await verify_user_password(user.password, db_user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误"
        )
    
    # 生成 token（sub必须是字符串）
    token = create_access_token(data={"sub": str(db_user.id)})
    
    return {
        "code": 200,
        "message": "登录成功",
        "data": {
            "token": token,
            "userInfo": {
                "id": db_user.id,
                "username": db_user.username,
                "nickname": db_user.nickname,
                "avatar": db_user.avatar,
                "gender": db_user.gender,
                "bio": db_user.bio
            }
        }
    }


@router.get("/info", response_model=dict)
async def get_user_info(
    current_user: User = Depends(get_current_user)
):
    """获取当前用户信息"""
    return {
        "code": 200,
        "message": "success",
        "data": {
            "id": current_user.id,
            "username": current_user.username,
            "nickname": current_user.nickname,
            "avatar": current_user.avatar,
            "gender": current_user.gender,
            "bio": current_user.bio
        }
    }


@router.put("/update", response_model=dict)
async def update_user(
    update_data: UserUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """更新用户信息"""
    update_dict = update_data.dict(exclude_unset=True)
    
    updated_user = await update_user_info(db, current_user.id, update_dict)
    
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="更新失败"
        )
    
    return {
        "code": 200,
        "message": "更新成功",
        "data": {
            "id": updated_user.id,
            "username": updated_user.username,
            "nickname": updated_user.nickname,
            "avatar": updated_user.avatar,
            "gender": updated_user.gender,
            "bio": updated_user.bio
        }
    }


@router.put("/password", response_model=dict)
async def change_password(
    password_data: PasswordChangeRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """修改用户密码"""
    # 验证旧密码
    if not await verify_user_password(password_data.oldPassword, current_user.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="当前密码错误"
        )
    
    # 更新密码
    from utils.security import get_hash_password
    new_password_hash = get_hash_password(password_data.newPassword)
    
    await update_user_info(db, current_user.id, {"password": new_password_hash})
    
    return {
        "code": 200,
        "message": "密码修改成功",
        "data": None
    }