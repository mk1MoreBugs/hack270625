from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_async_session
from app.models import User, UserRole
from app.crud import CRUDUser
from app.schemas import (
    TokenResponse, UserLogin, BuyerRegister,
    DeveloperRegister, AdminRegister, RefreshToken
)
from app.security import (
    get_password_hash, verify_password,
    create_access_token, create_refresh_token
)
import jwt
from app.config import settings

router = APIRouter(
    prefix="/api/v1/auth",
    tags=["auth"]
)


@router.post(
    "/register/buyer",
    response_model=TokenResponse,
    summary="Регистрация покупателя",
    description="Регистрация нового пользователя с ролью покупателя",
    responses={
        400: {"description": "Email уже зарегистрирован"},
        422: {"description": "Ошибка валидации"}
    }
)
async def register_buyer(
    user_data: BuyerRegister,
    db: AsyncSession = Depends(get_async_session)
):
    """Регистрация покупателя"""
    user_crud = CRUDUser(User)
    
    # Проверяем, не существует ли уже пользователь с таким email
    if await user_crud.get_by_email(db, user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email уже зарегистрирован"
        )
    
    # Создаем пользователя
    hashed_password = get_password_hash(user_data.password)
    user_dict = user_data.dict()
    user_dict["hashed_password"] = hashed_password
    del user_dict["password"]
    
    user = await user_crud.create(db, user_dict)
    
    # Создаем токены
    access_token = create_access_token(user.id, user.role)
    refresh_token = create_refresh_token(user.id)
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token
    )


@router.post(
    "/register/developer",
    response_model=TokenResponse,
    summary="Регистрация застройщика",
    description="Регистрация нового пользователя с ролью застройщика",
    responses={
        400: {
            "description": "Email уже зарегистрирован или застройщик с таким ИНН уже существует"
        },
        422: {"description": "Ошибка валидации"}
    }
)
async def register_developer(
    user_data: DeveloperRegister,
    db: AsyncSession = Depends(get_async_session)
):
    """Регистрация застройщика"""
    user_crud = CRUDUser(User)
    
    # Проверяем, не существует ли уже пользователь с таким email
    if await user_crud.get_by_email(db, user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email уже зарегистрирован"
        )
    
    # Проверяем, не существует ли уже застройщик с таким ИНН
    existing_developer = await user_crud.get_by_inn(db, user_data.inn)
    if existing_developer:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Застройщик с таким ИНН уже существует"
        )
    
    # Создаем пользователя
    hashed_password = get_password_hash(user_data.password)
    user_dict = user_data.dict()
    user_dict["hashed_password"] = hashed_password
    del user_dict["password"]
    
    user = await user_crud.create(db, user_dict)
    
    # Создаем токены
    access_token = create_access_token(user.id, user.role)
    refresh_token = create_refresh_token(user.id)
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token
    )


@router.post(
    "/register/admin",
    response_model=TokenResponse,
    summary="Регистрация администратора",
    description="Регистрация нового пользователя с ролью администратора",
    responses={
        400: {"description": "Email уже зарегистрирован"},
        422: {"description": "Ошибка валидации"}
    }
)
async def register_admin(
    user_data: AdminRegister,
    db: AsyncSession = Depends(get_async_session)
):
    """Регистрация администратора"""
    user_crud = CRUDUser(User)
    
    # Проверяем, не существует ли уже пользователь с таким email
    if await user_crud.get_by_email(db, user_data.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email уже зарегистрирован"
        )
    
    # Создаем пользователя
    hashed_password = get_password_hash(user_data.password)
    user_dict = user_data.dict()
    user_dict["hashed_password"] = hashed_password
    del user_dict["password"]
    
    user = await user_crud.create(db, user_dict)
    
    # Создаем токены
    access_token = create_access_token(user.id, user.role)
    refresh_token = create_refresh_token(user.id)
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token
    )


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Вход в систему",
    description="Аутентификация пользователя и получение токенов доступа",
    responses={
        401: {"description": "Неверный email или пароль"},
        400: {"description": "Неактивный пользователь"},
        422: {"description": "Ошибка валидации"}
    }
)
async def login(
    user_data: UserLogin,
    db: AsyncSession = Depends(get_async_session)
):
    """Вход пользователя"""
    user_crud = CRUDUser(User)
    
    # Получаем пользователя по email
    user = await user_crud.get_by_email(db, user_data.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный email или пароль"
        )
    
    # Проверяем пароль
    if not verify_password(user_data.password, user.hashed_password):
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
    
    # Создаем токены
    access_token = create_access_token(user.id, user.role)
    refresh_token = create_refresh_token(user.id)
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token
    )


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
    db: AsyncSession = Depends(get_async_session)
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
        user = await user_crud.get(db, user_id)
        
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