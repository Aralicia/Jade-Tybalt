from discord.ext import commands
from datetime import datetime
from dateutil import parser
import aiohttp
import json
import random
import asyncio

async def setup(bot):
    await bot.add_cog(GW2Shaman(bot))

async def teardown(bot):
    await bot.remove_cog('GW2Shaman')


class GW2Shaman(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, no_pm=True)
    async def when(self, ctx):
        """Give the expected date of the next patch
        *Uses that_shaman's timer*

        Example:
        !when
        """
        
        message = ctx.message
        try:
            url = "https://www.thatshaman.com/tools/countdown/?format=json"
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as r:
                    data = await r.text()
                    status = r.status
            parsed = json.loads(data)
        except:
            parsed = json.loads('{}')

        if 'when' in parsed and 'confirmed' in parsed:
            msg = ""
            when = parsed['when']
            date = parser.parse(when)

            ts = int(datetime.timestamp(date))

            if random.randrange(1, 10) == 1: #10% chance of a joke
                msg = random.choice([
                    "The next update will be `Soon™️`.",
                    "The next update is `on the table™️`.",
                    "The next update is `coming`.",
                    "The next update is `somewhere in the queue`."
                ])
                previous = await message.channel.send(msg, reference=message)
                await asyncio.sleep(5)
                if parsed['confirmed']:
                    msg = "Okay, it will be <t:{:d}:R>.".format(ts)
                else:
                    msg = "Okay, it should be <t:{:d}:R>".format(ts)
                await message.channel.send(msg, reference=previous)
            else:
                if parsed['confirmed']:
                    msg = "The next update will be <t:{:d}:R>.".format(ts)
                else:
                    msg = "The next update should be <t:{:d}:R>".format(ts)
                await message.channel.send(msg, reference=message)
        else:
            await message.channel.send('Sorry, I have no idea.', reference=message)

