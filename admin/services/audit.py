from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
from database.models import AuditLog
class AuditService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
    async def log(self, admin_telegram_id: int, action: str, entity_type: str, entity_id: str | None = None, before: dict | None = None, after: dict | None = None) -> AuditLog:
        row = AuditLog(admin_telegram_id=admin_telegram_id, action=action, entity_type=entity_type, entity_id=entity_id, before=before, after=after)
        self.session.add(row); await self.session.flush(); return row
