from discord.ext import commands
import discord
import sys
from discord import app_commands
from discord import ui
from discord import ButtonStyle
from tybalt import checks

async def setup(bot):
    await bot.add_cog(Contact(bot))

async def teardown(bot):
    await bot.remove_cog('Contact')

class ContactModal(ui.Modal, title="Contact Us"):
    message = ui.TextInput(label = "Your message", style = discord.TextStyle.long, max_length=1500)

    def __init__(self, channel):
        super().__init__()
        self.channel = channel

    async def on_submit(self, interaction: discord.Interaction):
        title = "### {} has submited a contact request".format(interaction.user.mention)
        embed = discord.Embed(title="New contact request", description=self.message.value, colour=0xCCCC00)
        embed.set_footer(
            text="{} (ID:{})".format(interaction.user.display_name, interaction.user.id),
            icon_url=interaction.user.display_avatar
        )
        await self.channel.send(title, embed=embed)

        await interaction.response.send_message("Thank you for your message. We may contact you in the future for further information.", ephemeral=True)


class PermissionModal(ui.Modal, title="Request Self-Promotion Permission"):
    message = ui.TextInput(label = "Your request", style = discord.TextStyle.long, max_length=1500)

    def __init__(self, channel):
        super().__init__()
        self.channel = channel

    async def on_submit(self, interaction: discord.Interaction):
        title = "### {} has submited a Self-promotion request".format(interaction.user.mention)
        embed = discord.Embed(title="New community message request", description=self.message.value, colour=0x0000FF)
        embed.set_footer(
            text="{} (ID:{})".format(interaction.user.display_name, interaction.user.id),
            icon_url=interaction.user.display_avatar
        )
        await self.channel.send(title, embed=embed)

        await interaction.response.send_message("Thank you for your message. We will contact you soon.", ephemeral=True)


class CommunityModal(ui.Modal, title="Request Community Message"):
    message = ui.TextInput(label = "Your request", style = discord.TextStyle.long, max_length=1500)

    def __init__(self, channel):
        super().__init__()
        self.channel = channel

    async def on_submit(self, interaction: discord.Interaction):
        title = "### {} has submited a Community Message request".format(interaction.user.mention)
        embed = discord.Embed(title="New community message request", description=self.message.value, colour=0x00CCCC)
        embed.set_footer(
            text="{} (ID:{})".format(interaction.user.display_name, interaction.user.id),
            icon_url=interaction.user.display_avatar
        )
        await self.channel.send(title, embed=embed)

        await interaction.response.send_message("Thank you for your message. We will contact you soon.", ephemeral=True)


class ReportModal(ui.Modal, title="Report Action"):
    message = ui.TextInput(label = "Your message", style = discord.TextStyle.long, max_length=1500)

    def __init__(self, channel):
        super().__init__()
        self.channel = channel

    async def on_submit(self, interaction: discord.Interaction):
        title = "### {} has submited a report ({})".format(interaction.user.mention, '<@&1154465387845521535>')
        embed = discord.Embed(title="New report", description=self.message.value, colour=0xFF0000)
        embed.set_footer(
            text="{} (ID:{})".format(interaction.user.display_name, interaction.user.id),
            icon_url=interaction.user.display_avatar
        )
        await self.channel.send(title, embed=embed)

        await interaction.response.send_message("Thank you for your report. We may contact you in the future for further information.", ephemeral=True)

class ContactView(ui.View):
    def __init__(self, channel):
        super().__init__()
        self.channel = channel

        button = ui.Button(emoji="\N{WARNING SIGN}", label="Report an issue", style=ButtonStyle.danger, custom_id="tybalt_contact_report")
        self.add_item(button)

        button = ui.Button(label="Self-Promotion Permission", style=ButtonStyle.primary, custom_id="tybalt_contact_perms")
        self.add_item(button)

        button = ui.Button(label="Request Community News", style=ButtonStyle.primary, custom_id="tybalt_contact_news")
        self.add_item(button)

        button = ui.Button(label="Other Message", style=ButtonStyle.secondary, custom_id="tybalt_contact_other")
        self.add_item(button)


class Contact(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = '1154465388994760720'

    @app_commands.command(name="contact", description="Contact the Mods")
    @app_commands.guild_only()
    async def slash_contact(self, interaction: discord.Interaction) -> None:
        channel = await self.bot.fetch_channel(self.channel_id)
        await interaction.response.send_modal(ContactModal(channel))

    @app_commands.command(name="report", description="Report an issue to the Mods")
    @app_commands.guild_only()
    async def slash_report(self, interaction: discord.Interaction) -> None:
        channel = await self.bot.fetch_channel(self.channel_id)
        await interaction.response.send_modal(ReportModal(channel))


    @commands.command(pass_context=True, no_pm=True)
    @checks.is_owner()
    @checks.has_prefix('$')
    async def contact_buttons(self, ctx):
        channel = await self.bot.fetch_channel(self.channel_id)
        content = "To contact the moderation team, please use one of the following buttons."

        view = ContactView(channel)
        message = await ctx.send(content, view=view);


    @commands.Cog.listener()
    async def on_interaction(self, interaction):
        if interaction.type == discord.InteractionType.component:
            if interaction.data['custom_id'] == "tybalt_contact_report":
                channel = await self.bot.fetch_channel(self.channel_id)
                await interaction.response.send_modal(ReportModal(channel))
            if interaction.data['custom_id'] == "tybalt_contact_perms":
                channel = await self.bot.fetch_channel(self.channel_id)
                await interaction.response.send_modal(PermissionModal(channel))
            if interaction.data['custom_id'] == "tybalt_contact_news":
                channel = await self.bot.fetch_channel(self.channel_id)
                await interaction.response.send_modal(CommunityModal(channel))
            if interaction.data['custom_id'] == "tybalt_contact_other":
                channel = await self.bot.fetch_channel(self.channel_id)
                await interaction.response.send_modal(ContactModal(channel))









