import discord
from discord.ext import commands

import datetime

import time
import subprocess
import traceback
from discord.ext.commands import errors, converter
import requests
import random
from random import choice as rnd
from random import choice, randint

import aiohttp
import asyncio
import sys
import json

import config

extensions = ['cogs.utility', 'cogs.help', 'cogs.economy', 'cogs.dev', 'cogs.music', 'cogs.server', 'cogs.levels']

class Botdev(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
    async def run_cmd(self, cmd: str) -> str:
         process =\
         await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
         results = await process.communicate()
         return "".join(x.decode("utf-8") for x in results)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def shutdown(self, ctx):
        await ctx.send("Shutting down..")
        await self.bot.logout()
                    
    @commands.command(hidden=True)
    @commands.is_owner()
    async def pull(self, ctx):
        msg = await ctx.send("Pulling..")
        shell = await self.run_cmd('git pull Siri --no-commit --no-edit --ff-only master')
        shell = str(shell)
        shell = shell.replace("https://github.com/paixlukee/Siri", "Github")
        embed = discord.Embed(colour=0x0000ff, description=f"```css\n{shell}```")
        embed.set_author(name="Pulled from Git..", icon_url="https://avatars0.githubusercontent.com/u/9919?s=280&v=4")
        await msg.delete()
        await ctx.send(embed=embed)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def shell(self, ctx, *, code):
        embed = discord.Embed(colour=0x000fff, description=f"```css\nConnecting to shell..```")
        embed.set_author(name="Please Wait.", icon_url=self.bot.user.avatar_url)
        msg = await ctx.send(embed=embed)
        shell = await self.run_cmd(code)
        embed = discord.Embed(colour=0x000fff, description=f"```css\n{shell}```")
        embed.set_author(name="Shell", icon_url=self.bot.user.avatar_url)
        await msg.delete()
        await ctx.send(embed=embed)


    @commands.command(pass_context=True)
    async def ping(self, ctx):
        """Get Siri's Ping"""
        t1 = time.perf_counter()
        await ctx.trigger_typing()
        t2 = time.perf_counter()
        ping_desc = ("Ping: `" + str(round((t2-t1)*1000)) + "ms`!")
        embed = discord.Embed(description=ping_desc)
        await ctx.send(embed=embed)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def load(self, ctx, extension):
        try:
            if extension == 'all':
                print('\x1b[1;36;40m' + '[UPDATE]: ' + '\x1b[0m' + 'Loaded all modules')
                print("------\n\n")
                loaded = []
                not_loaded = []
                for extension in extensions:
                    try:
                        self.bot.load_extension(extension)
                        loaded.append(f'`{extension}`')    
                    except Exception as error:
                        not_loaded.append(f'`{extension}` - `{error}`')
                        print('\x1b[1;31;40m' + '[COG-LOAD-ERROR]: ' + '\x1b[0m' + '{} was not loaded due to an error: {} '.format(extension, error))
                    
                loaded = '\n'.join(loaded)
                not_loaded = '\n'.join(not_loaded)
                embed = discord.Embed(colour=0x0000ff)
                embed.add_field(name='Loaded', value=loaded)
                if not_loaded is None:
                    embed.add_field(name='Not Loaded', value=not_loaded)
                await ctx.send(embed=embed)
            else:
                self.bot.load_extension("cogs.{}".format(extension))
                embed = discord.Embed(title="<:CheckMark:473276943341453312> Cog loaded:", color=0x5bff69, description="**Cog:** `cogs\{}.py`".format(extension))
                await ctx.send(embed=embed)
                print('\n\nCOG LOAD\n--[Cog loaded, {}.py]--\n\n'.format(extension))
        except Exception as error:
            print('\n\nEXTEN./COG ERROR: {} was not loaded due to an error: \n-- [{}] --\n\n'.format(extension, error))
            embed = discord.Embed(title="<:WrongMark:473277055107334144> Error loading cog:", color=0xff775b, description="**Cog:** `cogs\{}.py`\n**Errors:**\n```{}```".format(extension, error))
            await ctx.send(embed=embed)

    @commands.command(aliases=['un'], hidden=True)
    @commands.is_owner()
    async def unload(self, ctx, extension):
        self.bot.unload_extension("cogs.{}".format(extension))
        embed = discord.Embed(title="<:CheckMark:473276943341453312> Cog unloaded:", color=0x5bff69, description="**Cog:** `cogs\{}.py`".format(extension))
        print('\x1b[1;32;40m' + '[COG-RELOADED]: ' + '\x1b[0m' + '{} was unloaded successfully'.format(extension))
        await ctx.send(embed=embed)
            

    @commands.command(aliases=['re'], hidden=True)
    @commands.is_owner()
    async def reload(self, ctx, extension):
        try:
            self.bot.unload_extension("cogs.{}".format(extension))
            self.bot.load_extension("cogs.{}".format(extension))
            embed = discord.Embed(title="<:CheckMark:473276943341453312> Cog reloaded:", color=0x5bff69, description="**Cog:** `cogs\{}.py`".format(extension))
            await ctx.send(embed=embed)
            print('\n\nCOG RELOAD\n--[Cog reloaded, {}.py]--\n\n'.format(extension))
            print('\x1b[1;32;40m' + '[COG-RELOADED]: ' + '\x1b[0m' + '{} was loaded successfully'.format(extension))
        except Exception as error:
            print('\x1b[1;31;40m' + '[COG-RELOAD-ERROR]: ' + '\x1b[0m' + '{} was not reloaded due to an error: {} '.format(extension, error))
            embed = discord.Embed(title="<:WrongMark:473277055107334144> Error reloading cog:", color=0xff775b, description="**Cog:** `cogs\{}.py`\n**Errors:**\n```{}```".format(extension, error))
            await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        colours = [0x37749c, 0xd84eaf, 0x45b4de, 0x42f4c5, 0xffb5f3, 0x42eef4, 0xe751ff, 0x51ffad]
        if isinstance(error, commands.NotOwner):
            #trl = discord.Embed(title=("<:WrongMark:473277055107334144> You are not authorised to use this command!") , colour=0xff775b)
            #trl.set_footer(text="Sorry About That.")
            await ctx.send("<:redtick:492800273211850767> You are not authorised to use this command!")
        elif isinstance(error, commands.BadArgument):
            #embed = discord.Embed(title=("<:WrongMark:473277055107334144> There was an error!") , colour=0xff775b, description=f"```py\n{error}```")
            await ctx.send(f"<:redtick:492800273211850767> Error! {error}")
        elif isinstance(error, commands.CommandOnCooldown):
            minutes, seconds = divmod(error.retry_after, 60)
            hours, minutes = divmod(minutes, 60)
            if hours >= 1:
                hours = f"{round(hours)}h"
            else:
                hours = ""
            #embed = discord.Embed(colour=rnd(colours), description=f":alarm_clock: **You are on cooldown!** Please wait **{hours} {round(minutes)}m {round(seconds)}s**.")
            await ctx.send(f"<:redtick:492800273211850767> You are on cooldown! Please wait **{hours} {round(minutes)}m {round(seconds)}s**.")
        else:
            print("\x1b[1;31;40m" + f"[{type(error).__name__.upper()}]:" + "\x1b[0m" + error)
            
def setup(bot):
    bot.add_cog(Botdev(bot))
