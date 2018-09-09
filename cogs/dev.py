import discord
from discord.ext import commands

from datetime import datetime
import requests
import os

import time
from random import choice, randint
import random
from discord.ext.commands import errors, converter
from random import choice as rnd

import aiohttp
import asyncio
import json
from .utils import checks


class Developer:
    def __init__(self, bot):
        self.bot = bot
        self._last_result = None
                
    @commands.command(pass_context=True, aliases="resp")
    async def respond(self, ctx, ticket, id, *, message):
        if ctx.message.author.id =='396153668820402197':
            try:
                target = discord.utils.get(self.bot.get_all_members(), id=id)
                embed = discord.Embed(colour=0x00a6ff, description=f"\"{message}\" - **{ctx.message.author}**")
                embed.set_author(name=f"In response to ticket #{ticket}..", icon_url=self.bot.user.avatar_url)
                await self.bot.send_message(target, embed=embed)
                await self.bot.say(f":incoming_envelope: I have sent the response to the owner of Ticket **#**{ticket}.")
            except:
                try:
                    server = self.bot.get_server(id)
                    target = discord.utils.get(server.channels, name=ticket)
                    embed = discord.Embed(colour=0x00a6ff, description=f"\"{message}\" - **{ctx.message.author}**")
                    embed.set_author(name=f"Please turn on DMs for better support!", icon_url=self.bot.user.avatar_url)
                    await self.bot.send_message(target, embed=embed, content=":incoming_envelope: A member of this server attempted to contact support, but had their DMs disabled! **Here is the response from our Support Team:**")
                    await self.bot.say(f":incoming_envelope: I have sent the response to the server of the owner of that ticket") 
                except Exception as e:
                    await self.bot.say(f"**Error sending support response!**\n```{e}```")
        else:
            trl = discord.Embed(title=("<:WrongMark:473277055107334144> You are not authorised to use this command!") , colour=0xff775b)
            trl.set_footer(text="Sorry about that.")
            await self.bot.say(embed=trl)
            
    @commands.command(pass_context=True, aliases=['debug', 'ev'])
    async def eval(self, ctx, *, code):
        """thanksss skuwww"""
        try:
            env = {
                'bot': ctx.bot,
                'ctx': ctx,
                'channel': ctx.message.channel,
                'author': ctx.message.author,
                'guild': ctx.message.server,
                'message': ctx.message,
                'discord': discord,
                'commands': commands,
                'requests': requests,
                'os': os,
                '_': self._last_result
            }

            try:
                result = eval(code, env)
            except SyntaxError as e:
                embed = discord.Embed(colour=0x9059ff, description=":pencil2:**INPUT:**\n```py\n{}```\n:robot:**OUTPUT:**\n```py\n{}: {}```".format(code, e, lang="py"))
                embed.set_footer(text="Code Evaluation | {}".format(ctx.message.timestamp.__format__('%A %H:%m')), icon_url=self.bot.user.avatar_url)
                await self.bot.say(embed=embed)
                return
            except Exception as e:
                embed = discord.Embed(colour=0x9059ff, description=":pencil2:**INPUT:**\n```py\n{}```\n:robot:**OUTPUT:**\n```py\n{}: {}```".format(code, e, lang="py"))
                embed.set_footer(text="Code Evaluation | {}".format(ctx.message.timestamp.__format__('%A %H:%m')), icon_url=self.bot.user.avatar_url)
                await self.bot.say(embed=embed)
                return

            if asyncio.iscoroutine(result):
                result = await result

            self._last_result = result
            if code == "bot.http.token":
                embed = discord.Embed(colour=0x9059ff, description=":pencil2:**INPUT:**\n```py\n{}```\n:robot:**OUTPUT:**\n```py\nyou thought wrong.. slut```".format(code))
                embed.set_footer(text="Code Evaluation | {}".format(ctx.message.timestamp.__format__('%A %H:%m')), icon_url=self.bot.user.avatar_url)
                await self.bot.say(embed=embed)

            else:
                if len(result) > 1500:
                    await self.bot.send_message(ctx.message.channel, ":weary::ok_hand: The output is too long to send to chat. Here is **a** file..")
                    await self.bot.send_file(ctx.message.channel, 'assets\\hentai.txt', filename=f'click-for-hentai.txt')
                    return
                else:
                    try:
                        embed = discord.Embed(colour=0x9059ff, description=":pencil2:**INPUT:**\n```py\n{}```\n:robot:**OUTPUT:**\n```py\n{}: {}```".format(code, result, lang="py"))
                        embed.set_footer(text="Code Evaluation | {}".format(ctx.message.timestamp.__format__('%A %H:%m')), icon_url=self.bot.user.avatar_url)
                        await self.bot.say(embed=embed)
                        return
                    except Exception as e:
                        embed = discord.Embed(colour=0x9059ff, description=":pencil2:**INPUT:**\n```py\n{}```\n:robot:**OUTPUT:**\n```py\n{}: {}```".format(code, e, lang="py"))
                        embed.set_footer(text="Code Evaluation | {}".format(ctx.message.timestamp.__format__('%A %H:%m')), icon_url=self.bot.user.avatar_url)
                        await self.bot.say(embed=embed)
                        return
                    
        except Exception as e:
            embed = discord.Embed(colour=0x9059ff, description=":pencil2:**INPUT:**\n```py\n{}```\n:robot:**OUTPUT:**\n```py\n{}: {}```".format(code, e, lang="py"))
            embed.set_footer(text="Code Evaluation | {}".format(ctx.message.timestamp.__format__('%A %H:%m')), icon_url=self.bot.user.avatar_url)
            await self.bot.say(embed=embed)
            return
            

            
def setup(bot):
  bot.add_cog(Developer(bot))
