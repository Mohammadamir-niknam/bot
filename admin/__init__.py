from aiogram import Router
from admin.handlers.panel import router as panel_router

def setup_admin_routers() -> list[Router]:
    return [panel_router]
