import pkgutil
import keyword
import sys, os
import traceback
from discord import Guild
from discord.ext import commands
from tybalt import checks

async def setup(bot):
    module = CoreModuleManager(bot)
    await bot.add_cog(module)
    await module.autoload()

async def teardown(bot):
    await bot.remove_cog('CoreModuleManager')

class CoreModuleManager(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.config = self.bot.config(self)
        modules = self.config.get('modules')
        if modules is None:
            self.config.set('modules', [])
    
    async def autoload(self):
        modules = self.config.get('modules')
        for module in modules:
            try:
                await self.load(module)
            except Exception as e:
                print (e)

    async def load(self, name:str):
        try:
            await self.bot.load_extension(self.extension_path(name))
        except commands.ExtensionAlreadyLoaded as e:
            raise #already loaded, don't remove from liste
        except commands.ExtensionFailed as e:
            self.config_remove(name)
            print(traceback.format_exc())
            raise
        except Exception as e:
            self.config_remove(name)
            raise
        self.config_add(name)

    async def unload(self, name:str):
        try:
            await self.bot.unload_extension(self.extension_path(name))
        except Exception as e:
            self.config_remove(name)
            raise
        self.config_remove(name)

    async def reload(self, name:str):
        try:
            await self.bot.reload_extension(self.extension_path(name))
        except commands.ExtensionNotLoaded as e:
            await self.load(name)
        except commands.ExtensionFailed as e:
            self.config_remove(name)
            print(traceback.format_exc())
            raise
        except Exception as e:
            self.config_remove(name)
            raise
        self.config_add(name)

    async def activate(self, name:str, guild:Guild):
        modules = self.config.get('modules')
        if name in modules:
            confname = '{}_guilds'.format(name)
            guilds = self.config.get(confname.format(name))
            if guilds is None:
                guilds = []
            if guild.id not in guilds:
                guilds.append(guild.id)
                self.config.set(confname, modules)
                self.bot.dispatch("mod_activate", name, [guild])
                return True
        return False

    async def deactivate(self, name:str, guild:Guild):
        modules = self.config.get('modules')
        if name in modules:
            confname = '{}_guilds'.format(name)
            guilds = self.config.get(confname.format(name))
            if guilds is not None:
                if guild.id in guilds:
                    guilds.append(guild.id)
                    self.config.set(confname, modules)
                    self.bot.dispatch("mod_deactivate", name, [guild])
                    return True
        return False


    @commands.group(invoke_without_command=True, aliases=["mod","mods","module"])
    @checks.is_owner()
    @checks.has_prefix("$")
    async def modules(self, ctx):
        await self.help(ctx)

    @modules.command(name="load")
    async def cmd_load(self, ctx, extension_name:str):
        try:
           await self.load(extension_name)
        except commands.ExtensionNotFound as e:
            message = "Module \"{}\" doesn't exists.".format(extension_name)
        except commands.NoEntryPointError as e:
            message = "Module \"{}\" doesn't exists.".format(extension_name)
        except commands.ExtensionAlreadyLoaded as e:
            message = "Module \"{}\" is already loaded.".format(extension_name)
        except commands.ExtensionFailed as e:
            message = "Module \"{}\" crashed while loading.".format(extension_name)
        else:
            message = "Module \"{}\" loaded.".format(extension_name)
        await ctx.send(message, reference=ctx.message)

    @modules.command(name="unload")
    async def cmd_unload(self, ctx, extension_name:str):
        try:
            await self.unload(extension_name)
        except commands.ExtensionNotFound as e:
            message = "Module \"{}\" doesn't exists.".format(extension_name)
        except commands.ExtensionNotLoaded as e:
            message = "Module \"{}\" was not loaded.".format(extension_name)
        else:
            message = "Module \"{}\" unloaded.".format(extension_name)
        await ctx.send(message, reference=ctx.message)

    @modules.command(name="reload")
    async def cmd_reload(self, ctx, extension_name:str):
        try:
            await self.reload(extension_name)
        except commands.ExtensionNotFound as e:
            message = "Module \"{}\" doesn't exists.".format(extension_name)
        except commands.NoEntryPointError as e:
            message = "Module \"{}\" doesn't exists.".format(extension_name)
        except commands.ExtensionFailed as e:
            message = "Module \"{}\" crashed while reloading.".format(extension_name)
        else:
            message = "Module \"{}\" reloaded.".format(extension_name)
        await ctx.send(message, reference=ctx.message)

    @modules.command(name="list")
    async def cmd_list(self, ctx):
        module_path = os.path.abspath(os.path.dirname(sys.argv[0])) + '/modules'
        loaded = self.config.get('modules')
        available = []

        for finder, module_name, _ in pkgutil.iter_modules([module_path]):
            if module_name.isidentifier() and not keyword.iskeyword(module_name):
                available.append(module_name)

        unloaded = list(set(available) - set(loaded))
        unloaded.sort()

        message = "> **{} loaded modules:**\r\n> {}\r\n> \r\n> **{} unloaded modules:**\r\n> {}".format(
                len(loaded), ", ".join(loaded),
                len(unloaded), ", ".join(unloaded)
                )

        #TODO : replace quote & embed
        await ctx.send(message, reference=ctx.message)

    #@modules.command(name="activate")
    async def cmd_activate(self, ctx, extension_name:str):
        try:
            await self.activage (extension_name, ctx.message.guild.id)
        except commands.ExtensionNotFound as e:
            message = "Module \"{}\" doesn't exists.".format(extension_name)
        else:
            message = "Module \"{}\" activated.".format(extension_name)
        print(ctx.message.guild.id)

        #(status, message) = await self.do_activate(extension_name, ctx.message.guild.id)
        #loaded = self.config.get('modules')
        #activated = self.config.get('actives')
        #message = 

        #if extension_name in loaded:


    #@modules.command(name="deactivate")
    async def cmd_deactivate(self, ctx, extension_name:str):
        pass

    @modules.command(name="help")
    async def cmd_help(self, ctx):
        #TODO
        pass

    def extension_path(self, name):
        return 'modules.{}'.format(name)

    def config_add(self, name):
        modules = self.config.get('modules')
        if name not in modules:
            modules.append(name)
            modules.sort()
            self.config.set('modules', modules)

    def config_remove(self, name):
        modules = self.config.get('modules')
        if name in modules:
            modules.remove(name)
            self.config.set('modules', modules)

