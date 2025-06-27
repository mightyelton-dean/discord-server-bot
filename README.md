# Discord Music Bot

This is a Python Discord bot with the following features:

- Play music in voice channels
- Ping all users
- Download videos
- Generate images

## Requirements

- Python 3.8+
- discord.py
- yt-dlp
- pillow

## Setup

1. Install dependencies (already handled by setup):
   ```sh
   pip install discord.py yt-dlp pillow
   ```
2. Create a Discord bot and get your token: https://discord.com/developers/applications
3. Add your bot token to a `.env` file or directly in the script (not recommended for production).

## Usage

- Run the bot:
  ```sh
  python bot.py
  ```
- Use commands in your Discord server:
  - `!play <url>`: Play music from a YouTube URL
  - `!pingall`: Mention all users in the channel
  - `!download <url>`: Download a video from a URL
  - `!genimage <text>`: Generate an image with the given text

---

This project uses `discord.py`, `yt-dlp`, and `Pillow`.
