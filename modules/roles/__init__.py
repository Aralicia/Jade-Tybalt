from discord.ext import commands
import discord
import asyncio
from discord import app_commands
from tybalt import checks
from . import roles
from .Role import Role
from collections import namedtuple  
from discord.ui import Button
from discord import ButtonStyle

GUILD_GUILDWARS2 = discord.Object(144894829199884288)
GUILD_TYBALTTEST = discord.Object(887752546473627690)


async def setup(bot):
    await bot.add_cog(Roles(bot))

async def teardown(bot):
    await bot.remove_cog('Roles')

class RolesGateView(discord.ui.View):
    def __init__(self, bot, roles):
        super().__init__()
        self.bot = bot
        self.roles = roles

        for role in self.roles.values():
            self.add_item(Button(custom_id="tyb_rolesgate_"+role.key, label=role.name, emoji=role.emoji))

class RolesView(discord.ui.View):
    def __init__(self, bot, roles, guild, user):
        super().__init__()
        self.bot = bot
        self.roles = roles

        for role in self.roles.values():
            style = ButtonStyle.secondary
            if role.owned(user, guild):
                style = ButtonStyle.primary
            self.add_item(Button(custom_id="tyb_roles_"+role.key, label=role.name, emoji=role.emoji, style=style))

class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.roles = {
            # Temporary fake role - actually works like Guest
            #'robot' : Role(
            #    'guest',
            #    'Bot',
            #    '\N{ROBOT FACE}',
            #    'You are a bot, and are trying to infiltrate the discord.'
            #    ),
            roles.guest.key : roles.guest,
            roles.na.key : roles.na,
            roles.eu.key : roles.eu,
            roles.f2p.key : roles.f2p,
        }

    ###
    ### Role-specific commands
    ###

    @commands.command(pass_context=True, no_pm=True, aliases=["NA"])
    async def na(self, ctx):
        """Join NA role

        Example:
        !na
       """
        await self.toggle_role_command(ctx, role="na",
                added="Done ! You are now a NA player.",
                removed="Well, you **were** a NA player.")

    @commands.command(pass_context=True, no_pm=True, aliases=["EU"])
    async def eu(self, ctx):
        """Join EU role

        Example:
        !eu
       """
        await self.toggle_role_command(ctx, role="eu",
                added="Done ! You are now a EU player.",
                removed="Well, you **were** a EU player.")

    @commands.command(pass_context=True, no_pm=True, aliases=["F2P"])
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
    async def roles(self, ctx):
        """Deprecated. Please use /roles instead.
        """
        content = "> This command is deprecated, please use /roles instead."
        message = await ctx.send(content, reference=ctx.message);

    @app_commands.command(name="roles", description="Change your roles")
    @app_commands.guild_only()
    async def slash_roles(self, interaction: discord.Interaction) -> None:
        content = "Use the buttons below to change your roles"
        
        view = RolesView(self.bot, self.roles, interaction.user, interaction.guild)
        await interaction.response.send_message(content, view=view, ephemeral=True)
        #await view.wait()
    
    @commands.command(pass_context=True, no_pm=True)
    @checks.is_owner()
    @checks.has_prefix('$')
    async def rolesgate(self, ctx):
        content = "> **Welcome to the /r/Guildwars2 server.**\n> Please read the <#847640635048722432> and then use one the buttons below to chose a role and gain access to the discussion channels.\n> You can change this later in <#277148421327028224>; see the pinned messages there for details.\n> ";
        components = []

        for role in self.roles.values():
            content = "{}\n> {} : {} - {}".format(content, role.emoji, role.name, role.description)

        view = RolesGateView(self.bot, self.roles)
        message = await ctx.send(content, view=view);

    ###
    ### Listeners
    ###

    #@commands.Cog.listener()
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
        elif 'f2p' in changes.added:
            if 'eu' not in changes.left and 'na' not in changes.left and 'guest' not in changes.left:
                addlist.append(self.roles['guest'].role(after.guild))
        
        addlist = [i for i in addlist if i is not None]
        if len(addlist) > 0:
            await after.add_roles(*addlist)
        remlist = [i for i in remlist if i is not None]
        if len(remlist) > 0:
            await after.remove_roles(*remlist)

    #@commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        message, member, role = await self.get_reaction_context(payload)
        if member is None or role is None:
            return
        try:
            await role.toggle(member, message.guild)
            await message.remove_reaction(payload.emoji, member)
        except :
            print("{}".format(sys.exc_info()[0]))


    @commands.Cog.listener()
    async def on_interaction(self, interaction):
        if interaction.type == discord.InteractionType.component:
            for role in self.roles.values():
                # RolesGate Variant
                if interaction.data['custom_id'] == "tyb_rolesgate_"+role.key:
                    await role.toggle(interaction.user, interaction.guild)
                    await interaction.response.defer()
                # Slash Command Variant
                if interaction.data['custom_id'] == "tyb_roles_"+role.key:
                    await role.toggle(interaction.user, interaction.guild)
                    await asyncio.sleep(1)

                    # Get a new member object to get the new roles
                    member = interaction.guild.get_member(interaction.user.id)
                    
                    view = RolesView(self.bot, self.roles, member, interaction.guild)
                    await interaction.response.edit_message(view=view)

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
            if channel is None:
                return (None, None, None)

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
