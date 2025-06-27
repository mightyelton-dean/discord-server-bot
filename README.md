# Discord Music Bot

A Python Discord bot with the following features:
- Play music in voice channels (YouTube search or URL)
- Ping all users
- Download videos
- Generate images with text

## Requirements
- Python 3.8+
- `discord.py`
- `yt-dlp`
- `pillow`

## Setup

1. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
2. Create a Discord bot and get your token: https://discord.com/developers/applications
3. Set your bot token as an environment variable named `DISCORD_TOKEN` (recommended for Railway and other cloud platforms).

## Usage

- Run the bot locally:
  ```sh
  python bot.py
  ```
- Or deploy to Railway (recommended for 24/7 uptime):
  - Push your code to GitHub
  - Connect your repo on [Railway](https://railway.app/)
  - Set `DISCORD_TOKEN` in the Railway Variables tab
  - Deploy and monitor logs

## Bot Commands
- `!play <song name or YouTube URL>`: Play music (searches YouTube if not a URL)
- `!pause`: Pause the current song
- `!resume`: Resume paused music
- `!skip`: Skip the current song
- `!queue`: Show the current music queue
- `!nowplaying`: Show the currently playing song
- `!clear`: Clear the music queue
- `!stop`: Stop and disconnect the bot
- `!pingall`: Mention all users in the channel
- `!download <url>`: Download a video from a URL
- `!genimage <text>`: Generate an image with the given text
- `!help`: List all commands
- `!about`: Show info about the bot

---

This project uses `discord.py`, `yt-dlp`, and `Pillow`.
