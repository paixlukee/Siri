import discord
import asyncio
import datetime
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont, ImageColor, ImageOps, ImageFilter
from io import BytesIO
from random import choice as rnd
from random import randint
import json
import random
import config
import requests
from pymongo import MongoClient
import pymongo

client = MongoClient(config.mongo_client)
db = client['siri']

class Levels:
    def __init__(self, bot):
        self.bot = bot

    async def on_message(self, message):
        update = await self.update_data(message.author.id)
        if update == True:
            await self.add_experience(message.author.id)
            await self.level_up(message.author.id, message.guild.id, message.channel, message.author.name)


    async def update_data(self, user):
        data = db.posts.find_one({"user": user})
        if data:
            has_lvl = False
            for i in data.items():
                if i[0] == 'level':
                    has_lvl = True
            if has_lvl == False:
                db.posts.update_one({"user": user}, {"$set":{"level": 1}})
                db.posts.update_one({"user": user}, {"$set":{"exp": 0}})
                db.posts.update_one({"user": user}, {"$set":{"last_msg": None}})
                
            return True

        else:
            return False

    async def add_experience(self, user):
        data = db.posts.find_one({"user": user})
        if not data:
            cur_exp = data['exp']
            new_exp = cur_exp + 3
            db.posts.update_one({"user": user}, {"$set":{"exp": new_exp}})

    async def level_up(self, user, serverid, channel, name):
        data = db.posts.find_one({"user": user})
        servers = db.utility.find_one({"utility": "serverconf"})
        level = data['level']
        level_change = level
        exp = data['exp']
        exp_change = exp
        cur_exp = level
        end_exp = int(exp_change ** (1/4))

        if cur_exp < end_exp:
            level_change = end_exp

            if serverid in servers['level_msgs']:
                if serverid in servers['level_images']:
                    await message.channel.send(f"**{name}** just leveled up to **{level}**!")
                else:
                    await message.channel.send(f"**{name}** just leveled up to **{level}**!")

    @commands.command()
    async def lvlmsgs(self, ctx):
        servers = db.utility.find_one({"utility": "serverconf"})
        if ctx.guild.id in servers['lvl_msgs']:
            await ctx.send(f"Turned level messages off for **{ctx.guild}**.")
            db.utility.update_one({"utility": serverconf}, {"$pull":{"lvl_msgs": ctx.guild.id}})
        else:
            await ctx.send(f"Turned level messages on for **{ctx.guild}**.")
            db.utility.update_one({"utility": serverconf}, {"$push":{"lvl_msgs": ctx.guild.id}})

    @commands.command()
    async def lvlimgs(self, ctx):
        servers = db.utility.find_one({"utility": "serverconf"})
        if ctx.guild.id in servers['lvl_msgs']:
            await ctx.send(f"Turned level images off for **{ctx.guild}**.")
            db.utility.update_one({"utility": serverconf}, {"$pull":{"lvl_images": ctx.guild.id}})
        else:
            await ctx.send(f"Turned level images on for **{ctx.guild}**. Permission `level_messages` must be turned on for this to show any change.")
            db.utility.update_one({"utility": serverconf}, {"$push":{"lvl_images": ctx.guild.id}})



def setup(bot):
  bot.add_cog(Levels(bot))
