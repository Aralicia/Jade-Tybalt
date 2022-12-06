from discord.ext import commands


class GuildCog(commands.Cog):

    def __init__(self, bot):
        #self.__class__.__name__
        self.bot = bot
        self.activated_guilds = []
        self._mod_name = "";

    async def activate(self, guilds):
        pass

    async def deactivate(self, guilds):
        pass

    async def on_mod_activate(self, mod_name, guilds):
        if mod_name == self._mod_name:
            self.activated_guilds = GuildCog.get_activated_guilds(self._mod_name)
            self.activate(guilds)

    async def on_mod_deactivate(self, mod_name, guilds):
        if mod_name == self._mod_name:
            self.activated_guilds = GuildCog.get_activated_guilds(self._mod_name)
            self.deactivate(guilds)

    def update_activated_guild_list(mod_name):
        mod_config = self.bot.config('core.modules.CoreModuleManager')
        guilds = mod_config.get('{}_guilds'.format(mod_name))
        if guilds is None:
            return []
        return guilds

