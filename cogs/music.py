import asyncio

import discord
from discord.ext import commands
from yandex_music import ClientAsync

from config import YANDEX_MUSIC_TOKEN
from modules.player import Player


class Music(commands.Cog):
    def __init__(self, client, player):
        self.client = client
        self.player = player
        self.vc = None
        self.is_paused = True

    @commands.command(name='music')
    async def music_cmd(self, ctx, *args):
        track = await self.player.search_track(' '.join(args))
        self.player.queue.append(track)
        if self.player.current_track is not None:
            track_info = await self.player.get_track_info(track)
            await ctx.reply(f'Ok, I\'ll add to list: {track_info}')
        if self.player.current_track is None:
            await self._connect(ctx)

    @commands.command(name='playlist')
    async def playlist_cmd(self, ctx, *args):
        await self.player.playlist()
        await self._connect(ctx)

    @commands.command(name='pause')
    async def pause_cmd(self, ctx, ):
        if ctx.voice_client.is_paused():
            return
        ctx.voice_client.pause()

    @commands.command(name='resume')
    async def resume_cmd(self, ctx, ):
        if ctx.voice_client.is_playing():
            return
        ctx.voice_client.resume()

    @commands.command(name='clear')
    async def clear_cmd(self, ctx, ):
        self.player.queue.clear()
        await ctx.reply('OK, the concert is over for today. Finish your nao and go home.')

    async def _connect(self, ctx):
        if ctx.author.voice is None:
            ctx.reply('Fuck you! Who do I gather a group for if there are no listeners?!')
            return
        if ctx.voice_client is None:
            channel = ctx.message.author.voice.channel
            vc = await channel.connect()
        else:
            vc = ctx.voice_client

        while len(self.player.queue) > 0:
            await self.player.play()
            await ctx.send(f'Playing {self.player.current_track_info}')
            vc.play(discord.FFmpegPCMAudio(executable=r"FF/ffmpeg.exe", source=r'FF/track.mp3'))
            while vc.is_playing() or vc.is_paused():
                await asyncio.sleep(1)
        self.player.current_track = None
        vc.stop()
        await vc.disconnect()


async def setup(client):
    c = await (ClientAsync(YANDEX_MUSIC_TOKEN)).init()
    c = Player(c)
    await client.add_cog(Music(client, c))
