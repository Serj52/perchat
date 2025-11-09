from passlib.context import CryptContext
from pydantic import EmailStr
from jose import jwt
from datetime import datetime, timedelta, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from app.config import AUTH_SETTINGS

from app.users.crud import get_user_by_mail


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=366)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(to_encode, AUTH_SETTINGS['SECRET_KEY'], algorithm=AUTH_SETTINGS['ALGORITHM'])
    return encode_jwt


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


async def authenticate_user(email: EmailStr, password: str, session: AsyncSession):
    user = await get_user_by_mail(email=email, session=session)
    if not user or verify_password(plain_password=password, hashed_password=user.password) is False:
        return None
    return user
