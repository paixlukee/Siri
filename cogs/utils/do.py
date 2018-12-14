import discord
import datetime
import requests
import logging
import math
import re
import asyncio
import config
import subprocess

dbl_token = config.dbl_token

async def post(count, list:str):
    lists = ['dbl']
    if not list.lower() in lists:
        return f"'{list}' list not available."
    else:
      if list.lower() == 'dbl':
          try:
              data = {'server_count': count}
              headers = {'Authorization': dbl_token}
              p = requests.post('https://discordbots.org/api/bots/481337766379126784/stats', data=data, headers=headers).json()
              return "Server count has been posted.`"
          except Exception as e:
              return f'{type(e).__name__}: {e}'
              
async def shell(cmd):
    process =\
    await asyncio.create_subprocess_shell(cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE)
    results = await process.communicate()
    return "".join(x.decode("utf-8") for x in results)
