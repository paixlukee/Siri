import discord
from discord.ext import commands
from random import choice as rnd
import time
from discord.ext.commands import errors, converter
import config
from pymongo import MongoClient
import pymongo

client = MongoClient(config.mongo_client)
db = client['siri']

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.colours = [0x37749c, 0xd84eaf, 0x45b4de, 0x42f4c5, 0xffb5f3, 0x42eef4, 0xe751ff, 0x51ffad]
        self.utility = ["article", "avatar", "chatbot", "colour", "define","discordstatus", "hastebin","IMDb","langdetect", "map", "news","shorten", "search","serverinfo", "userinfo","strawpoll", "timer","translate", "weather", "wikipedia"]
        self.botc = ["ticket", "stats", "support", "ping"]
        self.economy = ["balance", "bank create", "birthday", "buy","daily","description", "eat", "flip","give", "level","lvlmsgs","leaderboard", "profile","setcolour", "shop", "slots"]
        self.music = ["play", "queue", "np", "shuffle", "repeat","stop", "volume", "pause", "resume", "leave", "msearch", "remove"]
        self.news = db.utility.find_one({"utility": "help"})
        
    @commands.command(aliases=['cmds', 'Help'])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def help(self, ctx, cmd:str=None):
        if not cmd:
            embed = discord.Embed(colour=rnd(self.colours), title="What can I help you with?", description="For help with a command, do `siri help command`.")
            embed.add_field(name="Bot", value=" | ".join(self.botc))
            embed.add_field(name="Utility", value=" | ".join(self.utility))
            embed.add_field(name="Economy", value=" | ".join(self.economy))
            embed.add_field(name="Music", value=" | ".join(self.music))
            embed.set_footer(text="Help Menu", icon_url="https://cdn.discordapp.com/icons/493325581606453248/5b26d49a78c617fbba0e9cf17c5d8ff0.png?size=1024")
            embed.set_image(url="http://media.idownloadblog.com/wp-content/uploads/2016/06/iOS-10-Siri-waveform-image-001.png")
            await ctx.send(embed=embed)
        else:
            if cmd.lower() == 'command':
                await ctx.send("<:redtick:492800273211850767> There is no command named \"command\". Replace \"command\" with one of the commands listed in the help menu.")
            else:
                _cmd = self.bot.get_command(cmd)
                if not _cmd:
                    await ctx.send(f"<:redtick:492800273211850767> No command called \"{cmd}\" found.")
                else:
                    _help = "> <".join(_cmd.clean_params)
                    desc = _cmd.help
                    if _cmd.clean_params:
                        params = f"<{_help}>"
                    else:
                        params = _help
                    embed2 = discord.Embed(description=f"**Command:** `{cmd}`\n\n```siri {_cmd} {params}\n\n{desc}```", colour=rnd(self.colours))
                    embed2.set_footer(text="Help Menu", icon_url="https://cdn.discordapp.com/icons/493325581606453248/5b26d49a78c617fbba0e9cf17c5d8ff0.png?size=1024")
                    await ctx.send(embed=embed2)            
                

    @commands.command()
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def oldhelp(self, ctx, l:str = None, cmd:str = None):
        """This Command."""
        if ctx.message.author.bot: return
        elif not l:
            embed = discord.Embed(colour=rnd(self.colours), description="**What can I help you with?**\n\n**For help with a category**.. `siri help category help`\n**For help with a command**.. `siri help command help`")
            embed.add_field(name="Current Categories..", value="`utility`  `bot`  `economy`  `music`")
            if not self.news['news'].lower() == 'none':
                embed.add_field(name="News..", value=f"```{self.news['news']}```")
            #embed.set_footer(text="Siri | NOT affiliated with Apple", icon_url="https://vignette.wikia.nocookie.net/logopedia/images/d/d0/Siri.png/revision/latest?cb=20170730135120")
            embed.set_image(url="http://media.idownloadblog.com/wp-content/uploads/2016/06/iOS-10-Siri-waveform-image-001.png")
            await ctx.send(embed=embed)

        elif cmd and not l:
            await ctx.send("<:redtick:492800273211850767> **Incorrect usage:** `siri help command <name>` or `siri help category <name>`")

        elif l == "Command" or l == "command" or l == "cmd":
            if not cmd:
                await ctx.send("<:redtick:492800273211850767> **Incorrect usage:** `siri help command <name>` or `siri help category <name>`")
            else:
                try:
                    _cmd = self.bot.get_command(cmd)
                    _help = "> <".join(_cmd.clean_params)
                    help = _help
                    h1 = _cmd.help
                    h2 = h1.replace("<>", "")
                    if _cmd.help is None:
                        embed2 = discord.Embed(description=f"**Command:** `{cmd}`\n\n```siri {_cmd} <{help}>\n\nNo Description yet.```")
                        embed2.set_author(name="Siri", icon_url="https://vignette.wikia.nocookie.net/logopedia/images/d/d0/Siri.png/revision/latest?cb=20170730135120")
                        if cmd.name.lower() == 'help':
                            embed2.set_footer(text="This is just a test command. Now try other commands that are listed in the help menu!")
                        await ctx.send(embed=embed2)
                    else:
                        embed2 = discord.Embed(description=f"**Command:** `{cmd}`\n\n```siri {_cmd} <{help}>\n\n{h2}```")
                        embed2.set_author(name="Siri", icon_url="https://vignette.wikia.nocookie.net/logopedia/images/d/d0/Siri.png/revision/latest?cb=20170730135120")
                        await ctx.send(embed=embed2)
                except:
                    await ctx.send(f"<:redtick:492800273211850767> No command called \"{cmd}\" found.")

        elif l == "Module" or l == "module" or l == "mdl" or l == 'c' or l == 'Category' or l == 'category':

            if cmd == "Utility" or cmd == "utility":
                modules = self.utility
                name = "Utility"
                d = "Utility Commands"
            elif cmd == "Help" or cmd == "help":
                modules = ["`help`"]
                name = "Help"
                d = "Help Menu"
            elif cmd == "Bot" or cmd == "bot":
                modules = self.botc
                name = "Bot"
                d = "Bot info/stats"
            elif cmd == "Economy" or cmd == "economy":
                modules = self.economy
                name = "Economy"
                d = "Economy Commands"
            elif cmd == "Music" or cmd == "music":
                modules = self.music
                name = "Music"
                d = "Music Commands"
            else:
                return await ctx.send(f"<:redtick:492800273211850767> No category named \"{cmd}\" found.")

            try:
                md = " ".join(modules)
                embed3 = discord.Embed(description=f"**Category:** `{name}`\n**Description:** `{d}`\n**Commands:** {md}")
                embed3.set_author(name="Siri", icon_url="https://vignette.wikia.nocookie.net/logopedia/images/d/d0/Siri.png/revision/latest?cb=20170730135120")
                if str(name).lower() == 'help':
                            embed3.set_footer(text="This is just a test command. Now try other categories that are listed in the help menu!")
                await ctx.send(embed=embed3)
            except:
                pass
        else:
            await ctx.send("<:redtick:492800273211850767> That's not an option! Options: `category`, `command`")

def setup(bot):
    bot.add_cog(Help(bot))
