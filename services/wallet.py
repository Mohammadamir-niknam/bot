"""Wallet accounting service."""
from __future__ import annotations
from decimal import Decimal
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from database.enums import TransactionStatus, TransactionType
from database.models import Transaction, Wallet

class WalletService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session
    async def get_wallet(self, user_id: int) -> Wallet:
        wallet = await self.session.scalar(select(Wallet).where(Wallet.user_id == user_id).with_for_update())
        if wallet is None:
            wallet = Wallet(user_id=user_id); self.session.add(wallet); await self.session.flush()
        return wallet
    async def credit(self, user_id: int, amount: Decimal, description: str) -> Wallet:
        wallet = await self.get_wallet(user_id); wallet.balance += amount
        self.session.add(Transaction(wallet_id=wallet.id, amount=amount, type=TransactionType.CREDIT, status=TransactionStatus.COMPLETED, description=description))
        await self.session.flush(); return wallet
    async def debit(self, user_id: int, amount: Decimal, description: str) -> bool:
        wallet = await self.get_wallet(user_id)
        if wallet.balance < amount:
            return False
        wallet.balance -= amount
        self.session.add(Transaction(wallet_id=wallet.id, amount=amount, type=TransactionType.DEBIT, status=TransactionStatus.COMPLETED, description=description))
        await self.session.flush(); return True
