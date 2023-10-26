import asyncio
from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from datetime import datetime
from datetime import timedelta
from sqlalchemy import select
from database import async_session
from database.models import User
import requests

router = Router()

async def get_schedule(days=1, subgroup=1):
    url = 'https://timetable.magtu.ru/api/v2/groups/31/schedule'
    data = requests.get(url)
    data = data.json()['schedule']
    if (datetime.now().isocalendar()[1]%2==0):
        timetable = data[1]['days']
    else:
        timetable = data[0]['days']

    today = datetime.now().isocalendar()[2]-1
    my_timetable = timetable[today:today+days]

    ans = []
    for i in my_timetable:
        s = ''
        for j in i['events']:
            s += f"{j['event_index']}. {j['course']} ({j['type']}) - {j['reverse']} Ауд. {j['location']}\n"
        ans.append(s)

    return ans

@router.message(Command('timetable'))
async def timetable_cmd(message: Message, command: CommandObject):
    async with async_session() as session:
        q = select(User).where(User.telegram_id == message.from_user.id)
        result = await session.execute(q)
        subgroup = result.scalars().one().subgroup
    timetable = await get_schedule(int(command.args), subgroup)
    for i in range(len(timetable)):
        await message.answer(f'Расписание за {datetime.strftime(datetime.today() + timedelta(days=i),"%d.%m.%y")}')
        await message.answer(timetable[i])