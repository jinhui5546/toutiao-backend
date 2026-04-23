from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession

from config.db_config import get_db
from crud.user import get_user_by_id
from models.user import User

# JWT配置
SECRET_KEY = "your-secret-key-change-this-in-production"  # 在生产环境中应该使用环境变量
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 7

# HTTP Bearer token
security = HTTPBearer(auto_error=False)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """创建访问令牌"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_token_from_request(request: Request) -> Optional[str]:
    """从请求中提取token，兼容多种格式"""
    # 方式1: Authorization: Bearer <token>
    auth_header = request.headers.get("Authorization")
    if auth_header:
        if auth_header.startswith("Bearer "):
            return auth_header[7:]
        # 方式2: Authorization: <token> (无前缀)
        return auth_header
    return None


async def get_current_user(
    request: Request,
    db: AsyncSession = Depends(get_db)
) -> User:
    """获取当前用户"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="无法验证凭据",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # 从请求中获取token
    token = await get_token_from_request(request)
    
    print(f"[Auth Debug] Authorization header: {request.headers.get('Authorization')}")
    print(f"[Auth Debug] Extracted token: {token}")
    
    if not token:
        print("[Auth Debug] Token is empty, raising exception")
        raise credentials_exception
    
    try:
        print(f"[Auth Debug] Decoding token...")
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id_raw = payload.get("sub")
        print(f"[Auth Debug] Decoded user_id (raw): {user_id_raw}, type: {type(user_id_raw)}")
        
        if user_id_raw is None:
            print("[Auth Debug] user_id is None, raising exception")
            raise credentials_exception
        
        # 兼容两种格式：字符串和整数
        if isinstance(user_id_raw, int):
            # 旧格式：整数（兼容旧的token）
            print(f"[Auth Debug] Found integer format (old token), using directly")
            user_id = user_id_raw
        elif isinstance(user_id_raw, str):
            # 新格式：字符串
            try:
                user_id = int(user_id_raw)
                print(f"[Auth Debug] Converted string to int: {user_id}")
            except (ValueError, TypeError):
                print(f"[Auth Debug] Invalid user_id format: {user_id_raw}")
                raise credentials_exception
        else:
            print(f"[Auth Debug] Unknown user_id type: {type(user_id_raw)}")
            raise credentials_exception
    except JWTError as e:
        print(f"[Auth Debug] JWTError: {str(e)}")
        raise credentials_exception
    
    user = await get_user_by_id(user_id, db)
    if user is None:
        print(f"[Auth Debug] User not found for id: {user_id}")
        raise credentials_exception
    
    print(f"[Auth Debug] Authentication successful for user: {user.username}")
    return user
