import discord
from discord.ext import commands
import json


class AFK:
    def __init__(self, bot):
        self.bot = bot
        
        
    @commands.group(pass_context=True, aliases=['away'])
    async def afk(self, ctx):
        """Set as AFK so users will know to stop bothering you."""
        if ctx.invoked_subcommand is None:
            await self.bot.say("`Incorrect Usage`\n```siri afk on|enable [reason]``` or ```siri afk off|disable```)
        
    @afk.command(pass_context=True, aliases=['enable'])
    async def on(self, ctx, *, reason=None):
        """Turn AFK On (AFK SUB)"""
        if reason is None:
            reason = 'No Reason'
        else:
            pass
        await self.afk_on(user=ctx.message.author.id, reason=reason)
        await self.bot.say("<:idle:483080613687984131> I have successfully set you as **AFK**!")
      
    @afk.command(pass_context=True, aliases=['disable'])
    async def off(self, ctx):
        """Turn AFK Off (AFK SUB)"""
        await self.afk_off(user=ctx.message.author.id)
        await self.bot.say(f"<:online:313956277808005120> Welcome back, **{ctx.message.author}**!")
        
        
    async def afk_on(self, user=None, reason=None):
        with open(r'assets\afk_members.json', 'r') as f:
            users = json.load(f)
            
        users[user]['AFK'] = True
        users[user]['reason'] = reason
        
        with open(r'assets\afk_members.json', 'w') as f:
            json.dump(users, f)
     
     async def afk_off(self, user=None):
        with open(r'assets\afk_members.json', 'r') as f:
            users = json.load(f)
            
        users[user]['AFK'] = False
        users[user]['reason'] = 'None'
        
        with open(r'assets\afk_members.json', 'w') as f:
            json.dump(users, f)
        
        
       
        
def setup(bot):
  bot.add_cog(AFK(bot))
