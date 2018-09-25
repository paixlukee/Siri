import discord
import lavalink
from discord.ext import commands
import datetime
import requests
import logging
import math
import re
from random import choice as rnd
try:
    from lyricsmaster import *
except:
    print('die')

time_rx = re.compile('[0-9]+')
url_rx = re.compile('https?:\/\/(?:www\.)?.+')

class Music:
    def __init__(self, bot):
        self.bot = bot
        self.votes = []
        self.ttrue = '<:greentick:492800272834494474>'
        self.tfals = '<:redtick:492800273211850767>'
        self.colour = [0x37749c, 0xd84eaf, 0x45b4de, 0x42f4c5, 0xffb5f3, 0x42eef4, 0xe751ff, 0x51ffad]
        if not hasattr(bot, 'lavalink'):
            # stuffs here
            self.bot.lavalink.register_hook(self.track_hook)

    async def track_hook(self, event):
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
    async def lyrics(self, ctx, *, query):
        provider = Genius()
        song = provider.get_lyrics(song=query)
        embed = discord.Embed(colour=rnd(self.colour), title=f"Lyrics for {song.title}:", description=song.lyrics)
        await ctx.send(embed=embed)
                    
                   
    @commands.command(aliases=['p'])
    async def play(self, ctx, *, query):
        """Play a track [url or query]"""
        player = self.bot.lavalink.players.get(ctx.guild.id)

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

        if not results or not results['tracks']:
            return await ctx.send(f"{self.tfals} There was nothing found for that song.")
        

        trl = discord.Embed(colour=rnd(self.colour))

        if results['loadType'] == "PLAYLIST_LOADED":
            tracks = results['tracks']

            for track in tracks:
                player.add(requester=ctx.author.id, track=track)


            t = results['tracks'][0]
            trl.description = f"{self.ttrue} Playlist, **{results['playlistInfo']['name']}** enqueued. ({len(tracks)} tracks)"
            #trl.set_footer(text=f"Siri Music | Requested by {ctx.author.name}", icon_url="https://vignette.wikia.nocookie.net/logopedia/images/d/d0/Siri.png/revision/latest?cb=20170730135120")
            await ctx.send(embed=trl)
            player.add(requester=ctx.author.id, track=t)
        else:
            t = results['tracks'][0]
            trl.description = f"{self.ttrue} [{t['info']['title']}]({t['info']['uri']}) enqueued."
            await ctx.send(embed=trl)
            player.add(requester=ctx.author.id, track=t)

        if not player.is_playing:
            await player.play()

    @commands.command(aliases=['forceskip', 'fs'])
    async def skip(self, ctx):
        """Skip a song"""
        #members = ctx.author.voice_channel.voice_members
        author = ctx.message.author
        player = self.bot.lavalink.players.get(ctx.guild.id)

        if not player.is_playing:
            return await ctx.send(f"{self.tfals} I am not playing anything.")   
        elif not ctx.author.voice or not ctx.author.voice.channel or player.connected_channel.id != ctx.author.voice.channel.id:
            return await ctx.send(f"{self.tfals} You aren't in my voice channel, #**{ctx.me.voice.channel}**")
        elif author.id == int(player.current.requester):
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

    @commands.command(aliases=['clear'])
    async def stop(self, ctx):
        """Stop music and clear the queue"""
        player = self.bot.lavalink.players.get(ctx.guild.id)
            
        if not player.is_playing:
            return await ctx.send(f"{self.tfals} I am not playing anything.")
        
        elif "DJ" in [x.name.upper() for x in ctx.author.roles] or ctx.author.guild_permissions.manage_guild or ctx.author.id = 396153668820402197:
        
        
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
        player = self.bot.lavalink.players.get(ctx.guild.id)

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

    @commands.command(aliases=['np', 'n', 'now'])
    async def nowplaying(self, ctx):
        """Get info on the current song"""
        
        player = self.bot.lavalink.players.get(ctx.guild.id)
        song = "None"
        req = self.bot.get_user(int(player.current.requester))

        if player.current:
            pos = lavalink.Utils.format_time(player.position)
            if player.current.stream:
                dur = 'LIVE'
            else:
                dur = lavalink.Utils.format_time(player.current.duration)
        #bar = await self.bar(volume=player.volume)
        embed = discord.Embed(colour=rnd(self.colour), title='Now Playing', description=f"[{player.current.title}]({player.current.uri})")
        embed.add_field(name="Duration", value=f"`[{pos} / {dur}]`")
        embed.add_field(name="Uploaded by", value=f"`{player.current.author}`")
        embed.add_field(name="Skip Requests", value=f"`[{len(self.votes)}/3]`")
        embed.add_field(name="Volume", value=f"`[{player.volume}]`")
        embed.add_field(name="Requested by", value=f"`{req.name}`")
        embed.set_thumbnail(url=player.current.thumbnail)
        await ctx.send(embed=embed)

    @commands.command(aliases=['q'])
    async def queue(self, ctx, page: int=1):
        """Fetch the queue"""
        player = self.bot.lavalink.players.get(ctx.guild.id)

        if not player.queue:
            return await ctx.send("There's nothing left in the queue!")

        items_per_page = 10
        pages = math.ceil(len(player.queue) / items_per_page)

        start = (page - 1) * items_per_page
        end = start + items_per_page
        
        emoji = '- :repeat: \n' if player.repeat else '\n'

        qlist = ''

        n_dur = lavalink.Utils.format_time(player.current.duration)

        q = len(player.queue)

        shuf = 'ON' if player.shuffle else 'OFF'

        
        for i, track in enumerate(player.queue[start:end], start=start):
            if player.current.stream:
                dur = 'LIVE'
            else:
                dur = lavalink.Utils.format_time(track.duration)
            qlist += f'**{i + 1}:** [{track.title}]({track.uri}) `{dur}` {emoji}\n'

        embed = discord.Embed(title=f"Queue ({q})", colour=rnd(self.colour), description=f"**Now:** [{player.current.title}]({player.current.uri}) `{n_dur}` {emoji}{qlist}")
        embed.set_footer(text=f"Page {page} of {pages} | Shuffle: {shuf}")
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)

    @commands.command(aliases=['resume'])
    async def pause(self, ctx):
        """Pause|Resume Music"""
        player = self.bot.lavalink.players.get(ctx.guild.id)

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
        player = self.bot.lavalink.players.get(ctx.guild.id)
        
        if not player.is_playing:
            return await ctx.send(f"{self.tfals} I'm not playing anything!")

        if not volume:
            return await ctx.send(f'**Volume**: **{player.volume}**%')

        await player.set_volume(volume)
        await ctx.send(f"{self.ttrue} Volume set to **{player.volume}**%")

    @commands.command()
    async def shuffle(self, ctx):
        """Shuffle the queue"""
        player = self.bot.lavalink.players.get(ctx.guild.id)

        if not player.is_playing:
            return await ctx.send(f"{self.tfals} I'm not playing anything!")

        player.shuffle = not player.shuffle

        await ctx.send(f"{self.ttrue} I have **{('enabled' if player.shuffle else 'disabled')}** shuffle.")
                       
    @commands.command()
    async def repeat(self, ctx):
        """Repeats the queue"""
        player = self.bot.lavalink.players.get(ctx.guild.id)

        if not player.is_playing:
            return await ctx.send(f"{self.tfals} I'm not playing anything!")

        player.repeat = not player.repeat

        await ctx.send(f"{self.ttrue} I have **{('enabled' if player.repeat else 'disabled')}** repeat.")


    @commands.command(aliases=['rm', 'pop'])
    async def remove(self, ctx, count: int):
        """Remove/pop a song from the queue"""
        player = self.bot.lavalink.players.get(ctx.guild.id)

        if not player.queue:
            return await ctx.send(f"{self.tfals} There is nothing queued!")

        if count > len(player.queue) or count < 1:
            return await ctx.send(f"{self.ttrue} Please choose a number that's in the queue!")

        count -= 1
        removed = player.queue.pop(count)

        embed = discord.Embed(colour=rnd(self.colour), description=f"{self.ttrue} [{removed.title}]({removed.uri}) has been removed from the queue.")

        await ctx.send(embed=embed)

    @commands.command(aliases=['find', 'f'])
    async def msearch(self, ctx, *, query):
        """Search for a track"""

        if not query.startswith('ytsearch:') and not query.startswith('scsearch:'):
            query = 'ytsearch:' + query

        results = await self.bot.lavalink.get_tracks(query)

        if not results or not results['tracks']:
            return await ctx.send(f"{self.tfals} I couldn't find anything!")

        tracks = results['tracks'][:10]

        data = ''
        for i, t in enumerate(tracks, start=0):
            data += f'**{i + 1}:** [{t["info"]["title"]}]({t["info"]["uri"]})\n'

        embed = discord.Embed(title=f"**Query:** {query}", colour=rnd(self.colour), description=f"{data}\n\nRespond with the number that you want to play. To cancel, send **cancel**.")
        embed.set_footer(text=f'Requested by {ctx.message.author}')
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)

        def check(m):
            return m.author == ctx.message.author

        msg = await self.bot.wait_for('message', check=check, timeout=20)
        numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        if msg.content == 'cancel' or msg == 'Cancel' or msg == 'CANCEL':
            await ctx.send("Aborted.")
        elif msg.content in numbers:
            query = t['info']['uri']
            #await ctx.send(t['info'])
                
            player = self.bot.lavalink.players.get(ctx.guild.id)

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

            #query = query.strip('<>')

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

                trl.title = "Playlist added to queue!"
                trl.description = f"{results['playlistInfo']['name']} - {len(tracks)} tracks!"
                await ctx.send(embed=trl)
            else:
                t = results['tracks'][0]
                trl.description = f"[{t['info']['title']}]({t['info']['uri']}) enqueued."
                #trl.set_thumbnail(url=player.thumbnail)
                trl.set_footer(text=f"Siri Music | Requested by {ctx.author.name}", icon_url="https://vignette.wikia.nocookie.net/logopedia/images/d/d0/Siri.png/revision/latest?cb=20170730135120")
                await ctx.send(embed=trl)
                player.add(requester=ctx.author.id, track=t)

            if not player.is_playing:
                await player.play()

        else:
            await ctx.send("Please respond with the number! `['cancel' to abort]`")


def setup(bot):
    bot.add_cog(Music(bot))
