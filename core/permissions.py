import re
from discord.ext import commands
from tybalt import checks

async def setup(bot):
    module = CorePermissionManager(bot)
    await bot.add_cog(module)

class CorePermissionManager(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.data = self.bot.data(self)
        #self.data.table("")
        pass


    @commands.group(invoke_without_command=False, aliases=["perms"], guild_only=True)
    @checks.is_owner()
    @checks.has_prefix("$")
    async def permissions(self, ctx):
        pass

    @permissions.command(name="allow")
    async def cmd_allow(self, ctx, *rule):
        rule = self.parse_rule(ctx, 'allow', rule)
        self.bot.permissions.store(rule)
        await ctx.send("Permissions Updated", reference=ctx.message)

    @permissions.command(name="deny")
    async def cmd_deny(self, ctx, *rule):
        rule = self.parse_rule(ctx, 'deny', rule)
        self.bot.permissions.store(rule)
        await ctx.send("Permissions Updated", reference=ctx.message)

    @permissions.command(name="clear")
    async def cmd_clear(self, ctx, *rule):
        rule = self.parse_rule(ctx, 'clear', rule)
        self.bot.permissions.clear(rule)
        await ctx.send("Permissions Updated", reference=ctx.message)

    @permissions.command(name="list")
    async def cmd_list(self, ctx, capability:str):
        result = [];
        rules = self.bot.permissions.query(ctx.guild, capability)
        for rule in rules:
            result.append(rule.describe(ctx))
        if len(result) == 0:
            await ctx.send("No rules for {}".format(capability))
        result.insert(0, "Rules for {}".format(capability))
        await ctx.send("\n- ".join(result), reference=ctx.message)

    def parse_rule(self, ctx, action, rule):
        guild = None
        permission = None
        sourceType = None
        source = None
        locationType = None
        location = None
        mode = 'perm'

        if ctx.guild is not None:
            guild = ctx.guild.id

        for token in rule:
            if token == 'for':
                mode = 'source'
            elif token == 'in':
                mode = 'location'
            elif mode == 'perm':
                if permission is not None:
                    raise SyntaxError('Multiple permissions are not allowed')
                #TODO check for malformed permissions ?
                permission = token
            elif mode == 'source':
                if source is not None:
                    raise SyntaxError('Multiple sources are not allowed')
                user_count = len(ctx.message.mentions)
                role_count = len(ctx.message.role_mentions)
                source_count = user_count + role_count
                if source_count > 1:
                    raise SyntaxError('Multiple sources are not allowed')
                elif source_count < 1:
                    raise SyntaxError('Malformed source')
                elif user_count == 1:
                    sourceType = 'user'
                    source = ctx.message.mentions[0].id
                elif role_count == 1:
                    sourceType = 'role'
                    source = ctx.message.role_mentions[0].id
            elif mode == 'location':
                if location is not None:
                    raise SyntaxError('Multiple locations are not allowed')
                location_count = len (ctx.message.channel_mentions)
                if location_count > 1:
                    raise SyntaxError('Multiple locations are not allowed')
                elif location_count < 1:
                    raise SyntaxError('Malformed location')
                locationType = 'channel'
                location = ctx.message.channel_mentions[0].id

        if permission is None:
            raise SyntaxError('Missing permission')
        return checks.Rule(guild, action, permission, sourceType, source, locationType, location)

