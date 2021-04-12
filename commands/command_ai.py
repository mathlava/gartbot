import discord
import aiohttp
import sys
import os

from dotenv import load_dotenv

load_dotenv(verbose=True)
MIYUBOT_TOKEN = os.environ.get("MIYUBOT_TOKEN")

async def main(message, arg):
    
    if arg.replace(' ', '') == '1':
        result = '全ての素数'
    else:
        url = 'https://mathlava.com/api/MiyuBot/index.php'
        params = {
            'client': 'GartBot',
            'token': MIYUBOT_TOKEN,
            'query': [{
                'function': 'primes',
                'command': 'sosekibun',
                'value': arg.replace(' ', '')
            }]
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=params) as r:
                if r.status == 200:
                    json = await r.json()
                else:
                    embed = discord.Embed(
                        title='接続エラー',
                        description=f'{r.status}',
                        color=0xff0000
                    )
                    return await message.reply(embed=embed)
        if json[0]['return']:
            result = ', '.join(json[0]['return'])
        elif json[0]['status'] == 'OK':
            result = '[1, 10000000) の範囲には見つかりませんでした'
    embed = discord.Embed(description=result)
    embed.set_author(
        name=message.author.name,
        icon_url=message.author.avatar_url
    )
    return await message.reply(embed=embed)
