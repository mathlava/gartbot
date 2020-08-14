import json
import os
import random
import re

import aiohttp
import discord


async def main(message, arg):

    fid = str(random.SystemRandom().randint(10000, 99999))
    here = os.path.dirname(__file__)
    with open(f'{here}/languages.json', 'r') as f:
        language_dict = json.load(f)
    arg = re.sub(r'```[A-z\-\+]*\n', '', arg).replace('```', '')
    url = 'https://wandbox.org/api/compile.json'
    language = arg.split()[0]
    code = arg.replace(language, '', 1).lstrip(' \n')
    language = language.lower().replace('pp', '++').replace('sharp', '#').replace('clisp', 'lisp').replace('lisp', 'clisp')
    if not language in language_dict.keys():
        embed = discord.Embed(
            title='言語が間違っています',
            description='対応している言語は以下の通りです\n' \
                + ', '.join(language_dict.keys()),
            color=0xff0000
        )
        embed.set_author(
            name=message.author.name,
            icon_url=message.author.avatar_url
        )
        return await message.channel.send(embed=embed)
    params = {
        'compiler': language_dict[language],
        'code': code,
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=params) as r:
            if r.status == 200:
                result = await r.json()
            else:
                embed = discord.Embed(
                    title='接続エラー',
                    description=f'{r.status}',
                    color=0xff0000
                )
                return await message.channel.send(embed=embed)
    status = result.get('status')
    signal = result.get('signal')
    stdout = result.get('program_output', '')
    compile_message = result.get('compiler_error')
    runtime_message = result.get('program_error')
    files = []
    if status == '0' or signal == 'Killed':
        if signal == 'Killed':
            embed = discord.Embed(
                title='実行結果',
                description=f'タイムアウト',
                color=0xff0000
            )
        else:
            embed = discord.Embed(
                title='実行結果',
                description=f'終了ステータス：{status}',
                color=0x008000
            )
        if len(stdout) <= 1000:
            embed.add_field(
                name='標準出力',
                value=f'```\n{stdout}\n```',
            )
        else:
            with open(f'{here}/run_temporary/{fid}_stdout.txt', 'w') as f:
                f.write(stdout)
            with open(f'{here}/run_temporary/{fid}_stdout.txt', 'r') as f:
                files.append(discord.File(f, 'stdout.txt'))
            os.remove(f'{here}/run_temporary/{fid}_stdout.txt')
        if compile_message:
            with open(f'{here}/run_temporary/{fid}_compile_message.txt', 'w') as f:
                f.write(stdout)
            with open(f'{here}/run_temporary/{fid}_compile_message.txt', 'r') as f:
                files.append(discord.File(f, 'compile_message.txt'))
            os.remove(f'{here}/run_temporary/{fid}_compile_message.txt')
        if runtime_message:
            with open(f'{here}/run_temporary/{fid}_runtime_message.txt', 'w') as f:
                f.write(stdout)
            with open(f'{here}/run_temporary/{fid}_runtime_message.txt', 'r') as f:
                files.append(discord.File(f, 'runtime_message.txt'))
            os.remove(f'{here}/run_temporary/{fid}_runtime_message.txt')
    else:
        if not signal is None:
            embed = discord.Embed(
                title='実行結果',
                description=f'終了シグナル：{signal}',
                color=0xff0000
            )
        else:
            embed = discord.Embed(
                title='実行結果',
                description=f'終了ステータス：{status}',
                color=0xff0000
            )
        if len(stdout) > 0 and len(stdout) <= 1000:
            embed.add_field(
                name='標準出力',
                value=f'```\n{stdout}\n```',
            )
        elif len(stdout) > 1000:
            with open(f'{here}/run_temporary/{fid}_stdout.txt', 'w') as f:
                f.write(stdout)
            with open(f'{here}/run_temporary/{fid}_stdout.txt', 'r') as f:
                files.append(discord.File(f, 'stdout.txt'))
            os.remove(f'{here}/run_temporary/{fid}_stdout.txt')
        if runtime_message:
            if len(runtime_message) <= 1000:
                embed.add_field(
                    name='ランタイムエラー',
                    value=f'```\n{runtime_message}\n```',
                )
            else:
                with open(f'{here}/run_temporary/{fid}_runtime_error.txt', 'w') as f:
                    f.write(stdout)
                with open(f'{here}/run_temporary/{fid}_runtime_error.txt', 'r') as f:
                    files.append(discord.File(f, 'runtime_error.txt'))
                os.remove(f'{here}/run_temporary/{fid}_runtime_error.txt')
            if compile_message:
                with open(f'{here}/run_temporary/{fid}_compile_error.txt', 'w') as f:
                    f.write(stdout)
                with open(f'{here}/run_temporary/{fid}_compile_error.txt', 'r') as f:
                    files.append(discord.File(f, 'compile_error.txt'))
                os.remove(f'{here}/run_temporary/{fid}_compile_error.txt')
        if compile_message:
            if len(compile_message) <= 1000:
                embed.add_field(
                    name='コンパイルエラー',
                    value=f'```\n{compile_message}\n```',
                )
            else:
                with open(f'{here}/run_temporary/{fid}_compile_error.txt', 'w') as f:
                    f.write(stdout)
                with open(f'{here}/run_temporary/{fid}_compile_error.txt', 'r') as f:
                    files.append(discord.File(f, 'compile_error.txt'))
                os.remove(f'{here}/run_temporary/{fid}_compile_error.txt')
    embed.set_author(name=message.author.name, icon_url=message.author.avatar_url)
    return await message.channel.send(embed=embed, files=files)
