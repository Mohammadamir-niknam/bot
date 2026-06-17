"""SQLAlchemy 2.x ORM models for telBotPropo."""
from __future__ import annotations
from decimal import Decimal
from sqlalchemy import BigInteger, Boolean, ForeignKey, Integer, Numeric, String, Text, UniqueConstraint, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.base import Base, TimestampMixin
from database.enums import AdminRole, OrderStatus, OrderType, TicketMessageSender, TicketStatus, TransactionStatus, TransactionType, UserStatus

class User(TimestampMixin, Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    username: Mapped[str | None] = mapped_column(String(64))
    full_name: Mapped[str | None] = mapped_column(String(255))
    status: Mapped[UserStatus] = mapped_column(String(32), default=UserStatus.ACTIVE)
    referral_code: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    referred_by_id: Mapped[int | None] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"))
    referral_points: Mapped[int] = mapped_column(Integer, default=0)
    wallet: Mapped["Wallet"] = relationship(back_populates="user", cascade="all, delete-orphan")

class Wallet(TimestampMixin, Base):
    __tablename__ = "wallets"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), unique=True)
    balance: Mapped[Decimal] = mapped_column(Numeric(18, 2), default=0)
    user: Mapped[User] = relationship(back_populates="wallet")

class Transaction(TimestampMixin, Base):
    __tablename__ = "transactions"
    id: Mapped[int] = mapped_column(primary_key=True)
    wallet_id: Mapped[int] = mapped_column(ForeignKey("wallets.id", ondelete="CASCADE"), index=True)
    amount: Mapped[Decimal] = mapped_column(Numeric(18, 2))
    type: Mapped[TransactionType] = mapped_column(String(32))
    status: Mapped[TransactionStatus] = mapped_column(String(32), default=TransactionStatus.COMPLETED)
    description: Mapped[str | None] = mapped_column(Text)
    metadata_json: Mapped[dict | None] = mapped_column(JSON)

class Order(TimestampMixin, Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    type: Mapped[OrderType] = mapped_column(String(32))
    status: Mapped[OrderStatus] = mapped_column(String(32), default=OrderStatus.PENDING, index=True)
    quantity: Mapped[int | None] = mapped_column(Integer)
    premium_plan_months: Mapped[int | None] = mapped_column(Integer)
    amount: Mapped[Decimal] = mapped_column(Numeric(18, 2))
    receipt_file_id: Mapped[str | None] = mapped_column(String(255))
    notes: Mapped[str | None] = mapped_column(Text)

class Referral(TimestampMixin, Base):
    __tablename__ = "referrals"
    __table_args__ = (UniqueConstraint("invited_user_id", name="uq_referral_invited_once"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    inviter_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    invited_user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    points_awarded: Mapped[int] = mapped_column(Integer, default=0)

class ReferralReward(TimestampMixin, Base):
    __tablename__ = "referral_rewards"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    threshold: Mapped[int] = mapped_column(Integer)
    reward_value: Mapped[str] = mapped_column(String(255))
    claimed: Mapped[bool] = mapped_column(Boolean, default=False)

class Ticket(TimestampMixin, Base):
    __tablename__ = "tickets"
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    subject: Mapped[str] = mapped_column(String(255))
    status: Mapped[TicketStatus] = mapped_column(String(32), default=TicketStatus.OPEN, index=True)

class TicketMessage(TimestampMixin, Base):
    __tablename__ = "ticket_messages"
    id: Mapped[int] = mapped_column(primary_key=True)
    ticket_id: Mapped[int] = mapped_column(ForeignKey("tickets.id", ondelete="CASCADE"), index=True)
    sender: Mapped[TicketMessageSender] = mapped_column(String(32))
    sender_telegram_id: Mapped[int | None] = mapped_column(BigInteger)
    text: Mapped[str | None] = mapped_column(Text)
    photo_file_id: Mapped[str | None] = mapped_column(String(255))

class AdminUser(TimestampMixin, Base):
    __tablename__ = "admin_users"
    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    role: Mapped[AdminRole] = mapped_column(String(32), default=AdminRole.SUPPORT)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

class Settings(TimestampMixin, Base):
    __tablename__ = "settings"
    key: Mapped[str] = mapped_column(String(128), primary_key=True)
    value: Mapped[str] = mapped_column(Text, default="")
    description: Mapped[str | None] = mapped_column(Text)

class AuditLog(TimestampMixin, Base):
    __tablename__ = "audit_logs"
    id: Mapped[int] = mapped_column(primary_key=True)
    admin_telegram_id: Mapped[int] = mapped_column(BigInteger, index=True)
    action: Mapped[str] = mapped_column(String(128), index=True)
    entity_type: Mapped[str] = mapped_column(String(128))
    entity_id: Mapped[str | None] = mapped_column(String(128))
    before: Mapped[dict | None] = mapped_column(JSON)
    after: Mapped[dict | None] = mapped_column(JSON)
