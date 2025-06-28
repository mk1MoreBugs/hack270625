from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import bcrypt
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_session
from app.models import User, UserRole
from app.crud import CRUDUser
from app.config import settings

# Настройки JWT
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 минут
REFRESH_TOKEN_EXPIRE_DAYS = 30    # 30 дней
ALGORITHM = "HS256"

# OAuth2 scheme для получения токена из заголовка
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def get_password_hash(password: str) -> str:
    """Создает хеш пароля"""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode(), salt).decode()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверяет соответствие пароля хешу"""
    return bcrypt.checkpw(
        plain_password.encode(),
        hashed_password.encode()
    )


def create_token(data: Dict[str, Any], expires_delta: timedelta) -> str:
    """Создает JWT токен"""
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.secret_key, algorithm=ALGORITHM)


def create_access_token(user_id: int, role: UserRole) -> str:
    """Создает access token"""
    return create_token(
        {"sub": str(user_id), "role": role.value},
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )


def create_refresh_token(user_id: int) -> str:
    """Создает refresh token"""
    return create_token(
        {"sub": str(user_id), "type": "refresh"},
        timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_async_session)
) -> User:
    """Получает текущего пользователя по токену"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
        if user_id is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    
    user_crud = CRUDUser(User)
    user = await user_crud.get(db, user_id)
    
    if user is None:
        raise credentials_exception
    
    return user


def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """Проверяет что пользователь активен"""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    return current_user


def check_role_access(allowed_roles: list[UserRole]):
    """Декоратор для проверки роли пользователя"""
    async def role_checker(current_user: User = Depends(get_current_active_user)):
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Operation not permitted"
            )
        return current_user
    return role_checker


# Предопределенные проверки ролей
get_current_buyer = check_role_access([UserRole.BUYER])
get_current_developer = check_role_access([UserRole.DEVELOPER])
get_current_admin = check_role_access([UserRole.ADMIN])

# Комбинированные проверки ролей
get_current_staff = check_role_access([UserRole.ADMIN])
get_current_business = check_role_access([UserRole.DEVELOPER, UserRole.ADMIN]) 