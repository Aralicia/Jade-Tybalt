import time
import re
from collections import namedtuple

from discord.ext import commands
from tybalt import checks

async def setup(bot):
    await bot.add_cog(AprilFools2024(bot))

async def teardown(bot):
    await bot.remove_cog('AprilFools2024')

class AprilFools2024(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.regex = re.compile(r"(I *am|I'? *m) +([^,;.?!]+)(.)?", re.IGNORECASE)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot == False and message.guild is not None:
            if message.guild.id == 1154465387803594812: #887752546473627690: #1154465387803594812
                search = self.regex.search(message.content)
                if search is not None:
                    if random.randrange(1, 11) == 1:
                        name = search.group(2)
                        affix = search.group(3)
                        if affix not in ['!','?']:
                            affix = ""
                        await message.author.edit(nick="{}{}".format(name, affix))

