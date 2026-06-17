from __future__ import annotations
from database.models import Settings
from database.repositories.base import Repository

DEFAULT_SETTINGS = {
    "star_price": "0", "premium_1m": "0", "premium_3m": "0", "premium_12m": "0",
    "mandatory_channel": "", "mandatory_channel_enabled": "false", "maintenance_mode": "false",
    "proxy_url_1": "", "proxy_url_2": "", "proxy_url_3": "", "referral_point": "1",
    "gift_15": "", "gift_25": "", "gift_50": "", "gift_100": "",
    "support_username": "", "trust_text": "",
}
class SettingsRepository(Repository[Settings]):
    model = Settings
    async def get_value(self, key: str, default: str = "") -> str:
        row = await self.get(key); return row.value if row else default
    async def set_value(self, key: str, value: str, description: str | None = None) -> Settings:
        row = await self.get(key)
        if row is None:
            row = Settings(key=key, value=value, description=description); self.session.add(row)
        else:
            row.value = value; row.description = description or row.description
        await self.session.flush(); return row
