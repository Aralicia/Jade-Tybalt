import discord
import sys
from discord import ForumChannel
from discord.ext import commands
from tybalt import checks


async def setup(bot):
    await bot.add_cog(Talk(bot))

async def teardown(bot):
    await bot.remove_cog('Talk')

class Talk(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True, no_pm=True)
    @checks.user_can('talk')
    async def say(self, ctx, *message):
        if message:
            await ctx.message.delete()
            message = await self.clean_text(message[0], ctx.message)
            files = await self.get_files(ctx.message)

            await ctx.send(message, files=files)
    
    @commands.command(pass_context=True, no_pm=True)
    @checks.user_can('talk')
    async def resay(self, ctx, reply, *message):
        if message:
            await ctx.message.delete()
            target = await ctx.fetch_message(reply);
            message = await self.clean_text(message[0], ctx.message)

            if target.author == target.guild.me:
                await target.edit(content=message)


    @commands.command(pass_context=True, no_pm=True)
    @checks.user_can('talk')
    async def reply(self, ctx, reply, *message):
        """
        """
        await ctx.message.delete()
        target = await ctx.fetch_message(reply);

        if (target):
            message = " ".join(message, )

            await ctx.send(message, reference=target)

    @commands.command(pass_context=True, no_pm=True)
    @checks.user_can('talk')
    async def forum(self, ctx, forum:ForumChannel, name, tags, *content):
        await ctx.message.delete()
        if forum is not None:
            try:
                message = " ".join(content)
                taglist = tags.split(",")
                available_tags = forum.available_tags
                found_tags = []
                missing_tags = []

                if taglist:
                    for tagname in taglist:
                        for tag in available_tags:
                            if tag.name == tagname:
                                found_tags.append(tag)
                                break
                        else:
                            missing_tags.append(tagname)
                    if missing_tags:
                        # missing tags
                        pass
                    else: 
                        await forum.create_thread(name=name, content=message, applied_tags=found_tags)
                else:
                    await forum.create_thread(name=name, content=message)
            except Exception as e:
                print(e)
                pass


    async def clean_text(self, start, message):
        text = message.content
        pos = text.find(start)
        print(pos);
        text = text[pos:]

        return text

    async def get_files(self, message):
        files = []
        for a in message.attachments:
            files.append(await a.to_file())
        return files

