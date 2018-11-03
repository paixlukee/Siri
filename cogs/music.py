import discord
import lavalink
from discord.ext import commands
import datetime
import requests
import logging
import math
import re
import asyncio
from random import choice as rnd

time_rx = re.compile('[0-9]+')
url_rx = re.compile('https?:\/\/(?:www\.)?.+')

class Music:
    def __init__(self, bot):
        self.bot = bot
        self.votes = []
        self.ttrue = '<:greentick:492800272834494474>'
        self.tfals = '<:redtick:492800273211850767>'
        self.colour = [0x37749c, 0xd84eaf, 0x45b4de, 0x42f4c5, 0xffb5f3, 0x42eef4, 0xe751ff, 0x51ffad]
        if not hasattr(bot, 'lavalink') or not bot.lavalink:
            lavalink.Client(bot=bot, loop=self.bot.loop, log_level=logging.WARNING)
            # {}
            self.bot.lavalink.register_hook(self._track_hook)

    def __unload(self):
        self.bot.loop.create_task(self.bot.lavalink.players.safe_clear())
        self.bot.lavalink.unregister_hook(self._track_hook)
        self.bot.lavalink.destroy()
        self.bot.lavalink = None

    async def _track_hook(self, event):
        if not hasattr(event, 'player'):
            return
        if isinstance(event, lavalink.Events.TrackStartEvent):
            c = event.player.fetch('channel')
            if c:
                c = self.bot.get_channel(c)
                if c:
                    self.votes.clear()
                    req = self.bot.get_user(int(event.track.requester))
                    dur = lavalink.Utils.format_time(event.track.duration)
                    embed = discord.Embed(colour=rnd(self.colour), title='Now Playing..', description=f"[{event.track.title}]({event.track.uri})")
                    embed.add_field(name="Duration", value=f"`[{dur}]`")
                    embed.set_thumbnail(url=event.track.thumbnail)
                    embed.set_footer(text=f"Siri Music | Requested by {req.name}")
                    await c.send(embed=embed)


        elif isinstance(event, lavalink.Events.QueueEndEvent):
            if event.player.shuffle:
                event.player.shuffle = not event.player.shuffle
            ch = event.player.fetch('channel')
            if ch:
                ch = self.bot.get_channel(ch)
                if ch:
                    embed = discord.Embed(colour=rnd(self.colour), title="Queue has concluded!", description="The queue has **concluded**! Are you going to enqueue anything else?")
                    await ch.send(embed=embed)


    @commands.command()
    async def lyrics(self, ctx, *, query=None):
        try:
            embed = discord.Embed(description="Fetching lyrics..")
            msg = await ctx.send(embed=embed)
            if not query:
                player = await self.bot.lavalink.get_player(ctx.guild.id)
                if not player.is_playing:
                    await ctx.send(f"{self.tfals} Nothing is playing, so I couldn't get any lyrics. To search for a song that isn't playing, use `siri lyrics <song-title>`.")
                else:
                    title = player.current.title
                    q = title.replace(" ", "+")
                    r = requests.get(f"https://some-random-api.ml/lyrics?title={q}").json()
                    s = str(r['lyrics'])
                    if len(s) > 2040:
                        lyrics = f"Seems like these lyrics are too long to display! Click [here]({r['links']['genius']}) to get them.\n\n*Powered by SomeRandomAPI*"
                    else:
                        lyrics = f"{r['lyrics']}\n\n*Powered by SomeRandomAPI*"
                    embed = discord.Embed(colour=0xffff00, title=r['title'], description=lyrics, url=r['links']['genius'])
                    embed.set_footer(text="Genius", icon_url="https://trashbox.ru/files/427612_ad428e/yp31wbgn.png")
                    await msg.edit(embed=embed)

            else:
               q = query.replace(" ", "+")
               r = requests.get(f"https://some-random-api.ml/lyrics?title={q}").json()
               if len(r['lyrics']) > 2040:
                   lyrics = f"Seems like these lyrics are too long to display! Click [here]({r['links']['genius']}) to get them.\n\n*Powered by SomeRandomAPI*"
               else:
                   lyrics = f"{r['lyrics']}\n\n*Powered by SomeRandomAPI*"
               embed = discord.Embed(colour=0xffff00, title=r['title'], description=lyrics, url=r['links']['genius'])
               embed.set_footer(text="Genius", icon_url="https://trashbox.ru/files/427612_ad428e/yp31wbgn.png")
               await msg.edit(embed=embed)
        except:
            embed = discord.Embed(description=f"{self.tfals} Nothing found for this track!")
            await msg.edit(embed=embed)


    @commands.command(aliases=['p', 'add', 'enqueue'])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def play(self, ctx, *, query):
        """Play a track [url or query]"""
        player = await self.bot.lavalink.get_player(ctx.guild.id)

        if not player.is_connected:
            if not ctx.author.voice or not ctx.author.voice.channel:
                return await ctx.send(f"{self.tfals} Please join a voice channel first.")

            permissions = ctx.author.voice.channel.permissions_for(ctx.me)

            if not permissions.connect or not permissions.speak:
                return await ctx.send(f"{self.tfals} I am unable to connect to your voice channel! Do I have the correct permissions?")

            player.store('channel', ctx.channel.id)
            await player.connect(ctx.author.voice.channel.id)

        else:
            if not ctx.author.voice or not ctx.author.voice.channel or player.connected_channel.id != ctx.author.voice.channel.id:
                return await ctx.send(f"{self.tfals} You aren't in my voice channel, #**{ctx.me.voice.channel}**")

        query = query.strip('<>')

        if not url_rx.match(query):
            query = f'ytsearch:{query}'

        results = await self.bot.lavalink.get_tracks(query)

        try:
            tracks = len(results['tracks'][0])
        except:
            tracks = 1

        if not results or (isinstance(results, dict) and not results['tracks']):
            return await ctx.send(f"{self.tfals} There was nothing found for that song.")

        if tracks > 100:
            await ctx.send(f"{self.tfals} Playlists cannot exceed **100** tracks! Become a patron to add more.")
        else:
            trl = discord.Embed(colour=rnd(self.colour))

        if isinstance(results, dict):
            t = results['tracks']
            if results['loadType'] == 'PLAYLIST_LOADED':
                trl.description = f"{self.ttrue} **{results['playlistInfo']['name']}** enqueued. ({tracks} tracks)"
                await ctx.send(embed=trl)
                for track in t:
                    player.add(requester=ctx.author.id, track=track)
            else:
                trl.description = f"{self.ttrue} [{t['info']['title']}]({t['info']['uri']}) enqueued."
                await ctx.send(embed=trl)
                player.add(requester=ctx.author.id, track=t)


        if not player.is_playing:
            await player.play()

    @commands.command(aliases=['forceskip', 'fs'])
    @commands.cooldown(1, 2, commands.BucketType.user)
    async def skip(self, ctx):
        """Skip a song"""
        author = ctx.message.author
        player = await self.bot.lavalink.get_player(ctx.guild.id)

        if not player.is_playing:
            return await ctx.send(f"{self.tfals} I am not playing anything.")
        elif not ctx.author.voice or not ctx.author.voice.channel or player.connected_channel.id != ctx.author.voice.channel.id:
            return await ctx.send(f"{self.tfals} You aren't in my voice channel, #**{ctx.me.voice.channel}**")
        elif author.id == int(player.current.requester) or "DJ" in [x.name.upper() for x in ctx.author.roles] or ctx.author.guild_permissions.manage_guild:
            await ctx.send(f"{self.ttrue} Track **Skipped**.")
            await player.skip()
        elif author.id not in self.votes:
            self.votes.append(author.id)
            if len(self.votes) >= 3:
                await ctx.send(f"{self.ttrue} Vote passed, **Skipping** track...")
                await player.skip()
                await asyncio.sleep(1)
                self.votes.clear()
            else:
                await ctx.send(f"{self.ttrue} You have voted to **skip** the track, currently at `[{len(self.votes)}/3]` votes.")
        else:
            await ctx.send(f"{self.tfals} You can only vote to skip once.")


    @commands.command(aliases=['pv', 'last'])
    async def previous(self, ctx):
        """Plays the previous song."""
        player = await self.bot.lavalink.get_player(ctx.guild.id)

        try:
            await player.play_previous()
            await ctx.send(f"{self.ttrue} Done.")
        except lavalink.NoPreviousTrack:
            await ctx.send(f"{self.tfals} No previous song!")

    @commands.command(aliases=['bass'])
    async def bassboost(self, ctx, level=None):
        """
        Set bassboost level.
        0 - OFF
        1 - LOW
        2 - MEDIUM
        3 - HIGH
        """
        gains = None

        player = await self.bot.lavalink.get_player(ctx.guild.id)

        levels = {
                '0': [(0, 0), (1, 0)],
                '1': [(0, 0.25), (1, 0.15)],
                '2': [(0, 0.50), (1, 0.25)],
                '3': [(0, 0.75), (1, 0.50)]
                }

        _levels = ['0', '1', '2', '3']

        if not level in _levels:
            await ctx.send(f"{self.tfals} Invalid level! View `siri help cmd bassboost` to view valid levels.")
        elif not level:
            await ctx.send(f"{self.tfals} You haven't specified a level! View `siri help cmd bassboost` to view valid levels.")
        #elif not "DJ" in [x.name.upper() for x in ctx.author.roles] or ctx.author.guild_permissions.manage_guild or not ctx.author.id == 396153668820402197:
            #await ctx.send(f"{self.tfals} You need a role named `DJ` or `manage_server` permissions to use this command!")
        else:
            if not level == '0':
                cl = level
                msg = await ctx.send(f"You are about to set bassboost to **Level {level}**! Are you sure you want to do this? :warning:")

                def check(reaction, user):
                    return user == ctx.message.author and str(reaction.emoji) in ['✅','❌']
                await msg.add_reaction("✅")
                await msg.add_reaction("❌")
                await asyncio.sleep(0.5)
                reaction, user = await self.bot.wait_for('reaction_add', timeout=20.0, check=check)
                if reaction.emoji == '❌':
                    await ctx.send("I won't set bassboot, then.")
                if reaction.emoji == '✅':
                    for lvl in levels.keys():
                        if lvl.startswith(level):
                            gains = levels[lvl]
                            break
                    await player.set_gains(*gains)
                    await ctx.send(f"{self.ttrue} Bassboost set to **Level {cl}**! Do `siri bassboost 0` to turn it off.")
            else:
                await ctx.send(f"{self.ttrue} Bassboost off.")

    @commands.command(aliases=['clear'])
    async def stop(self, ctx):
        """Stop music and clear the queue"""
        player = await self.bot.lavalink.get_player(ctx.guild.id)

        if not player.is_playing:
            return await ctx.send(f"{self.tfals} I am not playing anything.")

        elif "DJ" in [x.name.upper() for x in ctx.author.roles] or ctx.author.guild_permissions.manage_guild or ctx.author.id == 396153668820402197:


            if player.repeat:
                player.repeat = not player.repeat
            if player.shuffle:
                player.shuffle = not player.shuffle
            player.queue.clear()
            self.votes.clear()
            await player.stop()
            embed = discord.Embed(colour=rnd(self.colour), title="Queue has concluded!", description="The queue has **concluded**! Are you going to enqueue anything else?")
            await ctx.send(embed=embed)

        else:
            await ctx.send("You need a role named `DJ` or `manage_server` permissions to use this command!")


    @commands.command(aliases=['leave'])
    async def disconnect(self, ctx):
        """Leave the current voice channel"""
        player = await self.bot.lavalink.get_player(ctx.guild.id)

        if not player.is_connected:
            return await ctx.send(f"{self.tfals} I'm not in a voice channel!")

        elif not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
            return await ctx.send(f"{self.tfals} You're not in #**{ctx.me.voice.channel}**!")

        elif "DJ" in [x.name.upper() for x in ctx.author.roles] or ctx.author.guild_permissions.manage_guild or ctx.author.id == 396153668820402197:

            player.queue.clear()
            await player.disconnect()
            await ctx.send(f"{self.ttrue} I have **disconnected**.")

        else:
            await ctx.send("You need a role named `DJ` or `manage_server` permissions to use this command!")

    @commands.command(aliases=['np', 'now'])
    async def nowplaying(self, ctx):
        """Get info on the current song"""

        player = await self.bot.lavalink.get_player(ctx.guild.id)
        song = "None"
        req = self.bot.get_user(int(player.current.requester))

        if not player.is_playing:
            return await ctx.send(f"{self.tfals} I am not playing anything.")

        if player.current:
            pos = lavalink.Utils.format_time(player.position)
            if player.current.stream:
                dur = 'LIVE'
            else:
                dur = lavalink.Utils.format_time(player.current.duration)
        #bar = await self.bar(volume=player.volume)

        def rcheck(reaction, user):
            return user == ctx.message.author and str(reaction.emoji) in ['⏹','⏭', '📖']

        embed = discord.Embed(colour=rnd(self.colour), title='Now Playing', description=f"[{player.current.title}]({player.current.uri})")
        embed.add_field(name="Duration", value=f"`[{pos} / {dur}]`")
        embed.add_field(name="Uploaded by", value=f"`{player.current.author}`")
        embed.add_field(name="Skip Requests", value=f"`[{len(self.votes)}/3]`")
        embed.add_field(name="Volume", value=f"`[{player.volume}]`")
        embed.add_field(name="Requested by", value=f"`{req.name}`")
        embed.set_thumbnail(url=player.current.thumbnail)
        msg = await ctx.send(embed=embed)
        book = await msg.add_reaction("📖")
        stop = await msg.add_reaction("⏹")
        skip = await msg.add_reaction("⏭")
        await asyncio.sleep(0.5)
        reaction, user = await self.bot.wait_for('reaction_add', timeout=60.0, check=rcheck)
        if reaction.emoji == '⏹':
            if "DJ" in [x.name.upper() for x in ctx.author.roles] or ctx.author.guild_permissions.manage_guild or ctx.author.id == 396153668820402197:


                if player.repeat:
                    player.repeat = not player.repeat
                if player.shuffle:
                    player.shuffle = not player.shuffle
                player.queue.clear()
                self.votes.clear()
                await player.stop()
                embed = discord.Embed(colour=rnd(self.colour), title="Queue has concluded!", description="The queue has **concluded**! Are you going to enqueue anything else?")
                await ctx.send(embed=embed)

            else:
                await ctx.send("You need a role named `DJ` or `manage_server` permissions to use this command!")

        elif reaction.emoji == '⏭':
            author = ctx.message.author
            if not player.is_playing:
                return await ctx.send(f"{self.tfals} I am not playing anything.")
            elif not ctx.author.voice or not ctx.author.voice.channel or player.connected_channel.id != ctx.author.voice.channel.id:
                return await ctx.send(f"{self.tfals} You aren't in my voice channel, #**{ctx.me.voice.channel}**")
            elif author.id == int(player.current.requester) or "DJ" in [x.name.upper() for x in ctx.author.roles] or ctx.author.guild_permissions.manage_guild:
                await ctx.send(f"{self.ttrue} Track **Skipped**.")
                await player.skip()
            elif author.id not in self.votes:
                self.votes.append(author.id)
                if len(self.votes) >= 3:
                    await ctx.send(f"{self.ttrue} Vote passed, **Skipping** track...")
                    await player.skip()
                    await asyncio.sleep(1)
                    self.votes.clear()
                else:
                    await ctx.send(f"{self.ttrue} You have voted to **skip** the track, currently at `[{len(self.votes)}/3]` votes.")
            else:
                await ctx.send(f"{self.tfals} You can only vote to skip once.")
        elif reaction.emoji == '📖':
            try:
                embed = discord.Embed(description="Fetching lyrics..")
                msg = await ctx.send(embed=embed)
                title = player.current.title
                q = title.replace(" ", "+")
                r = requests.get(f"https://some-random-api.ml/lyrics?title={q}").json()
                s = str(r['lyrics'])
                if len(s) > 2040:
                    lyrics = f"Seems like these lyrics are too long to display! Click [here]({r['links']['genius']}) to get them.\n\n*Powered by SomeRandomAPI*"
                else:
                    lyrics = f"{r['lyrics']}\n\n*Powered by SomeRandomAPI*"
                embed = discord.Embed(colour=0xffff00, title=r['title'], description=lyrics, url=r['links']['genius'])
                embed.set_footer(text="Genius", icon_url="https://trashbox.ru/files/427612_ad428e/yp31wbgn.png")
                await msg.edit(embed=embed)
            except Exception as e:
                embed = discord.Embed(description=f"{self.tfals} Nothing found for this track!")
                await msg.edit(embed=embed)
        else:
            pass

    @commands.command(aliases=['q'])
    async def queue(self, ctx, page: int=1):
        """Fetch the queue"""
        player = await self.bot.lavalink.get_player(ctx.guild.id)
        shuf = 'ON' if player.shuffle else 'OFF'
        n_dur = lavalink.Utils.format_time(player.current.duration)

        if not player.queue and player.is_playing:
            embed = discord.Embed(title=f"Queue:", colour=rnd(self.colour), description=f"**Now:** [{player.current.title}]({player.current.uri}) `{n_dur}`")
            embed.set_footer(text=f"Page 1 of 1 | Shuffle: {shuf}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)
        elif not player.queue:
            return await ctx.send("There's nothing left in the queue!")

        else:

            items_per_page = 11
            pages = math.ceil(len(player.queue) / items_per_page)

            start = (page - 1) * items_per_page
            end = start + items_per_page

            emoji = '- :repeat: \n' if player.repeat else '\n'

            qlist = ''

            q = len(player.queue)

            for i, track in enumerate(player.queue[start:end], start=start):
                if player.current.stream:
                    dur = 'LIVE'
                else:
                    dur = lavalink.Utils.format_time(track.duration)
                qlist += f'**{i + 1}:** [{track.title}]({track.uri}) `{dur}` {emoji}'

            embed = discord.Embed(title=f"Queue ({q}):", colour=rnd(self.colour), description=f"**Now:** [{player.current.title}]({player.current.uri}) `{n_dur}` {emoji}{qlist}")
            embed.set_footer(text=f"Page {page} of {pages} | Shuffle: {shuf}")
            embed.timestamp = datetime.datetime.utcnow()
            await ctx.send(embed=embed)

    @commands.command(aliases=['resume'])
    async def pause(self, ctx):
        """Pause|Resume Music"""
        player = await self.bot.lavalink.get_player(ctx.guild.id)

        if not player.is_playing:
            return await ctx.send(f"{self.tfals} I'm not playing anything!")

        if player.paused:
            await player.set_pause(False)
            await ctx.send(f"{self.ttrue} Track **Resumed**")
        else:
            await player.set_pause(True)
            await ctx.send(f"{self.ttrue} Track **Paused**")

    @commands.command(aliases=['vol'])
    async def volume(self, ctx, volume: int=None):
        """Check the volume, or set the volume"""
        player = await self.bot.lavalink.get_player(ctx.guild.id)

        if not player.is_playing:
            return await ctx.send(f"{self.tfals} I'm not playing anything!")

        if not volume:
            return await ctx.send(f'**Volume**: **{player.volume}**%')

        await player.set_volume(volume)
        await ctx.send(f"{self.ttrue} Volume set to **{player.volume}**%")

    @commands.command()
    async def shuffle(self, ctx):
        """Shuffle the queue"""
        player = await self.bot.lavalink.get_player(ctx.guild.id)

        if not player.is_playing:
            return await ctx.send(f"{self.tfals} I'm not playing anything!")

        player.shuffle = not player.shuffle

        await ctx.send(f"{self.ttrue} I have **{('enabled' if player.shuffle else 'disabled')}** shuffle.")

    @commands.command()
    async def repeat(self, ctx):
        """Repeats the queue"""
        player = await self.bot.lavalink.get_player(ctx.guild.id)

        if not player.is_playing:
            return await ctx.send(f"{self.tfals} I'm not playing anything!")

        player.repeat = not player.repeat

        await ctx.send(f"{self.ttrue} I have **{('enabled' if player.repeat else 'disabled')}** repeat.")

    @commands.command(aliases=['rm', 'pop'])
    async def remove(self, ctx, count: int):
        """Remove/pop a song from the queue"""
        player = await self.bot.lavalink.get_player(ctx.guild.id)

        if not player.queue:
            return await ctx.send(f"{self.tfals} There is nothing queued!")

        if count > len(player.queue) or count < 1:
            return await ctx.send(f"{self.tfals} Please choose a number that's in the queue!")

        if not "DJ" in [x.name.upper() for x in ctx.author.roles] or ctx.author.guild_permissions.manage_guild or not ctx.author.id == 396153668820402197:
            return await ctx.send(f"{self.tfals} You must have the `DJ` role or `MANAGE_SERVER` permissions to use this command! Use `siri dj` to get the role.")

        count -= 1
        removed = player.queue.pop(count)

        embed = discord.Embed(colour=rnd(self.colour), description=f"{self.ttrue} [{removed.title}]({removed.uri}) has been removed from the queue.")

        await ctx.send(embed=embed)

    @commands.command(aliases=['find', 'ms'])
    async def msearch(self, ctx, *, query):
        """Search for a track"""
        qu = query
        if not query.startswith('ytsearch:') and not query.startswith('scsearch:'):
            query = 'ytsearch:' + query

        results = await self.bot.lavalink.get_tracks(query)

        if not results or not results['tracks']:
            return await ctx.send(f"{self.tfals} I couldn't find anything!")

        tracks = results['tracks'][:10]

        data = ''
        for i, t in enumerate(tracks, start=0):
            data += f'**{i + 1}:** [{t["info"]["title"]}]({t["info"]["uri"]})\n'

        embed = discord.Embed(title=f"**Query:** {qu}", colour=rnd(self.colour), description=f"{data}\n\nRespond with the number that you want to play. To cancel, send **cancel**.")
        embed.set_footer(text=f'Requested by {ctx.message.author}')
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)

        def check(m):
            return m.author == ctx.message.author

        msg = await self.bot.wait_for('message', check=check, timeout=20)
        numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        if msg.content == 'cancel' or msg == 'Cancel' or msg == 'CANCEL':
            await ctx.send("Aborted.")
        elif int(msg.content) <= int(msg.content) + 1:
            query = results['tracks'][int(msg.content) - 1]['info']['uri']

            player = await self.bot.lavalink.get_player(ctx.guild.id)

            if not player.is_connected:
                if not ctx.author.voice or not ctx.author.voice.channel:
                    await ctx.send('Please join a voice channel first.')

                permissions = ctx.author.voice.channel.permissions_for(ctx.me)

                if not permissions.connect or not permissions.speak:
                    await ctx.send("I am unable to connect to your voice channel! Do I have the correct permissions?")

                player.store('channel', ctx.channel.id)
                await player.connect(ctx.author.voice.channel.id)
            else:
                if not ctx.author.voice or not ctx.author.voice.channel or player.connected_channel.id != ctx.author.voice.channel.id:
                    await ctx.send(f"You aren't in my voice channel, #**{ctx.me.voice.channel}**")

            if not url_rx.match(query):
                query = f'ytsearch:{query}'

            results = await self.bot.lavalink.get_tracks(query)

            if not results or not results['tracks']:
                await ctx.send('There was nothing found for that song.')

            trl = discord.Embed(colour=rnd(self.colour))

            if results['loadType'] == "PLAYLIST_LOADED":
                tracks = results['tracks']

                for track in tracks:
                    player.add(requester=ctx.author.id, track=track)

                trl.description = f"{self.ttrue} **{results['playlistInfo']['name']}** enqueued. ({tracks} tracks)"
                await ctx.send(embed=trl)
            else:
                t = results['tracks'][0]
                trl.description = f"{self.ttrue} [{t['info']['title']}]({t['info']['uri']}) enqueued."
                #trl.set_footer(text=f"Siri Music | Requested by {ctx.author.name}", icon_url="https://vignette.wikia.nocookie.net/logopedia/images/d/d0/Siri.png/revision/latest?cb=20170730135120")
                await ctx.send(embed=trl)
                player.add(requester=ctx.author.id, track=t)

            if not player.is_playing:
                await player.play()

        else:
            await ctx.send("That wasn't a valid number! Aborting..")


def setup(bot):
    bot.add_cog(Music(bot))
