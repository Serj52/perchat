from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import models


async def get_user_by_mail(email: EmailStr, session: AsyncSession):
    async with session.begin():
        user = await session.execute(select(models.User).filter_by(email=email))
        return user.scalar()


async def get_user_by_id(user_id: int, session: AsyncSession):
    async with session.begin():
        user = await session.execute(select(models.User).filter_by(id=user_id))
        return user.scalar()


async def create_user(name: str, hashed_password: str, email: EmailStr,
                      session: AsyncSession):
    async with session.begin():
        db_user = models.User(name=name, password=hashed_password, email=email)
        session.add(db_user)
        return db_user
