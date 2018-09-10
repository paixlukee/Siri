import discord
from discord.ext import commands
import requests
import json


class Crypto:
    def __init__(self, bot):
        self.bot = bot
        
        
    @commands.command(aliases=['btc'])
    async def bitcoin(self, ctx):
        """Get BTC Stats"""
        try:
            await self.add_money(user=ctx.message.author.id, count=1)
        except:
            pass
        r = requests.get("https://www.bitstamp.net/api/v2/ticker/btcusd/").json()
        e = requests.get("https://www.bitstamp.net/api/v2/ticker/btceur/").json()
        embed = discord.Embed(colour=0xf4d142)
        embed.add_field(name="1 Bitcoin equals..", value=f"**$**{r['last']}\n**€**{e['last']}")
        embed.add_field(name="BTC High..", value=f"**$**{r['high']}\n**€**{e['high']}")
        embed.set_thumbnail(url="https://static.vecteezy.com/system/resources/previews/000/205/146/non_2x/vector-bitcoin-symbol-on-orange-background.jpg")
        await ctx.send(embed=embed)

    @commands.command(aliases=['xrp'])
    async def ripple(self, ctx):
        """Get XRP Stats"""
        try:
            await self.add_money(user=ctx.message.author.id, count=1)
        except:
            pass
        r = requests.get("https://www.bitstamp.net/api/v2/ticker/xrpusd/").json()
        e = requests.get("https://www.bitstamp.net/api/v2/ticker/xrpeur/").json()
        embed = discord.Embed(colour=0x0000ff)
        embed.add_field(name="1 Ripple equals..", value=f"**$**{r['last']}\n**€**{e['last']}")
        embed.add_field(name="XRP High..", value=f"**$**{r['high']}\n**€**{e['high']}")
        embed.set_thumbnail(url="https://www.cryptocoinsnieuws.nl/wp-content/uploads/2018/01/ripple-xrp.png")
        await ctx.send(embed=embed)

    @commands.command(aliases=['ltc'])
    async def litecoin(self, ctx):
        """Get LTC Stats"""
        try:
            await self.add_money(user=ctx.message.author.id, count=1)
        except:
            pass
        r = requests.get("https://www.bitstamp.net/api/v2/ticker/ltcusd/").json()
        e = requests.get("https://www.bitstamp.net/api/v2/ticker/ltceur/").json()
        embed = discord.Embed()
        embed.add_field(name="1 Litecoin equals..", value=f"**$**{r['last']}\n**€**{e['last']}")
        embed.add_field(name="LTC High..", value=f"**$**{r['high']}\n**€**{e['high']}")
        embed.set_thumbnail(url="https://a1finance.cz/wp-content/uploads/2017/08/Official_Litecoin_Logo.jpg")
        await ctx.send(embed=embed)
        
    @commands.command(aliases=['eth'])
    async def ethereum(self, ctx):
        """Get ETH Stats"""
        try:
            await self.add_money(user=ctx.message.author.id, count=1)
        except:
            pass
        r = requests.get("https://www.bitstamp.net/api/v2/ticker/ethusd/").json()
        e = requests.get("https://www.bitstamp.net/api/v2/ticker/etheur/").json()
        embed = discord.Embed(colour=0x00a6ff)
        embed.add_field(name="1 Ethereum equals..", value=f"**$**{r['last']}\n**€**{e['last']}")
        embed.add_field(name="ETH High..", value=f"**$**{r['high']}\n**€**{e['high']}")
        embed.set_thumbnail(url="https://cryptorunner.com/wp-content/uploads/2017/10/ethereum-symbol.png")
        await ctx.send(embed=embed)
        
        
def setup(bot):
  bot.add_cog(Crypto(bot))
