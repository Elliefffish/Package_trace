import os
import logging

from dotenv import load_dotenv
from bot import bot

load_dotenv()
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")

if not DISCORD_BOT_TOKEN:
    logging.error("DISCORD_BOT_TOKEN is not set")
    raise ValueError("DISCORD_BOT_TOKEN is not set")

if __name__ == "__main__":
    bot.run(DISCORD_BOT_TOKEN)
