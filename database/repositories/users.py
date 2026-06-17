from __future__ import annotations
import secrets
from sqlalchemy import select
from database.models import User, Wallet
from database.repositories.base import Repository

class UserRepository(Repository[User]):
    model = User
    async def get_by_telegram_id(self, telegram_id: int) -> User | None:
        return await self.session.scalar(select(User).where(User.telegram_id == telegram_id))
    async def get_or_create(self, telegram_id: int, username: str | None, full_name: str | None) -> User:
        user = await self.get_by_telegram_id(telegram_id)
        if user:
            user.username = username; user.full_name = full_name
            return user
        user = User(telegram_id=telegram_id, username=username, full_name=full_name, referral_code=secrets.token_urlsafe(8))
        self.session.add(user); await self.session.flush()
        self.session.add(Wallet(user_id=user.id))
        await self.session.flush()
        return user
