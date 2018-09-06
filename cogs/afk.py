import discord
from discord.ext import commands
import json


class AFK:
    def __init__(self, bot):
        self.bot = bot
        
        
    @commands.group(pass_context=True, aliases=['away'])
    async def afk(self, ctx):
        """Set as AFK so users will know to stop bothering you."""
        ...
        
    @afk.command(pass_context=True, aliases=['enable'])
    async def on(self, ctx):
        """Turn AFK On (AFK SUB)"""
        ...
      
    @afk.command(pass_context=True, aliases=['disable'])
    async def off(self, ctx):
        """Turn AFK Off (AFK SUB)"""
        ...
        
        
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
