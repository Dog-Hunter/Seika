import yandex_music as ym


class Player:
    def __init__(self, client: ym.ClientAsync):
        self.client = client
        self.current_track = None
        self.current_track_info = None
        self.queue = []
        self.station_id = None
        self.station_from = None

    async def search_track(self, query):
        search_result = await self.client.search(query)
        search_result = search_result.best.result
        return search_result

    async def download_track(self):
        await self.current_track.download_async(r'FF/track.mp3')

    async def get_track_info(self, track):
        track_name = track.title
        try:
            if len(track.artists) > 1:
                artist = ', '.join([i.name for i in track.artists])
            else:
                artist = track.artists[0].name
        except:
            artist = 'I don\'t give a fuck who are they'
        album = track.albums[0].title
        return f'{artist} - {track_name} ({album})'

    async def play(self):
        self.current_track = self.queue.pop(0)
        self.current_track_info = await self.get_track_info(self.current_track)
        await self.download_track()

    async def next(self):
        self.current_track = self.queue.pop(0)
        self.download_track()

    async def playlist(self, playlist_id=3):
        tracks = (await self.client.users_playlists(playlist_id)).tracks
        tracks = [i.track for i in tracks]
        self.queue = tracks
