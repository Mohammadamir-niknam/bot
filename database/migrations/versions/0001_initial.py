"""initial schema
Revision ID: 0001_initial
Revises: 
Create Date: 2026-06-17
"""
from __future__ import annotations
from alembic import op
import sqlalchemy as sa
revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table("users", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("telegram_id", sa.BigInteger(), nullable=False), sa.Column("username", sa.String(64)), sa.Column("full_name", sa.String(255)), sa.Column("status", sa.String(32), nullable=False), sa.Column("referral_code", sa.String(32), nullable=False), sa.Column("referred_by_id", sa.Integer()), sa.Column("referral_points", sa.Integer(), nullable=False), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False), sa.UniqueConstraint("telegram_id"), sa.UniqueConstraint("referral_code"))
    op.create_table("wallets", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("user_id", sa.Integer(), nullable=False), sa.Column("balance", sa.Numeric(18, 2), nullable=False), sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"), sa.UniqueConstraint("user_id"))
    op.create_table("settings", sa.Column("key", sa.String(128), primary_key=True), sa.Column("value", sa.Text(), nullable=False), sa.Column("description", sa.Text()), sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False), sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False))

def downgrade() -> None:
    op.drop_table("settings"); op.drop_table("wallets"); op.drop_table("users")
