import discord
import asyncio
import datetime
from discord.ext import commands
from random import choice as rnd
import config
import requests

class Server:
    def __init__(self, bot):
        self.bot = bot
        
    async def on_member_join(self, member):
        if member.guild.id == 493325581606453248:
            log = self.bot.get_channel(495840490147807235)
            embed = discord.Embed(colour=0x42f46b, description=f"Welcome to **Siri Support**, {member.mention}! Please review the rules in <#493326871594008576>, for support, <#493331059459489802> is the channel for you, the <@&493327873982332938> is ready to help!")
            embed.set_thumbnail(url=member.avatar_url_as(format='png'))
            embed.set_footer(text="Member Join", icon_url=member.guild.icon_url)
            embed.timestamp = datetime.datetime.utcnow()
            await log.send(embed=embed)
            #
            await member.send("Welcome to **Siri Support**, Please review the rules & info in <#493326871594008576>, for support, <#493331059459489802> is the channel for you, the Support Team is ready to help!")
        elif member.guild.id == 482922868410417163:
            log = self.bot.get_channel(482926662401654795)
            resp = ['derpy is qt', 'this server qt', 'am i qt boat?', 'mmlol', 'be good or bearcop', 'augu is best loli', 'sam good boye', 'FGHJKLKJHG', 'dm me qt', 'do u play osu i play osu r u good at osu i like osu i made osu skin my osu username is xosiri_qt123', 'ok cool idc bitch', 'are u interested in donating $5 to the Discord Bot Rights movement?', 'whats ur favourite anime i like spongebob', 'praise sam he giv good back rubs']
            await log.send(f"<a:welcomeglitch:498634744251285516> hi, **{member.name}**! {rnd(resp)}")  
    async def on_member_remove(self, member):
        if member.guild.id == 493325581606453248:
            quotes = ['So long, farewell, auf Wiedersehen, goodbye. I leave and heave a sigh and say goodbye.', 'Hasta la vista, baby', 'Good luck, we\'re all counting on you', 'You have been my friend. That in itself is a tremendous thing.', 'Never say goodbye because goodbye means going away and going away means forgetting', 'I make it easier for people to leave by making them hate me a little.', 'Agh.. finally.']
            log = self.bot.get_channel(495840490147807235)
            embed = discord.Embed(colour=0xf44141, description=f"Goodbye, **{member}**! {rnd(quotes)}")
            embed.set_thumbnail(url=member.avatar_url_as(format='png'))
            embed.set_footer(text="Member Leave", icon_url=member.guild.icon_url)
            embed.timestamp = datetime.datetime.utcnow()
            await log.send(embed=embed)
        elif member.guild.id == 482922868410417163:
            log = self.bot.get_channel(482926662401654795)
            resp = ['okay.. well. you\'re a nuisance anyways', 'i dont care what u have to say', 'finally u gone', 'u prob suck anyways', 'FGHJKLHGFDHG', 'ok cool idc bitchhhh', 'cu later hoe']
            await log.send(f"<:leave:498635244128305152> byebye, **{member.name}**! {rnd(resp)}")  
            
    async def on_message_edit(self, before, after):
        if before.guild.id == 493325581606453248 and not before.author.id == 481337766379126784:
            log = self.bot.get_channel(495861144871763969)
            embed = discord.Embed(colour=0xffff00)
            embed.add_field(name="Before", value=before.content)
            embed.add_field(name="After", value=after.content)
            embed.set_footer(text="Message Edit", icon_url=before.guild.icon_url_as(format='png')) 
            embed.timestamp = datetime.datetime.utcnow()
            await log.send(embed=embed, content=f":pencil: **{before.author}** has **edited** a message in **#{before.channel}**:")
            
    async def on_message_delete(self, message):
        if message.guild.id == 493325581606453248 and not message.author.id == 481337766379126784:
            log = self.bot.get_channel(495861144871763969)
            embed = discord.Embed(colour=0xff0000)
            embed.add_field(name="Content", value=message.content)
            embed.set_footer(text="Message Delete", icon_url=message.guild.icon_url_as(format='png')) 
            embed.timestamp = datetime.datetime.utcnow()
            await log.send(embed=embed, content=f":wastebasket: **{message.author}** has **removed** a message in **#{message.channel}**:")
            
    async def on_member_update(self, before, after):
        if before.guild.id == 493325581606453248:
            message = before
            log = self.bot.get_channel(495861144871763969)           
            embed = discord.Embed(colour=0x82b1ff)
            if not before.name == after.name:
                cnt = f":page_facing_up: **{before}** has changed their **username**:"
                embed.add_field(name="Before", value=before)
                embed.add_field(name="After", value=after)
                embed.set_footer(text="Username Edit", icon_url=message.guild.icon_url_as(format='png')) 
                embed.timestamp = datetime.datetime.utcnow()   
                await log.send(embed=embed, content=cnt)
            elif not before.nick == after.nick:
                cnt = f":name_badge: **{before}** has changed their **nickname**:"
                embed.add_field(name="Before", value=before.nick)
                embed.add_field(name="After", value=after.nick)
                embed.set_footer(text="Nickname Edit", icon_url=message.guild.icon_url_as(format='png')) 
                embed.timestamp = datetime.datetime.utcnow()
                await log.send(embed=embed, content=cnt)
            elif not before.roles == after.roles:
                cnt = f":ledger: **{before}** has got their **roles** updated:"
                embed.add_field(name="Before", value=" ".join([x.mention for x in before.roles]))
                embed.add_field(name="After", value=" ".join([x.mention for x in after.roles]))
                embed.set_footer(text="Role Update", icon_url=message.guild.icon_url_as(format='png')) 
                embed.timestamp = datetime.datetime.utcnow() 
                await log.send(embed=embed, content=cnt)
            else:
                pass
                              
            
    @commands.command(pass_context=True)
    async def kick(self, ctx, user: discord.Member= None, *, reason=None):
        author = ctx.message.author
        guild = ctx.message.guild
        if author.guild_permissions.kick_members:
            if reason is None:
                await guild.kick(user)
                await ctx.send(f"<:greentick:492800272834494474> **{user.name}** has been **kicked** by **{author.name}**!")
                try:
                    await user.send(f":boot: You have been **kicked** from **{ctx.guild}**! **Reason:** *N/A*")
                except:
                    pass
            else:
                await guild.kick(user, reason=f"\"{reason}\" - {author}")            
                await ctx.send(f"<:greentick:492800272834494474> **{user.name}** has been **kicked** by **{author.name}**! **Reason:** `{reason}`")
                try:
                    await user.send(f":boot: You have been **kicked** from **{ctx.guild}**! **Reason:** `{reason}`")
                except:
                    pass
        else:
            await ctx.send(f"<:redtick:492800273211850767> You're not a mod..")

    @commands.command(pass_context=True)
    async def ban(self, ctx, user: discord.Member= None, *, reason=None):
        author = ctx.message.author
        guild = ctx.message.guild
        if author.guild_permissions.ban_members:
            if reason is None:
                try:
                    await user.send(f":hammer_pick: You have been **banned** from **{ctx.guild}**! **There was no reason set for your ban**")
                except:
                    pass
                await guild.ban(user, reason=f"Ban by {ctx.author} [NO REASON]")
                await ctx.send(f"<:greentick:492800272834494474> **{user.name}** has been **banned** by **{ctx.message.author.name}**!")
            else:
                try:
                    await user.send(f":hammer_pick: You have been **banned** from **{ctx.guild}**! **Reason:** `{reason}`")
                except:
                    pass
                await guild.ban(user, reason=f"\"{reason}\" - Ban by {ctx.author}")
                await ctx.send(f"<:greentick:492800272834494474> **{user.name}** has been **banned** by **{ctx.message.author.name}**! **Reason:** `{reason}`")
        else:
            await ctx.send(f"<:redtick:492800273211850767> You're not a mod!")
            
    @commands.command(pass_context=True, aliases=['idban'])
    async def hackban(self, ctx, uid:int, *, reason=None):
        author = ctx.author
        guild = ctx.guild
        if author.guild_permissions.ban_members:
            if not reason:
                await self.bot.http.ban(user_id=uid, guild_id=guild.id, reason=f"[NO REASON] - ID-Ban by {ctx.author}")
                await ctx.send(f"<:greentick:492800272834494474> **Unknown User** has been **banned** by **{ctx.message.author.name}**!")
            else:
                await self.bot.http.ban(user_id=uid, guild_id=guild.id, reason=f"\"{reason}\" - ID-Ban by {ctx.author}")
                await ctx.send(f"<:greentick:492800272834494474> **Unknown User** has been **banned** by **{ctx.message.author.name}**! **Reason:** `{reason}`")
        else:
            await ctx.send(f"<:redtick:492800273211850767> You're not a mod!")

    @commands.command(pass_context=True)
    async def mute(self, ctx, user: discord.Member= None, amount:int=None):
        author = ctx.message.author
        guild = ctx.message.guild
        if author.guild_permissions.kick_members:
            role = discord.utils.get(ctx.guild.roles, name="Muted")
            await user.add_roles(role)
            
            if amount is None:
                await ctx.send(f"<:greentick:492800272834494474> **{user.name}** has been **muted** for **10 minutes**! (default time!)")
                try:
                    await user.send(f"You have been **muted** in **{ctx.guild}**! **Time:** `10 minutes (600 seconds)`")  
                except:
                    pass
                await asyncio.sleep(600)
                await user.remove_roles(role)
                try:
                    await user.send(f"You have been **unmuted** in **{ctx.guild}**!")
                except:
                    pass
            else:
                seconds = amount * 60
                await ctx.send(f"<:greentick:492800272834494474> **{user.name}** has been **muted** for **{amount} minute(s)**!")
                await user.send(f"You have been **muted** in **{ctx.guild}**! **Time:** `{amount} minute(s) ({seconds} seconds)`")
                try:
                    await asyncio.sleep(seconds)
                    await user.remove_roles(role)
                    try:
                        await user.send(f"You have been **unmuted** in **{ctx.guild}**!")
                    except:
                        pass
                except Exception as e:
                    await ctx.send(e)
        else:
            await ctx.send(f"<:redtick:492800273211850767> You're not a mod..")

    @commands.command(pass_context=True)
    async def unmute(self, ctx, user: discord.Member= None):
        author = ctx.message.author
        guild = ctx.message.guild
        if author.guild_permissions.kick_members:
            try:
                role = discord.utils.get(ctx.guild.roles, name="Muted")
                await ctx.send(f"<:greentick:492800272834494474> **{user.name}** has been unmuted!")
                await user.remove_roles(role)
                try:
                    await user.send(f"You have been **unmuted** in **{ctx.guild}**!")
                except:
                    pass
            except:
                await ctx.send(f"<:redtick:492800273211850767> **{user.name}** isn't muted!")
        else:
            await ctx.send(f"<:redtick:492800273211850767> You're not a mod..")
            
    @commands.command(aliases=['sr'])
    async def selfrole(self, ctx, opt, role: discord.Role):
        if ctx.guild.id == 493325581606453248:
            if opt == 'remove' or opt == 'r':
                if role.name == 'updates':
                    if not "updates" in [x.name for x in ctx.author.roles]:
                        await ctx.send("<:redtick:492800273211850767> I can't remove a role that you don't have!")
                    else:
                        await ctx.send(f"<:greentick:492800272834494474> Self-Role, **UPDATES**, has been successfully removed from **{ctx.author}**!")
                        await ctx.author.remove_roles(role)    
                        
                else:
                    await ctx.send(f"`{role}` isn't a self-role!")

            if opt == 'add' or opt == 'a':
                if role.name == 'updates':
                    await ctx.send(f"<:greentick:492800272834494474> Self-Role, **UPDATES**, has been successfully given to **{ctx.author}**!")
                    await ctx.author.add_roles(role)
                else:
                    await ctx.send(f"`{role}` isn't a self-role!")
        else:
            pass
        
    @commands.command(aliases=['rb'])
    async def reportbug(self, ctx, *, topic, option=None, description=None):
        """Bug Report Command (Siri Support Server Only)"""
        if ctx.guild.id == 493325581606453248:
            args = topic.split('|')
            topic = args[0]
            option = args[1]
            description = args[2]  
            if not description:
                await ctx.send(f"<:redtick:492800273211850767> {ctx.author.mention}, Incorrect Arguments. **Usage:** `siri bugreport <topic> <option> <description>` *Do not include < or > in your report.*", delete_after=10)
            
            data = {
                    "name": description, 
                    "desc": f'**Command/Topic:** {topic}\n**Description:** {description}\n**Submitted by:** {ctx.author} ({ctx.author.id})\n\nThis bug is **{str(option).upper()}**.',
                    "idList": 'User-Submitted Bugs',
                    "pos": 'top'
            }
            r = requests.get(f"https://api.trello.com/1/cards/xg637BcY?key={config.key}&token={config.token}", data=data)
            trello_link = None
            
            await ctx.message.delete()
            msg = await ctx.send(f"<:greentick:492800272834494474> {ctx.author.mention}, your report has been sent! Check it out in <#508462645163065362>. I have also sent a transcipt to your DMs.", delete_after=10)
            
            embed = discord.Embed(colour=0x00f0ff, description="Bug Report Transcript")
            embed.add_field(name="Topic/Command:", value=str(topic).capitalize())
            embed.add_field(name="Option:", value=str(option).capitalize())
            embed.add_field(name="Description:", value=description)
            embed.set_footer(text="Thank you for submitting a bug!")
            await ctx.author.send(embed=embed)
                                       
                             
        else:
            pass
def setup(bot):
  bot.add_cog(Server(bot))
