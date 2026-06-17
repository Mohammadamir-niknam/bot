"""Database enums for telBotPropo."""
from __future__ import annotations
from enum import StrEnum

class UserStatus(StrEnum):
    ACTIVE = "ACTIVE"; BLOCKED = "BLOCKED"
class AdminRole(StrEnum):
    SUPER_ADMIN = "SUPER_ADMIN"; ADMIN = "ADMIN"; SUPPORT = "SUPPORT"
class OrderType(StrEnum):
    STARS = "STARS"; PREMIUM = "PREMIUM"
class OrderStatus(StrEnum):
    PENDING = "Pending"; WAITING_PAYMENT = "WaitingPayment"; PAID = "Paid"; APPROVED = "Approved"; REJECTED = "Rejected"; COMPLETED = "Completed"
class TransactionType(StrEnum):
    CREDIT = "CREDIT"; DEBIT = "DEBIT"; ORDER_PAYMENT = "ORDER_PAYMENT"; REFUND = "REFUND"; ADMIN_ADJUSTMENT = "ADMIN_ADJUSTMENT"
class TransactionStatus(StrEnum):
    PENDING = "PENDING"; COMPLETED = "COMPLETED"; REJECTED = "REJECTED"
class TicketStatus(StrEnum):
    OPEN = "OPEN"; CLOSED = "CLOSED"
class TicketMessageSender(StrEnum):
    USER = "USER"; ADMIN = "ADMIN"
