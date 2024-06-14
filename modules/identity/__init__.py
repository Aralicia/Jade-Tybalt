from tybalt import checks
import discord
from discord.ext import commands
from discord.ext import tasks

async def setup(bot):
    await bot.add_cog(TybaltIdentityModule(bot))

async def teardown(bot):
    await bot.remove_cog('TybaltIdentityModule')


class TybaltIdentityModule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.identity = None;
        self.data = self.bot.data(self)
        self.data.table('identities', {
            'key' : 'TEXT PRIMARY KEY',
            'name' : 'TEXT',
        })
        self.data.table('activities', {
            'identity' : 'TEXT',
            'activity' : 'TEXT'
        })
        self.data.table('replies', {
            'identity' : 'TEXT',
            'reply' : 'TEXT'
        })
        self.ticker.start()
    
    def __del__(self):
        self.ticker.cancel()
        pass
    
    # ACTIVITY TICK
    @tasks.loop(minutes=15.0)
    async def ticker(self):
        await self.tick()
        return

    async def tick(self):
        if self.identity is None:
            await self.set_identity(await self.get_identity())
        activity = self.random_activity()
        if activity is not None:
            await self.bot.change_presence(activity=discord.Game(activity))

    # AUTO REPLIES
    @commands.Cog.listener()
    async def on_message(self, message):
        if len(message.mentions) == 1 and message.mentions[0].id == self.bot.user.id and message.author.bot is False:
            ctx = await self.bot.get_context(message);
            if await checks.user_can('identity_reply').predicate(ctx):
                reply = self.random_reply()
                if reply is not None:
                    await message.channel.send(reply, reference=message)

    # COMMANDS
    @commands.group(invoke_without_command=False, guild_only=True, pass_context=True)
    @checks.user_can('identity_change')
    async def identity(self, ctx):
        pass

    @identity.command(name="list", pass_context=True)
    async def identity_list(self, ctx):
        query = "SELECT key, name, current FROM identities ORDER BY key ASC"
        result = self.data.db.execute(query).fetchall()
        message = "Available identities:"
        for identity in result:
            message = "{}\r\n- {}: {}".format(message, identity[0], identity[1])
            if identity[2] == True:
                message = "{} *(current)*".format(message)
        await ctx.send(message, reference=ctx.message)

    @identity.command(name="set", pass_context=True)
    async def identity_set(self, ctx, name:str):
        await self.set_identity(name)

    @identity.command(name="random", pass_context=True)
    async def identity_random(self, ctx):
        query = "SELECT key FROM identities ORDER BY random() LIMIT 1"
        result = self.data.db.execute(query).fetchone()
        if result is not None:
            await self.set_identity(result[0])

    # HELPERS
    async def get_identity(self):
        if self.identity is None:
            query = "SELECT key FROM identities WHERE current = 1 LIMIT 1"
            result = self.data.db.execute(query).fetchone()
            if result is not None:
                return result[0]
        return None

    async def set_identity(self, identity):
        if identity != self.identity and identity is not None:
            query = "SELECT key, name FROM identities WHERE key = ? LIMIT 1"
            params = (identity,)
            result = self.data.db.execute(query, params).fetchone()
            if result is not None:
                print(self.data.db.execute("UPDATE identities set current = 0"))
                print(self.data.db.execute("UPDATE identities set current = 1 WHERE key = ?", (identity,)))
                self.identity = result[0]
                await self.bot.get_guild(1154465387803594812).get_member(self.bot.user.id).edit(nick=result[1])
                #await self.bot.get_guild(887752546473627690).get_member(self.bot.user.id).edit(nick=result[1])
                activity = self.random_activity()
                if activity is not None:
                    await self.bot.change_presence(activity=discord.Game(activity))
    
    def random_activity(self):
        if self.identity is not None:
            query = "SELECT activity FROM activities WHERE identity = ? ORDER BY random() LIMIT 1"
            params = (self.identity,)
            result = self.data.db.execute(query, params).fetchone()
            if result is not None:
                return result[0]
        return None
    
    def random_reply(self):
        if self.identity is not None:
            query = "SELECT reply FROM replies WHERE identity = ? ORDER BY random() LIMIT 1"
            params = (self.identity,)
            result = self.data.db.execute(query, params).fetchone()
            if result is not None:
                return result[0]
        return None
