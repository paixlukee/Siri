import discord
import asyncio
import datetime
from discord.ext import commands
from random import choice as rnd
from random import randint
import random
import config
import requests

class Server:
    def __init__(self, bot):
        self.bot = bot
        
    async def on_message(self, message):
        if message.channel.id == 494480470839525378 and not message.author.id == 481337766379126784:
            await asyncio.sleep(0.5)
            await message.delete()
            
    async def on_member_join(self, member):
        if member.guild.id == 493325581606453248:
            await member.add_roles(discord.utils.get(member.guild.roles, name="Member"))
            log = self.bot.get_channel(495840490147807235)
            mutual = "`, `".join([x.name for x in self.bot.guilds if member in x.members])
            embed = discord.Embed(colour=0x42f46b, description=f"Welcome to **Siri Support**, {member.mention}! Please review the rules in <#493326871594008576>, for support, <#493331059459489802> is the channel for you, the <@&493327873982332938> is ready to help!\n\n**Mutual Guilds**: `{mutual}`")
            embed.set_thumbnail(url=member.avatar_url_as(format='png'))
            embed.set_footer(text="Member Join", icon_url=member.guild.icon_url)
            embed.timestamp = datetime.datetime.utcnow()
            await log.send(embed=embed)
            #
            await member.send("Welcome to **Siri Support**, Please review the rules & info in <#493326871594008576>, for support, <#493331059459489802> is the channel for you, the Support Team is ready to help!")
        elif member.guild.id == 433339597188104192:
            await member.send('Hello! Welcome to the Nest guild. Please fill out the required information in <#458437461119598593>. If you have any questions or concerns, DM an Admin.')
            await self.bot.get_channel(472471188170604544).send(f'<@&464126145898479646>, A member ({member.mention}) has joined the server. Please approve them with `siri apv @{member.name}` after they fill out the required information in <#458437461119598593>. To deny them, do `siri dny @{member.name} REASON`.')
        elif member.guild.id == 482922868410417163:
            log = self.bot.get_channel(482926662401654795)
            resp = ['derpy is qt', 'this server qt', 'am i qt boat?', 'mmlol', 'be good or bearcop', 'augu is best loli', 'sam good boye', 'FGHJKLKJHG', 'dm me qt', 'do u play osu i play osu r u good at osu i like osu i made osu skin my osu username is xosiri_qt123', 'ok cool idc bitch', 'are u interested in donating $5 to the Discord Bot Rights movement?', 'whats ur favourite anime i like spongebob', 'praise sam he giv good back rubs']
            await log.send(f"<a:welcomeglitch:498634744251285516> hi, **{member.name}**! {rnd(resp)}") 
        elif member.guild.id == 608050333423239235:
            general = self.bot.get_channel(608050333423239241)
            footers = ['Did you know: According to extensive research by scientists around the globe, traps are indeed, not gay.']
            embed = discord.Embed(description='Read the rules in <#609143513124175894>. Choose North or South by clicking a reaction below. Choose carefully, you have to ask an admin to change!')
            embed.set_author(icon_url=ctx.author.avatar_url_as(format='png'), name="Welcome, lukee")
            embed.set_footer(text=rnd(footers))
            await general.send(embed=embed)
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
 
    @commands.command()
    @commands.is_owner()
    async def gmember(self, ctx):
        msg = await ctx.send(f"Adding roles to **{ctx.guild.member_count} users**.")
        for user in ctx.guild.members:
            await user.add_roles(discord.utils.get(ctx.guild.roles, name="Member"))
        msg.delete()
        await ctx.send(f"Added roles to **{ctx.guild.member_count}**")
  
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
        
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def apv(self, ctx, member: discord.Member):
        try:
            await member.add_roles(discord.utils.get(ctx.guild.roles, name="Detective Solvers"))
            await ctx.message.add_reaction('👍')
            await member.send('You have been approved. You can now view the general channels.')
            r1 = random.randint(0, 9)
            r2 = random.randint(0, 9)
            rt = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k']
            code = str(r1) + rnd(rt) + str(r2) + rnd(rt)
            await self.bot.get_channel(472471188170604544).send(f'→ **{ctx.author}** has approved a member ({member.mention}). [code. `{code}`]')
        except Exception as e:
            await ctx.send(f'<:redtick:492800273211850767> `{e}`')
            
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def dny(self, ctx, member: discord.Member, *, reason='N/A'):
        await ctx.message.add_reaction('👍')
        await member.send(f'You have been denied access to the Nest guild. Reason: `{reason}`')
        r1 = random.randint(0, 9)
        r2 = random.randint(0, 9)
        rt = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k']
        code = str(r1) + rnd(rt) + str(r2) + rnd(rt)
        await self.bot.get_channel(472471188170604544).send(f'→ **{ctx.author}** has denied a member ({member.mention}), reason: `{reason}`. [code. `{code}`]')
        await ctx.guild.kick(member, reason='Denied access to server.')
                     
        
    @commands.command(aliases=['bugreport'])
    async def reportbug(self, ctx, *, topic, option=None, description=None):
        """Bug Report Command (Siri Support Server Only)"""
        if ctx.channel.id == 494480470839525378:
            await ctx.message.delete()           
            args = topic.split('|')
            topic = args[0]
            option = args[1]
            description = args[2]  
            if not description:
                await ctx.send(f"<:redtick:492800273211850767> {ctx.author.mention}, Incorrect Arguments. **Usage:** `siri bugreport <topic> <option> <description>` *Do not include < or > in your report.*", delete_after=10)
            if str(option).lower() not in ['major', 'minor', ' minor ', ' major ', 'minor ', 'major ', ' minor', ' major']:
                await ctx.send(f"<:redtick:492800273211850767> {ctx.author.mention}, Incorrect Arguments. Option must be either `Major` or `Minor`. Ex. `siri reportbug Help | Minor | description here`", delete_after=10)
            else:
                data = {
                        "name": description, 
                        "desc": f'This is a user-submitted card.\n\n**Command/Topic:** {str(topic).capitalize()}\n\n**Description:** {description}\n\n**Submitted by:** {ctx.author} ({ctx.author.id})\n\n\nThis bug is **{str(option).upper()}**.',
                        "idList": '5bde5b1cb1304b380ff9d72e',
                        "pos": 'top'
                }
                r = requests.post(f"https://api.trello.com/1/cards?key={config.trello_key}&token={config.trello_token}", data=data).json()
                trello_link = r['url']

                msg = await ctx.send(f"<:greentick:492800272834494474> {ctx.author.mention}, your report has been sent! Check it out in <#508462645163065362> or on {trello_link}. I have also sent a transcipt to your DMs.", delete_after=10)

                embed = discord.Embed(colour=0x00f0ff, description="Bug Report Transcript")
                embed.add_field(name="Topic/Command:", value=str(topic).capitalize())
                embed.add_field(name="Option:", value=str(option).capitalize())
                embed.add_field(name="Description:", value=description)
                embed.add_field(name="Link:", value=trello_link)
                embed.set_footer(text="Thank you for submitting a bug!")
                await ctx.author.send(embed=embed)
                                                                    
        else:
            pass
        
def setup(bot):
  bot.add_cog(Server(bot))
