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


###
###
extension = ['cogs.utility', 'cogs.help', 'cogs.music', 'cogs.economy']

prefixes = ['hey siri ', 'siri ', 'Siri ', 'Hey Siri ', 'siri, '] 

bot = commands.Bot(command_prefix=prefixes)

bot.remove_command("help")

@bot.event
async def status_task():
    users = len(set(bot.get_all_members()))
    sayings = [f'{users} users smile', f'{str(len(bot.servers))} servers', 'What can I help you with?']
    while True:
        await bot.change_presence(game=discord.Game(name=f'{rnd(sayings)} | siri help', type=3))
        await asyncio.sleep(30)

@bot.event
async def on_ready():
    log = bot.get_channel("478821892309123091")
    print('\n\n------')
    print('Logged in as:\n')
    print(bot.user.name)
    print(bot.user.id)
    print('------\n\n')
    bot.loop.create_task(status_task())
    embed = discord.Embed(title='⚡ **Siri** is connected!', description=f"**Servers**.. `{str(len(bot.servers))}`")
    await bot.send_message(log, embed=embed)
    bot.loop.create_task(status_task())

@bot.event ###
async def on_server_join(server):
    log = bot.get_channel("478821892309123091")
    embed = discord.Embed(description=f":tada: **Yay!** Siri has joined `{server.name}`! Siri is now in `{str(len(bot.servers))}` servers!")
    await bot.send_message(log, embed=embed)
    #server shit
    target = discord.utils.get(server.channels, name="bot")
    target2 = discord.utils.get(server.channels, name="bots")
    target3 = discord.utils.get(server.channels, name="bot-commands")
    target4 = discord.utils.get(server.channels, name="bot-spam")
    target5 = discord.utils.get(server.channels, name="testing")
    target6 = discord.utils.get(server.channels, name="testing-1")
    target7 = discord.utils.get(server.channels, name="general")
    target8 = discord.utils.get(server.channels, name="shitposts")
    target9 = discord.utils.get(bot.get_all_members(), id=server.owner.id)
    embed = discord.Embed(colour=0x0000ff, title="👋 Hello!", description="Hello! I am DiscordSiri.\n\n> **For help, do** `siri help`\n> **For support, do** `siri ticket <message>`\n> **Want even more support? Join my server:** https://discord.gg/2RSErBu\n> **To chat with me, ping me!**\n> **To create a profile and start earning §, do** `siri bank create`\n\n> **Other prefixes:** `hey siri`  `siri,`")
    embed.set_image(url="https://image.ibb.co/mJY82z/siribanner.png")
    embed.set_footer(text="Bot created by lukee#0420", icon_url=bot.user.avatar_url)
    try:
        await bot.send_message(target, embed=embed)
    except:
        try:
            await bot.send_message(target2, embed=embed)
        except:
            try:
                await bot.send_message(target3, embed=embed)
            except:
                try:
                    await bot.send_message(target4, embed=embed)
                except:
                    try:
                        await bot.send_message(target5, embed=embed)
                    except:
                        try:
                            await bot.send_message(target6, embed=embed)
                        except:
                            try:
                                await bot.send_message(target7, embed=embed)
                            except:
                                try:
                                    await bot.send_message(target8, embed=embed)
                                except:
                                    await bot.send_message(target9, embed=embed)

        


@bot.event ###
async def on_server_remove(server):
    log = bot.get_channel("478821892309123091")
    embed = discord.Embed(description=f":thumbsdown: **Aw!** Siri has been kicked from `{server.name}`.. Siri is now in `{str(len(bot.servers))}` servers.")
    await bot.send_message(log, embed=embed)

#bot.remove_command('help')

@bot.command(pass_context=True, hidden=True, aliases=['changelog'])
async def cl(ctx, option, link, *, message):
    a = random.randint(1, 9)
    b = random.randint(1, 9)
    c = random.randint(1, 9)
    letters = ['a', 'A', 'b', 'B', 'C', 'd', 'n', 'x', 'Y', 'y', 's', 'S', 'i', 'k', 'K', 'g', 'G', 'm', 'c']
    letters2 = ['q', 'Q', 'p', 'P', 'o', 'v', 'V', 'z', 'e', 'E', 'I', 'L', 't', 'T', 'r', 'R', 'j', 'J', 'O']
    randc = f'{a}{rnd(letters)}{b}{rnd(letters2)}{c}'
    if ctx.message.author.id =='396153668820402197':
        c = bot.get_channel('478833607126024192')
        if option == 'other' or option == 'o':
            #try:
            embed = discord.Embed(colour=0xe0e0e0, title=f"Changelog Update ID. {randc}", description=f"```diff\n* {message}```")
            embed.set_image(url=link)
            #except:
                #embed = discord.Embed(colour=0xe0e0e0, title=f"Changelog Update ID. {randc}", description=f"```diff\n* {message}```")
            await bot.send_message(c, embed=embed)
            await bot.say(":ok_hand: Done.")
        elif option == 'add' or option == 'a':
            #try:
            embed = discord.Embed(colour=0xe0e0e0, title=f"Changelog Update ID. {randc}", description=f"```diff\n+ {message}```")
            embed.set_image(url=link)
            #except:
                #embed = discord.Embed(colour=0xe0e0e0, title=f"Changelog Update ID. {randc}", description=f"```diff\n+ {message}```")
            await bot.send_message(c, embed=embed)
            await bot.say(":ok_hand: Done.")
        elif option == 'remove' or option == 'r':
            #try:
            embed = discord.Embed(colour=0xe0e0e0, title=f"Changelog Update ID. {randc}", description=f"```diff\n- {message}```")
            embed.set_image(url=link)
            #except:
                #embed = discord.Embed(colour=0xe0e0e0, title=f"Changelog Update ID. {randc}", description=f"```diff\n- {message}```")
            await bot.send_message(c, embed=embed)
            await bot.say(":ok_hand: Done.")
        else:
            await bot.say("That isn't an option.")
    else:
        trl = discord.Embed(title=("<:WrongMark:473277055107334144> You are not authorised to use this command!") , colour=0xff775b)
        trl.set_footer(text="Sorry about that.")
        await bot.say(embed=trl)

@bot.command(pass_context=True, hidden=True)
async def shutdown(ctx):
    if ctx.message.author.id =='396153668820402197':
        await bot.say("Goodbye. Nice talking to you.")
        await bot.logout()
    else:
        trl = discord.Embed(title=("<:WrongMark:473277055107334144> You are not authorised to use this command!") , colour=0xff775b)
        trl.set_footer(text="Sorry about that.")
        await bot.say(embed=trl)

@bot.command(pass_context=True, hidden=True)
async def restart(ctx):
    if ctx.message.author.id =='396153668820402197':
        await bot.say("I'll see you in a bit!")
        await bot.logout()
        subprocess.call([sys.executable, r"siri.py"])
    else:
        trl = discord.Embed(title=("<:WrongMark:473277055107334144> You are not authorised to use this command!") , colour=0xff775b)
        trl.set_footer(text="Sorry about that.")
        await bot.say(embed=trl)
        
        
@bot.command(pass_context=True, hidden=True)
async def pull(ctx):
    if ctx.message.author.id =='396153668820402197':
        shell = await run_cmd('git pull Siri --no-commit --no-edit --ff-only master')
        await run_cmd('git fetch --all')
        embed = discord.Embed(colour=0x0000ff, description=f"```{shell}```")
        embed.set_author(name="Pulled from git..", icon_url="https://avatars0.githubusercontent.com/u/9919?s=280&v=4")
        msg = await bot.say(embed=embed)
    else:
        trl = discord.Embed(title=("<:WrongMark:473277055107334144> You are not authorised to use this command!") , colour=0xff775b)
        trl.set_footer(text="Sorry about that.")
        await bot.say(embed=trl)

@bot.command(pass_context=True, hidden=True)
async def shell(ctx, *, code):
    if ctx.message.author.id =='396153668820402197':
        embed = discord.Embed(colour=0x000fff, description=f"```Connecting to shell..```")
        embed.set_author(name="Please Wait.", icon_url=bot.user.avatar_url)
        msg = await bot.say(embed=embed)
        shell = await run_cmd(code)
        embed = discord.Embed(colour=0x000fff, description=f"```{shell}```")
        embed.set_author(name="Shell", icon_url=bot.user.avatar_url)
        await bot.delete_message(msg)
        await bot.say( embed=embed)
    else:
        trl = discord.Embed(title=("<:WrongMark:473277055107334144> You are not authorised to use this command!") , colour=0xff775b)
        trl.set_footer(text="Sorry about that.")
        await bot.say(embed=trl)


@bot.command(pass_context=True)
async def ping(ctx):
    """Get Siri's Ping"""
    if ctx.message.author.bot: return
    else:
        t1 = time.perf_counter()
        await bot.send_typing(ctx.message.channel)
        t2 = time.perf_counter()
        ping_desc = ("Ping: `" + str(round((t2-t1)*1000)) + "ms`!")
        embed = discord.Embed(description=ping_desc)
        await bot.say(embed=embed)

@bot.command(pass_context=True, hidden=True)
async def load(ctx, extension):
    if ctx.message.author.id =='396153668820402197':
        try:
            bot.load_extension("cogs.{}".format(extension))
            embed = discord.Embed(title="<:CheckMark:473276943341453312> Cog loaded:", color=0x5bff69, description="**Cog:** `cogs\{}.py`".format(extension))
            await bot.say(embed=embed)
            print('\n\nCOG LOAD\n--[Cog loaded, {}.py]--\n\n'.format(extension))
        except Exception as error:
            print('\n\nEXTEN./COG ERROR: {} was not loaded due to an error: \n-- [{}] --\n\n'.format(extension, error))
            embed = discord.Embed(title="<:WrongMark:473277055107334144> Error loading cog:", color=0xff775b, description="**Cog:** `cogs\{}.py`\n**Errors:**\n```{}```".format(extension, error))
            await bot.say(embed=embed)
    else:
        trl = discord.Embed(title=("<:WrongMark:473277055107334144> You are not authorised to use this command!") , colour=0xff775b)
        trl.set_footer(text="Sorry about that.")
        await bot.say(embed=trl)

@bot.command(pass_context=True, aliases=['un'], hidden=True)
async def unload(ctx, extension):
    if ctx.message.author.id =='396153668820402197':
        bot.unload_extension("cogs.{}".format(extension))
        embed = discord.Embed(title="<:CheckMark:473276943341453312> Cog unloaded:", color=0x5bff69, description="**Cog:** `cogs\{}.py`".format(extension))
        await bot.say(embed=embed)
    else:
        trl = discord.Embed(title=("<:WrongMark:473277055107334144> You are not authorised to use this command!") , colour=0xff775b)
        trl.set_footer(text="Sorry About That.")
        await bot.say(embed=trl)

@bot.command(pass_context=True, aliases=['re'], hidden=True)
async def reload(ctx, extension):
    if ctx.message.author.id =='396153668820402197':
        try:
            bot.unload_extension("cogs.{}".format(extension))
            bot.load_extension("cogs.{}".format(extension))
            embed = discord.Embed(title="<:CheckMark:473276943341453312> Cog reloaded:", color=0x5bff69, description="**Cog:** `cogs\{}.py`".format(extension))
            await bot.say(embed=embed)
            print('\n\nCOG RELOAD\n--[Cog reloaded, {}.py]--\n\n'.format(extension))
        except Exception as error:
            print('\n\nEXTEN./COG ERROR: {} was not reloaded due to an error: \n-- [{}] --\n\n'.format(extension, error))
            embed = discord.Embed(title="<:WrongMark:473277055107334144> Error reloading cog:", color=0xff775b, description="**Cog:** `cogs\{}.py`\n**Errors:**\n```{}```".format(extension, error))
            await bot.say(embed=embed)
    else:
        trl = discord.Embed(title=("<:WrongMark:473277055107334144> You are not authorised to use this command!") , colour=0xff775b)
        trl.set_footer(text="Sorry about that.")
        await bot.say(embed=trl)

if __name__ == '__main__':
    for extension in extension:
        try:
            bot.load_extension(extension)
        except Exception as error:
            print('\n\nEXTEN./COG ERROR: {} was not loaded due to an error: \n-- [{}] --\n\n'.format(extension, error))

bot.run(token_here)
