import discord
import datetime
import requests
import logging
import math
import re
import asyncio
import config

dbl_token = config.dbl_token

async def post(self, list:str):
  lists = ['dbl']
  if not list.lower() in lists:
      return f"'{list}' list not available."
  else:
      if list.lower() == 'dbl':
          try:
              data = {'server_count': len(self.bot.guilds)}
              headers = {'Authorization': dbl_token}
              p = requests.post('https://discordbots.org/api/bots/481337766379126784/stats', data=data, headers=headers).json()
              return "Server count has been posted.`"
      except Exception as e:
          return f'{type(e).__name__}: {e}'
