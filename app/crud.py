from sqlalchemy.future import select
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from app import models
from typing import Optional

async def get_or_create_user(session: AsyncSession, telegram_id: int, username: Optional[str] = None):
    q = await session.execute(select(models.User).where(models.User.telegram_id == telegram_id))
    user = q.scalars().first()
    if user:
        return user
    user = models.User(telegram_id=telegram_id, username=username)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

async def save_user_setting(session: AsyncSession, user_id: int, key: str, value: str, encrypted: bool = False):
    setting = models.UserSetting(user_id=user_id, key=key, value=value, encrypted=encrypted)
    session.add(setting)
    await session.commit()
    await session.refresh(setting)
    return setting

async def get_user_setting(session: AsyncSession, user_id: int, key: str):
    q = await session.execute(select(models.UserSetting).where(models.UserSetting.user_id==user_id, models.UserSetting.key==key))
    return q.scalars().first()

async def create_project(session: AsyncSession, user_id: int, name: str, path: str, zip_path: str = None):
    p = models.Project(user_id=user_id, name=name, path=path, zip_path=zip_path)
    session.add(p)
    await session.commit()
    await session.refresh(p)
    return p

async def log_operation(session: AsyncSession, user_id: int, project_id: int, action: str, detail: str = None):
    op = models.OperationLog(user_id=user_id, project_id=project_id, action=action, detail=detail)
    session.add(op)
    await session.commit()
    await session.refresh(op)
    return op
