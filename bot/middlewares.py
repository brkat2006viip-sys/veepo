from aiogram import BaseMiddleware, types
from aiogram.types import Message
from app.database import AsyncSessionLocal
from app.crud import get_or_create_user

class DBSessionMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        async with AsyncSessionLocal() as session:
            data["db"] = session
            try:
                if isinstance(event, Message):
                    user = await get_or_create_user(session, event.from_user.id, getattr(event.from_user, "username", None))
                    data["db_user"] = user
            except Exception:
                # don't block handler creation due to DB issues
                data["db_user"] = None
            return await handler(event, data)
