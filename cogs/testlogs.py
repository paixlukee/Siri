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
import config

class Help:
    def __init__(self, bot):
        self.bot = bot

    @commands.group(aliases=['cmds', 'commands', 'Help'])
    async def help(self, ctx, command=None):
        embed = discord.Embed(description=f'To view more information for a command, do {config.prefix}help')
        embed.set_author(name='Help Commands', icon_url=ctx.me.avatar_url_as(format='png'))
        embed.add_field(name='Utility', value='command, command, command')
        embed.add_field(name='Fun', value='command, command, command')
        embed.add_field(name='Moderation', value='command, command, command')
        #embed.add_field(name='Music', value='command, command, command')
        #embed.add_field(name='Custom Commands', value='...')
        await ctx.send(embed=embed)



def setup(bot):
    bot.add_cog(Help(bot))
