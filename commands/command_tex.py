import asyncio
import random
import os
import re
import subprocess

import aiohttp
import discord


async def main(message, arg):

    arg = arg.replace('```tex', '').replace('```', '')
    fid = str(random.SystemRandom().randint(10000, 99999))
    here = os.path.dirname(__file__)

    with open(f'{here}/tex_template/tex.tex', 'r') as f:
        tex_con = f.read().replace('[REPLACE]', arg.strip())
    
    with open(f'{here}/tex_temporary/{fid}.tex', 'w') as f: 
        f.write(tex_con)
        
    files = {
        'file': open(f'{here}/tex_temporary/{fid}.tex', 'r')
    }

    async with aiohttp.ClientSession() as session:
        async with session.post('https://tex.amas.dev/texjpg', data=files) as r:
            if r.status == 200:
                try:
                    res = await r.text()
                except aiohttp.client_exceptions.ClientPayloadError:
                    old_message = await message.channel.send(f'[tex] 数秒お待ち下さい...')
                    await asyncio.sleep(2)
                    cmd = f'nohup curl -X POST -F file=@{here}/tex_temporary/{fid}.tex https://tex.amas.dev/texjpg > {fid}.txt &'
                    subprocess.call(cmd, shell=True)
                    await asyncio.sleep(2)
                    await old_message.delete()
                    with open(f'{fid}.txt', 'r') as f:
                        res = f.read()
                    os.remove(f'{fid}.txt')
            else:
                return message.channel.send(f'[tex] 接続エラー：{r.status}')
        
    os.remove(f'{here}/tex_temporary/{fid}.tex')
    match = re.search(r'https://tex\.amas\.dev/files/[a-z|0-9]+\.jpg', res)
        
    if match:
        async with aiohttp.ClientSession() as session:
            async with session.get(match.group()) as r:
                if r.status == 200:
                    with open(f'{here}/tex_temporary/{fid}.jpg', 'wb') as f:
                        f.write(await r.read())

                    file = discord.File(f'{here}/tex_temporary/{fid}.jpg', filename='tex.jpg')
                    embed = discord.Embed(color=0x008000)
                    embed.set_image(url=f'attachment://tex.jpg')
                    embed.set_author(name=message.author.name, icon_url=message.author.avatar_url)
                    os.remove(f'{here}/tex_temporary/{fid}.jpg')
                    return await message.channel.send(file=file, embed=embed)
                else:
                    return message.channel.send(f'[tex] 接続エラー：{r.status}')
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
