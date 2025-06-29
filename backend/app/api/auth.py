from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_session
from app.models import User, UserRole
from app.crud import CRUDUser
from app.schemas import (
    TokenResponse, UserLogin, BuyerRegister,
    DeveloperRegister, AdminRegister, RefreshToken,
    UserCreate, UserRead, Token
)
from app.security import (
    get_password_hash, verify_password,
    create_access_token, create_refresh_token
)
import jwt
from app.config import settings
from typing import Optional

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)


@router.post(
    "/register",
    response_model=UserRead,
    summary="Регистрация нового пользователя",
    description="""
    Регистрация нового пользователя в системе.
    
    Доступные роли:
    - buyer: Покупатель
    - developer: Застройщик (требуется указать company_name)
    - admin: Администратор
    
    Поле company_name является обязательным только для роли developer.
    """,
    responses={
        400: {"description": "Неверные данные регистрации"},
        422: {"description": "Ошибка валидации"}
    }
)
async def register(
    user_data: UserCreate,
    session: AsyncSession = Depends(get_async_session)
) -> UserRead:
    """Регистрация нового пользователя"""
    # Проверяем, что company_name указано для developer
    if user_data.role == UserRole.DEVELOPER and not user_data.company_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Для роли developer необходимо указать company_name"
        )
    
    # Проверяем, что company_name не указано для других ролей
    if user_data.role != UserRole.DEVELOPER and user_data.company_name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Поле company_name доступно только для роли developer"
        )

    # Проверяем существование пользователя
    existing_user = await session.get(User, user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким email уже существует"
        )

    # Создаем нового пользователя
    hashed_password = get_password_hash(user_data.password)
    user = User(
        email=user_data.email,
        hashed_password=hashed_password,
        display_name=user_data.display_name,
        role=user_data.role,
        phone=user_data.phone,
        company_name=user_data.company_name if user_data.role == UserRole.DEVELOPER else None
    )
    
    session.add(user)
    await session.commit()
    await session.refresh(user)
    
    return UserRead.from_orm(user)


@router.post(
    "/login",
    response_model=Token,
    summary="Вход в систему",
    description="Авторизация пользователя и получение токена доступа",
    responses={
        401: {"description": "Неверный email или пароль"},
        400: {"description": "Неактивный пользователь"},
        422: {"description": "Ошибка валидации"}
    }
)
async def login(
    email: str,
    password: str,
    session: AsyncSession = Depends(get_async_session)
) -> Token:
    """Вход пользователя"""
    user_crud = CRUDUser(User)
    
    # Получаем пользователя по email
    user = await user_crud.get_by_email(session, email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль"
        )
    
    # Проверяем пароль
    if not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль"
        )
    
    # Проверяем что пользователь активен
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Неактивный пользователь"
        )
    
    access_token = create_access_token(data={"sub": user.email, "role": user.role})
    return Token(access_token=access_token, token_type="bearer")


@router.post(
    "/refresh",
    response_model=TokenResponse,
    summary="Обновление токенов",
    description="Обновление токенов доступа по refresh токену",
    responses={
        400: {"description": "Неверный тип токена"},
        401: {"description": "Недействительный токен"},
        422: {"description": "Ошибка валидации"}
    }
)
async def refresh_tokens(
    token_data: RefreshToken,
    session: AsyncSession = Depends(get_async_session)
):
    """Обновление токенов"""
    try:
        # Декодируем refresh token
        payload = jwt.decode(
            token_data.refresh_token,
            settings.secret_key,
            algorithms=["HS256"]
        )
        
        # Проверяем что это refresh token
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Неверный тип токена"
            )
        
        user_id = int(payload.get("sub"))
        
        # Получаем пользователя
        user_crud = CRUDUser(User)
        user = await user_crud.get(session, user_id)
        
        if not user or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Недействительный токен"
            )
        
        # Создаем новые токены
        access_token = create_access_token(user.id, user.role)
        refresh_token = create_refresh_token(user.id)
        
        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token
        )
        
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Недействительный токен"
        ) 