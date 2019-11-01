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

#extensions = ['cogs.utility', 'cogs.help', 'cogs.economy', 'cogs.dev', 'cogs.music']

def prefix(bot, message):
    """Siri's prefix list"""
    return commands(*config.prefixes)(bot, message)

#class Siri(commands.AutoShardedBot):
    #def __init__(self):
        #super().__init__(command_prefix=config.prefixes)
        #self.remove_command("help")
        #bot = Siri
        
bot = commands.Bot(command_prefix=config.prefixes)
        
    #async def on_message_edit(self, before, after):
        #if not self.is_ready() or after.author.bot:
            #return

        #await self.process_commands(after)

async def run_cmd(cmd: str) -> str:
     process =\
     await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
     results = await process.communicate()
     return "".join(x.decode("utf-8") for x in results)

async def status_task():
    users = len(set(bot.get_all_members()))
    sayings = [f'{users} users smile', f'{str(len(bot.guilds))} guilds', 'What can I help you with?']
    while True:
        await bot.change_presence(status=discord.Status.online, activity=discord.Activity(name=f'{rnd(sayings)} | siri help', type=discord.ActivityType.watching))
        await asyncio.sleep(30)

@bot.event
async def on_ready():
    log = bot.get_channel(493330793599598592)
    print(f'\n ____  _      _ \n'\
                '/ ___|(_)_ __(_)\n'\
                '\___ \| |  __| |\n'\
                ' ___) | | |  | |\n'\
                '|____/|_|_|  |_|')
    print(f'Discord Version {discord.__version__}\n------')
    print(f'[UPDATE] Logged in as: {bot.user.name} ({str(bot.user.id)})')
    print(f"[AWAITING] Run 'siri load all'")
    bot.loop.create_task(status_task())
    embed = discord.Embed(title='⚡ **Siri** is connected!', description=f"**Guilds**.. `{str(len(bot.guilds))}`")
    try:
        await log.send(embed=embed)
    except:
        print('\n\nfailed to send message to 478821892309123091 (#logs)')

@bot.event
async def on_guild_join(guild):
    log = bot.get_channel(493330793599598592)
    server = guild
    embed = discord.Embed(colour=0x62f442, description=f"Siri has joined `{guild.name}`! Siri is now in `{str(len(bot.guilds))}` guilds!")
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
    embed = discord.Embed(colour=0x0000ff, title="👋 Hello!", description="Hello! I am DiscordSiri.\n\n**For help, do** `siri help`\n**For support, do** `siri ticket <message>`\n**Want even more support? Join my guild:** https://discord.gg/VuvB4gt\n**To chat with me, ping me!**\n**To create a profile and start earning §, do** `siri bank create`")
    embed.set_image(url="https://image.ibb.co/mJY82z/siribanner.png")
    embed.set_footer(text="Siri created by lukee#0420 - Thank you for adding me!", icon_url=bot.user.avatar_url)
    for x in targets:
        try:
            await x.send(embed=embed)
        except:
            continue
        break

@bot.event
async def on_guild_remove(guild):
    log = bot.get_channel(493330793599598592)
    embed = discord.Embed(colour=0xf44141, description=f"Siri has been kicked from `{guild.name}`.. Siri is now in `{str(len(bot.guilds))}` guilds.")
    embed.set_footer(text=f'ID: {guild.id}', icon_url=guild.icon_url_as(format='png'))
    await log.send(embed=embed)

@bot.event
async def on_message(message):
    if message.author.bot: 
        return
    else:
        await bot.process_commands(message)
        
        
if __name__ == '__main__':
    bot.load_extension("cogs.bot")
    
        
bot.run(config.token, bot=True, reconnect=True)
    #def run(self):
        #super().run(config.token, reconnect=True)
        
        
