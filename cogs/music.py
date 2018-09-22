import discord
import lavalink
from discord.ext import commands
import datetime
import requests
import logging
import math
import re

from random import choice as rnd

time_rx = re.compile('[0-9]+')
url_rx = re.compile('https?:\/\/(?:www\.)?.+')

class Music:
    def __init__(self, bot):
        self.bot = bot
        self.colour = [0x37749c, 0xd84eaf, 0x45b4de, 0x42f4c5, 0xffb5f3, 0x42eef4, 0xe751ff, 0x51ffad]
        if not hasattr(bot, 'lavalink'):
            #stuffs here
            self.bot.lavalink.register_hook(self.track_hook)

    async def track_hook(self, event):
        if isinstance(event, lavalink.Events.TrackStartEvent):
            c = event.player.fetch('channel')
            if c:
                c = self.bot.get_channel(c)
                if c:
                    dur = lavalink.Utils.format_time(event.track.duration)
                    embed = discord.Embed(colour=rnd(self.colour), title='Now Playing..', description=f"[{event.track.title}]({event.track.uri})")
                    embed.add_field(name="Duration", value=f"`[{dur}]`")
                    embed.set_thumbnail(url=event.track.thumbnail)
                    await c.send(embed=embed)
                    
        elif isinstance(event, lavalink.Events.QueueEndEvent):
            ch = event.player.fetch('channel')
            if ch:
                ch = self.bot.get_channel(ch)
                if ch:
                    embed = discord.Embed(colour=rnd(self.colour), title="Queue has concluded!", description="The queue has **concluded**! Are you going to enqueue anything else?")
                    await ch.send(embed=embed)


    @commands.command(aliases=['p'])
    async def play(self, ctx, *, query):
        player = self.bot.lavalink.players.get(ctx.guild.id)

        if not player.is_connected:
            if not ctx.author.voice or not ctx.author.voice.channel:
                return await ctx.send('Please join a voice channel first.')

            permissions = ctx.author.voice.channel.permissions_for(ctx.me)

            if not permissions.connect or not permissions.speak:
                return await ctx.send("I am unable to connect to your voice channel! Do I have the correct permissions?")

            player.store('channel', ctx.channel.id)
            await player.connect(ctx.author.voice.channel.id)
        else:
            if not ctx.author.voice or not ctx.author.voice.channel or player.connected_channel.id != ctx.author.voice.channel.id:
                return await ctx.send(f"You aren't in my voice channel, #**{ctx.me.voice.channel}**")

        query = query.strip('<>')

        if not url_rx.match(query):
            query = f'ytsearch:{query}'

        results = await self.bot.lavalink.get_tracks(query)

        if not results or not results['tracks']:
            return await ctx.send('There was nothing found for that song.')

        trl = discord.Embed(colour=rnd(self.colour))

        if results['loadType'] == "PLAYLIST_LOADED":
            tracks = results['tracks']

            for track in tracks:
                player.add(requester=ctx.author.id, track=track)


            t = results['tracks'][0]
            trl.description = f"Playlist, **{results['playlistInfo']['name']}** enqueued. ({len(tracks)} tracks)"
            trl.set_footer(text=f"Siri Music | Requested by {ctx.author.name}", icon_url="https://vignette.wikia.nocookie.net/logopedia/images/d/d0/Siri.png/revision/latest?cb=20170730135120")
            await ctx.send(embed=trl)
            player.add(requester=ctx.author.id, track=t)
        else:
            t = results['tracks'][0]
            trl.description = f"[{t['info']['title']}]({t['info']['uri']}) enqueued."
            #trl.set_thumbnail(url=player.thumbnail)
            trl.set_footer(text=f"Siri Music | Requested by {ctx.author.name}", icon_url="https://vignette.wikia.nocookie.net/logopedia/images/d/d0/Siri.png/revision/latest?cb=20170730135120")
            await ctx.send(embed=trl)
            player.add(requester=ctx.author.id, track=t)

        if not player.is_playing:
            await player.play()

    @commands.command(aliases=['forceskip', 'fs'])
    async def skip(self, ctx):
        player = self.bot.lavalink.players.get(ctx.guild.id)

        if not player.is_playing:
            return await ctx.send("I am not playing anything.")

        await ctx.send("Track **Skipped**.")
        await player.skip()

    @commands.command(aliases=['clear'])
    async def stop(self, ctx):
        player = self.bot.lavalink.players.get(ctx.guild.id)

        if not player.is_playing:
            return await ctx.send("I am not playing anything.")

        player.queue.clear()
        await player.stop()
        embed = discord.Embed(colour=rnd(self.colour), title="Queue has concluded!", description="The queue has **concluded**! Are you going to enqueue anything else?")
        await ctx.send(embed=embed)

    @commands.command(aliases=['np', 'n', 'now'])
    async def nowplaying(self, ctx):
        player = self.bot.lavalink.players.get(ctx.guild.id)
        song = "None"

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
        embed.add_field(name="Volume", value=f"`[{player.volume}]`")
        embed.set_thumbnail(url=player.current.thumbnail)
        await ctx.send(embed=embed)

    @commands.command(aliases=['q'])
    async def queue(self, ctx, page: int=1):
        player = self.bot.lavalink.players.get(ctx.guild.id)

        if not player.queue:
            return await ctx.send("There's nothing left in the queue!")

        items_per_page = 10
        pages = math.ceil(len(player.queue) / items_per_page)

        start = (page - 1) * items_per_page
        end = start + items_per_page

        qlist = ''

        n_dur = lavalink.Utils.format_time(player.current.duration)

        q = len(player.queue)

        shuf = 'ON' if player.shuffle else 'OFF'

        if player.current.stream:
            dur = 'LIVE'
        else:
            dur = lavalink.Utils.format_time(track.duration)

        
        for i, track in enumerate(player.queue[start:end], start=start):
            qlist += f'**{i + 1}:** [{track.title}]({track.uri}) `{dur}`\n'

        embed = discord.Embed(title=f"Queue ({q})", colour=rnd(self.colour), description=f"**Now:** [{player.current.title}]({player.current.uri}) `{n_dur}`\n{qlist}")
        embed.set_footer(text=f"Page {page} of {pages} | Shuffle: {shuf}")
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)

    @commands.command(aliases=['resume'])
    async def pause(self, ctx):
        player = self.bot.lavalink.players.get(ctx.guild.id)

        if not player.is_playing:
            return await ctx.send("I'm not playing anything!")

        if player.paused:
            await player.set_pause(False)
            await ctx.send('Track **Resumed**')
        else:
            await player.set_pause(True)
            await ctx.send('Track **Paused**')

    @commands.command(aliases=['vol'])
    async def volume(self, ctx, volume: int=None):
        player = self.bot.lavalink.players.get(ctx.guild.id)

        if not volume:
            return await ctx.send(f'**V**olume**:** {player.volume}%')

        await player.set_volume(volume)
        await ctx.send(f'Volume set to **{player.volume}**%')

    @commands.command()
    async def shuffle(self, ctx):
        player = self.bot.lavalink.players.get(ctx.guild.id)

        if not player.is_playing:
            return await ctx.send('There is nothing playing!')

        player.shuffle = not player.shuffle

        await ctx.send('I have **' + ('enabled' if player.shuffle else 'disabled') + '** shuffle.')


    @commands.command(aliases=['rm'])
    async def remove(self, ctx, count: int):
        player = self.bot.lavalink.players.get(ctx.guild.id)

        if not player.queue:
            return await ctx.send("There is nothing queued.")

        if count > len(player.queue) or count < 1:
            return await ctx.send("Please choose a number that's actually in the queue.")

        count -= 1
        removed = player.queue.pop(count)

        embed = discord.Embed(colour=rnd(self.colour), description=f"[{removed.title}]({removed.uri}) has been removed from the queue.")

        await ctx.send(embed=embed)

    @commands.command(aliases=['find', 'f'])
    async def search(self, ctx, *, query):

        queryw = query

        if not query.startswith('ytsearch:') and not query.startswith('scsearch:'):
            query = 'ytsearch:' + query

        results = await self.bot.lavalink.get_tracks(query)

        if not results or not results['tracks']:
            return await ctx.send("I couldn't find anything!")

        tracks = results['tracks'][:10]

        data = ''
        for i, t in enumerate(tracks, start=0):
            data += f'**{i + 1}:** [{t["info"]["title"]}]({t["info"]["uri"]})\n'

        embed = discord.Embed(title=f"**Query:** {queryw}", colour=rnd(self.colour), description=f"{data}\n\nRespond with the number that you want to play. To cancel, send **cancel**.")
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
            await ctx.send(t['info'])
                
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


    @commands.command(aliases=['leave'])
    async def disconnect(self, ctx):
        player = self.bot.lavalink.players.get(ctx.guild.id)

        if not player.is_connected:
            return await ctx.send('Not connected.')

        if not ctx.author.voice or (player.is_connected and ctx.author.voice.channel.id != int(player.channel_id)):
            return await ctx.send('You\'re not in my voicechannel!')

        player.queue.clear()
        await player.disconnect()
        await ctx.send('I have **disconnected**.')


def setup(bot):
    bot.add_cog(Music(bot))
