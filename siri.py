import discord
from discord.ext import commands

import datetime

import time
import subprocess
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

extension = ['cogs.utility', 'cogs.help', 'cogs.crypto', 'cogs.economy']

class Siri(commands.AutoShardedBot):
    def __init__(self):
        prefixes = ['hey siri ', 'siri ', 'Siri ', 'Hey Siri ', 'siri, '] 
        super().__init__(command_prefix=prefixes)
        self.remove_command("help")
        self.add_command(self.shutdown)
        self.add_command(self.cl)
        self.add_command(self.restart)
        self.add_command(self.pull)
        self.add_command(self.shell)
        self.add_command(self.ping)
        self.add_command(self.load)
        self.add_command(self.unload)
        self.add_command(self.reload)

    async def run_cmd(self, cmd: str) -> str:
         process =\
         await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
         results = await process.communicate()
         return "".join(x.decode("utf-8") for x in results)

    async def status_task(self):
        users = len(set(self.get_all_members()))
        sayings = [f'{users} users smile', f'{str(len(self.guilds))} guilds', 'What can I help you with?']
        while True:
            # await self.change_presence(game=discord.Game(name=, type=3))
            game = discord.Activity(name=f'{rnd(sayings)} | siri help', type=discord.ActivityType.watching)
            await self.change_presence(status=discord.Status.online, activity=game)
            await asyncio.sleep(30)

    async def on_ready(self):
        log = self.get_channel(478821892309123091)
        print('\n\n------')
        print('Logged in as:\n')
        print(self.user.name)
        print(str(self.user.id))
        print('------\n\n')
        self.loop.create_task(self.status_task())
        embed = discord.Embed(title='⚡ **Siri** is connected!', description=f"**guilds**.. `{str(len(self.guilds))}`")
        try:
            await log.send(embed=embed)
        except:
            pass #this is just to ignore the error message luke :P

    async def on_guild_join(self, guild):
        log = self.get_channel(478821892309123091)
        embed = discord.Embed(description=f":tada: **Yay!** Siri has joined `{guild.name}`! Siri is now in `{str(len(self.guilds))}` guilds!")
        await log.senf(embed=embed)
        target = discord.utils.get(guild.channels, name="bot")
        target2 = discord.utils.get(guild.channels, name="bots")
        target3 = discord.utils.get(guild.channels, name="bot-commands")
        target4 = discord.utils.get(guild.channels, name="bot-spam")
        target5 = discord.utils.get(guild.channels, name="testing")
        target6 = discord.utils.get(guild.channels, name="testing-1")
        target7 = discord.utils.get(guild.channels, name="general")
        target8 = discord.utils.get(guild.channels, name="shitposts")
        target9 = discord.utils.get(self.get_all_members(), id=guild.owner.id)
        embed = discord.Embed(colour=0x0000ff, title="👋 Hello!", description="Hello! I am DiscordSiri.\n\n> **For help, do** `siri help`\n> **For support, do** `siri ticket <message>`\n> **Want even more support? Join my guild:** https://discord.gg/2RSErBu\n> **To chat with me, ping me!**\n> **To create a profile and start earning §, do** `siri bank create`\n\n> **Other prefixes:** `hey siri`  `siri,`")
        embed.set_image(url="https://image.ibb.co/mJY82z/siribanner.png")
        embed.set_footer(text="self created by lukee#0420", icon_url=self.user.avatar_url)
        try:
            await target.send(embed=embed)
        except:
            try:
                await target2.send(embed=embed)
            except:
                try:
                    await target3.send(embed=embed)
                except:
                    try:
                        await target4.send(embed=embed)
                    except:
                        try:
                            await target5.send(embed=embed)
                        except:
                            try:
                                await target6.send(embed=embed)
                            except:
                                try:
                                    await target7.send(embed=embed)
                                except:
                                    try:
                                        await target8.send(embed=embed)
                                    except:
                                        await target9.send(embed=embed)

    async def on_guild_remove(self, guild):
        log = self.get_channel(478821892309123091)
        embed = discord.Embed(description=f":thumbsdown: **Aw!** Siri has been kicked from `{guild.name}`.. Siri is now in `{str(len(self.guilds))}` guilds.")
        await log.send(embed=embed)

    @commands.command(hidden=True, aliases=['changelog'])
    async def cl(self, ctx, option, link, *, message):
        a = random.randint(1, 9)
        b = random.randint(1, 9)
        c = random.randint(1, 9)
        letters = ['a', 'A', 'b', 'B', 'C', 'd', 'n', 'x', 'Y', 'y', 's', 'S', 'i', 'k', 'K', 'g', 'G', 'm', 'c']
        letters2 = ['q', 'Q', 'p', 'P', 'o', 'v', 'V', 'z', 'e', 'E', 'I', 'L', 't', 'T', 'r', 'R', 'j', 'J', 'O']
        randc = f'{a}{rnd(letters)}{b}{rnd(letters2)}{c}'
        if ctx.message.author.id =='396153668820402197':
            c = self.get_channel('478833607126024192')
            if option == 'other' or option == 'o':
                #try:
                embed = discord.Embed(colour=0xe0e0e0, title=f"Changelog Update ID. {randc}", description=f"```diff\n* {message}```")
                embed.set_image(url=link)
                #except:
                    #embed = discord.Embed(colour=0xe0e0e0, title=f"Changelog Update ID. {randc}", description=f"```diff\n* {message}```")
                await c.send( embed=embed)
                await ctx.send(":ok_hand: Done.")
            elif option == 'add' or option == 'a':
                #try:
                embed = discord.Embed(colour=0xe0e0e0, title=f"Changelog Update ID. {randc}", description=f"```diff\n+ {message}```")
                embed.set_image(url=link)
                #except:
                    #embed = discord.Embed(colour=0xe0e0e0, title=f"Changelog Update ID. {randc}", description=f"```diff\n+ {message}```")
                await c.send( embed=embed)
                await ctx.send(":ok_hand: Done.")
            elif option == 'remove' or option == 'r':
                #try:
                embed = discord.Embed(colour=0xe0e0e0, title=f"Changelog Update ID. {randc}", description=f"```diff\n- {message}```")
                embed.set_image(url=link)
                #except:
                    #embed = discord.Embed(colour=0xe0e0e0, title=f"Changelog Update ID. {randc}", description=f"```diff\n- {message}```")
                await c.send( embed=embed)
                await ctx.send(":ok_hand: Done.")
            else:
                await ctx.send("That isn't an option.")
        else:
            trl = discord.Embed(title=("<:WrongMark:473277055107334144> You are not authorised to use this command!") , colour=0xff775b)
            trl.set_footer(text="Sorry about that.")
            await ctx.send(embed=trl)

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
        subprocess.call([sys.executable, r"siri.py"])
            
            
    @commands.command(hidden=True)
    @commands.is_owner()
    async def pull(self, ctx):
        shell = await run_cmd('git pull Siri --no-commit --no-edit --ff-only master')
        await run_cmd('git fetch --all')
        embed = discord.Embed(colour=0x0000ff, description=f"```css\n{shell}```")
        embed.set_author(name="Pulled from git..", icon_url="https://avatars0.githubusercontent.com/u/9919?s=280&v=4")
        msg = await ctx.send(embed=embed)

    @commands.command(hidden=True)
    @commands.is_owner()
    async def shell(self, ctx, *, code):
        embed = discord.Embed(colour=0x000fff, description=f"```css\nConnecting to shell..```")
        embed.set_author(name="Please Wait.", icon_url=self.user.avatar_url)
        msg = await ctx.send(embed=embed)
        shell = await run_cmd(code)
        embed = discord.Embed(colour=0x000fff, description=f"```css\n{shell}```")
        embed.set_author(name="Shell", icon_url=self.user.avatar_url)
        await self.delete_message(msg)
        await ctx.send( embed=embed)


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
        if isinstance(error, commands.NotOwner):
            trl = discord.Embed(title=("<:WrongMark:473277055107334144> You are not authorised to use this command!") , colour=0xff775b)
            trl.set_footer(text="Sorry About That.")
            await ctx.send(embed=trl)
        elif isinstance(error, commands.BadArgument):
            await ctx.send(error)
        else:
            await ctx.send(error)

    async def on_message(self, message):
        if message.author.bot: return
        await self.process_commands(message)

    def run(self):
        super().run(config.token, reconnect=True)
