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
from pymongo import MongoClient
import pymongo

client = MongoClient(config.mongo_client)
db = client['siri']

class Moderation:
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def logs(self, ctx, channel:discord.TextChannel=None):
        """Set logs for your server"""
        if ctx.author.guild_permissions.kick_members:
            servers = db.utility.find_one({"utility": "serverconf"})
            if not channel:
                await ctx.send("<:redtick:492800273211850767> You didn't specify which channel.")
            elif ctx.guild.id in servers[0]['logs']:
                await ctx.send(f"Turned logs off for this server.")
                db.utility.update_one({"utility": "serverconf"}, {"$pull":{"logs": {ctx.guild.id: channel.id}}})
            else:
                await ctx.send(f"Turned logs on for {channel.mention}.")
                db.utility.update_one({"utility": "serverconf"}, {"$push":{"logs": {ctx.guild.id: channel.id}}})
        else:
            await ctx.send("<:redtick:492800273211850767> You don't have permission `manage_guild`.")
            
    @commands.command(pass_context=True)
    async def kick(self, ctx, user: discord.Member= None, *, reason=None):
        author = ctx.message.author
        guild = ctx.message.guild
        if author.guild_permissions.kick_members:
            if reason is None:
                await guild.kick(user)
                await ctx.send(f"<:greentick:492800272834494474> **{user.name}** has been **kicked** by **{author.name}**!")
                try:
                    await user.send(f":boot: You have been **kicked** from **{ctx.guild}**! **Reason:** *N/A*")
                except:
                    pass
            else:
                await guild.kick(user, reason=f"\"{reason}\" - {author}")            
                await ctx.send(f"<:greentick:492800272834494474> **{user.name}** has been **kicked** by **{author.name}**! **Reason:** `{reason}`")
                try:
                    await user.send(f":boot: You have been **kicked** from **{ctx.guild}**! **Reason:** `{reason}`")
                except:
                    pass
        else:
            await ctx.send(f"<:redtick:492800273211850767> You're not a mod..")

    @commands.command(pass_context=True)
    async def ban(self, ctx, user: discord.Member= None, *, reason=None):
        author = ctx.message.author
        guild = ctx.message.guild
        if author.guild_permissions.ban_members:
            if reason is None:
                try:
                    await user.send(f":hammer_pick: You have been **banned** from **{ctx.guild}**! **There was no reason set for your ban**")
                except:
                    pass
                await guild.ban(user, reason=f"Ban by {ctx.author} [NO REASON]")
                await ctx.send(f"<:greentick:492800272834494474> **{user.name}** has been **banned** by **{ctx.message.author.name}**!")
            else:
                try:
                    await user.send(f":hammer_pick: You have been **banned** from **{ctx.guild}**! **Reason:** `{reason}`")
                except:
                    pass
                await guild.ban(user, reason=f"\"{reason}\" - Ban by {ctx.author}")
                await ctx.send(f"<:greentick:492800272834494474> **{user.name}** has been **banned** by **{ctx.message.author.name}**! **Reason:** `{reason}`")
        else:
            await ctx.send(f"<:redtick:492800273211850767> You're not a mod!")
            
    @commands.command(pass_context=True, aliases=['idban'])
    async def hackban(self, ctx, uid:int, *, reason=None):
        author = ctx.author
        guild = ctx.guild
        if author.guild_permissions.ban_members:
            if not reason:
                await self.bot.http.ban(user_id=uid, guild_id=guild.id, reason=f"[NO REASON] - ID-Ban by {ctx.author}")
                await ctx.send(f"<:greentick:492800272834494474> **Unknown User** has been **banned** by **{ctx.message.author.name}**!")
            else:
                await self.bot.http.ban(user_id=uid, guild_id=guild.id, reason=f"\"{reason}\" - ID-Ban by {ctx.author}")
                await ctx.send(f"<:greentick:492800272834494474> **Unknown User** has been **banned** by **{ctx.message.author.name}**! **Reason:** `{reason}`")
        else:
            await ctx.send(f"<:redtick:492800273211850767> You're not a mod!")

    @commands.command(pass_context=True)
    async def mute(self, ctx, user: discord.Member= None, amount:int=None):
        author = ctx.message.author
        guild = ctx.message.guild
        if author.guild_permissions.kick_members:
            role = discord.utils.get(ctx.guild.roles, name="Muted")
            await user.add_roles(role)
            
            if amount is None:
                await ctx.send(f"<:greentick:492800272834494474> **{user.name}** has been **muted** for **10 minutes**! (default time!)")
                try:
                    await user.send(f"You have been **muted** in **{ctx.guild}**! **Time:** `10 minutes (600 seconds)`")  
                except:
                    pass
                await asyncio.sleep(600)
                await user.remove_roles(role)
                try:
                    await user.send(f"You have been **unmuted** in **{ctx.guild}**!")
                except:
                    pass
            else:
                seconds = amount * 60
                await ctx.send(f"<:greentick:492800272834494474> **{user.name}** has been **muted** for **{amount} minute(s)**!")
                await user.send(f"You have been **muted** in **{ctx.guild}**! **Time:** `{amount} minute(s) ({seconds} seconds)`")
                try:
                    await asyncio.sleep(seconds)
                    await user.remove_roles(role)
                    try:
                        await user.send(f"You have been **unmuted** in **{ctx.guild}**!")
                    except:
                        pass
                except Exception as e:
                    await ctx.send(e)
        else:
            await ctx.send(f"<:redtick:492800273211850767> You're not a mod..")

    @commands.command(pass_context=True)
    async def unmute(self, ctx, user: discord.Member= None):
        author = ctx.message.author
        guild = ctx.message.guild
        if author.guild_permissions.kick_members:
            try:
                role = discord.utils.get(ctx.guild.roles, name="Muted")
                await ctx.send(f"<:greentick:492800272834494474> **{user.name}** has been unmuted!")
                await user.remove_roles(role)
                try:
                    await user.send(f"You have been **unmuted** in **{ctx.guild}**!")
                except:
                    pass
            except:
                await ctx.send(f"<:redtick:492800273211850767> **{user.name}** isn't muted!")
        else:
            await ctx.send(f"<:redtick:492800273211850767> You're not a mod..")
            



def setup(bot):
    bot.add_cog(Moderation(bot))
