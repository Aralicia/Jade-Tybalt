from discord.ext import commands
from tybalt import checks
from random import choice, randint
from .basic_roller import roll
import discord


async def setup(bot):
    await bot.add_cog(RandomModule(bot))

async def teardown(bot):
    await bot.remove_cog('RandomModule')


class RandomModule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.ball = [
                "As I see it, yes",
                "It is certain",
                "It is decidedly so",
                "Most likely",
                "Outlook good",
                "Signs point to yes",
                "Without a doubt",
                "Yes",
                "Yes – definitely",
                "You may rely on it",
                "Reply hazy, try again",
                "Ask again later",
                "Better not tell you now",
                "Cannot predict now",
                "Concentrate and ask again",
                "Don't count on it",
                "My reply is no",
                "My sources say no",
                "Outlook not so good",
                "Very doubtful",
                "Do I really look like a Diviner ?"
            ]

    @commands.command(pass_context=True, no_pm=True)
    @checks.user_can('choose')
    async def choose(self, ctx, *choices):
        # TODO : Escape choices to avoid Pings
        if len(choices) > 1:
            await ctx.send(choice(choices))
        elif len(choices) == 1:
            await ctx.send("{}, obviously".format(choices[0]))
        else:
            await ctx.send("Choose what ?")

    @commands.command(name="8", aliases=["8ball"], pass_context=True, no_pm=True)
    @checks.user_can('8ball')
    async def _8ball(self, ctx, *, question: str):
        if (question.endswith("?") and question != "?"):
            await ctx.send(choice(self.ball))
        else:
            await ctx.send("That's not a question.")

    @commands.command(pass_context=True, no_pm=True, aliases=["r"])
    @checks.user_can('roll')
    async def roll(self, ctx, *, formula: str):
        if formula.isdigit():
            # Basic roll to max
            number = int(formula)
            n = randint(1, number)
            await ctx.send(
                ":game_die: {n} :game_die:".format(
                    n=n
                ),
                reference=ctx.message
            )
        else:
            result = roll(formula)
            print(result)
            message = ":game_die: **{n}** = {exp} :game_die:".format(
                    n=result.result,
                    exp=result.expanded.replace('+', ' + ').replace('-', ' - ')
                )
            if result.comment is not None:
                message = "{} : {}".format(result.comment, message);
            await ctx.send(message, reference=ctx.message)
