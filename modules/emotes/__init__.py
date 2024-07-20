from discord.ext import commands
from tybalt import checks
from random import choice
import discord


async def setup(bot):
    await bot.add_cog(EmotesModule(bot))

async def teardown(bot):
    await bot.remove_cog('EmotesModule')


class EmotesModule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.flip_table = self.make_flip_table()

    @commands.command(pass_context=True, no_pm=True)
    @checks.user_can('emote')
    async def hug(self, ctx, user: discord.Member, intensity: int=3):
        hug = choice([
            '(っ˘̩╭╮˘̩)っ', '(っ´▽｀)っ', '╰(*´︶`*)╯', '(つ≧▽≦)つ', '(づ￣ ³￣)づ'
        ])
        await ctx.send("{}{}".format(hug, user.display_name))

    @commands.command(pass_context=True, no_pm=True)
    @checks.user_can('emote')
    async def flip(self, ctx, user: discord.Member):
        if (user.id == self.bot.user.id):
            user = ctx.author
        name = user.display_name.translate(self.flip_table)
        name = name[::-1]
        await user.edit(nick=name)
        await ctx.send("(╯°□°）╯︵  {}".format(name))

    def make_flip_table(self):
        norm_lower  = "abcdefghijklmnopqrstuvwxyz"
        norm_upper  = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        norm_number = "0123456789"
        norm_extra  = "()[]"
        norm = norm_lower + norm_upper + norm_number + norm_extra

        flip_lower  = "ɐqɔpǝɟƃɥᴉɾʞlɯuodbɹsʇnʌʍxʎz"
        flip_upper  = "∀qƆpƎℲפHIſʞ˥WNOԀQᴚS┴∩ΛMX⅄Z"
        flip_number = "0ІᘔƐᔭ59Ɫ86"
        flip_extra  = ")(]["
        flip = flip_lower + flip_upper + flip_number + flip_extra

        table_from = norm + flip
        table_to = flip + norm

        return str.maketrans(table_from, table_to)
