from discord.ext import commands
from discord.ext.commands import view

async def setup(bot):
    module = CoreOverrides(bot)
    await bot.add_cog(module)
    await module.autoload()

async def teardown(bot):
    await bot.remove_cog('CoreOverrides')

class CoreOverrides(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
    
    async def autoload(self):
        view._quotes = {
            '"': '"',
            "“": "”"
        }
        view._all_quotes = set(view._quotes.keys()) | set(view._quotes.values())

