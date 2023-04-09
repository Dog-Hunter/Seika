import os
import discord
from config import DISCORD_TOKEN
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix='/', intents=intents)

@client.event
async def on_ready():
    for i in os.listdir('./cogs'):
        if '.py' in i:
            await client.load_extension(f'cogs.{i[:-3]}')
    print('All loadings complete')

client.run(DISCORD_TOKEN)