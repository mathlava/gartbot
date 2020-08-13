import os
import random
import re

import aiohttp
import discord


async def main(message, arg):

    arg = arg.replace('```tex', '').replace('```', '')
    fid = str(random.SystemRandom().randint(10000, 99999))
    here = os.path.dirname(__file__)

    with open(f'{here}/tex_temporary/{fid}.tex', mode='w') as f:
        f.write(arg)
        
    files = {
        'file': open(f'{here}/tex_temporary/{fid}.tex', 'r'),
    }

    async with aiohttp.ClientSession() as session:
        async with session.post('https://tex.amas.dev/default', data=files) as r:
            if r.status == 200:
                res = await r.text()
                os.remove(f'{here}/tex_temporary/{fid}.tex')
            else:
                return await message.channel.send(f'[texpdf] 接続エラー：{r.status}')

    match = re.search(r'https://tex.amas.dev/files/[a-z|0-9]+.pdf', res)
    
    if match:
        async with aiohttp.ClientSession() as session:
            async with session.get(match.group()) as r:
                with open(f'{fid}.pdf', 'wb') as f:
                    if status == 200:
                        f.write(r.read())
                    else:
                        return await message.channel.send(f'[texpdf] 接続エラー：{r.status}')

        embed = discord.Embed(color=0x008000)
        embed.set_author(name=message.author.name, icon_url=message.author.avatar_url)

        return await message.channel.send(file=discord.File(f'{fid}.pdf'), embed=embed)
        os.remove(f'{fid}.pdf')
        
    else:
        if match := re.search(r'!.*', res, re.S):
            errmsg = match.group()[:match.group().find('No pages of output.')]
        else:
            errmsg = res
        if len(errmsg) > 1000:
            errmsg = errmsg[:1000] + '...'

        embed = discord.Embed(
            title='レンダリングエラー',
            description=f'```\n{errmsg}\n```',
            color=0xff0000
            )
        embed.set_author(name=message.author.name, icon_url=message.author.avatar_url)
        return await message.channel.send(embed=embed)
