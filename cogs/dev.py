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
import datetime
from .utils import checks


class Developer:
    def __init__(self, bot):
        self.bot = bot
        self._last_result = None
                
    @commands.command(aliases=["resp"])
    @commands.is_owner()
    async def respond(self, ctx, ticket, id, *, message):
        try:
            target = discord.utils.get(self.bot.get_all_members(), id=id)
            embed = discord.Embed(colour=0x00a6ff, description=f"\"{message}\" - **{ctx.message.author}**")
            embed.set_author(name=f"In response to ticket #{ticket}..", icon_url=self.bot.user.avatar_url)
            await target.send(embed=embed)
            await ctx.send(f":incoming_envelope: I have sent the response to the owner of Ticket **#**{ticket}.")
        except:
            try:
                guild = self.bot.get_guild(id)
                target = discord.utils.get(guild.channels, name=ticket)
                embed = discord.Embed(colour=0x00a6ff, description=f"\"{message}\" - **{ctx.message.author}**")
                embed.set_author(name=f"Please turn on DMs for better support!", icon_url=self.bot.user.avatar_url)
                await target.send(embed=embed, content=":incoming_envelope: A member of this guild attempted to contact support, but had their DMs disabled! **Here is the response from our Support Team:**")
                await ctx.send(f":incoming_envelope: I have sent the response to the guild of the owner of that ticket") 
            except Exception as e:
                await ctx.send(f"**Error sending support response!**\n```{e}```")
            
    @commands.command(aliases=['debug', 'ev'])
    @commands.is_owner()
    async def eval(self, ctx, *, code):
        """thanksss skuwww"""
        try:
            env = {
                'bot': ctx.bot,
                'ctx': ctx,
                'channel': ctx.message.channel,
                'author': ctx.message.author,
                'guild': ctx.message.guild,
                'message': ctx.message,
                'discord': discord,
                'random': random,
                'commands': commands,
                'requests': requests,
                'os': os,
                '_': self._last_result
            }

            try:
                result = eval(code, env)
            except SyntaxError as e:
                embed = discord.Embed(colour=0x9059ff, description=":pencil2:**INPUT:**\n```py\n{}```\n:robot:**OUTPUT:**\n```py\n{}```".format(code, e))
                embed.set_footer(text="Code Evaluation", icon_url=self.bot.user.avatar_url)
                embed.timestamp = datetime.datetime.utcnow()
                await ctx.send(embed=embed)
                return
            except Exception as e:
                embed = discord.Embed(colour=0x9059ff, description=":pencil2:**INPUT:**\n```py\n{}```\n:robot:**OUTPUT:**\n```py\n{}```".format(code, e))
                embed.set_footer(text="Code Evaluation", icon_url=self.bot.user.avatar_url)
                embed.timestamp = datetime.datetime.utcnow()
                await ctx.send(embed=embed)
                return

            if asyncio.iscoroutine(result):
                result = await result

            self._last_result = result
            if code == "bot.http.token":
                embed = discord.Embed(colour=0x9059ff, description=":pencil2:**INPUT:**\n```py\n{}```\n:robot:**OUTPUT:**\n```py\nyou thought wrong.. slut```".format(code))
                embed.set_footer(text="Code Evaluation", icon_url=self.bot.user.avatar_url)
                embed.timestamp = datetime.datetime.utcnow()
                await ctx.send(embed=embed)

            else:
                if len(result) > 1500:
                    r = requests.post(f"https://hastebin.com/documents",
                    data=result.encode('utf-8')).json()
                    await self.bot.send_message(ctx.message.channel, ":weary::ok_hand: The output is too long to send to chat. Here is a hastebin file for ya.. :point_right: https://hastebin.com/" + r['key'])
                    return
                else:
                    try:
                        embed = discord.Embed(colour=0x9059ff, description=":pencil2:**INPUT:**\n```py\n{}```\n:robot:**OUTPUT:**\n```py\n{}```".format(code, result))
                        embed.set_footer(text="Code Evaluation", icon_url=self.bot.user.avatar_url)
                        embed.timestamp = datetime.datetime.utcnow()
                        await ctx.send(embed=embed)
                        return
                    except Exception as e:
                        embed = discord.Embed(colour=0x9059ff, description=":pencil2:**INPUT:**\n```py\n{}```\n:robot:**OUTPUT:**\n```py\n{}```".format(code, e))
                        embed.set_footer(text="Code Evaluation", icon_url=self.bot.user.avatar_url)
                        embed.timestamp = datetime.datetime.utcnow()
                        await ctx.send(embed=embed)
                        return

        except Exception as e:
            embed = discord.Embed(colour=0x9059ff, description=":pencil2:**INPUT:**\n```py\n{}```\n:robot:**OUTPUT:**\n```py\n{}```".format(code, e))
            embed.set_footer(text="Code Evaluation", icon_url=self.bot.user.avatar_url)
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)
            return
        
        
    @commands.command(pass_context=True, aliases=['fp', 'forcepost'])
    @commands.is_owner()
    async def post(self, ctx, e = None):
        if e is not None:
            try:
                headers = {'Authorization': fight_me}
                data = {'server_count': len(self.bot.guilds)}
                api_url = 'https://discordbots.org/api/bots/' + str(self.bot.user.id) + '/stats'
                p = requests.post(api_url, data=data, headers=headers).json()
                chan = self.bot.get_channel("478821892309123091")
                msg = await ctx.send("<a:loading:473279565670907914> **Posting** server count..")
                await asyncio.sleep(5)
                await msg.edit(f"<:CheckMark:473276943341453312> Server count **posted**! (`{p}`)")
                embed = discord.Embed(colour=0x008AE2, title="<a:dblheartbeat:393548388664082444> Update!", description="Server Count successfully posted to DBL! (**{}** Servers)".format(len(self.bot.servers)))
                embed.set_footer(text="Force-Posted")
                await chan.send(embed=embed)

            except Exception as e:
                fmt = '```py\n{}: {}\n```'
                embed = discord.Embed(title="<:WrongMark:473277055107334144> **An error occurred while processing your request**", color=0xff0000, description=fmt.format(type(e).__name__, e))
                await ctx.send(embed=embed)
        else:
            await ctx.send("no bitch ")
            

            
def setup(bot):
  bot.add_cog(Developer(bot))
