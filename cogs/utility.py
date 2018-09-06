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
        if message.author.bot: return
        if message.content.startswith('<@481337766379126784> '):
            await self.bot.send_typing(message.channel)
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
            await self.bot.send_message(message.channel, f"**{message.author.name}**, {response}")


    @commands.command(pass_context=True, name='wikipedia', aliases=['wiki', 'w'])
    async def _wikipedia(self, context, *, q: str = None):
        """Search Information on Wikipedia"""
        try:
            await self.add_money(user=ctx.message.author.id, count=1)
        except:
            pass 

        embed = discord.Embed(description="<a:loading:473279565670907914> Searching..")
        msg = await self.bot.say(embed=embed)
        if q is None:
            await self.bot.say("Include the query with the command!")
        elif q == 'penis' or q == 'Penis' or q == 'orgy' or q == 'Orgy' or q == 'vagina' or q == 'Vagina' or q == 'Breast' or q == 'breast' or q == 'Nipple' or q == 'nipple' or q == 'Porn' or q == 'porn' or q == 'adult videos' or q == 'XXX':
            await self.bot.say(f":warning: **Caution!** That is NSFW!")
        else:

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
            async with session.get(url, params=payload, headers={'user-agent': 'Siri v1'}) as r:
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
                await self.bot.delete_message(msg)
                await self.bot.say(embed=embed)
            else:
                await self.bot.delete_message(msg)
                await self.bot.say("<:WrongMark:473277055107334144> I could not find anything with that query..")

    @commands.command(pass_context=True, aliases=['info', 'botinfo'])
    async def stats(self, ctx):
        """- Information about myself."""
        try:
            await self.add_money(user=ctx.message.author.id, count=1)
        except:
            pass
        if ctx.message.author.bot: return
        else:

            author = ctx.message.author

            #RAM = self.process.memory_full_info().rss  /  1024 ** 2

            stat = discord.Embed(color=0x36393E, description=f"**Siri. by lukee#0420**\n\n\n> **Python**... `3.6`\n> **Ubuntu**... `18.04`\n> **Servers**... `{str(len(self.bot.servers))}`\n> **Messages Received**... `{str(len(self.bot.messages))}\n> **RAM Usage**... `??MB`")


            await self.bot.say(embed=stat)

    @commands.command(pass_context = True)
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
            server = ctx.message.server

            channel = self.bot.get_channel("481352533676392469")

            stat = discord.Embed(color = discord.Color(0xcd87ff))
            stat.set_author(name=server, icon_url=server.icon_url)
            stat.set_footer(text="Ticket ID: {}".format(random_c))

            stat.add_field(name="User", value=author, inline=False)
            stat.add_field(name="User ID", value=author.id, inline=False)
            stat.add_field(name="Server ID", value=server.id, inline=False)
            stat.add_field(name="Time:", value="{} UTC".format(ctx.message.timestamp))
            stat.add_field(name="Message", value=message, inline=False)

            embed = discord.Embed(title="<:CheckMark:473276943341453312> **Ticket Sent!**", description="Please wait until you get a DM from a staff member. Please do not overuse this command, or you will be blocked from using it.\n\n(Cooldown is `15` minutes!)")
            embed.set_footer(text=f"KEEP THIS TICKET ID: {random_c}")
            await self.bot.say(embed=embed)
            await self.bot.send_message(channel, embed=stat)
            print("\n\n\n----\n\n\"{}\" has sent a ticket:\n\n".format(author))
            print(message)
            print("\n----\n\n\n")

    @commands.command(pass_context=True, aliases=['chat', 'cb'])
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
            #await self.bot.say(f"{ctx.message.author.mention}, {r['entities']['intent'][0]['value']}")
        #except:
        resp = r.json()
        response = resp['result']['fulfillment']['messages'][0]['speech']
        ra = requests.get("https://api.dialogflow.com/v1/contexts?v=20150910&sessionId=12345", headers={"Authorization" : "Bearer 1663b12fcc24462e9711d9801be96485"}).json()
        #await self.bot.say(ra)
        await self.bot.say(f"**{ctx.message.author.name}**, {response}")

    @commands.command(pass_context=True, aliases=['lookup', 'websearch'])
    async def search(self, ctx, *, query = None):
        embed = discord.Embed(description="<a:loading:473279565670907914> Searching..")
        msg = await self.bot.say(embed=embed)
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
            await self.bot.delete_message(msg)
            await self.bot.say("`Incorrect Usage`\n```siri search <search-query>```")
        elif query == 'porn' or query == 'Porn' or query == 'orgy' or query == 'Orgy' or query == 'gay porn' or query == 'penis' or query == 'Penis' or query == 'gay' or query == 'Gay' or query == 'ass' or query == 'Ass' or query == 'tits' or query == 'Tits' or query == 'Boobs' or query == 'boobs' or query == 'Lesbian' or query == 'lesbian' or query == 'cock' or query == 'Cock' or query == 'hentai' or query == 'Hentai' or query == 'Sex' or query == 'sex':
            await self.bot.delete_message(msg)
            await self.bot.say("I couldn't find anything..")

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
                #await self.bot.say(f":ok_hand:\n{r}")#relatedSearch
                await self.bot.say(embed=embed)
                await self.bot.delete_message(msg)
            except:
                await self.bot.delete_message(msg)
                await self.bot.say(f"I couldn't find anything..")

    @commands.command(pass_context=True)
    async def test(self, ctx):
        await self.bot.say("This is just a better test.")

    @commands.command(pass_context=True, hidden=True)
    @checks.admin_or_permissions(manage_server=True)
    async def uwu(self, ctx, c:int, *, message):
        for e in range(c):
            await self.bot.say(message)

    @commands.command(pass_context=True, aliases=['IMDb'])
    async def imdb(self, ctx, *, title= None):
        """Search a movie/series on IMDb"""
        try:
            await self.add_money(user=ctx.message.author.id, count=1)
        except:
            pass
        if title is None:
            await self.bot.say("Please include the series/movie title!")
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
                await self.bot.say(embed=embed)

            except Exception as e:
                await self.bot.say(f"I couldn't find that movie or series..")

    @commands.command(pass_context=True, aliases=['today'])
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
            embed.add_field(name="Published at..", value={publishedat[:-4]})
            embed.set_thumbnail(url=re['urlToImage'])
            embed.set_footer(text=f"© {re['source']['name']} & NewsAPI")

            await self.bot.say(embed=embed, content=f":newspaper: | Here is a popular story from the **News**..")
        except:
            await self.bot.say("There was an issue getting the news article.. Check back in a few hours.")

    @commands.command(pass_context=True)
    async def article(self, ctx, *, query = None):#03d8e32c7dd349e3b9efe0338e08e890
        """Search for an article in the News"""
        try:
            await self.add_money(user=ctx.message.author.id, count=1)
        except:
            pass
        if query is None:
            await self.bot.say("`Incorrect Usage`\n```siri article <search-query>```")
        else:

            try:
                q = query.replace(" ", "%20")
                r = requests.get(f"https://newsapi.org/v2/everything?q={q}&apiKey=03d8e32c7dd349e3b9efe0338e08e890").json()
                
                re = r['articles'][0]
                pa = re['publishedAt']
                publishedat = pa.replace("T", " ").replace("Z", " ").replace("-", "/").replace("{'", "").replace("'}", "")
                embed = discord.Embed(title=re['title'], description=re['description'], url=re['url'])
                embed.add_field(name="Published at..", value={publishedat[:-4]})
                embed.set_thumbnail(url=re['urlToImage'])
                embed.set_footer(text=f"© {re['source']['name']} & NewsAPI")

                await self.bot.say(embed=embed, content=f":newspaper: | Here is what I found for **\"{query}\"** in the **News**..")
            except:
                await self.bot.say("I couldn't find any article that matched your query..")

    @commands.command(pass_context=True, aliases=['dict', 'dictionary'])
    async def define(self, ctx, *, word):#CRED: 6cd11931 #KEY: a6d815d3a40f53811de4aad036361e5a
        """Define a word"""
        await self.bot.send_typing(ctx.message.channel)
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

            await self.bot.say(embed=embed, content=f":books: | Here is the definition for **{word}**:")
        except Exception as e:
            await self.bot.say("I couldn't find that word in the dictionary.")
            #await self.bot.say(e)
            #await self.bot.say(rnd(re['etymologies']))
            #await self.bot.say(rnd(re['senses'][0]['definitions']))
            #await self.bot.say(re['senses'][0]['examples'][0]['text'])

    @commands.command(pass_context=True)
    async def hastebin(self, ctx, *, message):
        """Send your text to a haste bin

        TIP: if your text is in a codeblock, it removes the three grave accents when adding to the hastebin"""
        try:
            await self.add_money(user=ctx.message.author.id, count=1)
        except:
            pass
        msg = message.replace("```", "")
        r = requests.post(f"https://hastebin.com/documents",
        data=msg.encode('utf-8')).json()
        embed = discord.Embed(colour=0x00a6ff, description="I have successfully generated a custom hastebin link for you!")
        embed.set_thumbnail(url='https://pbs.twimg.com/profile_images/1664989409/twitter_400x400.png')
        embed.set_author(name="Success!", icon_url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTVSMTdCINzzsBHiXSXQyq2QEcPRII27vkMdjpMLxBrpqDHIpXb")
        embed.add_field(name="Hastebin link", value='https://hastebin.com/' + r['key'])
        await self.bot.say(embed=embed)
    

    @commands.command(pass_context=True, aliases=['dstatus'])
    async def discordstatus(self, ctx):
        """Get Discord Status"""
        try:
            await self.add_money(user=ctx.message.author.id, count=1)
        except:
            pass
        embed = discord.Embed(description="<a:loading:473279565670907914> Fetching..")
        msg = await self.bot.say(embed=embed)
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



        embed = discord.Embed(colour=0x8faaef, title="Discord Status", url="http://status.discordapp.com", description=f"{emoji} **Discord**\n*{description}*\n{emoji2} **API**\n *{ind}*\n\n**Next Maintenance:**{maint}\n\n**Unresolved Incidents:**{inc}")
        embed.set_thumbnail(url="https://yt3.ggpht.com/a-/ACSszfHkcq8jw1JefOzyp7pui7vBjA66h5cFwbtC-g=s900-mo-c-c0xffffffff-rj-k-no")
        await self.bot.delete_message(msg)
        await self.bot.say(embed=embed)

    @commands.command(pass_context=True, aliases=['poll'])
    async def strawpoll(self, ctx, *, question, options= None):
        """Creates a strawpoll. Separate with ', '"""
        try:
            await self.add_money(user=ctx.message.author.id, count=1)
        except:
            pass
        options_list = question.split(', ')
        title = options_list[0]
        options_list.remove(title)
        if len(options_list) < 2:
            await self.bot.say("You have to have at least **2** options!")
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
            await self.bot.say(embed=embed)

    @commands.command(pass_context=True, aliases=['mapimage'])
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
            await self.bot.say(embed=embed)
        except:
            await self.bot.say("There was an error processing your image.")
    @commands.command(pass_context=True)
    async def translate(self, ctx, lang_code, *, message):
        """Translate some text"""
        try:
            await self.add_money(user=ctx.message.author.id, count=1)
        except:
            pass
        to = lang_code
        msg = message.replace(" ", "+")#dont steal my key lol
        async with aiohttp.ClientSession(headers={'Accept': 'application/json'}) as session:
                async with session.get(f"https://translate.yandex.net/api/v1.5/tr.json/translate?key=trnsl.1.1.20180825T052109Z.c36b5e400701326d.b710f868bfd135fe1f3b1e490a3db5f02ae83db3&lang={to}&text={msg}") as get:
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
                    embed.set_author(name='TRANSLATION', icon_url='https://vignette.wikia.nocookie.net/logopedia/images/d/d0/Siri.png/revision/latest?cb=20170730135120')
                    await self.bot.say(embed=embed)

    @commands.command(pass_context=True, aliases=['detect'])
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
                    await self.bot.say(embed=embed)

    @commands.command(pass_context=True)
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
                    w = resp['main']['temp']
                    c = resp['sys']['country']
                    i = c.replace("A", "a").replace("B", "b").replace("C", "c").replace("D", "d").replace("E", "e").replace("F", "f").replace("G", "g").replace("H", "h").replace("I", "i").replace("J", "j").replace("K", "k").replace("L", "l").replace("M", "m").replace("N", "n").replace("O", "o").replace("P", "p").replace("Q", "q").replace("R", "r").replace("S", "s").replace("T", "t").replace("U", "u").replace("V", "v").replace("W", "w").replace("X", "x").replace("Y", "y").replace("Z", "z")
                    flag = f"http://fotw.fivestarflags.com/images/{i[:-1]}/{i}.gif"
                    icon = "http://openweathermap.org/img/w/" + resp['weather'][0]['icon'] + ".png"
                    embed = discord.Embed(description=f"{resp['weather'][0]['description']}")
                    embed.set_author(name=f"{resp['name']}, {resp['sys']['country']}", icon_url=icon)
                    embed.add_field(name="Temperature", value=f"{resp['main']['temp']}°F")
                    embed.add_field(name="Weather", value=resp['weather'][0]['main'])
                    embed.add_field(name="Humidity", value=f"{resp['main']['humidity']}%")
                    embed.add_field(name="Wind Speed", value=f"{resp['wind']['speed']}mph")
                    embed.set_thumbnail(url=flag)
                    if w > 56:
                        await self.bot.say(f"It's nice outside.. up to **{resp['main']['temp_max']}°F**!")
                    else:
                        await self.bot.say(f"Brr. Take a jacket!.. up to **{resp['main']['temp_max']}°F**!")
                    await self.bot.say(embed=embed)

    @commands.command(pass_context=True)
    async def servers(self, ctx):
        r = requests.get("https://discordbots.org/api/bots/481337766379126784").json()
        users = len(set(self.bot.get_all_members()))
        channels = len([c for c in self.bot.get_all_channels()])
        emojis = len([c for c in self.bot.get_all_emojis()])
        #commands = len([c for c in self.bot.get_all_commands()])
        text = f"I am in **{str(len(self.bot.servers))} servers**!\nI can see **{channels} channels**!\nI am with **{users} users**!\nI can use **{emojis} emojis**!\nI have **{r['points']} DBL votes**!\n\n[DBL](https://discordbots.org/bot/481337766379126784) | [Vote](https://discordbots.org/bot/481337766379126784/vote) | [Invite](https://discordapp.com/api/oauth2/authorize?client_id=481337766379126784&scope=bot&permissions=0)"
        embed = discord.Embed(description=text)
        try:
            await self.add_money(user=ctx.message.author.id, count=1)
        except:
            pass
        await self.bot.say(embed=embed)


    @commands.command(pass_context=True, aliases="resp")
    async def respond(self, ctx, ticket, id, *, message):
        if ctx.message.author.id =='396153668820402197':
            target = discord.utils.get(self.bot.get_all_members(), id=id)
            embed = discord.Embed(colour=0x00a6ff, description=f"\"{message}\"")
            embed.set_author(name=f"In response to ticket #{ticket}..", icon_url=self.bot.user.avatar_url)
            await self.bot.send_message(target, embed=embed)
            await self.bot.say(f":incoming_envelope: I have sent the response to the owner of Ticket **#**{ticket}.")
        else:
            trl = discord.Embed(title=("<:WrongMark:473277055107334144> You are not authorised to use this command!") , colour=0xff775b)
            trl.set_footer(text="Sorry about that.")
            await self.bot.say(embed=trl)

    @commands.command(pass_context=True, aliases=['shorten', 'linkshorten'])
    async def link(self, ctx, url):
        """- Shorten a link"""
        await self.bot.send_typing(ctx.message.channel)
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
            await self.bot.say(embed=embed)
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
                await self.bot.say(embed=embed)
            except Exception as e:
                await self.bot.say("If you are seeing this.. please contact lukee#0420")
                await self.bot.say("```{}: {}```".format(e, type(e).__name__))
            except:
                embed = discord.Embed(colour=0xff0000)
                embed.add_field(name="Error..", value="Invalid Link")
                await self.bot.say(embed=embed)


    @commands.command(pass_context=True)
    async def support(self, ctx):
        await self.bot.say("__**Support**__:\nTo submit a ticket, do `siri ticket <message>`..\nTo join a support server, click here: https://discord.gg/2RSErBu")


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

    @commands.command(pass_context=True, aliases=['color'])
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
                            await self.bot.say("<:WrongMark:473277055107334144> **There was an error.** Please include the hex with your message.")
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

                            msg = await self.bot.say(embed=embed)
                            await self.bot.add_reaction(msg, '🎨')
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

                            msg = await self.bot.say(embed=embed)
                            await self.bot.add_reaction(msg, '🎨')
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

                            msg = await self.bot.say(embed=embed)
                            await self.bot.add_reaction(msg, '🎨')
                    except Exception:
                        await self.bot.say("<:WrongMark:473277055107334144> **There was an error.** The API may be down or there was something wrong with the hex you gave me..")
                    except:
                        await self.bot.say("<:WrongMark:473277055107334144> **There was an error.** The API may be down or there was something wrong with the hex you gave me..")


    @commands.command(pass_context=True, aliases=['pfp'])
    async def avatar(self, ctx, user: discord.User= None):
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

            await self.bot.say(embed=trl)
        else:

            trl = discord.Embed(title=("{}'s avatar:".format(user)) , colour=user.colour, description="[Link]({})".format(user.avatar_url))
            trl.set_image(url=user.avatar_url)

            await self.bot.say(embed=trl)

    @commands.command(pass_context=True, aliases=['serverinformation'])
    async def serverinfo(self, ctx):
        """- Information about this server."""
        if ctx.message.author.bot: return
        try:
            await self.add_money(user=ctx.message.author.id, count=1)
        except:
            pass
        else:

            message = ctx.message

            author = ctx.message.author

            server = ctx.message.server

            roles = list(author.roles)
            permissions = list(author.server_permissions)

            roles = [x.id for x in server.role_hierarchy]

            #emoji_name = [x.name for x in self.bot.get_all_emojis]

            #emoji_id = [x.id for x in self.bot.get_all_emojis]

            #emojis = "<:" + emoji_name + ":" + emoji_id + ">"

            roles = '>, <@&'.join(roles)
            roles = roles.replace("@everyone", "")
            e = roles[:-13]
            ea = e.replace("@deleted-role", "@everyone")

            #el = ' '.join(emojis)

            rl = discord.Embed(colour=0x00e1e1)
            rl.set_author(name="Server Info", icon_url=server.icon_url)
            rl.set_thumbnail(url=server.icon_url)
            rl.add_field(name="Name:", value='{}'.format(server), inline=False)
            rl.add_field(name="ID:", value=server.id)
            rl.add_field(name="Region:", value=server.region)
            rl.add_field(name="Emojis:", value=f"**{str(len(server.emojis))}**")

            rl.add_field(name="Roles:", value=f"<@&{ea[:-10]} (**{str(len(server.roles))}**)")


            rl.add_field(name='Server Owner:', value=server.owner.mention)
            rl.add_field(name='Server Created:', value=server.created_at.__format__('%A, %B %d, %Y'))
            rl.add_field(name="Members:", value=server.member_count)
            rl.add_field(name="Channels:", value=str(len(server.channels)))
            rl.add_field(name="Verification:", value=server.verification_level)


            await self.bot.say(embed=rl)




    @commands.command(pass_context=True, aliases=['userinformation'])
    async def userinfo(self, ctx, user: discord.User= None):
        """- Information about a member"""
        if ctx.message.author.bot: return
        try:
            await self.add_money(user=ctx.message.author.id, count=1)
        except:
            pass

        if user is None:

            message = ctx.message

            author = ctx.message.author

            server = ctx.message.server

            roles = list(author.roles)
            permissions = list(author.server_permissions)

            await self.bot.add_reaction(message, '🔍')

            rl = discord.Embed(colour=author.colour)
            rl.set_author(name="User Info", icon_url=author.avatar_url)
            rl.set_thumbnail(url=author.avatar_url)
            rl.add_field(name="Username:", value='{}'.format(author), inline=False)
            rl.add_field(name="Nickname:", value=author.nick)
            rl.add_field(name="Status:", value=author.status)
            rl.add_field(name="Playing:", value=author.game)

            rl.add_field(name="Roles:", value=author.top_role.name + " **(" + str(len(author.roles)) + ")**")


            rl.add_field(name='Joined Server:', value=author.joined_at.__format__('%A, %B %d, %Y'))
            rl.add_field(name='Account Created:', value=author.created_at.__format__('%A, %B %d, %Y'))
            rl.add_field(name="User ID:", value=author.id)


            await self.bot.say(embed=rl)

        else:

            message = ctx.message

            server = ctx.message.server

            await self.bot.add_reaction(message, '🔍')

            trl = discord.Embed(colour=user.colour)
            trl.set_author(name="User Info", icon_url=user.avatar_url)
            trl.set_thumbnail(url=user.avatar_url)
            trl.add_field(name="Username:", value='{}'.format(user), inline=False)
            trl.add_field(name="Nickname:", value=user.nick)
            trl.add_field(name="Status:", value=user.status)
            trl.add_field(name="Playing:", value=user.game)
            trl.add_field(name="Roles:", value=user.top_role.name + " **(" + str(len(user.roles)) + ")**")


            trl.add_field(name='Joined Server:', value=user.joined_at.__format__('%A, %B %d, %Y'))
            trl.add_field(name='Account Created:', value=user.created_at.__format__('%A, %B %d, %Y'))
            trl.add_field(name="User ID:", value=user.id)


            await self.bot.say(embed=trl)


def setup(bot):
    bot.add_cog(Utility(bot))
