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

extensions = ['cogs.utility', 'cogs.help', 'cogs.economy', 'cogs.dev', 'cogs.music']

class Siri(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(command_prefix=config.prefixes)
        self.remove_command("help")
        self.add_command(self.shutdown)
        self.add_command(self.restart)
        self.add_command(self.pull)
        self.add_command(self.shell)
        self.add_command(self.ping)
        self.add_command(self.load)
        self.add_command(self.unload)
        self.add_command(self.reload)
        
    async def on_message_edit(self, before, after):
        if not self.is_ready() or after.author.bot:
            return

        await self.process_commands(after)#hi thanks

    async def run_cmd(self, cmd: str) -> str:
         process =\
         await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
         results = await process.communicate()
         return "".join(x.decode("utf-8") for x in results)

    async def status_task(self):
        users = len(set(self.get_all_members()))
        sayings = [f'{users} users smile', f'{str(len(self.guilds))} guilds', 'What can I help you with?']
        while True:
            game = discord.Activity(name=f'{rnd(sayings)} | siri help', type=discord.ActivityType.watching)
            await self.change_presence(status=discord.Status.online, activity=game)
            await asyncio.sleep(30)

    async def on_ready(self):
        log = self.get_channel(493330793599598592)
        print(f'\n ____  _      _ \n'\
                '/ ___|(_)_ __(_)\n'\
                '\___ \| |  __| |\n'\
                ' ___) | | |  | |\n'\
                '|____/|_|_|  |_|')
        print('\n------')
        print(f'[UPDATE] Logged in as: {self.user.name} ({str(self.user.id)})')
        print(f"[AWAITING] Run 'siri load all'")
        self.loop.create_task(self.status_task())
        embed = discord.Embed(title='⚡ **Siri** is connected!', description=f"**Guilds**.. `{str(len(self.guilds))}`")
        try:
            await log.send(embed=embed)
        except:
            print('\n\nfailed to send message to 478821892309123091 (#logs)')

    async def on_guild_join(self, guild):
        log = self.get_channel(493330793599598592)
        server = guild
        embed = discord.Embed(colour=0xf44141, description=f"Siri has joined `{guild.name}`! Siri is now in `{str(len(self.guilds))}` guilds!")
        embed.set_footer(text=f'ID: {guild.id}', icon_url=guild.icon_url_as(format='png'))
        await log.send(embed=embed)
        targets = [
            discord.utils.get(server.channels, name="bot"),
            discord.utils.get(server.channels, name="bots"),
            discord.utils.get(server.channels, name="bot-commands"),
            discord.utils.get(server.channels, name="bot-spam"),
            discord.utils.get(server.channels, name="bot-channel"),
            discord.utils.get(server.channels, name="testing"),
            discord.utils.get(server.channels, name="testing-1"),
            discord.utils.get(server.channels, name="general"),
            discord.utils.get(server.channels, name="shitposts"),
            guild.get_member(guild.owner.id)
            ]
        embed = discord.Embed(colour=0x0000ff, title="👋 Hello!", description="Hello! I am DiscordSiri.\n\n> **For help, do** `siri help`\n> **For support, do** `siri ticket <message>`\n> **Want even more support? Join my guild:** https://discord.gg/CjRP2Mc\n> **To chat with me, ping me!**\n> **To create a profile and start earning §, do** `siri bank create`\n\n> **Other prefixes:** `hey siri`  `siri,`")
        embed.set_image(url="https://image.ibb.co/mJY82z/siribanner.png")
        embed.set_footer(text="Siri created by lukee#0420", icon_url=self.user.avatar_url)
        for x in targets:
            try:
                await x.send(embed=embed)
            except:
                continue
            break

    async def on_guild_remove(self, guild):
        log = self.get_channel(493330793599598592)
        embed = discord.Embed(colour=0x62f442, description=f"Siri has been kicked from `{guild.name}`.. Siri is now in `{str(len(self.guilds))}` guilds.")
        embed.set_footer(text=f'ID: {guild.id}', icon_url=guild.icon_url_as(format='png'))
        await log.send(embed=embed)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def shutdown(self, ctx):
        await ctx.send("Goodbye. Nice talking to you.")
        await self.logout()

    @commands.command(hidden=True)
    @commands.is_owner()
    async def restart(self, ctx):
        await ctx.send("I'll see you in a bit!")
        await self.logout()
        subprocess.call([sys.executable, r"launcher.py"])
            
            
    @commands.command(hidden=True)
    @commands.is_owner()
    async def pull(self, ctx):
        msg = await ctx.send("Pulling..")
        shell = await self.run_cmd('git pull Siri --no-commit --no-edit --ff-only master')
        await self.run_cmd('git fetch --all')
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
        embed.set_author(name="Please Wait.", icon_url=self.user.avatar_url)
        msg = await ctx.send(embed=embed)
        shell = await self.run_cmd(code)
        embed = discord.Embed(colour=0x000fff, description=f"```css\n{shell}```")
        embed.set_author(name="Shell", icon_url=self.user.avatar_url)
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
                print(f'[UPDATE] Loaded all modules')
                print("------\n\n")
                for extension in extensions:
                    loaded = []
                    not_loaded = []
                    try:
                        self.load_extension(extension)
                        loaded.append(f'`{extension}`')    
                    except Exception as error:
                        not_loaded.append(f'`{extension}` - `{error}`')
                        print('\n\nEXTEN./COG ERROR: {} was not loaded due to an error: \n-- [{}] --\n\n'.format(extension, error))
                    
                    loaded = '\n'.join(loaded)
                    not_loaded = '\n'.join(not_loaded)
                    embed = discord.Embed(colour=0x0000ff)
                    embed.add_field(name='Loaded', value=loaded)
                    if not_loaded is None:
                        embed.add_field(name='Not Loaded', value=not_loaded)
                        
                    await ctx.send(embed=embed)
            else:
                self.load_extension("cogs.{}".format(extension))
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
        self.unload_extension("cogs.{}".format(extension))
        embed = discord.Embed(title="<:CheckMark:473276943341453312> Cog unloaded:", color=0x5bff69, description="**Cog:** `cogs\{}.py`".format(extension))
        await ctx.send(embed=embed)
            

    @commands.command(aliases=['re'], hidden=True)
    @commands.is_owner()
    async def reload(self, ctx, extension):
        try:
            self.unload_extension("cogs.{}".format(extension))
            self.load_extension("cogs.{}".format(extension))
            embed = discord.Embed(title="<:CheckMark:473276943341453312> Cog reloaded:", color=0x5bff69, description="**Cog:** `cogs\{}.py`".format(extension))
            await ctx.send(embed=embed)
            print('\n\nCOG RELOAD\n--[Cog reloaded, {}.py]--\n\n'.format(extension))
        except Exception as error:
            print('\n\nEXTEN./COG ERROR: {} was not reloaded due to an error: \n-- [{}] --\n\n'.format(extension, error))
            embed = discord.Embed(title="<:WrongMark:473277055107334144> Error reloading cog:", color=0xff775b, description="**Cog:** `cogs\{}.py`\n**Errors:**\n```{}```".format(extension, error))
            await ctx.send(embed=embed)

    async def on_command_error(self, ctx, error):
        colours = [0x37749c, 0xd84eaf, 0x45b4de, 0x42f4c5, 0xffb5f3, 0x42eef4, 0xe751ff, 0x51ffad]
        if isinstance(error, commands.NotOwner):
            trl = discord.Embed(title=("<:WrongMark:473277055107334144> You are not authorised to use this command!") , colour=0xff775b)
            trl.set_footer(text="Sorry About That.")
            await ctx.send(embed=trl)
        elif isinstance(error, commands.BadArgument):
            embed = discord.Embed(title=("<:WrongMark:473277055107334144> There was an error!") , colour=0xff775b, description=f"```py\n{error}```")
            await ctx.send(embed=embed)
        elif isinstance(error, commands.CommandOnCooldown):
            minutes, seconds = divmod(error.retry_after, 60)
            hours, minutes = divmod(minutes, 60)
            if hours >= 1:
                hours = f"{round(hours)}h"
            else:
                hours = ""
            embed = discord.Embed(colour=rnd(colours), description=f":alarm_clock: **You are on cooldown!** Please wait **{hours} {round(minutes)}m {round(seconds)}s**.")
            await ctx.send(embed=embed)
        else:
            print(f"[{type(error).__name__.upper()}]: {error}")

    async def on_message(self, message):
        if message.author.bot: return
        await self.process_commands(message)
        

    def run(self):
        super().run(config.token, reconnect=True)
       
