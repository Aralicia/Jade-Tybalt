#!/usr/bin/env python3.10
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from tybalt.checks import Permissions
from tybalt.data import DataStore, Config, Data

class Tybalt(commands.Bot):
    
    def __init__(self):
        #load_dotenv()

        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.presences = True

        self.config = DataStore(Config)
        self.data = DataStore(Data)
        self.permissions = Permissions(self)

        super().__init__(command_prefix=('$', '!'), intents=intents)

    def run(self):
        token = self.config('env').get('DISCORD_TOKEN')
        super().run(token)

    async def on_ready(self):
        print(f'We have logged in as {self.user}')
        await self.load_extension('core.modules')
        await self.load_extension('core.permissions')
        print('Bot ready')

    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.errors.CommandNotFound):
            #TODO : handle custom commands ?
            pass
        elif isinstance(error, commands.errors.CheckFailure):
            pass # User doesn't have permission. Ignore
        else:
            print(error.__class__.__module__ + '.' + error.__class__.__qualname__)
            print(error)
        

tybalt = Tybalt();
tybalt.run();

