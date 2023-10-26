import asyncio
import time

from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from aiogram import Router
from aiogram.filters import CommandStart
from sqlalchemy import select, insert

from database import async_session
from database.models import User

router = Router()


class CreateUser(StatesGroup):
    send_surname_and_name = State()
    send_subgroup = State()


@router.message(CommandStart())
async def start_cmd(message: Message, state: FSMContext):
    await message.answer('Hi! My name is Seika\n'
                         'Let\'s fill some data')
    if (await is_user_exsist(message.from_user.id)):
        await asyncio.sleep(0.5)
        await message.answer('Stop... Fuck!.. So, where do such idiots come from? I already have you data', reply_markup=main_keyboard.keyboard)
        await state.clear()
    else:
        await message.answer('Samurai, what\'s your name')
        await state.set_state(CreateUser.send_surname_and_name)


@router.message(CreateUser.send_surname_and_name)
async def send_subgroup(message: Message, state: FSMContext):
    await state.update_data(fio=message.text)
    await message.answer('Now tell me your subgroup')
    await state.set_state(CreateUser.send_subgroup)


@router.message(CreateUser.send_subgroup)
async def end_cmd(message: Message, state: FSMContext):
    data = await (state.get_data())
    data = [
        {
            'telegram_id': message.from_user.id,
            'telegram_name': message.from_user.username,
            'surname': data['fio'].split()[0],
            'name': data['fio'].split()[-1],
            'subgroup': int(message.text.lower())
        }
    ]
    async with async_session() as session:
        await session.execute(
            insert(User),
            data
        )
        await session.commit()
    await message.answer('Good girl, it turns out you\'re not that dumb, congratulations', reply_markup=main_keyboard.keyboard)
    await state.clear()


async def is_user_exsist(telegram_id):
    async with async_session() as session:
        q = select(User).where(User.telegram_id == telegram_id)
        result = await session.execute(q)
        if (len(result.fetchall()) == 0):
            return False
    return True
