from discord.ext import commands
from datetime import datetime
from dateutil import parser
import aiohttp
import json
import random
import asyncio

async def setup(bot):
    await bot.add_cog(GW2Wiki(bot))

async def teardown(bot):
    await bot.remove_cog('GW2Wiki')


class GW2Wiki(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    async def slash_():
        pass

