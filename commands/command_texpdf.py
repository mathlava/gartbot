import random
import subprocess

import discord


async def main(message: discord.Message, arg: str):

    arg = arg.replace('```tex', '').replace('```', '')
    # file id
    fid = str(random.SystemRandom().randrange(10000, 100000))

    tex_con = arg.strip()

    if '\\input' in tex_con or '\\include' in tex_con \
            or '\\csname' in tex_con or '\\listinginput' in tex_con \
            or '\\verbinput' in tex_con or '\\lstinputlisting' in tex_con \
            or '\\subfile' in tex_con or '\\import' in tex_con \
            or '\\tempfile' in tex_con or '\\makeatletter' in tex_con \
            or '\\pdffiledump' in tex_con:
        embed = discord.Embed(
            title='使用できない文字列が含まれています',
            color=0xff0000
        )
        embed.set_author(
            name=message.author.name,
            icon_url=message.author.avatar_url
        )
        return await message.reply(embed=embed)

    with open('/tmp/' + fid + '.tex', 'w') as f:
        f.write(tex_con)

    try:
        uplatex = subprocess.run(
            [
                'uplatex',
                '-halt-on-error',
                '-output-directory=/tmp',
                '/tmp/' + fid + '.tex'
            ],
            timeout=10
        )
    except subprocess.TimeoutExpired:
        embed = discord.Embed(
            title='タイムアウト',
            color=0xff0000
        )
        embed.set_author(
            name=message.author.name,
            icon_url=message.author.avatar_url
        )
        return await message.reply(embed=embed)

    if uplatex.returncode != 0:
        with open('/tmp/' + fid + '.log', 'r') as f:
            err = f.read().split('!')[1].split('Here')[0]
        subprocess.run(f'rm /tmp/{fid}.*', shell=True)
        embed = discord.Embed(
            title='レンダリングエラー',
            description=f'```\n{err}\n```',
            color=0xff0000
        )
        embed.set_author(
            name=message.author.name,
            icon_url=message.author.avatar_url
        )
        return await message.reply(embed=embed)
    else:
        subprocess.run(
            [
                'dvipdfmx',
                '-q',
                '-o',
                '/tmp/' + fid + '.pdf',
                '/tmp/' + fid + '.dvi'
            ],
            timeout=10
        )
        embed = discord.Embed(color=0x008000)
        embed.set_author(
            name=message.author.name,
            icon_url=message.author.avatar_url
        )
        my_msg = await message.reply(
            file=discord.File('/tmp/' + fid + '.pdf'),
            embed=embed
        )
        subprocess.run(f'rm /tmp/{fid}.*', shell=True)
        return my_msg
