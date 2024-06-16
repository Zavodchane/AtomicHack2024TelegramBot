from typing import Type

from sqlalchemy.ext.asyncio import AsyncSession

from src.user.models import User


async def get_user(
    user_id: str,
    session: AsyncSession,
) -> User | Type[User]:
    user = await session.get(User, user_id)
    if user is None:
        await create_user(user_id, session)
    return user


async def create_user(
    user_id: str,
    session: AsyncSession,
) -> User:
    user: User = User(id=user_id)
    session.add(user)
    await session.commit()
    return user
