from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault


async def set_commands(bot: Bot):
    commands = [
        BotCommand(
            command='absence',
            description='record your absenteeism'
        ),
        BotCommand(
            command='timetable',
            description='I think U understand it)'
        )
    ]
    await bot.set_my_commands(commands, BotCommandScopeDefault())