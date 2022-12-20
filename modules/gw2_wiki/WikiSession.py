from discord.ext import commands
from urllib import parse
import aiohttp
import json
import random
import asyncio
import traceback
from collections import Counter
from tybalt import checks

class WikiSession:
    def __init__(self):
        self.session = None
        self.base_url = "https://wiki.guildwars2.com/"

    async def login(self):
        if self.session is None:
            return await self.prepare_session()
        else:
            pass #no login necessary. yet.

    async def opensearch(self, search, limit=11):
        return await self.api('opensearch', parameters = {
            "limit" : limit,
            "redirects" : "resolve",
            "search" : search
        })

    async def api(self, action, parameters={}):
        parameters["action"] = action;
        parameters["format"] = "json";
        data = await self.raw('api.php?'+parse.urlencode(parameters))
        parsed = json.loads(data)
        return parsed

    async def raw(self, query):
        await self.prepare_session()
        url = self.base_url + query
        try:
            r = await self.session.get(url)
            if (r.status >= 300):
                print('http error : {}'.format(r.status))
                print(await r.text())
                data = "[]"
            else:
                data = await r.text()
        except Exception as e:
            print(e)
            data = "[]"
        return data

    async def prepare_session(self):
        if self.session is None:
            headers = {
                "User-Agent":"TybaltBot/v2",
                #"User-Agent":"Mozilla/5.0 (Windows NT 6.2; WOW64; rv:17.0) Gecko/20100101 Firefox/17.0",
            }
            self.session = aiohttp.ClientSession(headers=headers)
            await self.login()

    def unload(self):
        if self.session is not None:
            asyncio.create_task(self.session.close())


