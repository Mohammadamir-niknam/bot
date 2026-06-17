from aiogram import Router
from handlers.common.start import router as start_router
from handlers.user.menu import router as user_router
from handlers.orders.orders import router as orders_router
from handlers.wallet.wallet import router as wallet_router
from handlers.referral.referral import router as referral_router
from handlers.support.support import router as support_router

def setup_routers() -> list[Router]:
    return [start_router, user_router, orders_router, wallet_router, referral_router, support_router]
