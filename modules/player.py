import yandex_music as ym

import config

config.YANDEX_MUSIC_TOKEN


class Player:
    def __init__(self, client):
        self.client = client
        self.current_track = None
        self.current_track_info = None
        self.queue = []

    async def search_track(self, query):
        search_result = await self.client.search(query)
        search_result = search_result.best.result
        return search_result

    async def download_track(self):
        await self.current_track.download_async(r'FF/track.mp3')

    async def get_track_info(self, track):
        track_name = track.title
        if len(self.current_track.artists) > 1:
            artist = ', '.join([i.name for i in self.current_track.artists])
        else:
            artist = self.current_track.artists[0].name
        album = self.current_track.albums[0].title
        return f'{artist} - {track_name} ({album})'

    async def play(self):
        self.current_track = self.queue.pop(0)
        self.current_track_info = await self.get_track_info(self.current_track)
        await self.download_track()

    async def next(self):
        self.current_track = self.queue.pop(0)
        self.download_track()

    async def clear_queue(self):
        self.queue.clear()