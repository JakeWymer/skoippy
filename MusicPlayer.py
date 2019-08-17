import ffmpeg
import discord
import os
import asyncio
import sys

class MusicPlayer:
    @classmethod
    async def create(cls, message_ctx):
        self = cls()
        self.guild_id = message_ctx.guild.id
        self.text_channel = message_ctx.channel
        welcome_text = 'You must be in a voice channel to use Skoip Bot!'
        voice_ctx = message_ctx.author.voice
        
        if voice_ctx:
            self.player = await voice_ctx.channel.connect()
            self.queue = []
            welcome_text = 'Skoip Skoip'
            await self.send_message(welcome_text)
            return self
        
        await self.send_message(welcome_text)
        return None

    async def leave(self):
        await self.player.disconnect()
        self.queue = []

    async def queue_songs(self, songs):
        self.queue = songs + self.queue
        await self.send_message(f'{len(songs)} songs added to queue')
        if not self.player.is_playing():
            await self._play_music()

    def play_next(self, e=None):
        asyncio.run_coroutine_threadsafe(self._play_music(), self.player.loop)

    async def skip(self):
        await self.send_message('Skoipping...')
        await self._play_music()

    async def _play_music(self):
        if len(self.queue) == 0:
            return
        filepath = f'downloads/{self.guild_id}.mp3'
        if not os.path.exists(filepath):
            f = open(filepath, 'x')
        song = self.queue.pop()
        song_title = song.title
        bestaudio = song.getbestaudio()
        url = bestaudio.url
        stream = ffmpeg.input(url)
        stream = ffmpeg.output(stream, filepath)
        stream = ffmpeg.overwrite_output(stream)
        ffmpeg.run(stream)
        message_text = f'Now playing {song_title}'
        await self.send_message(message_text)
        self.player.play(discord.FFmpegPCMAudio(filepath), after=self.play_next)

    async def send_message(self, message):
        await self.text_channel.send(message)
