import os
import discord
import pafy
import asyncio
from MusicPlayer import MusicPlayer
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
client = commands.Bot(command_prefix = '>')
music_players = {}
pafy.set_api_key(os.getenv('YOUTUBE_KEY'))

@client.event
async def on_ready():
    print('Skoip Skoip')

async def join(ctx):
    p = await MusicPlayer.create(ctx.message)
    if p:
        music_players[ctx.guild.id] = p
    return p
    
@client.command(pass_context=True, aliases=['l'])
async def leave(ctx):
    p = music_players.get(ctx.guild.id)
    if p:
        await p.leave()
        music_players.pop(ctx.guild.id)

@client.command(pass_context=True, aliases=['p'])
async def play(ctx, url):
    music_player = music_players.get(ctx.guild.id)
    songs = []
    if not music_player:
        music_player = await join(ctx)
    if 'playlist' in url:
        playlist = pafy.get_playlist2(url)
        songs = [song for song in playlist]
    else:
        song = pafy.new(url)
        songs.append(song)
    await music_player.queue_songs(songs)

@client.command(pass_context=True, aliases=['s'])
async def skip(ctx):
    music_player = music_players.get(ctx.guild.id)
    if not music_player:
        music_player = await join(ctx)
    await music_player.skip()
    
client.run(os.getenv('APP_KEY'))
