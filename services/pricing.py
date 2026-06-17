"""Pricing service for Stars and Premium."""
from __future__ import annotations
from decimal import Decimal
from database.repositories.settings import SettingsRepository

class PricingService:
    def __init__(self, settings_repo: SettingsRepository) -> None:
        self.settings_repo = settings_repo
    async def stars_amount(self, quantity: int) -> Decimal:
        price = Decimal(await self.settings_repo.get_value("star_price", "0"))
        return price * quantity
    async def premium_amount(self, months: int) -> Decimal:
        key = {1: "premium_1m", 3: "premium_3m", 12: "premium_12m"}[months]
        return Decimal(await self.settings_repo.get_value(key, "0"))
