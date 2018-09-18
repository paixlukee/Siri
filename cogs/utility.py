import discord
from discord.ext import commands

from datetime import datetime
import requests

import time
from random import choice, randint
import random
from discord.ext.commands import errors, converter
from random import choice as rnd

import re

import aiohttp
import asyncio
import json
from .utils import checks


class Colour:
    def __init__(self, _hex):
        self._hex = _hex

    @property
    def hex(self):
        if '#' in self_hex:
            self._hex = self_hex.replace('#', '', 1)
        match = re.match(r'[.]{8}')
        return match
    


class Utility:
    def __init__(self, bot):
        self.bot = bot


    async def add_money(self, user=None, count=None):
        with open('assets\\economy.json', 'r') as f:
                users = json.load(f)
                users[user]['money'] += count
        with open('assets\\economy.json', 'w') as f:
                 json.dump(users, f)

    async def take_money(self, user=None, count=None):
        with open('assets\\economy.json', 'r') as f:
                users = json.load(f)
                users[user]['money'] -= count
        with open('assets\\economy.json', 'w') as f:
                 json.dump(users, f)

    async def on_message(self, message):
        if message.content.startswith('<@481337766379126784> '):
            fmsg = message.content
            msg = fmsg.replace("<@481337766379126784> ", "")
            r = requests.post("https://api.dialogflow.com/v1/query?v=20150910",
                    data = json.dumps({
                            "contexts": [
                            "shop"
                            ],
                            "lang": "en",
                            "query": msg,
                            "sessionId": "12345",
                            "timezone": "America/New_York"
                          }),
                    headers={
                        "Content-type": "application/json"
                        ,"Authorization" : "Bearer 1663b12fcc24462e9711d9801be96485"
                    })

            resp = r.json()
            response = resp['result']['fulfillment']['messages'][0]['speech']
            await message.channel.send(f"**{message.author.name}**, {response}")


    @commands.command(name='wikipedia', aliases=['wiki', 'w'])
    async def _wikipedia(self, ctx, *, q: str = None):
        """Search Information on Wikipedia"""
        if not ctx.channel.is_nsfw():
            return await ctx.send('You can use this in only nsfw channels.')
        try:
            await self.add_money(user=ctx.message.author.id, count=1)
        except:
            pass 

        embed = discord.Embed(description="<a:loading:473279565670907914> Searching..")
        msg = await ctx.send(embed=embed)

        try:
            async with aiohttp.ClientSession(headers={'Accept': 'application/json'}) as session:
                    async with session.get(f'https://en.wikipedia.org/w/api.php?action=query&titles={q}&prop=pageimages&format=json&pithumbsize=400') as get:
                        resp = await get.json()
                        for page in resp['query']['pages']:
                            img = resp['query']['pages'][page]['thumbnail']['source']
        except:
            pass

        query = q
        url = 'https://en.wikipedia.org/w/api.php?'
        payload = {}
        payload['action'] = 'query'
        payload['format'] = 'json'
        payload['prop'] = 'extracts'
        payload['titles'] = ''.join(query).replace(' ', '+')
        payload['exsentences'] = '5'
        payload['redirects'] = '1'
        payload['explaintext'] = '1'
        conn = aiohttp.TCPConnector(verify_ssl=False)
        session = aiohttp.ClientSession(connector=conn)
        async with session.get(url, params=payload, headers={'user-agent': 'Siri v2'}) as r:
            result = await r.json()
        session.close()
        if '-1' not in result['query']['pages']:
            for page in result['query']['pages']:
                title = result['query']['pages'][page]['title']
                desc = result['query']['pages'][page]['extract'].replace('\n', '\n\n')
                l = 'https://en.wikipedia.org/wiki/{}'.format(title.replace(' ', '_'))
            if len(desc) > 50:
                embed = discord.Embed(title=title, description=u'\u2063\n{}[...]({})\n\u2063'.format(desc[:-30], l), url=l)
            else:
                embed = discord.Embed(title=title, description=u'\u2063\n{}\n\u2063'.format(desc, l), url=l)
            embed.set_footer(text='Siri Knowledge', icon_url='https://vignette.wikia.nocookie.net/logopedia/images/d/d0/Siri.png/revision/latest?cb=20170730135120')
            try:    
                embed.set_thumbnail(url=img)
            except:
                pass
            await msg.delete()
            await ctx.send(embed=embed)
        else:
            await msg.delete()
            await ctx.send("<:WrongMark:473277055107334144> I could not find anything with that query..")

    @commands.command(aliases=['info', 'botinfo', 'status'])
    async def stats(self, ctx):
        """- Information about myself."""
        try:
            await self.add_money(user=ctx.message.author.id, count=1)
        except:
            pass
        
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://discordbots.org/api/bots/481337766379126784") as r:
                r = await r.json()
        users = len(set(self.bot.get_all_members()))
        channels = []
        for guild in self.bot.guilds:
            for channel in guild.channels:
                channels.append(channel)
        channels = len(channels)
        emojis = len(self.bot.emojis)
        commands = len(self.bot.all_commands)

        author = ctx.message.author

        #RAM = self.process.memory_full_info().rss  /  1024 ** 2

        stat = discord.Embed(color=0x36393E, description=f"**Siri. by lukee#0420**\n\n\n" \
        f"> **Python**... `3.6`\n>" \
        f"> **Ubuntu**... `18.04`\n>" \
        f"> **RAM Usage**... `??MB`\n\n")
        f"I am in **{str(len(self.bot.guilds))} servers**!\n"\
        f"I can see **{channels} channels**!\n"\
        f"I am with **{users} users**!\n"\
        f"I can use **{emojis} emojis**!\n"\
        f'I have **{commands} commands**!\n'\
        f"I have **{r['points']} DBL votes**!\n\n\n"\
        f"[DBL](https://discordbots.org/bot/481337766379126784) |"\
        f" [Vote](https://discordbots.org/bot/481337766379126784/vote) |"\
        f" [Invite](https://discordapp.com/api/oauth2/authorize?client_id=481337766379126784&scope=bot&permissions=0)"

        await ctx.send(embed=stat)
        

    @commands.command()
    @commands.cooldown(1, 900, commands.BucketType.user)
    async def ticket(self, ctx, *, message):
        """- Send a ticket to my Creator."""
        a = random.randint(1, 9)
        b = random.randint(1, 9)
        c = random.randint(1, 9)
        d = random.randint(1, 9)
        letters = ['a', 'A', 'b', 'B', 'C', 'd', 'n', 'x', 'Y', 'y', 's', 'S', 'i', 'k', 'K', 'g', 'G', 'm', 'c']
        letters2 = ['q', 'Q', 'p', 'P', 'o', 'v', 'V', 'z', 'e', 'E', 'I', 'L', 't', 'T', 'r', 'R', 'j', 'J', 'O']
        random_c = f'{a}{rnd(letters)}{b}{rnd(letters2)}{c}'
        try:
            await self.add_money(user=ctx.message.author.id, count=1)
        except:
            pass
        if ctx.message.author.bot: return
        else:

            author = ctx.message.author
            guild = ctx.message.guild

            channel = self.bot.get_channel(481352533676392469)

            stat = discord.Embed(color = discord.Color(0xcd87ff))
            stat.set_author(name=guild, icon_url=guild.icon_url)
            stat.set_footer(text="Ticket ID: {}".format(random_c))

            stat.add_field(name="User", value=author, inline=False)
            stat.add_field(name="User ID", value=author.id, inline=False)
            stat.add_field(name="Guild ID", value=guild.id, inline=False)
            stat.timestamp = ctx.message.created_at
            stat.add_field(name="Message", value=message, inline=False)

            embed = discord.Embed(
                title="<:CheckMark:473276943341453312> **Ticket Sent!**",
                description="Please wait until you get a DM from a staff member." \
                            "Please do not overuse this command, or you will be blocked from using it."\
                            "\n\n"\
                            "(Cooldown is `15` minutes!)")
            embed.set_footer(text=f"KEEP THIS TICKET ID: {random_c}")
            await ctx.send(embed=embed)
            await channel.send(embed=stat)
            print("\n\n\n----\n\n\"{}\" has sent a ticket:\n\n".format(author))
            print(message)
            print("\n----\n\n\n")

    @commands.command(aliases=['chat', 'cb'])
    async def chatbot(self, ctx, *, message):
        """Chat with me!"""
        try:
            await self.add_money(user=ctx.message.author.id, count=1)
        except:
            pass
        r = requests.post("https://api.dialogflow.com/v1/query?v=20150910",
        data = json.dumps({
                "contexts": [
                "shop"
                ],
                "lang": "en",
                "query": message,
                "sessionId": "12345",
                "timezone": "America/New_York"
              }),
        headers={
            "Content-type": "application/json"
            ,"Authorization" : "Bearer 1663b12fcc24462e9711d9801be96485"
        })

        #try:
            #await ctx.send(f"{ctx.message.author.mention}, {r['entities']['intent'][0]['value']}")
        #except:
        resp = r.json()
        response = resp['result']['fulfillment']['messages'][0]['speech']
        ra = requests.get("https://api.dialogflow.com/v1/contexts?v=20150910&sessionId=12345", headers={"Authorization" : "Bearer 1663b12fcc24462e9711d9801be96485"}).json()
        #await ctx.send(ra)
        await ctx.send(f"**{ctx.message.author.name}**, {response}")

    @commands.command(aliases=['lookup', 'websearch'])
    async def search(self, ctx, *, query = None):
        embed = discord.Embed(description="<a:loading:473279565670907914> Searching..")
        msg = await ctx.send(embed=embed)
        """Search The Web

        Advanced:

        Terms can be excluded through a leading minus:
        siri -alexa

        You can mix terms with..
        siri, alexa
        siri AND alexa

        Phrases can be surrounded by double-quotes:
        "siri"

        """
        try:
            await self.add_money(user=ctx.message.author.id, count=1)
        except:
            pass
        if query is None:
            await msg.delete()
            await ctx.send("`Incorrect Usage`\n```siri search <search-query>```")
        elif query == 'porn' or query == 'Porn' or query == 'orgy' or query == 'Orgy' or query == 'gay porn' or query == 'penis' or query == 'Penis' or query == 'gay' or query == 'Gay' or query == 'ass' or query == 'Ass' or query == 'tits' or query == 'Tits' or query == 'Boobs' or query == 'boobs' or query == 'Lesbian' or query == 'lesbian' or query == 'cock' or query == 'Cock' or query == 'hentai' or query == 'Hentai' or query == 'Sex' or query == 'sex':
            await msg.delete()
            await ctx.send("I couldn't find anything..")

        else:

            q = query.replace(" ", "%20")
            r = requests.get(f"https://contextualwebsearch-websearch-v1.p.mashape.com/api/Search/WebSearchAPI?q={q}&count=1&autocorrect=true",
            headers={
                    "X-Mashape-Key": "P0dWACT2bvmshnRsp9rKObno2hVZp1hLGCmjsnvBJ85tceAyv8",
                    "X-Mashape-Host": "contextualwebsearch-websearch-v1.p.mashape.com"
                    #"Accept": "application/json"
            }).json()
            try:
                re = r['value'][0]
                t = re['title']
                title = t.replace("<b>", "").replace("</b>", "")
                d = re['description']
                description = d.replace("<b>", "").replace("</b>", "")
                s = r['relatedSearch']
                es = ", ".join(s)
                search = es.replace("<b>", "").replace("</b>", "")
                embed = discord.Embed(colour=0x6d68ff, description=f"Top Result (**{r['totalCount']}**):\n\n**{title}**\n\n*{description}*\n\n{re['url']}\n\n**Related..**\n\n{search}")
                try:
                    embed.set_thumbnail(url=re['image']['url'])
                except:
                    pass
                #await ctx.send(f":ok_hand:\n{r}")#relatedSearch
                await ctx.send(embed=embed)
                await msg.delete()
            except:
                await msg.delete()
                await ctx.send(f"I couldn't find anything..")


    #RATELIMITS!!!!!!!!
    @commands.command(hidden=True)
    @checks.admin_or_permissions(manage_guild=True)
    async def uwu(self, ctx, c:int, *, message):
        for e in range(c):
            await ctx.send(message)

    @commands.command(aliases=['IMDb'])
    async def imdb(self, ctx, *, title= None):
        """Search a movie/series on IMDb"""
        try:
            await self.add_money(user=ctx.message.author.id, count=1)
        except:
            pass
        if title is None:
            await ctx.send("Please include the series/movie title!")
        else:
            try:
                mv = title.replace(" ", "+")
                r = requests.get(f"http://www.omdbapi.com/?t={mv}&apikey=e82f2fc2").json()
                try:
                    imdb_url = "https://www.imdb.com/title/" + r['imdbID']
                except:
                    imdb_url = "https://www.imdb.com/404"
                #actors = r[0]['actors']
                #tag = r[0]['genres']
                #link = f"http://" + r[0]['poster'] 
                #tags = " | ".join(tag)
                try:
                    if r['Metascore'] == 'N/A':
                        meta = "Not Rated"
                    else:
                        meta = r['Metascore'] + "/100"
                except:
                    meta = "Not Rated"

                try:
                    imd = r['imdbRating']
                except:
                    imd = "Not Rated"

                embed = discord.Embed(title=r['Title'], description=f"<:imdb:484905488547315730> **{imd}/10**\n<:meta:484905490170642442> **{meta}**\n\n{r['Plot']}", url=imdb_url)
                try:
                    embed.add_field(name="Release..", value=f"{r['Released']} ({r['Year']})")
                except:
                    pass
                try:
                    embed.add_field(name="Avg. Duration", value=r['Runtime'])
                except:
                    pass
                try:
                    embed.add_field(name="Starring..", value=r['Actors'])
                except:
                    pass
                try:
                    embed.add_field(name="Language(s)..", value=r['Language'])
                except:
                    pass
                try:
                    embed.add_field(name="Rated..", value=r['Rated'])
                except:
                    pass
                try:
                    embed.add_field(name="Seasons..", value=r['totalSeasons'])
                except:
                    pass
                try:
                    embed.set_thumbnail(url=r['Poster'])
                except:
                    pass
                try:
                    embed.set_footer(text=f"🏷️ {r['Genre']}")
                except:
                    pass
                await ctx.send(embed=embed)

            except Exception as e:
                await ctx.send(f"I couldn't find that movie or series..")

    @commands.command(aliases=['today'])
    async def news(self, ctx):#03d8e32c7dd349e3b9efe0338e08e890
        """Get a popular story from the News"""
        try:
            await self.add_money(user=ctx.message.author.id, count=1)
        except:
            pass
        try:
            r = requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey=03d8e32c7dd349e3b9efe0338e08e890").json()
        
            re = r['articles'][0]
            pa = re['publishedAt']
            publishedat = pa.replace("T", " ").replace("Z", " ").replace("-", "/").replace("{'", "").replace("'}", "")
            embed = discord.Embed(title=re['title'], description=re['description'], url=re['url'])
            embed.add_field(name="Published at..", value=publishedat[:-4]) # these brakcets annoyed me so I removed them
            embed.set_thumbnail(url=re['urlToImage'])
            embed.set_footer(text=f"© {re['source']['name']} & NewsAPI")

            await ctx.send(embed=embed, content=f":newspaper: | Here is a popular story from the **News**..")
        except:
            await ctx.send("There was an issue getting the news article.. Check back in a few hours.")

    @commands.command()
    async def article(self, ctx, *, query = None):#03d8e32c7dd349e3b9efe0338e08e890
        """Search for an article in the News"""
        try:
            await self.add_money(user=ctx.message.author.id, count=1)
        except:
            pass
        if query is None:
            await ctx.send("`Incorrect Usage`\n```siri article <search-query>```")
        else:

            try:
                q = query.replace(" ", "%20")
                r = requests.get(f"https://newsapi.org/v2/everything?q={q}&apiKey=03d8e32c7dd349e3b9efe0338e08e890").json()
                
                re = r['articles'][0]
                pa = re['publishedAt']
                publishedat = pa.replace("T", " ").replace("Z", " ").replace("-", "/").replace("{'", "").replace("'}", "")
                embed = discord.Embed(title=re['title'], description=re['description'], url=re['url'])
                embed.add_field(name="Published at..", value=publishedat[:-4]) # these brakcets annoyed me so I removed them
                embed.set_thumbnail(url=re['urlToImage'])
                embed.set_footer(text=f"© {re['source']['name']} & NewsAPI")

                await ctx.send(embed=embed, content=f":newspaper: | Here is what I found for **\"{query}\"** in the **News**..")
            except:
                await ctx.send("I couldn't find any article that matched your query..")

    @commands.command(aliases=['dict', 'dictionary'])
    async def define(self, ctx, *, word):#CRED: 6cd11931 #KEY: a6d815d3a40f53811de4aad036361e5a
        """Define a word"""
        await ctx.trigger_typing()
        try:
            await self.add_money(user=ctx.message.author.id, count=1)
        except:
            pass
        try:
            q = word.replace(" ", "%20")
            r = requests.get(f"https://od-api.oxforddictionaries.com:443/api/v1/entries/en/{q}",
                headers={
                    'app_id': '6cd11931', 
                    'app_key': 'a6d815d3a40f53811de4aad036361e5a'
                }).json()
            
            re = r['results'][0]['lexicalEntries'][0]['entries'][0]
            #publishedat = pa.replace("T", " ").replace("Z", " ").replace("-", "/").replace("{'", "").replace("'}", "")
            embed = discord.Embed(title=word, description=rnd(re['senses'][0]['definitions']), url=f"https://en.oxforddictionaries.com/definition/{q}")#, description=re['senses'][0]['definitions'], url=f"https://en.oxforddictionaries.com/definition/{q}")
            try:
                embed.add_field(name="Etymologies..", value=rnd(re['etymologies']))
            except:
                pass
            try:
                embed.add_field(name="Examples..", value=f"\n\"{re['senses'][0]['examples'][0]['text']}\"")
            except:
                pass
            embed.set_footer(text=f"© Oxford Dictionary")

            await ctx.send(embed=embed, content=f":books: | Here is the definition for **{word}**:")
        except Exception as e:
            await ctx.send("I couldn't find that word in the dictionary.")
            #await ctx.send(e)
            #await ctx.send(rnd(re['etymologies']))
            #await ctx.send(rnd(re['senses'][0]['definitions']))
            #await ctx.send(re['senses'][0]['examples'][0]['text'])

    async def post(self, content):
        async with aiohttp.ClientSession() as session:
            async with session.post("https://hastebin.com/documents",data=content.encode('utf-8')) as post:
                post = await post.json()
                return "https://hastebin.com/{}".format(post['key'])

    @commands.command()
    async def hastebin(self, ctx, *, message):
        """Send your text to a haste bin

        TIP: if your text is in a codeblock, it removes the three grave accents when adding to the hastebin"""
        async with ctx.typing():
            try:
                await self.add_money(user=ctx.message.author.id, count=1)
            except:
                pass
            try:
                url = await self.post(message)
            except aiohttp.ContentTypeError:
                return await ctx.send('There is something wrong with the api. Sorry.')
            embed = discord.Embed(
                colour=discord.Colour(0x00a6ff),
                description="I have successfully generated a custom hastebin link for you!")
            embed.set_thumbnail(url='https://pbs.twimg.com/profile_images/1664989409/twitter_400x400.png')
            embed.set_author(name="Success!",
                icon_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTVSMTdCINzzsBHiXSXQyq2QEcPRII27vkMdjpMLxBrpqDHIpXb")
            embed.add_field(name="Hastebin link", value=url)
            await ctx.send(embed=embed)
    

    @commands.command(aliases=['dstatus'])
    async def discordstatus(self, ctx):
        """Get Discord Status"""
        try:
            await self.add_money(user=ctx.message.author.id, count=1)
        except:
            pass
        embed = discord.Embed(description="<a:loading:473279565670907914> Fetching..")
        msg = await ctx.send(embed=embed)
        r = requests.get("https://srhpyqt94yxb.statuspage.io/api/v2/status.json").json()
        e = requests.get("https://srhpyqt94yxb.statuspage.io/api/v2/scheduled-maintenances/upcoming.json").json()
        s = requests.get("https://srhpyqt94yxb.statuspage.io/api/v2/summary.json").json()
        p = requests.get("https://srhpyqt94yxb.statuspage.io/api/v2/incidents/unresolved.json")

        indicators = r['status']['indicator']
        description = r['status']['description']


        if indicators == 'none':
            emoji = "<:online:468721284390453268>"
        elif indicators == 'minor':
            emoji = "<:idle:483080613687984131>"
        elif indicators == 'major':
            emoji = "<:idle:483080613687984131>"
        elif indicators == 'critical':
            emoji = "<:dnd:478843647282905088>"
        else:
            emoji = "**?**"

        try:
            sc = e['scheduled_maintenances'][0]
            inc = f"\n[{sc['name']}]({shortlink})\n*{sc['status']}*\n`{sc['scheduled_for']}`"
        except:
            maint = f"\n*No Scheduled Maintenance.*"

        try:
            ac = p['incidents'][0]
            inc = f"\n[{ac['name']}]({shortlink})\n**Impact:** {ac['impact']}\n*{ac['status']}*\n`{ac['created_at']}`"
        except:
            inc = f"\n*No Unresolved Incidents.*"

        indicator = s['components'][0]['status']


        if indicator == 'operational':
            emoji2 = "<:online:468721284390453268>"
            ind = "All Systems Operational"
        elif indicator == 'degraded_performance':
            emoji2 = "<:idle:483080613687984131>"
            ind = "Partial System Outage"
        elif indicator == 'partial_outage':
            emoji2 = "<:idle:483080613687984131>"
            ind = "Partial System Outage"
        elif indicator == 'major_outage':
            emoji2 = "<:dnd:478843647282905088>"
            ind = "Major Service Outage"
        else:
            emoji2 = "**?**"
            ind = "???"



        embed = discord.Embed(colour=0x8faaef, title="Discord Status", url="http://status.discordapp.com",
            description=
            f"{emoji} **Discord**\n"\
            f"*{description}*\n{emoji2} **API**\n "\
            f"*{ind}*\n\n**Next Maintenance:**{maint}\n\n"\
            f"**Unresolved Incidents:**{inc}")
        embed.set_thumbnail(
            url="https://yt3.ggpht.com/a-/ACSszfHkcq8jw1JefOzyp7pui7vBjA66h5cFwbtC-g=s900-mo-c-c0xffffffff-rj-k-no")
        await msg.edit(embed=embed)

    @commands.command(aliases=['poll'])
    async def strawpoll(self, ctx, *, question, options= None):
        """Creates a strawpoll. Separate with ', '"""
        try:
            await self.add_money(user=ctx.message.author.id, count=1)
        except:
            pass
        async with ctx.typing():
            options_list = question.split(', ')
            title = options_list[0]
            options_list.remove(title)
            if len(options_list) < 2:
                await ctx.send("You have to have at least **2** options!")
            else:
                req = {"title": title, "options": options_list}
                r = requests.post('https://www.strawpoll.me/api/v2/polls',
                            headers={
                            'content-type': 'application/json'
                            },
                                           
                            data=json.dumps(req))
                resp = r.json()
                embed = discord.Embed(colour=0xfefe00, description="I have successfully created a poll for you!")
                embed.set_thumbnail(url='https://pbs.twimg.com/profile_images/737742455643070465/yNKcnrSA_400x400.jpg')
                embed.set_author(name="Success!")
                embed.add_field(name="Strawpoll link..", value=f"https://strawpoll.me/{resp['id']}")
                await ctx.send(embed=embed)

    @commands.command(aliases=['mapimage'])
    async def map(self, ctx, *, location):#app_id=HKvIwMJ55iDxTJdHr03l&app_code=CZiIfYufln4tXB4UU9mbZA
        """Get a custom map image"""
        try:
            await self.add_money(user=ctx.message.author.id, count=1)
        except:
            pass
        embed = discord.Embed()
        try:
            ct = location.replace(" ", "+").replace(",", "")
            embed.set_image(url=f"https://image.maps.api.here.com/mia/1.6/mapview?&z=12&i=1&app_id=HKvIwMJ55iDxTJdHr03l&app_code=CZiIfYufln4tXB4UU9mbZA&ci={ct}&&&")
            await ctx.send(embed=embed)
        except:
            await ctx.send("There was an error processing your image.")

    @commands.command()
    async def translate(self, ctx, lang_code, *, message):
        """Translate some text"""
        try:
            await self.add_money(user=ctx.message.author.id, count=1)
        except:
            pass
        to = lang_code
        msg = message.replace(" ", "+")#dont steal my key lol
        async with aiohttp.ClientSession(headers={'Accept': 'application/json'}) as session:
                async with session.get(
                    f"https://translate.yandex.net/api/v1.5/tr.json/translate?key=trnsl.1.1.20180825T052109Z"\
                    f".c36b5e400701326d.b710f868bfd135fe1f3b1e490a3db5f02ae83db3&lang={to}&text={msg}") as get:
                    resp = await get.json()
                    lan = resp["lang"]
                    tex = resp["text"]
                    lang = lan.replace("-", " -> ")
                    text = rnd(tex)
                    embed = discord.Embed()
                    embed.add_field(name="Language..", value=f"`{lang}`")
                    embed.add_field(name="From..", value=f"`{message}`")
                    embed.add_field(name="To..", value=f"`{text}`")
                    embed.set_thumbnail(url="https://cdn6.aptoide.com/imgs/4/8/8/48860afe26ae45e7f0ab3737017e5ab5_icon.png?w=240")
                    embed.set_author(name='TRANSLATION',
                        icon_url='https://vignette.wikia.nocookie.net/logopedia/images/d/d0/Siri.png/revision/latest?cb=20170730135120')
                    await ctx.send(embed=embed)

    @commands.command(aliases=['detect'])
    async def langdetect(self, ctx, *, message):
        """Detect Language from text"""
        msg = message.replace(" ", "+")
        try:
            await self.add_money(user=ctx.message.author.id, count=1)
        except:
            pass
        async with aiohttp.ClientSession(headers={'Accept': 'application/json'}) as session:
                async with session.get(f"https://translate.yandex.net/api/v1.5/tr.json/detect?key=trnsl.1.1.20180825T052109Z.c36b5e400701326d.b710f868bfd135fe1f3b1e490a3db5f02ae83db3&text={msg}") as get:
                    resp = await get.json()
                    lang = resp["lang"]
                    embed = discord.Embed(title="Success!", description=f"This language has been detected as.. **{lang}**")
                    flag = f"http://fotw.fivestarflags.com/images/{lang[:-1]}/{lang}.gif"
                    embed.set_footer(text='Siri Knowledge', icon_url='https://vignette.wikia.nocookie.net/logopedia/images/d/d0/Siri.png/revision/latest?cb=20170730135120')
                    await ctx.send(embed=embed)

    @commands.command()
    async def weather(self, ctx, *, cityname):
        """Weather in a specified location"""
        location = cityname
        try:
            await self.add_money(user=ctx.message.author.id, count=1)
        except:
            pass
        async with aiohttp.ClientSession(headers={'Accept': 'application/json'}) as session:
            async with session.get(f"https://api.openweathermap.org/data/2.5/weather?q={location}&APPID=f8f21ceb5e624851c948c33ffbe43f1d&units=Imperial") as get:
                resp = await get.json()
                if get.status == 404:
                    return await ctx.send("I couldn't find that place! Did you spell it correctly?")
                w = resp['main']['temp']
                c = resp['sys']['country']
                i = c.replace("A", "a").replace("B", "b").replace("C", "c").replace("D", "d").replace("E", "e").replace("F", "f").replace("G", "g").replace("H", "h").replace("I", "i").replace("J", "j").replace("K", "k").replace("L", "l").replace("M", "m").replace("N", "n").replace("O", "o").replace("P", "p").replace("Q", "q").replace("R", "r").replace("S", "s").replace("T", "t").replace("U", "u").replace("V", "v").replace("W", "w").replace("X", "x").replace("Y", "y").replace("Z", "z")
                flag = f"http://fotw.fivestarflags.com/images/{i[:-1]}/{i}.gif"
                icon = "http://openweathermap.org/img/w/" + resp['weather'][0]['icon'] + ".png"
                embed = discord.Embed(description=f"{resp['weather'][0]['description']}", colour=0x37749c)
                embed.set_author(name=f"{resp['name']}, {resp['sys']['country']}", icon_url=icon)
                embed.add_field(name="Temperature", value=f"{resp['main']['temp']}°F")
                embed.add_field(name="Weather", value=resp['weather'][0]['main'])
                embed.add_field(name="Humidity", value=f"{resp['main']['humidity']}%")
                embed.add_field(name="Wind Speed", value=f"{resp['wind']['speed']}mph")
                embed.set_thumbnail(url=flag)
                if w > 56:
                    await ctx.send(f":flag_{i}: It's nice in **{resp['name']}**!.. up to **{resp['main']['temp_max']}°F**!")
                else:
                    await ctx.send(f"Brr. Take a jacket!.. up to **{resp['main']['temp_max']}°F**!")
                await ctx.send(embed=embed)
          
    @commands.command(aliases=['shorten', 'linkshorten'])
    async def link(self, ctx, url):
        """- Shorten a link"""
        await ctx.trigger_typing()
        try:
            await self.add_money(user=ctx.message.author.id, count=1)
        except:
            pass
        try:
            a = random.randint(1, 9)
            b = random.randint(1, 9)
            c = random.randint(1, 9)
            d = random.randint(1, 9)
            letters = ['a', 'A', 'b', 'B', 'C', 'd', 'n', 'x', 'Y', 'y', 's', 'S', 'i', 'k', 'K', 'g', 'G', 'm', 'c']
            letters2 = ['q', 'Q', 'p', 'P', 'o', 'v', 'V', 'z', 'e', 'E', 'I', 'L', 't', 'T', 'r', 'R', 'j', 'J', 'O']
            random_c = f'{a}{rnd(letters)}{c}{rnd(letters2)}'
            r = requests.post("https://api.rebrandly.com/v1/links",
            data = json.dumps({
                    "destination": url
                  , "domain": { "fullName": "rebrand.ly" }
                 , "slashtag": f"{random_c}"
                 , "title": f"Siri/{ctx.message.author.name} #{random_c}"
              }),
            headers={
            "Content-type": "application/json"
            ,"apikey": "8e3346d5ea124d7480ce12c0140f3c59"
            })
            link = r.json()
            embed = discord.Embed(colour=0x00a6ff, description="I have successfully generated a custom link for you!")
            embed.set_thumbnail(url='https://finaldesign.it/wp-content/uploads/2017/06/Rebrandly-favicon-250x250.png')
            embed.set_author(name="Success!", icon_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTVSMTdCINzzsBHiXSXQyq2QEcPRII27vkMdjpMLxBrpqDHIpXb")#
            embed.add_field(name="Original Link..", value=url)
            embed.add_field(name="Shortened Link..", value="https://{}".format(link["shortUrl"]))
            embed.set_footer(text="Powered by rebrand.ly")
            await ctx.send(embed=embed)
        except:
            try:
                a = random.randint(1, 9)
                b = random.randint(1, 9)
                c = random.randint(1, 9)
                d = random.randint(1, 9)
                letters = ['a', 'A', 'b', 'B', 'C', 'd', 'n', 'x', 'Y', 'y', 's', 'S', 'i', 'k', 'K', 'g', 'G', 'm', 'c']
                letters2 = ['q', 'Q', 'p', 'P', 'o', 'v', 'V', 'z', 'e', 'E', 'I', 'L', 't', 'T', 'r', 'R', 'j', 'J', 'O']
                random_c = f'{a}{rnd(letters)}{c}{rnd(letters2)}'
                https = 'https://' + url
                r = requests.post("https://api.rebrandly.com/v1/links",
                data = json.dumps({
                        "destination": https
                      , "domain": { "fullName": "rebrand.ly" }
                     , "slashtag": f"{random_c}"
                     , "title": f"Siri/{ctx.message.author.name} #{random_c}"
                     , "isPublic": True
                  }),
                headers={
                "Content-type": "application/json"
                ,"apikey": "8e3346d5ea124d7480ce12c0140f3c59"
                })
                link = r.json()
                embed = discord.Embed(colour=0x00a6ff, description="I have successfully generated a custom link for you!")
                embed.set_thumbnail(url='https://finaldesign.it/wp-content/uploads/2017/06/Rebrandly-favicon-250x250.png')
                embed.set_author(name="Success!", icon_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTVSMTdCINzzsBHiXSXQyq2QEcPRII27vkMdjpMLxBrpqDHIpXb")
                embed.add_field(name="Original Link..", value=https)
                embed.add_field(name="Shortened Link..", value="https://{}".format(link["shortUrl"]))
                embed.set_footer(text="Powered by rebrand.ly")
                await ctx.send(embed=embed)
            except Exception as e:
                await ctx.send("If you are seeing this.. please contact lukee#0420")
                await ctx.send("```{}: {}```".format(e, type(e).__name__))
            except:
                embed = discord.Embed(colour=0xff0000)
                embed.add_field(name="Error..", value="Invalid Link")
                await ctx.send(embed=embed)


    @commands.command()
    async def support(self, ctx):
        await ctx.send("__**Support**__:\nTo submit a ticket, do `siri ticket <message>`..\nTo join a support guild, click here: https://discord.gg/2RSErBu")


    @commands.command(aliases=['color'])
    async def colour(self, ctx, col = None):
        """- Get info about a colour."""

        #r = requests.get(f"http://www.colourlovers.com/api/color/{col}&format=json").json()
        #image = r.get("imageUrl")
        try:
            await self.add_money(user=ctx.message.author.id, count=1)
        except:
            pass
        async with aiohttp.ClientSession(headers={'Accept': 'application/json'}) as session: #http://www.colourlovers.com/api/color/ff0000&format=json
            async with session.get(f"http://www.thecolorapi.com/id?hex={col}") as get:
                resp = await get.json()

                try:
                    if col is None:
                        await ctx.send("<:WrongMark:473277055107334144> **There was an error.** Please include the hex with your message.")
                    elif col == 'ff':
                        c = resp['name']['value']
                        hx = resp['hex']['value']
                        img = f"https://dummyimage.com/300/00/ff.png&text=++{c}+"
                        embed = discord.Embed(colour=0xffffff, title=resp['name']['value'], description=f"Information about the colour, **{c}** **(**{hx}**)**:")
                        embed.add_field(name="Hex", value=resp['hex']['value'])
                        embed.add_field(name="RGB", value=resp['rgb']['value'])
                        embed.add_field(name="HSL", value=resp['hsl']['value'])
                        embed.add_field(name="XYZ", value=resp['XYZ']['value'])
                        embed.add_field(name="CMYK", value=resp['cmyk']['value'])
                        embed.add_field(name="Closest Hex", value=resp['name']['closest_named_hex'])
                        embed.set_thumbnail(url=img)
                        embed.set_footer(text="thecolorapi.com")

                        msg = await ctx.send(embed=embed)
                        await msg.add_reaction('🎨')
                    elif col == 'fff':
                        c = resp['name']['value']
                        hx = resp['hex']['value']
                        img = f"https://dummyimage.com/300/00/00.png&text=++{c}+"
                        embed = discord.Embed(colour=0xffffff, title=resp['name']['value'], description=f"Information about the colour, **{c}** **(**{hx}**)**:")
                        embed.add_field(name="Hex", value=resp['hex']['value'])
                        embed.add_field(name="RGB", value=resp['rgb']['value'])
                        embed.add_field(name="HSL", value=resp['hsl']['value'])
                        embed.add_field(name="XYZ", value=resp['XYZ']['value'])
                        embed.add_field(name="CMYK", value=resp['cmyk']['value'])
                        embed.add_field(name="Closest Hex", value=resp['name']['closest_named_hex'])
                        embed.set_thumbnail(url=img)
                        embed.set_footer(text="thecolorapi.com")

                        msg = await ctx.send(embed=embed)
                        await msg.add_reaction('🎨')
                    else:
                        c = resp['name']['value']
                        hx = resp['hex']['value']
                        img = f"https://dummyimage.com/300/{col}/ff.png&text=+++{c}++"
                        embed = discord.Embed(colour=0xffffff, title=resp['name']['value'], description=f"Information about the colour, **{c}** **(**{hx}**)**:")
                        embed.add_field(name="Hex", value=resp['hex']['value'])
                        embed.add_field(name="RGB", value=resp['rgb']['value'])
                        embed.add_field(name="HSL", value=resp['hsl']['value'])
                        embed.add_field(name="XYZ", value=resp['XYZ']['value'])
                        embed.add_field(name="CMYK", value=resp['cmyk']['value'])
                        embed.add_field(name="Closest Hex", value=resp['name']['closest_named_hex'])
                        embed.set_thumbnail(url=img)
                        embed.set_footer(text="thecolorapi.com")

                        msg = await ctx.send(embed=embed)
                        await msg.add_reaction('🎨')
                except Exception:
                    await ctx.send("<:WrongMark:473277055107334144> **There was an error.** The API may be down or there was something wrong with the hex you gave me..")
                except:
                    await ctx.send("<:WrongMark:473277055107334144> **There was an error.** The API may be down or there was something wrong with the hex you gave me..")


    @commands.command(aliases=['pfp'])
    async def avatar(self, ctx, user: discord.Member= None):
        """- Get a member's avatar"""
        author = ctx.message.author
        try:
            await self.add_money(user=ctx.message.author.id, count=1)
        except:
            pass
        if ctx.message.author.bot: return

        if user is None:

            trl = discord.Embed(title=("{}'s avatar:".format(author)) , colour=author.colour, description="[Link]({})".format(author.avatar_url))
            trl.set_image(url=author.avatar_url)

            await ctx.send(embed=trl)
        else:

            trl = discord.Embed(title=("{}'s avatar:".format(user)) , colour=user.colour, description="[Link]({})".format(user.avatar_url))
            trl.set_image(url=user.avatar_url)

            await ctx.send(embed=trl)

    @commands.command(aliases=['serverinformation', 'guildinfo'])
    async def serverinfo(self, ctx):
        """- Information about this guild."""
        try:
            await self.add_money(user=ctx.message.author.id, count=1)
        except:
            pass

        message = ctx.message
        author = ctx.message.author
        guild = ctx.message.guild
        roles = list(author.roles)
        permissions = list(author.guild_permissions)
        #roles = []
        #for guild in self.bot.guilds:
            #x.id for role in guild.role_hierarchy:
                #roles.append(x.id)
                #ea = '>, <@&'.join(str(x.id))
        rl = discord.Embed(colour=discord.Color(0x00e1e1))
        rl.set_author(name="Server Info", icon_url=guild.icon_url)
        rl.set_thumbnail(url=guild.icon_url)
        rl.add_field(name="Name:", value='{}'.format(guild), inline=False)
        rl.add_field(name="ID:", value=guild.id)
        rl.add_field(name="Region:", value=guild.region)
        rl.add_field(name="Emojis:", value=f"**{str(len(guild.emojis))}**")
        rl.add_field(name="Roles:", value=f"**{str(len(guild.roles))}**")
        rl.add_field(name='Guild Owner:', value=guild.owner.mention)
        rl.add_field(name="Members:", value=guild.member_count)
        rl.add_field(name="Channels:", value=str(len(guild.channels)))
        rl.add_field(name="Verification:", value=guild.verification_level)
        rl.add_field(name='Server Created:', value=guild.created_at.__format__('%A, %B %d, %Y'))
        await ctx.send(embed=rl)

    @commands.command(aliases=['userinformation'])
    async def userinfo(self, ctx, member: discord.Member= None):
        """- Information about a member"""
        try:
            await self.add_money(user=ctx.message.author.id, count=1)
        except:
            pass
        
        if member is None:
            user = ctx.message.author
        else:
            user = member

        message = ctx.message
        guild = ctx.message.guild
        await message.add_reaction('🔍')
        trl = discord.Embed(colour=user.colour)
        trl.set_author(name=user, icon_url=user.avatar_url)
        trl.set_thumbnail(url=user.avatar_url)
        #trl.add_field(name="Username:", value='{}'.format(user), inline=False)
        trl.add_field(name="Nickname:", value=user.nick)
        trl.add_field(name="Status:", value=user.status)
        trl.add_field(name="Playing:", value=user.activity)
        trl.add_field(name="Roles:", value=user.top_role.name + " **(" + str(len(user.roles)) + ")**")
        trl.add_field(name='Account Created:', value=user.created_at.__format__('%A, %B %d, %Y'))
        trl.add_field(name='Joined Server:', value=user.joined_at.__format__('%A, %B %d, %Y'))
        trl.add_field(name="User ID:", value=user.id)
        await ctx.send(embed=trl)


def setup(bot):
    bot.add_cog(Utility(bot))
