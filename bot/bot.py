from discord.ext import commands

from .cogs import Message, Parcel
from .models import init_db


class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        print(f"Logged in as {self.user}")

        # Load cogs
        await self.add_cog(Message(self))
        await self.add_cog(Parcel(self))

        # Sync commands
        # await self.tree.sync()

        # Init database
        init_db()
