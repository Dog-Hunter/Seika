import asyncio

from aiogram import Dispatcher, Bot
from aiogram.enums import ParseMode
from sqlalchemy.ext.asyncio import create_async_engine
from database.models import Base
from database import engine
from handlers.users import router

token = ''

dp = Dispatcher()
dp.include_router(router)

bot = Bot(token, parse_mode=ParseMode.HTML)

async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await dp.start_polling(bot)

asyncio.run(main())
