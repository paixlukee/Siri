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
        if data:
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
        new_lvl = int(exp_change ** (1/4))

        if cur_exp < new_lvl:
            db.posts.update_one({"user": user}, {"$set":{"level": new_lvl}})
            await self.add_money(user, 50)

            if serverid in servers['level_msgs']:
                if not serverid in servers['level_images']:
                    await channel.send(f"**{name}** just levelled up to **Level {new_lvl}**!")
                else:
                    #await message.channel.send(f"**{name}** just leveled up to **{level}**!")
                    await channel.send(file=discord.File('lumodal.png'))
                    
                    
    async def add_money(self, user:int, count):
        data = db.posts.find_one({"user": user})
        bal = data['money']
        money = int(bal) + count
        db.posts.update_one({"user": user}, {"$set":{"money": money}})
        
    @commands.command(aliases=['rank'])
    async def level(self, ctx, user: discord.User = None):
        if user:
            data = db.posts.find_one({"user": user.id})
            await ctx.send(f"{user.name}'s siri level is {data['level']} (cmd is WIP)")
        else:
            data = db.posts.find_one({"user": ctx.author.id})
            #card_link = requests.get("https://i.ibb.co/16QRQJC/sirirankcard.jpg")
            card_link = Image.open("sirirankcard.jpg")
            #img = Image.open(BytesIO(card_link.content))
            draw = ImageDraw.Draw(card_link)
            font_size = 14
            if len(str(ctx.author)) > 26:
                font_size = 14
            elif len(str(ctx.author)) > 15:
                font_size = 17
            elif len(str(ctx.author)) > 10:
                font_size = 25
            elif len(str(ctx.author)) < 9:
                font_size = 30
            else:
                font_size = 32
            font = ImageFont.truetype("Raleway-Medium.ttf", font_size, encoding="unic")
            font_2 = ImageFont.truetype("Raleway-Medium.ttf", 10, encoding="unic")
            level = data['level']
            draw.text((43,48), str(ctx.author), font=font, fill=(30, 30, 30, 30))
            draw.text((42,122), text=f"LEVEL {level}", font=font_2, fill=(50, 50, 50, 50))
            draw.rectangle([(42,88), (300, 120)], fill=(68, 116, 219, 0))
            bytes = BytesIO()
            card_link.save(bytes, 'PNG')
            bytes.seek(0)
            await ctx.send(file=discord.File(bytes.getvalue(), "sirirankcard.jpg"))
        
    @commands.command()
    async def lvlmsgs(self, ctx):
        """Set level messages for your server"""
        servers = db.utility.find_one({"utility": "serverconf"})
        if ctx.guild.id in servers['level_msgs']:
            await ctx.send(f"Turned level messages off for **{ctx.guild}**.")
            db.utility.update_one({"utility": "serverconf"}, {"$pull":{"level_msgs": ctx.guild.id}})
        else:
            await ctx.send(f"Turned level messages on for **{ctx.guild}**.")
            db.utility.update_one({"utility": "serverconf"}, {"$push":{"level_msgs": ctx.guild.id}})

    @commands.command()
    async def lvlimgs(self, ctx):
        servers = db.utility.find_one({"utility": "serverconf"})
        if ctx.guild.id in servers['level_msgs']:
            await ctx.send(f"Turned level images off for **{ctx.guild}**.")
            db.utility.update_one({"utility": "serverconf"}, {"$pull":{"level_images": ctx.guild.id}})
        else:
            await ctx.send(f"Turned level images on for **{ctx.guild}**. Permission `level_messages` must be turned on for this to show any change.")
            db.utility.update_one({"utility": "serverconf"}, {"$push":{"level_images": ctx.guild.id}})



def setup(bot):
  bot.add_cog(Levels(bot))
