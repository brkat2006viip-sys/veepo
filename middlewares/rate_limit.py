from aiogram import BaseMiddleware
import time

class RateLimitMiddleware(BaseMiddleware):
    def __init__(self, limit=1.0):
        self.limit = limit
        self._users = {}

    async def __call__(self, handler, event, data):
        uid = getattr(event.from_user, "id", None)
        now = time.time()
        last = self._users.get(uid, 0)
        if now - last < self.limit:
            # drop or add delay
            return
        self._users[uid] = now
        return await handler(event, data)
