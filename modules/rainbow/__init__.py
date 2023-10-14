import discord
import random
from discord.ext import commands
from discord import MessageType

def setup(bot):
    bot.add_cog(TybaltRainbow())

async def setup(bot):
    await bot.add_cog(TybaltRainbow(bot))

async def teardown(bot):
    await bot.remove_cog('TybaltRainbow')


class TybaltRainbow(commands.Cog):
    """Tybalt Rainbow."""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        author = message.author
        if author.bot == False and message.guild is not None and message.type == MessageType.default:
            rainbow_roles = self.get_rainbow_roles(message.guild)
            if rainbow_roles:
                if (self.is_rainbowed(author, rainbow_roles) == False):
                    await self.rainbowize(author, rainbow_roles)

    @commands.command(pass_context=True, no_pm=True)
    async def rainbow(self, ctx):
        message = ctx.message
        author = message.author
        if author.bot == False and message.guild is not None:
            rainbow_roles = self.get_rainbow_roles(message.guild)
            if rainbow_roles:
                await self.rainbowize(author, rainbow_roles)
            await message.delete()

    async def rainbowize(self, user, roles):
        for role in roles:
            if (role in user.roles):
                await user.remove_roles(role)
        role = random.choice(roles)
        await user.add_roles(role)
        if random.random() < 0.1: # Extra : Adding rainbow to name (10% chance)
            nick = user.display_name
            emoji_rainbow = '🌈';
            if random.random() < 0.5:
                nick = "{} {}".format(nick, emoji_rainbow)
            else:
                nick = "{} {}".format(emoji_rainbow, nick)
            try:
                await user.edit(nick=nick)
            except:
                pass


    def get_rainbow_roles(self, guild):
        rolenames = ["Green", "Orange", "Yellow", "Purple", "Blue", "Red", "Pink"]
        rainbow_roles = []
        roles = guild.roles
        for role in roles:
            if role.name in rolenames:
                rainbow_roles.append(role)
        return rainbow_roles


    def is_rainbowed(self, author, roles):
        for role in roles:
            if (role in author.roles):
                return True
        return False

