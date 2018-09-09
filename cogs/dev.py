import discord
from discord.ext import commands

from datetime import datetime
import requests

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
            
    @commands.command(pass_context=True, aliases=['eval', 'exec', 'ev', 'ex'], hidden=True)
    async def debug(self, ctx, *, code):
        if ctx.message.author.id =='396153668820402197':

            if code == 'bot.http.token':
                embed = discord.Embed(colour=0x9059ff, description=":pencil2:**INPUT:**\n```py\n{}```\n:robot:**OUTPUT:**\n```py\nyou thought wrong.. slut```".format(code))
                embed.set_footer(text="Code Evaluation | {}".format(ctx.message.timestamp.__format__('%A %H:%m')), icon_url=self.bot.user.avatar_url)
                await self.bot.say(embed=embed)
            elif code == 'bot.logout()':
                prm = '{object Promise}'
                embed = discord.Embed(colour=0x9059ff, description=":pencil2:**INPUT:**\n```py\n{}```\n:robot:**OUTPUT:**\n```py\n{}```".format(code, prm))
                embed.set_footer(text="Code Evaluation | {}".format(ctx.message.timestamp.__format__('%A %H:%m')), icon_url=self.bot.user.avatar_url)
                await self.bot.say(embed=embed)
                await self.bot.logout()
            elif code == 'bot.lcount':
                users = len(set(self.bot.get_all_members()))
                channels = len([c for c in self.bot.get_all_channels()])
                servers = str(len(self.bot.servers))
                prm = {"servers": servers, "channels": channels, "users": users}
                embed = discord.Embed(colour=0x9059ff, description=":pencil2:**INPUT:**\n```py\n{}```\n:robot:**OUTPUT:**\n```py\n{}```".format(code, prm))
                embed.set_footer(text="Code Evaluation | {}".format(ctx.message.timestamp.__format__('%A %H:%m')), icon_url=self.bot.user.avatar_url)
                await self.bot.say(embed=embed)
            elif code == 'print(bot.servers)':
                embed = discord.Embed(colour=0x9059ff, description=":pencil2:**INPUT:**\n```py\n{}```\n:robot:**OUTPUT:**\n```py\n:-```".format(code))
                embed.set_footer(text="Code Evaluation | {}".format(ctx.message.timestamp.__format__('%A %H:%m')), icon_url=self.bot.user.avatar_url)
                await self.bot.say(embed=embed)
                for e in self.bot.servers:
                    #users = len(set(self.bot.get_all_members()))
                    print(f"{e.name} [{e.id}] ({len(e.members)}),")
            elif code == 'cogs.economy.json':#yes my eval sux so i have to do it like this fuck off
                with open('assets\\economy.json', 'r') as f:
                    users = json.load(f)
                embed = discord.Embed(colour=0x9059ff, description=":pencil2:**INPUT:**\n```py\n{}```\n:robot:**OUTPUT:**\n```py\n{}```".format(code, users))
                embed.set_footer(text="Code Evaluation | {}".format(ctx.message.timestamp.__format__('%A %H:%m')), icon_url=self.bot.user.avatar_url)
                await self.bot.say(embed=embed)
            elif code == 'server.channels':
                 embed = discord.Embed(colour=0x9059ff, description=":pencil2:**INPUT:**\n```py\n{}```\n:robot:**OUTPUT:**\n```py\n{}```".format(code, list))
                 embed.set_footer(text="Code Evaluation | {}".format(ctx.message.timestamp.__format__('%A %H:%m')), icon_url=self.bot.user.avatar_url)
                 await self.bot.say(embed=embed)
                    
            else:
                


                author = ctx.message.author
                channel = ctx.message.channel

                code = code.strip('` ')
                result = None

                global_vars = globals().copy()
                global_vars['bot'] = self.bot
                global_vars['ctx'] = ctx
                global_vars['message'] = ctx.message
                global_vars['author'] = ctx.message.author
                global_vars['channel'] = ctx.message.channel
                global_vars['server'] = ctx.message.server

                try:
                    result = eval(code, global_vars, locals())
                except Exception as e:
                    embed = discord.Embed(colour=0x9059ff, description=":pencil2:**INPUT:**\n```py\n{}```\n:robot:**OUTPUT:**\n```py\n{}: {}```".format(code, type(e).__name__, str(e), lang="py"))
                    embed.set_footer(text="Code Evaluation | {}".format(ctx.message.timestamp.__format__('%A %H:%m')), icon_url=self.bot.user.avatar_url)
                    #await self.bot.say(('{}: {}'.format(type(e).__name__, str(e), lang="py")))
                    await self.bot.say(embed=embed)
                    return#enumerate(

                for page, i in result:

                    if i != 0 and i % 1 == 0:
                        b = open("khaki-eval.txt","w")
                        b.write("\n{}".format(page, lang="py"))
                        b.close()

                        await self.bot.send_message(ctx.message.channel, "The output is too long to send to chat. Here is the file..")
                        await self.bot.send_file(ctx.message.channel, 'assets\\eval.txt', filename=f'siri-eval.txt')
                        return
                    else:
                        embed = discord.Embed(colour=0x9059ff, description=":pencil2:**INPUT:**\n```py\n{}```\n:robot:**OUTPUT:**\n```py\n{}```".format(code, page, lang="py"))
                        embed.set_footer(text="Code Evaluation | {} ".format(ctx.message.timestamp.__format__('%A %H:%m')), icon_url=self.bot.user.avatar_url)
                        #await self.bot.say(('{}: {}'.format(type(e).__name__, str(e), lang="py")))
                        await self.bot.say(embed=embed)
                        return
        else:
            trl = discord.Embed(title=("<:WrongMark:473277055107334144> You are not authorised to use this command!") , colour=0xff775b)

            await self.bot.say(embed=trl)
            

            
def setup(bot):
  bot.add_cog(Developer(bot))
