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
        
    async def on_member_join(self, member):
        if not member.id == 481337766379126784:
            servers = db.utility.find_one({"utility": "serverconf"})
            findings = None
            for x in servers['logs']:
                if x['guild'] == member.guild.id:
                    findings = x 
            if findings:
                await self.bot.get_channel(findings['channel']).send(f":wave: **{member}** has joined the server. `ID: {member.id}`")
            
    async def on_member_remove(self, member):
        if not member.id == 481337766379126784:
            servers = db.utility.find_one({"utility": "serverconf"})
            findings = None
            for x in servers['logs']:
                if x['guild'] == member.guild.id:
                    findings = x 
            if findings:
                await self.bot.get_channel(findings['channel']).send(f":wave: **{member}** has left the server. `ID: {member.id}`")
            
    async def on_message_edit(self, before, after):
        if not before.author.id == 481337766379126784:
            servers = db.utility.find_one({"utility": "serverconf"})
            findings = None
            for x in servers['logs']:
                if x['guild'] == before.guild.id:
                    findings = x 
            if findings:
                embed = discord.Embed(colour=0xffff00)
                embed.add_field(name="Before", value=before.content)
                embed.add_field(name="After", value=after.content)
                embed.set_footer(text="Message Edit") 
                embed.timestamp = datetime.datetime.utcnow()
                await self.bot.get_channel(findings['channel']).send(embed=embed, content=f":pencil: **{before.author}** edited a message in {before.channel.mention}:")
            
    async def on_message_delete(self, message):
        if not message.author.id == 481337766379126784:
            servers = db.utility.find_one({"utility": "serverconf"})
            findings = None
            for x in servers['logs']:
                if x['guild'] == message.guild.id:
                    findings = x 
            if findings:
                embed = discord.Embed(colour=0xff0000)
                embed.add_field(name="Content", value=message.content)
                embed.set_footer(text="Message Delete") 
                embed.timestamp = datetime.datetime.utcnow()
                await self.bot.get_channel(findings['channel']).send(embed=embed, content=f":wastebasket: **{message.author}** deleted a message in {message.channel.mention}:")
 
async def on_member_update(self, before, after):
    if not before.id == 481337766379126784:
        servers = db.utility.find_one({"utility": "serverconf"})
        findings = None
        print(dir(before))
        for x in servers['logs']:
            if x['guild'] == before.guild.id:
                findings = x 
        if findings:                    
            if not before.nick == after.nick:
                
                embed = discord.Embed(colour=0xffff00)
                embed.add_field(name="Before", value=before)
                embed.add_field(name="After", value=after)
                embed.set_footer(text="Nickname Edit") 
                embed.timestamp = datetime.datetime.utcnow()   
                await self.bot.get_channel(findings['channel']).send(embed=embed, content=f":name_badge: **{member}** has changed their nickname:")
                
            elif not before.roles == after.roles:
                
                if int(before.roles) > int(after.roles):
                    type = "Add"
                    colour = 0x00ff00
                else:
                    type = "Remove"
                    colour = 0xff0000
                role = 'h'    
                embed = discord.Embed(colour=colour)
                embed.add_field(name="Role", value=role)
                embed.set_footer(text=f"Role {type}") 
                embed.timestamp = datetime.datetime.utcnow()   
                await self.bot.get_channel(findings['channel']).send(embed=embed, content=f":ledger: **{member}** has got their roles updated:")
            else:
                print('p')
            
async def on_user_update(self, before, after):
    if not before.id == 481337766379126784:
        servers = db.utility.find_one({"utility": "serverconf"})
        findings = None
        for x in servers['logs']:
            if x['guild'] == before.guild.id:
                findings = x 
        if findings:
            if not before.name == after.name:
                
                embed = discord.Embed(colour=0xffff00)
                embed.add_field(name="Before", value=before)
                embed.add_field(name="After", value=after)
                embed.set_footer(text="Username Edit") 
                embed.timestamp = datetime.datetime.utcnow()   
                await self.bot.get_channel(findings['channel']).send(embed=embed, content=f":page_facing_up: **{member}** has changed their username:")
                
            elif not before.avatar == after.avatar:
                
                embed = discord.Embed(colour=0xff0000)
                embed_after = discord.Embed(colour=0x00ff00)
                embed.add_field(name="Avatar Before", value=before.avatar_url_as(format='png'))  
                embed.add_field(name="Avatar After", value=after.avatar_url_as(format='png'))
                embed.set_footer(text="Avatar Update") 
                embed.timestamp = datetime.datetime.utcnow() 
                await self.bot.get_channel(findings['channel']).send(embed=embed, content=f":frame_photo: **{member}** has changed their avatar:")
            else:
                print('p')

                

                    
    @commands.command()
    async def logs(self, ctx, channel:discord.TextChannel=None):
        """Set logs for your server"""
        if ctx.author.guild_permissions.kick_members:
            servers = db.utility.find_one({"utility": "serverconf"})
            findings = None
            for x in servers['logs']:
                if x['guild'] == ctx.guild.id:
                    findings = x
            if not channel:
                await ctx.send("<:redtick:492800273211850767> You didn't specify a channel.")
            elif findings:
                await ctx.send("Turned logs off for this server.")
                db.utility.update_one({"utility": "serverconf"}, {"$pull":{ "logs": {"guild": ctx.guild.id, "channel": channel.id}}})
            else:
                await ctx.send(f"Turned logs on for {channel.mention}.")
                db.utility.update_one({"utility": "serverconf"}, {"$push": {"logs": {"guild":ctx.guild.id, "channel": channel.id}}})
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
