import logging

from discord.ext import commands

from .cogs import Parcel
from .utils import init_db

logger = logging.getLogger("discord_bot")


class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        logger.info(f"Logged in as {self.user}")

        # Init database
        init_db()

        # Load cogs
        await self.add_cog(Parcel(self))

        # Sync application commands
        await self.tree.sync()
