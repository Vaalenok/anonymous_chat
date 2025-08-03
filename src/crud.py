from sqlalchemy import select

from database import connection
from src.model import User, Status


@connection()
async def create_user(new_user: User, session):
    session.add(new_user)
    await session.flush()
    return new_user


@connection(commit=False)
async def get_user(user_id: int, session):
    result = await session.execute(select(User).filter_by(user_id=user_id))
    user = result.scalars().first()
    return user


@connection()
async def update_user(new_user: User, session):
    await session.merge(new_user)
    await session.flush()


@connection(commit=False)
async def get_searching_users(session):
    result = await session.execute(select(User).filter_by(status=Status.SEARCH))
    users = result.scalars().all()
    return users
