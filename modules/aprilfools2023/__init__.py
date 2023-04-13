import time
from collections import namedtuple

from discord.ext import commands
from tybalt import checks

async def setup(bot):
    await bot.add_cog(AprilFools2023(bot))

async def teardown(bot):
    await bot.remove_cog('AprilFools2023')

class Doppleganger:
    def __init__(self, channel):
        print("Doppleganger init")
        self.guild = None
        self.channel = channel
        self.target = None
        self.hunter = None
        self.hunter_nick = None
        self.status = "resting"
        self.cooldown = None

        self.untargetable = [
            362339436027183104,
            259546131166396416,
            186158597279842305,
            201852669000679424,
            233094561910620162,
            155156087962730496,
            129987084617383936,
            111235765769371648,
            120261179095384065,
            143972236099846144,
            121796968245755905,
            216744009396256768,
            251778255760130050,
            114698444584517640,
            138678055940915200,
            66162534385725440
        ]

    def set_guild(self, guild):
        self.guild = guild
        pass

    def should_act(self):
        if self.cooldown is None:
            return True
        if self.status == "resting":
            return (self.cooldown + 15 * 60) < time.time()
        if self.status == "targeting":
            return (self.cooldown + 1 * 60) < time.time()
        if self.status == "hunting":
            return (self.cooldown + 5 * 60) < time.time()
        return False

    async def act(self, author):
        if self.status == "resting":
            await self.targeting(author)
        elif self.status == "targeting":
            await self.hunting(author)
        elif self.status == "hunting":
            await self.resting()

    async def targeting(self, target):
        if target.id in self.untargetable:
            return
        self.target = target
        self.cooldown = time.time()
        self.status = "targeting"
        user_mention = "<@{}>".format(target.id)
        message = "*{}, Something is coming for you...*".format(user_mention)
        await self.guild.get_channel(self.channel).send(message)

    async def hunting(self, hunter):
        if hunter.id == self.target.id:
            return
        self.hunter = hunter
        self.hunter_nick = hunter.nick
        self.cooldown = time.time()
        self.status = "hunting"
        target_mention = "<@{}>".format(self.target.id)
        message = "**A crazed doppelganger now hunts {}!**".format(target_mention)
        await hunter.edit(nick="Legendary {}".format(self.target.display_name))
        await self.guild.get_channel(self.channel).send(message)

    async def resting(self):
        target_mention = "<@{}>".format(self.target.id)
        hunter = self.hunter
        hunter_nick = self.hunter_nick
        self.target = None
        self.hunter = None
        self.hunter_nick = None
        self.cooldown = time.time()
        self.status = "resting"
        message = "**The doppelganger has returned to Augury Rock. {} is no longer hunted.**".format(target_mention)
        await hunter.edit(nick = hunter_nick)
        await self.guild.get_channel(self.channel).send(message)


class AprilFools2023(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data = {
            144894829199884288: Doppleganger(453190639564095488) # Guild Wars 2
            #144894829199884288: Doppleganger(299954336950386690) # Guild Wars 2 - ara-ara
            #887752546473627690: Doppleganger(895299111186759721) # Tybalt's Hideout

        }

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot == False and message.guild is not None:
            if message.guild.id in self.data:
                data = self.data[message.guild.id]
                data.set_guild(message.guild)
                if data.should_act():
                    await data.act(message.author)

