import discord
from discord.ext import commands

import dbl

import datetime

import time
from random import choice, randint
import subprocess
from discord.ext.commands import errors, converter
from random import choice as rnd

import aiohttp
import asyncio
import sys

if not discord.opus.is_loaded():
    # the 'opus' library here is opus.dll on windows
    # or libopus.so on linux in the current directory
    # you should replace this with the location the
    # opus library is located in and with the proper filename.
    # note that on windows this DLL is automatically provided for you
    discord.opus.load_opus('opus')


class VoiceEntry:
    def __init__(self, message, player):
        self.requester = message.author
        self.channel = message.channel.id
        self.player = player

    def __str__(self):
        fmt = 'and requested by {}'
        duration = self.player.duration
        if duration:
            fmt = fmt + ' [length: {0[0]}m {0[1]}s]'.format(divmod(duration, 60))
        return fmt.format(self.requester)



class VoiceState:
    def __init__(self, bot):
        self.current = None
        self.voice = None
        self.bot = bot
        self.play_next_song = asyncio.Event()
        self.songs = asyncio.Queue()
        self.skip_votes = set() # a set of user_ids that voted
        self.audio_player = self.bot.loop.create_task(self.audio_player_task())

    def is_playing(self):
        if self.voice is None or self.current is None:
            return False

        player = self.current.player
        return not player.is_done()

    @property
    def player(self):
        return self.current.player

    def skip(self):
        self.skip_votes.clear()
        if self.is_playing():
            self.player.stop()

    def toggle_next(self):
        self.bot.loop.call_soon_threadsafe(self.play_next_song.set)

    async def audio_player_task(self):
        while True:
            self.play_next_song.clear()
            self.current = await self.songs.get()
            next = discord.Embed(colour=0x36393E, description="Now playing **{}**!".format(str(self.current)))
            await self.bot.send_message(self.current.channel, embed=next)
            self.current.player.start()
            await self.play_next_song.wait()

class Music:
    def __init__(self, bot):
        self.bot = bot
        self.voice_states = {}
        self.queue = {}
        self.players = {}


    def get_voice_state(self, server):
        state = self.voice_states.get(server.id)
        if state is None:
            state = VoiceState(self.bot)
            self.voice_states[server.id] = state

        return state

    def check_queue(self, server):
        if self.queue[server] != []:
            player = self.queue[server].pop(0)
            self.players[server] = player
            
            p = player.start()
            return p
            #embed = discord.Embed(title="Now playing..", description=f"`{player.title}`")
            #await self.bot.say(embed=embed)

    def duration_to_str(dura, duration):
        minutes, seconds = divmod(duration, 60)
        hours, minutes = divmod(minutes, 60)
        days, hours = divmod(hours, 24)

        duration = []
        if days > 0: duration.append(f'{days}d')
        if hours > 0: duration.append(f'{hours}hrs')
        if minutes > 0: duration.append(f'{minutes}m')
        if seconds > 0 or len(duration) == 0: duration.append(f'{seconds}s')

        return ' '.join(duration)

    async def create_voice_client(self, channel):
        voice = await self.bot.join_voice_channel(channel)
        state = self.get_voice_state(channel.server)
        state.voice = voice

    def __unload(self):
        for state in self.voice_states.values():
            try:
                state.audio_player.cancel()
                if state.voice:
                    self.bot.loop.create_task(state.voice.disconnect())
            except:
                pass
    @commands.command(pass_context=True, no_pm=True)
    async def join(self, ctx):
        if ctx.message.author.bot: return

        author = ctx.message.author

        voice_channel = author.voice_channel

        try:
            await self.create_voice_client(voice_channel)
            je = discord.Embed(colour = 0x36393E, title='I have joined **' + voice_channel.name + '**!')
            await self.bot.say(embed=je)
        except discord.ClientException:
            await self.bot.say('<:x_:453601440167100416> **Uh.** Either you are not in a voice channel or I am already in a voice channel in this server..')
        else:
            pass

    @commands.command(pass_context=True, no_pm=True, aliases=['vol', 'v'])
    async def volume(self, ctx, value : int):
        server = ctx.message.server
        if ctx.message.author.bot: return

        state = self.get_voice_state(ctx.message.server)
        if state.voice is None:
            await self.bot.say("<:x_:453601440167100416> **Uh.** I don't think anything is playing..")

        elif value > 200:
            await self.bot.say("<:x_:453601440167100416> Volume cannot be higher than **200%**!")

        #try:
            #del self.voice_states[server.id]
            #player = state.player
            #player.volume = value / 100
            #await self.bot.say("<:toxh:449941181325901824> I have set the **volume** to `{:.0%}`".format(player.volume))
        #except:
            #pass
        else:
            player = state.player
            player.volume = value / 100
            await self.bot.say('<:toxh:449941181325901824> I have set the **volume** to **{:.0%}**'.format(player.volume))


    @commands.command(pass_context=True, no_pm=True)
    async def pause(self, ctx):
        if ctx.message.author.bot: return
        server = ctx.message.server
        state = self.get_voice_state(ctx.message.server)
        if state.voice is None:
            await self.bot.say("<:x_:453601440167100416> **Uh.** I don't think anything is playing..")

        #try:
            #del self.voice_states[server.id]
            #player = state.player
            #player.pause()
            #await self.bot.say("<:toxh:449941181325901824> I have **paused** the music!")
        #except:
            #pass
        else:
            player = state.player
            player.pause()
            await self.bot.say("<:toxh:449941181325901824> I have **paused** the player!")

    @commands.command(pass_context=True, no_pm=True)
    async def resume(self, ctx):
        if ctx.message.author.bot: return

        server = ctx.message.server

        state = self.get_voice_state(ctx.message.server)
        if state.voice is None:
            await self.bot.say("<:x_:453601440167100416> **Uh.** I don't think anything is playing..")
        #try:
            #del self.voice_states[server.id]
            #player = state.player
            #player.resume()
            #await self.bot.say("<:toxh:449941181325901824> I have **resumed** the music!")
        #except:
            #pass
        else:
            player = state.player
            player.resume()
            await self.bot.say("<:toxh:449941181325901824> I have **resumed** the player!")
            

    @commands.command(pass_context=True, no_pm=True)
    async def stop(self, ctx):
        if ctx.message.author.bot: return
        server = ctx.message.server
        state = self.get_voice_state(server)

        #if state.is_playing():
            #player = state.player
            #player.stop()
            #await self.bot.say("<:toxh:449941181325901824> I have **stopped** the music, bye!")

        try:
            state.audio_player.cancel()
            del self.voice_states[server.id]
            await state.voice.disconnect()
            await self.bot.say("<:toxh:449941181325901824> I have **stopped** the music, bye!")
        except:
            pass
        #else:
            #await self.bot.say("<:x_:453601440167100416> **Uh.** I don't think anything is playing..")

    @commands.command(pass_context=True, no_pm=True, aliases=['s'])
    async def skip(self, ctx):
        if ctx.message.author.bot: return

        state = self.get_voice_state(ctx.message.server)
        if state.voice is None:
            await self.bot.say('**Uh.** Not playing any music right now...')
            return

        voter = ctx.message.author
        if voter == state.current.requester:
            await self.bot.say('<:toxh:449941181325901824> Song **skipped**...')
            state.skip()
        elif voter.id not in state.skip_votes:
            state.skip_votes.add(voter.id)
            total_votes = len(state.skip_votes)
            if total_votes >= 3:
                await self.bot.say('<:toxh:449941181325901824> Vote passed, **skipping** song...')
                state.skip()
            else:
                await self.bot.say('You have voted to **skip** the song, currently at `{}/3` votes.'.format(total_votes))
        else:
            await self.bot.say('You can only vote to skip **once**.')

    @commands.command(pass_context=True, no_pm=True, aliases=['np'])
    async def playing(self, ctx):
        if ctx.message.author.bot: return


        state = self.get_voice_state(ctx.message.server)
        player = state.player
        if state.voice is None:

            await self.bot.say('Nothing is playing.. Start with `yt <yt-video-or-link>`')
        else:
            skip_count = len(state.skip_votes)
            trl = discord.Embed(description=f"```\"{player.title}\" uploaded by {player.uploader} {state.current}```")
            trl.add_field(name="**Skip Requests**", value=f"`{skip_count}`")
            trl.add_field(name="**...**", value="👍 `{}` 👎 `{}`\n\n".format(player.views, player.likes, player.dislikes))
            trl.set_author(name="Siri Music", icon_url="https://vignette.wikia.nocookie.net/logopedia/images/d/d0/Siri.png/revision/latest?cb=20170730135120")
            await self.bot.say(embed=trl)

    @commands.command(pass_context=True)
    async def checkq(self, ctx):
        await self.bot.say(f"`{self.queue}`")

    @commands.command(pass_context=True, no_pm=True, aliases=['q'])
    async def queue(self, ctx):
        try:
            q = "**,** ".join(self.queue)
            embed = discord.Embed(description=f"{self.queue}")
            await self.bot.say(embed=embed, content=f"**{ctx.message.server}**'s Queue..")
        except:
            await self.bot.say("Queue is **empty**.. Queue up some songs with `siri yt <yt-video>`!")

    @commands.command(pass_context=True, aliases=['addq'])
    async def addqueue(self, ctx, *, video):
        server = ctx.message.server
        state = self.get_voice_state(server)
        opts = {
            'default_search': 'auto',
            'quiet': True,
        }
        player = await state.voice.create_ytdl_player(video, ytdl_options=opts, after=lambda: self.check_queue(server.id))
        self.players[id] = player
        if server.id in self.queue:
            self.queue[server.id].append(player.url)
        else:
            self.queue[server.id] = [player.url]
        await self.bot.say(f"<:toxh:449941181325901824> `{player.title}` **added** to queue.")

    @commands.command(pass_context=True, aliases=['youtube', 'p', 'play'])
    async def yt(self, ctx, *, url):
        if ctx.message.author.bot: return

        message = ctx.message
        author = ctx.message.author
        channel = ctx.message.channel
        server = ctx.message.server

        state = self.get_voice_state(server)
        opts = {
            'default_search': 'auto',
            'quiet': True,
        }
        try:

            if state.voice is None:
                await self.bot.say("It seems like I am not in a voice channel.. Summon me with `siri join`!")

            else:
            
            #elif not fplayer.is_done():
                #msg = await self.bot.say("<:yt:466282995049955358> :mag: Getting **{}** from **YouTube**..".format(url))
                #next_song = []
                #next_song.append(url)
                #await asyncio.sleep(2)
                #await self.bot.edit_message(f"<:yt:466282995049955358> `{player.title}` will be played after this song is over..")
                    try:                    
                        msg = await self.bot.say("<:yt:466282995049955358> :mag: Fetching **\"{}\"** from **YouTube**..".format(url))
                        player = await state.voice.create_ytdl_player(url, ytdl_options=opts, after=lambda: self.check_queue(server.id))
                        nt = player.duration / 60
                        dur = player.duration
                        du = self.duration_to_str(dur)
                        trl = discord.Embed(description=f"**{player.title}** added.")
                        trl.set_thumbnail(url="https://i.pinimg.com/originals/ae/7e/0d/ae7e0d3782d2eb6a62c631e03d828d2b.png")
                        trl.add_field(name="**Duration**", value=f"`{du}`" )
                        trl.add_field(name="**Uploaded by**", value=f"`{player.uploader}`")
                        trl.add_field(name="**...**", value="👍 `{}` 👎 `{}`\n\n".format(player.views, player.likes, player.dislikes))
                        trl.set_author(name="Siri Music", icon_url="https://vignette.wikia.nocookie.net/logopedia/images/d/d0/Siri.png/revision/latest?cb=20170730135120")

                        await self.bot.delete_message(msg)
                        player.volume = 0.6
                        entry = VoiceEntry(ctx.message, player)
                        await state.songs.put(entry)
                        await self.bot.add_reaction(message, "▶")
                        await self.bot.say(embed=trl)

                        player.start()
                        while not player.is_done():
                            await asyncio.sleep(2)
                        for x in self.bot.voice_clients:
                            if(x.server == ctx.message.server):
                                server = ctx.message.server
                                await self.bot.say(f"Song `{player.title}` has ended.")
                                self.check_queue(server.id)
                                print(':-')

                                    #player = await state.voice.create_ytdl_player(next_song, ytdl_options=opts, after=state.toggle_next)
                                    #n_t = player.duration / 60
                                    #trl = discord.Embed(description=f"**{player.title}** added.")
                                    #trl.set_thumbnail(url="https://i.pinimg.com/originals/ae/7e/0d/ae7e0d3782d2eb6a62c631e03d828d2b.png")
                                    #trl.add_field(name="**Duration**", value=f"`{n_t}min`")
                                    #trl.add_field(name="**Uploaded by**", value=f"`{player.uploader}`")
                                    #trl.add_field(name="**...**", value="👍 `{}` 👎 `{}`\n\n".format(player.views, player.likes, player.dislikes))
                                    #trl.set_author(name="Siri Music", icon_url="https://vignette.wikia.nocookie.net/logopedia/images/d/d0/Siri.png/revision/latest?cb=20170730135120")

                                    #await self.bot.delete_message(msg)
                                    #await self.bot.say(embed=trl)

                                    #player.start()


                    except Exception as e:
                        await asyncio.sleep(2)
                        fmt = '```py\n{}: {}\n```'
                        fmt2 = '\n\nERROR IN MUSIC.PY (cmd. yt):\n{}: {}\n\n'
                        embed = discord.Embed(title="<:x_:453601440167100416> **An error occurred while processing your request**", color=0xff0000, description=fmt.format(type(e).__name__, e))
                        await self.bot.send_message(ctx.message.channel, embed=embed)
                        print(fmt2.format(type(e).__name__, e))

        except:
            fmt = '```py\n{}: {}\n```'
            fmt2 = '\n\nERROR IN MUSIC.PY (cmd. yt):\n{}: {}\n\n'
            embed = discord.Embed(title="<:x_:453601440167100416> **An error occurred while processing your request**", color=0xff0000, description=fmt.format(type(e).__name__, e))
            await self.bot.send_message(ctx.message.channel, embed=embed)
            print(fmt2.format(type(e).__name__, e))


def setup(bot):
    bot.add_cog(Music(bot))