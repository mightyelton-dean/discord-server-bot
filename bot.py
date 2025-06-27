import os
import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
import yt_dlp
from PIL import Image, ImageDraw, ImageFont
import asyncio

TOKEN = os.getenv('DISCORD_TOKEN')  # Replace with your token or use .env
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

# --- Music Player ---
# Music queue and helpers
guild_queues = {}

def get_queue(ctx):
    return guild_queues.setdefault(ctx.guild.id, [])

@bot.command()
async def play(ctx, url: str):
    queue = get_queue(ctx)
    queue.append(url)
    if not ctx.voice_client or not ctx.voice_client.is_playing():
        await _play_next(ctx)
    else:
        await ctx.send(f"Added to queue: {url}")

async def _play_next(ctx):
    queue = get_queue(ctx)
    if not queue:
        await ctx.send("Queue is empty.")
        return
    url = queue[0]
    if ctx.author.voice is None and ctx.voice_client is None:
        await ctx.send("You must be in a voice channel to use this command.")
        return
    channel = ctx.author.voice.channel if ctx.author.voice else ctx.voice_client.channel
    if ctx.voice_client is None:
        await channel.connect()
    elif ctx.voice_client.channel != channel:
        await ctx.voice_client.move_to(channel)
    ydl_opts = {'format': 'bestaudio', 'noplaylist': True, 'quiet': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        audio_url = info['url']
    source = FFmpegPCMAudio(audio_url)
    def after_playing(e=None):
        queue.pop(0)
        fut = asyncio.run_coroutine_threadsafe(_play_next(ctx), bot.loop)
        try:
            fut.result()
        except Exception:
            pass
    ctx.voice_client.stop()
    ctx.voice_client.play(source, after=after_playing)
    await ctx.send(f'Now playing: {info.get("title", url)}')

@bot.command()
async def pause(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.pause()
        await ctx.send("Paused.")
    else:
        await ctx.send("Nothing is playing.")

@bot.command()
async def resume(ctx):
    if ctx.voice_client and ctx.voice_client.is_paused():
        ctx.voice_client.resume()
        await ctx.send("Resumed.")
    else:
        await ctx.send("Nothing is paused.")

@bot.command()
async def skip(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send("Skipped.")
    else:
        await ctx.send("Nothing is playing.")

@bot.command()
async def queue(ctx):
    queue = get_queue(ctx)
    if not queue:
        await ctx.send("Queue is empty.")
    else:
        msg = '\n'.join(f"{i+1}. {url}" for i, url in enumerate(queue))
        await ctx.send(f"Current queue:\n{msg}")

@bot.command()
async def clear(ctx):
    queue = get_queue(ctx)
    queue.clear()
    await ctx.send("Queue cleared.")

@bot.command()
async def stop(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        get_queue(ctx).clear()
        await ctx.send("Stopped, disconnected, and cleared queue.")

# --- Ping All ---
@bot.command()
async def pingall(ctx):
    if not ctx.guild:
        await ctx.send("This command can only be used in a server.")
        return
    mentions = ' '.join(member.mention for member in ctx.guild.members if not member.bot)
    await ctx.send(f"{mentions}")

# --- Download Video ---
@bot.command()
async def download(ctx, url: str):
    await ctx.send("Downloading video...")
    ydl_opts = {'outtmpl': 'video.%(ext)s', 'format': 'bestvideo+bestaudio/best', 'quiet': True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
    await ctx.send(file=discord.File(filename))
    os.remove(filename)

# --- Generate Image ---
@bot.command()
async def genimage(ctx, *, text: str):
    img = Image.new('RGB', (400, 100), color=(73, 109, 137))
    d = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except:
        font = ImageFont.load_default()
    d.text((10, 25), text, font=font, fill=(255, 255, 0))
    img.save('output.png')
    await ctx.send(file=discord.File('output.png'))
    os.remove('output.png')

# --- Help and About ---
@bot.command()
async def help(ctx):
    cmds = [
        "!play <url> — Play music from a YouTube URL",
        "!pause — Pause the current song",
        "!resume — Resume paused music",
        "!skip — Skip the current song",
        "!queue — Show the current music queue",
        "!clear — Clear the music queue",
        "!stop — Stop and disconnect the bot",
        "!pingall — Mention all users in the channel",
        "!download <url> — Download a video from a URL",
        "!genimage <text> — Generate an image with the given text",
        "!about — Show info about the bot"
    ]
    await ctx.send("Available commands:\n" + '\n'.join(cmds))

@bot.command()
async def about(ctx):
    await ctx.send("Discord Music Bot by GitHub Copilot. Features: music, ping, download, image generation.")

# --- Run Bot ---
bot.run(TOKEN)
