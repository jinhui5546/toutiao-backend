from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# 用户注册/登录请求
class UserRequest(BaseModel):
    username: str
    password: str


# 用户更新请求
class UserUpdateRequest(BaseModel):
    nickname: Optional[str] = None
    avatar: Optional[str] = None
    gender: Optional[str] = None
    bio: Optional[str] = None
    phone: Optional[str] = None


# 修改密码请求
class PasswordChangeRequest(BaseModel):
    oldPassword: str
    newPassword: str


# 用户信息响应
class UserInfoResponse(BaseModel):
    id: int
    username: str
    nickname: Optional[str] = None
    avatar: Optional[str] = None
    gender: Optional[str] = 'unknown'
    bio: Optional[str] = '这个人很懒，什么都没留下'
    
    class Config:
        from_attributes = True


# 登录/注册响应
class AuthResponse(BaseModel):
    token: str
    userInfo: UserInfoResponse