import asyncio
import random
import os
import subprocess
import io

import discord


async def main(message, arg):

    arg = arg.replace('```tex', '').replace('```', '')
    fid = str(random.SystemRandom().randint(10000, 99999))
    here = os.path.dirname(__file__)

    tex_con = arg.strip()

    with open(f'/tmp/' + fid + '.tex', 'w') as f:
        f.write(tex_con)

    try:
        _ = subprocess.run(['uplatex', '-halt-on-error', '-output-directory=/tmp', '/tmp/' + fid + '.tex'], timeout=10)
    except subprocess.TimeoutExpired:
        embed = discord.Embed(
            title='タイムアウト',
            color=0xff0000
        )
        embed.set_author(name=message.author.name, icon_url=message.author.avatar_url)
        return await message.channel.send(embed=embed)
    dvipdfmx = subprocess.run(['dvipdfmx', '-q', '-o', '/tmp/' + fid + '.pdf', '/tmp/' + fid + '.dvi'])

    if dvipdfmx.returncode != 0:
        with open('/tmp/' + fid + '.log', 'r') as f:
            err = f.read().split('!')[1].split('Here')[0]
        embed = discord.Embed(
            title='レンダリングエラー',
            description=f'```\n{err}\n```',
            color=0xff0000
        )
        embed.set_author(name=message.author.name, icon_url=message.author.avatar_url)
        return await message.channel.send(embed=embed)
    else:
        embed = discord.Embed(color=0x008000)
        embed.set_author(name=message.author.name, icon_url=message.author.avatar_url)
        return await message.channel.send(file=discord.File('/tmp/' + fid + '.pdf'), embed=embed)
