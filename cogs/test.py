import discord
from discord.ext import commands
import datetime
import requests
import random
import math
import time
from discord.ext.commands import errors, converter
from random import choice, randint
from random import choice, randint as rnd
import aiohttp
import asyncio
import json
import os
import re
import config

class Test:
    def __init__(self, bot):
        self.bot = bot

    async def on_message(self, message):
        if message.channel.id == 605099421897588736:
            def check(m):
                return m.channel == message.channel
            custom_emoji = re.findall(r'<:\w*:\d*>', message.content)
            custom_emoji = [int(e.split(':')[1].replace('>', '')) for e in custom_emoji]
            custom_emoji = [discord.utils.get(client.get_all_emojis(), id=e) for e in custom_emoji]
            if custom_emoji:
                history = await message.channel.history(limit=3).flatten()
                emoji = []
                for x in history:
                    custom_emoji = re.findall(r'<:\w*:\d*>', message.content)
                    custom_emoji = [int(e.split(':')[1].replace('>', '')) for e in custom_emoji]
                    custom_emoji = [discord.utils.get(client.get_all_emojis(), id=e) for e in custom_emoji]
                    if custom_emoji:
                        emoji.append(x)
                        
                if len(emoji) == 3:
                    for x in emoji:
                        x.delete()
                    await message.channel.send("Don't spam! Keep emoji spam in #emoji-spam")
            



def setup(bot):
    bot.add_cog(Test(bot))
