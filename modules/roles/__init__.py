from discord.ext import commands
import discord
from tybalt import checks
from . import roles
from .Role import Role
from collections import namedtuple

async def setup(bot):
    await bot.add_cog(Roles(bot))

async def teardown(bot):
    await bot.remove_cog('Roles')

class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.roles = {
            # Temporary fake role - actually works like Guest
            'robot' : Role(
                'guest',
                'Bot',
                '\N{ROBOT FACE}',
                'You are a bot, and are trying to infiltrate the discord.'
                ),
            roles.guest.key : roles.guest,
            roles.na.key : roles.na,
            roles.eu.key : roles.eu,
            roles.f2p.key : roles.f2p,
        }

    ###
    ### Role-specific commands
    ###

    @commands.command(pass_context=True, no_pm=True, aliases=["NA"])
    @checks.has_prefix('$')
    async def na(self, ctx):
        """Join NA role

        Example:
        !na
       """
        await self.toggle_role_command(ctx, role="na",
                added="Done ! You are now a NA player.",
                removed="Well, you **were** a NA player.")

    @commands.command(pass_context=True, no_pm=True, aliases=["EU"])
    @checks.has_prefix('$')
    async def eu(self, ctx):
        """Join EU role

        Example:
        !eu
       """
        await self.toggle_role_command(ctx, role="eu",
                added="Done ! You are now a EU player.",
                removed="Well, you **were** a EU player.")

    @commands.command(pass_context=True, no_pm=True, aliases=["F2P"])
    @checks.has_prefix('$')
    async def f2p(self, ctx):
        """Join F2P role

        Example:
        !f2p
       """
        await self.toggle_role_command(ctx, role="f2p",
                added="Done ! You are now a F2P player.",
                removed="Congratulations, you are no longer a F2P player.")

    ###
    ### Role commands
    ###

    @commands.command(pass_context=True, no_pm=True)
    @checks.has_prefix('$')
    async def roles(self, ctx):
        """Display a message on which you can mention to change your roles (In dev)

        Example:
        !roles
        """
        content = "> **User Roles**\n> Use the reactions below this message to gain or lose the following roles :";

        for role in self.roles.values():
            content = "{}\n> {} : {} - {}".format(content, role.emoji, role.name, role.description)

        message = await ctx.send(content, reference=ctx.message);

        for role in self.roles.values():
            await message.add_reaction(role.emoji)


    ###
    ### Listeners
    ###

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.roles == after.roles:
            return
        changes = self.get_roles_diff(before.roles, after.roles)
        addlist = [];
        remlist = [];
        if 'eu' in changes.added or 'na' in changes.added:
            remlist.append(self.roles['guest'].role(after.guild))
        elif 'guest' in changes.added:
            remlist.append(self.roles['eu'].role(after.guild));
            remlist.append(self.roles['na'].role(after.guild));
        elif 'eu' in changes.removed or 'na' in changes.removed:
            if 'eu' not in changes.left and 'na' not in changes.left:
                addlist.append(self.roles['guest'].role(after.guild))
        
        addlist = [i for i in addlist if i is not None]
        if len(addlist) > 0:
            await after.add_roles(*addlist)
        remlist = [i for i in remlist if i is not None]
        if len(remlist) > 0:
            await after.remove_roles(*remlist)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        message, member, role = await self.get_reaction_context(payload)
        if member is None or role is None:
            return
        try:
            await role.toggle(member, message.guild)
            await message.remove_reaction(payload.emoji, member)
        except :
            print("{}".format(sys.exc_info()[0]))

    ###
    ### Helpers
    ###

    async def toggle_role_command(self, ctx, role, added, removed):
        if role not in self.roles:
            await ctx.send("The role \"{}\" doesn't exist.".format(role), reference=ctx.message)
            return
        try:
            if await self.roles[role].toggle(ctx.message.author, ctx.message.guild):
                await ctx.send(added, reference=ctx.message)
            else:
                await ctx.send(removed, reference=ctx.message)
        except discord.Forbidden:
            raise
            await ctx.send("I need permissions to edit roles first.", reference=ctx.message)
        except ValueError as e:
            await ctx.send("The role \"{}\" doesn't exist.".format(role), reference=ctx.message)
        except Exception as e:
            print(e)
            await ctx.send("Something went wrong.", reference=ctx.message)

    def get_roles_diff(self, before, after):
        added = []
        removed = []
        left = []
        for role in after:
            if role not in before:
                added.append(role.name.lower())
            left.append(role.name.lower())
        for role in before:
            if role not in after:
                removed.append(role.name.lower())
        return namedtuple('diff', 'added removed left')(added, removed, left)

    async def get_reaction_context(self, payload):
        try:
            guild = self.bot.get_guild(payload.guild_id)
            member = guild.get_member(payload.user_id)
            channel = guild.get_channel(payload.channel_id)
            emoji = payload.emoji

            if not member.bot:
                message = await channel.fetch_message(payload.message_id)
                if message.author == guild.me:
                    for role in self.roles.values():
                        if (emoji.name == role.emoji):
                            return (message, member, role)
                return (message, member, None)
            return (None, member, None)
        except:
            print("{}".format(sys.exc_info()[0]))
        return (None, None, None)
