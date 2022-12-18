from discord.ext import commands
from tybalt import checks

async def setup(bot):
    await bot.add_cog(TestModule(bot))

async def teardown(bot):
    await bot.remove_cog('TestModule')


class TestModule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data = self.bot.data(self)
        self.data.table('test', ['id','name'])

    @commands.command(pass_context=True, no_pm=True)
    @checks.user_can('test')
    @checks.has_prefix('$')
    async def test(self, ctx):
        await ctx.send("TEST", reference=ctx.message);
