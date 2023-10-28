import asyncio

from aiogram import Dispatcher, Bot
from aiogram.enums import ParseMode
from database.models import Base
from database import engine
from handlers.users import create_user
from handlers.timetable import timetable
from handlers.thuja import add_absences
import config
import commands

token = '6514646017:AAEpN-y8UhG3tyN0RxQXvnG-leFd9l0uU_g'

dp = Dispatcher()
dp.include_router(create_user.router)
dp.include_router(timetable.router)
dp.include_router(add_absences.router)

bot = Bot(token, parse_mode=ParseMode.HTML)

async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await commands.set_commands(bot)
    await dp.start_polling(bot)

asyncio.run(main())
