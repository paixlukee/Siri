import discord
from discord.ext import commands
import json


class Account:
    def __init__(self):
        self.s = '§'


async def add_money(self, user=None, count=None):
    with open('C:\\Users\\Luke Jeffries\\Siri\\cogs\\economy.json', 'r') as f:
            users = json.load(f)
            users[user]['money'] += count
    with open('C:\\Users\\Luke Jeffries\\Siri\\cogs\\economy.json', 'w') as f:
             json.dump(users, f)

async def take_money(self, user=None, count=None):
    with open('C:\\Users\\Luke Jeffries\\Siri\\cogs\\economy.json', 'r') as f:
            users = json.load(f)
            users[user]['money'] -= count
    with open('C:\\Users\\Luke Jeffries\\Siri\\cogs\\economy.json', 'w') as f:
             json.dump(users, f)