from .GW2Wiki import GW2Wiki

async def setup(bot):
    await bot.add_cog(GW2Wiki(bot))

async def teardown(bot):
    await bot.remove_cog('GW2Wiki')

