import discord
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont, ImageColor, ImageOps, ImageFilter
from io import BytesIO

import datetime
import requests
import random

import time
from discord.ext.commands import errors, converter
from random import choice, randint

import aiohttp
import asyncio
import sys
import subprocess
import json
import os


os.chdir(r'C:\\Users\\Luke Jeffries\\Lady Tohru\\cogs')

class Economy:
    def __init__(self, bot):
        self.bot = bot
        self.s = '§'

    @commands.command(pass_context=True, aliases=['setcolor'])
    async def setcolour(self, ctx, colour):
        """Sets Profile Colour

        Colours:
        - Red
        - Orange
        - Yellow
        - Green
        - Blue
        - Violet
        - Pink
        - White

        """
        with open('assets//economy.json', 'r') as f:
            users = json.load(f)

        if colour is None:
            await self.bot.say("`Incorrect Usage`\n```siri setcolour <colour-name>```")

        elif ctx.message.author.id in users:
            
            if colour == 'pink' or colour == 'Pink':
                await self.set_col(users, user=ctx.message.author.id, colour=0xff93f4)
                await self.bot.say("Set.")
            elif colour == 'blue' or colour == 'Blue':
                await self.set_col(users, user=ctx.message.author.id, colour=0x0000ff)
                await self.bot.say("Set.")
            elif colour == 'green' or colour == 'Green':
                await self.set_col(users, user=ctx.message.author.id, colour=0x00ff00)
                await self.bot.say("Set.")
            elif colour == 'red' or colour == 'Red':
                await self.set_col(users, user=ctx.message.author.id, colour=0xff0000)
                await self.bot.say("Set.")
            elif colour == 'violet' or colour == 'Violet':
                await self.set_col(users, user=ctx.message.author.id, colour=0xa341f4)
                await self.bot.say("Set.")
            elif colour == 'orange' or colour == 'Orange':
                await self.set_col(users, user=ctx.message.author.id, colour=0xff9d00)
                await self.bot.say("Set.")
            elif colour == 'yellow' or colour == 'Yellow':
                await self.set_col(users, user=ctx.message.author.id, colour=0xffff00)
                await self.bot.say("Set.")
            elif colour == 'white' or colour == 'White':
                await self.set_col(users, user=ctx.message.author.id, colour=0xffffff)
                await self.bot.say("Set.")
            else:
                await self.bot.say("That isn't a valid colour! View the colour list with `siri help cmd setcolour`\n```If you would like to suggest a colour, send a ticket ('siri ticket <message>') with the colour name and hex.```")
            
            with open('assets/economy.json', 'w') as f:
                json.dump(users, f)
        else:
            await self.bot.say("You don't have a bank account, create one with `siri bank create`!")

    @commands.command(pass_context=True)
    async def description(self, ctx, *, message):
        """Sets Profile Description"""
        with open(r'assets\economy.json', 'r') as f:
            users = json.load(f)

        if message is None:
            await self.bot.say("`Incorrect Usage`\n```siri description <description>```")

        elif len(message) > 400:
            await self.bot.say("Description cannot be longer than 400 characters!")

        elif ctx.message.author.id in users:
            await self.bot.say("Set.")
            await self.set_desc(users, user=ctx.message.author.id, description=message)
            with open('C:\\Users\\Luke Jeffries\\Siri\\cogs\\economy.json', 'w') as f:
                json.dump(users, f)
        else:
            await self.bot.say("You don't have a bank account, create one with `siri bank create`!")

    @commands.command(pass_context=True, aliases=['birthday'])
    async def bday(self, ctx, day=None, month=None, year=None):
        """Sets Profile Birthday"""
        with open('assets\\economy.json', 'r') as f:
            users = json.load(f)
        try:
            date = day.split('-')
        except:
            pass
        if day is None:
            await self.bot.say("`Incorrect Usage`\n```siri birthday DD-MM-YYYY```") 
        elif len(date) < 3:
            await self.bot.say("`Incorrect Format`\n```DD-MM-YYYY```")           
        elif ctx.message.author.id in users:
            await self.bot.say("Set.")
            bday = date
            await self.set_bday(users, user=ctx.message.author.id, date=bday)
            with open('C:\\Users\\Luke Jeffries\\Siri\\cogs\\economy.json', 'w') as f:
                json.dump(users, f)
        else:
            await self.bot.say("You don't have a bank account, create one with `siri bank create`!")

    @commands.command(pass_context=True, aliases=['market', 'shop'])
    async def store(self, ctx):
        """Buy an item from the Apple Store"""
        embed = discord.Embed(colour=0xa341f4, title="Welcome to the Apple Store!", description="Items:")
        embed.add_field(name=f"[1] 🍎 Apple ({self.s}2)", value=f"Get a shiny red apple.. almost as amazing as *the* Apple Company.")
        embed.add_field(name=f"[2] 📱 iPhone ({self.s}300)", value=f"Is that an iPhone 4? The best phone ever tbh")
        embed.add_field(name=f"[3] 🏠 House ({self.s}2000)", value=f"Wait.. since when can you buy homes at the Apple Store?")
        embed.set_footer(text="To buy an item, do 'siri buy <item>' or 'siri buy <item-number>'")
        embed.set_thumbnail(url="https://c.slashgear.com/wp-content/uploads/2016/06/apple-store-800x420.jpg")
        await self.bot.say(embed=embed)

    @commands.command(pass_context=True)
    async def eat(self, ctx):
        """Eat an apple"""
        with open('assets//economy.json', 'r') as f:
            users = json.load(f)
        if ctx.message.author.id in users:
            if users[ctx.message.author.id]['apple'] > 0:
                responses = ['Yum.', 'Mmm.', 'Tasty?', 'Mm. Sounds good!']
                await self.bot.say(f"You ate :apple:`1`! | {random.choice(responses)}") 
                await self.apple(users, user=ctx.message.author.id, count=-1)
            else:
                await self.bot.say("You don't have any apples!")
        else:
            await self.bot.say("You don't have a bank account, create one with `siri bank create`!")
        

    @commands.command(pass_context=True)
    async def buy(self, ctx, item = None):
        """Buy an item ('siri store' to see the items)"""
        with open('assets//economy.json', 'r') as f:
            users = json.load(f)
        msg = await self.bot.say("Processing..")
        if not ctx.message.author.id in users:
            await self.bot.say("You don't have a bank account, create one with `siri bank create`!")
        elif item is None:
            await self.bot.say("`Incorrect Usage`\n```siri buy <item>```")
            await self.bot.delete_message(msg)
        elif item == 'apple' or item == 'Apple' or item == '1': #2
            if users[ctx.message.author.id]['money'] < 2:
                await self.bot.say("You don't have enough to buy this item!")
                await self.bot.delete_message(msg)
            else:
                await self.take_money(users, user=ctx.message.author.id, count=2)
                await self.apple(users, user=ctx.message.author.id, count=1)
                await self.bot.delete_message(msg)
                await self.bot.say("You have successfully bought :apple:`1` from the Apple Store!")
        elif item == 'iphone' or item == 'iPhone' or item == 'Iphone' or item == 'IPhone' or item == '2': #300
            chance = random.randint(1, 25)
            chance_b = random.randint(1, 25)
            if users[ctx.message.author.id]['money'] < 300:
                await self.bot.say("You don't have enough to buy this item!")
                await self.bot.delete_message(msg)
            elif chance == chance_b:
                await self.take_money(users, user=ctx.message.author.id, count=300)
                await self.bot.delete_message(msg)
                await self.bot.say(f"**BOGO!** You have won :iphone:`2` for the price of one!")
                await self.iphone(users, user=ctx.message.author.id, count=2)
            else:
                await self.take_money(users, user=ctx.message.author.id, count=300)
                await self.bot.delete_message(msg)
                await self.bot.say("You have successfully bought :iphone:`1` from the Apple Store!")
                await self.iphone(users, user=ctx.message.author.id, count=1)
        elif item == 'house' or item == 'House' or item == '3': #2,000
            await self.bot.delete_message(msg)
            if users[ctx.message.author.id]['money'] < 2000:
                await self.bot.say("You don't have enough to buy this item!")
            else:
                await self.take_money(users, user=ctx.message.author.id, count=2000)
                await self.bot.say("You have successfully bought :house:`1` from the Apple Store!")
                await self.house(users, user=ctx.message.author.id, count=1)
        else:
            await self.bot.say("I couldn't find that item.. Do `siri shop` to see what we have..")

    @commands.command(pass_context=True, aliases=['Profile'])
    async def profile(self, ctx, user: discord.User=None):
        """Get user profile"""
        with open('assets//economy.json', 'r') as f:
            users = json.load(f)

        if user is None:
            member = ctx.message.author

        else:
            try:
                member = user
            except:
                try:
                    member = "<@" + user + ">"
                except:
                    await self.bot.say("There was an error! I-I tried everything..!")

        if member.id in users:
            bal = users[member.id]['money']
            description = users[member.id]['description']
            bday = users[member.id]['birthday']
            colour = users[member.id]['colour']
            embed = discord.Embed(colour=colour, title=f"{member.name} #{member.discriminator}", description=f'**"**{description}**"**')
            if bday == 'BNS':
                embed.add_field(name="Birthday..", value="BIRTHDAY NOT SET: `siri birthday DD-MM-YYYY`")
            else:
                embed.add_field(name="Birthday..", value="**/**".join(bday))
            if colour == 0:
                embed.add_field(name="Colour..", value="COLOUR NOT SET: `siri setcolour <colour-name>`")
            elif colour == 16749556:
                embed.add_field(name="Colour..", value="<:pink:485323891317669888>")
            elif colour == 255:
                embed.add_field(name="Colour..", value="<:blue:485324426460528651>")
            elif colour == 16711680:
                embed.add_field(name="Colour..", value="<:red:485325173919318027>")
            elif colour == 65280:
                embed.add_field(name="Colour..", value="<:green:485325683594231818>")
            elif colour == 10699252:
                embed.add_field(name="Colour..", value="<:purple:485582995533725727>")
            elif colour == 16751872:
                embed.add_field(name="Colour..", value="<:orange:485585130216488975>")
            elif colour == 16776960:
                embed.add_field(name="Colour..", value="<:yellow:485585695109546006>")
            elif colour == 16777215:
                embed.add_field(name="Colour..", value="<:white:485587580323233827>")
            else:
                embed.add_field(name="Colour..", value=colour)

            embed.add_field(name="Balance..", value=f"**{self.s}**{bal}")
            #embed.add_field(name="Experience..", value=f"{points}**XP**")
            embed.add_field(name="Inventory..", value=f":apple:**{users[member.id]['apple']}**:iphone:**{users[member.id]['iphone']}**:house:**{users[member.id]['house']}**")
            embed.set_footer(text="CONTACTS", icon_url="https://cdn1.iconfinder.com/data/icons/style-2-stock/807/Contacts-01.png")
            embed.set_thumbnail(url=member.avatar_url)
            await self.bot.say(embed=embed)
        else:
            await self.bot.say(f"{member.mention} doesn't have a bank account, create one with `siri bank create`!")


    @commands.command(pass_context=True)
    async def give(self, ctx, count:int, user: discord.User=None):
        """Give your money to another user"""
        with open('assets//economy.json', 'r') as f:
            users = json.load(f)

        #b = ''.join(count)

        if ctx.message.author == user:
            await self.bot.say("Giving money to yourself..?")

        elif count < 0:
            await self.bot.say(f"You can't give under **{self.s}**1!")

        elif users[ctx.message.author.id]['money'] < count:
            await self.bot.say(f"You don't have **{self.s}**{count}!")

        elif not user.id in users:
            await self.bot.say(f"{user.mention} doesn't have a bank account!")
        elif count is None:
            await self.bot.say("`Incorrect Usage`\n```siri give <@user> <count>```")

        elif ctx.message.author.id in users:
            #try:
            await self.add_money(users, user=user.id, count=count)
            await self.take_money(users, user=ctx.message.author.id, count=count)
            embed = discord.Embed(colour=0xeeeeff, description=f"{ctx.message.author.mention} has given {user.mention} **{self.s}**{count}!")
            await self.bot.say(embed=embed)

            with open('assets//economy.json', 'w') as f:
                json.dump(users, f)
            #except:
                #await self.bot.say("")
        else:
            await self.bot.say("You don't have a bank account, create one with `siri bank create`!") 


    @commands.command(pass_context=True)
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def daily(self, ctx):
        """Get your daily §15"""
        with open('assets//economy.json', 'r') as f:
            users = json.load(f)

        if ctx.message.author.id in users:
            await self.add_money(users, user=ctx.message.author.id, count=15)
            embed = discord.Embed(colour=0xeeeeff, description=f"For being a good sport all day, I have added **{self.s}**15 to your bank account! You can get more in **24**hrs!")
            embed.set_footer(text=f"Balance: {self.s}{users[ctx.message.author.id]['money']}")
            await self.bot.say(embed=embed)

            with open('assets//economy.json', 'w') as f:
                json.dump(users, f)
        else:
            await self.bot.say("You don't have a bank account, create one with `siri bank create`!") 

    @commands.command(pass_context=True, aliases=['bal'])
    async def balance(self, ctx, user:discord.User=None):
        """Check your balance"""
        with open('assets//economy.json', 'r') as f:
            users = json.load(f)

        if user is None:

            if ctx.message.author.id in users:
                embed = discord.Embed(colour=0x0e0eff, description=f"You have **{self.s}**{users[ctx.message.author.id]['money']} left in your bank account.")
                await self.bot.say(embed=embed)
            else:
                await self.bot.say("You don't have a bank account, create one with `siri bank create`!")  
        else:
            if user.id in users:
                embed = discord.Embed(colour=0x0e0eff, description=f"**{user.name}** has **{self.s}**{users[user.id]['money']} left.")
                await self.bot.say(embed=embed)
            else:
                await self.bot.say(f"{user.mention} doesn't have a bank account!") 


    @commands.group(pass_context=True)
    async def bank(self, ctx):
        if ctx.invoked_subcommand is None:
            with open('assets//economy.json', 'r') as f:
                users = json.load(f)

            if ctx.message.author.id in users:
                await self.bot.say("Check your balance with `siri balance`!")
            else:
                await self.bot.say("You don't have a bank account, create one with `siri bank create`!")


    @bank.command(pass_context=True, name="create")
    async def _create(self, ctx):
        """Create an account"""
        msg = await self.bot.say("Please wait..")
        with open('assets//economy.json', 'r') as f:
            users = json.load(f)

        if ctx.message.author.id in users:
            await self.bot.delete_message(msg)
            await self.bot.say("You already have an account!")
        else:

            await self.update_data(users, ctx.message.author.id)
            await self.add_money(users, user=ctx.message.author.id, count=20)

            with open('assets//economy.json', 'w') as f:
                json.dump(users, f)

            await self.bot.delete_message(msg)
            await self.bot.say(f"**Hooray!** I have successfully created a bank account for you! **P.S.** I gave you **{self.s}**20 as a welcome gift!")

    @bank.command(pass_context=True, name="fcreate")
    async def _fcreate(self, ctx, user: discord.User):
        """Create an account"""
        msg = await self.bot.say("Please wait..")
        with open('assets//economy.jsonn', 'r') as f:
            users = json.load(f)
        if ctx.message.author.id =='396153668820402197':

            await self.update_data(users, user.id)
            await self.add_money(users, user=user.id, count=20)

            with open('assets//economy.json', 'w') as f:
                json.dump(users, f)

            await self.bot.delete_message(msg)
            await self.bot.say(f"I have force-created an account for {user.mention}! (Also added **{self.s}**20 LOL)")
        else:
            trl = discord.Embed(title=("<:WrongMark:473277055107334144> You are not authorised to use this command!") , colour=0xff775b)
            trl.set_footer(text="Sorry about that.")
            await self.bot.say(embed=trl)


    @commands.command(pass_context=True)
    async def mtransfer(self, ctx, count:int, user: discord.User=None):
        with open('assets//economy.json', 'r') as f:
            users = json.load(f)
        if ctx.message.author.id =='396153668820402197':
            await self.bot.say(":ok_hand: Done.")
            try:
                await self.add_money(users, user=user.id, count=count)

                with open('assets//economy.json', 'w') as f:
                    json.dump(users, f)   
            except Exception as e:
                await self.bot.say("```e```")         
        else:
            trl = discord.Embed(title=("<:WrongMark:473277055107334144> You are not authorised to use this command!") , colour=0xff775b)
            trl.set_footer(text="Sorry about that.")
            await self.bot.say(embed=trl)


    async def update_data(self, users, user):
        users[user] = {}
        users[user]['money'] = 0
        users[user]['colour'] = 0
        users[user]['apple'] = 0
        users[user]['iphone'] = 0
        users[user]['house'] = 0
        users[user]['description'] = "DESCRIPTION NOT SET: `siri description <description>`"
        users[user]['birthday'] = "BNS"

    async def apple(self, users, user=None, count=None):
        users[user]['apple'] += count
        with open('assets//economy.json', 'w') as f:
                json.dump(users, f)

    async def iphone(self, users, user=None, count=None):
        users[user]['iphone'] += count
        with open('assets//economy.json', 'w') as f:
                json.dump(users, f)

    async def house(self, users, user=None, count=None):
        users[user]['house'] += count
        with open('assets//economy.json', 'w') as f:
                json.dump(users, f)

    async def set_desc(self, users, user=None, description=None):
        users[user]['description'] = description

    async def set_bday(self, users, user=None, date=None):
        users[user]['birthday'] = date

    async def set_col(self, users, user=None, colour=None):
        users[user]['colour'] = colour

    async def add_money(self, users, user=None, count=None):
        users[user]['money'] += count

    async def take_money(self, users, user=None, count=None):
        users[user]['money'] -= count

def setup(bot):
  bot.add_cog(Economy(bot))
