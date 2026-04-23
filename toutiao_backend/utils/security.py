from passlib.context import CryptContext
password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_hash_password(password:str):
    """对密码进行哈希加密"""
    return password_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    return password_context.verify(plain_password, hashed_password)

