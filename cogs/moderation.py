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

class Moderation:
    def __init__(self, bot):
        self.bot = bot

    ...
            



def setup(bot):
    bot.add_cog(Moderation(bot))
