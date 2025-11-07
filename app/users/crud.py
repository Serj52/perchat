from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.users import models


async def get_user(email: EmailStr, session: AsyncSession):
    async with session.begin():
        user = await session.execute(select(models.Users).filter_by(email=email))
        return user.scalar()