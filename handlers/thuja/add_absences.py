import asyncio
from datetime import datetime

from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import Command
from sqlalchemy import select, insert
from database import async_session
from database.models import User, Absence

router = Router()

class Absences(StatesGroup):
    a = State()
    end = State()

@router.message(Command('absence'))
async def add_absences(message: Message, state: FSMContext):
    await message.answer('Tell me what happend to U again?...')
    await asyncio.sleep(0.3)
    await message.answer('Doesn\'t matter, so when you\'re gone?')
    await asyncio.sleep(0.2)
    await message.answer('Hint: my favorite format is DD-MM-YYYY. I think hint is clear?')
    await state.set_state(Absences.a)

@router.message(Absences.a)
async def add_date(message: Message, state: FSMContext):
    await state.update_data(date=message.text)
    await message.answer('Well, now tell my... WHAT THE FUCK DO YOU THINK YOU CAN SKIP?')
    await state.set_state(Absences.end)

@router.message(Absences.end)
async def end_absences(message: Message, state: FSMContext):
    async with async_session() as session:
        q = select(User).where(User.telegram_id == message.from_user.id)
        result = await session.execute(q)
    data = await (state.get_data())
    data = [{
        'user_id':result.scalars().one().id,
        'data': datetime.strptime(data['date'], '%d-%m-%Y').date(),
        'text': message.text
    }]
    async with async_session() as session:
        await session.execute(
            insert(Absence),
            data
        )
        await session.commit()
    await message.answer('Great, now get lost')

