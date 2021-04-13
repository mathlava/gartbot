import time

import discord

async def main(message: discord.Message, arg: str):

    s = list(message.content[3:])
    m = [0]
    p = 0
    h = 0
    exit_code = 0
    er = ''
    out16 = ''
    outbytes = b''
    start = time.time()

    while True:
        if s[h] == '>':
            p += 1
            if p == len(m):
                m.append(0)
        elif s[h] == '<':
            p -= 1
            if p < 0:
                exit_code = 1
                er += 'ポインタは負の値をとれません'
        elif s[h] == '+':
            m[p] += 1
            if m[p] == 256:
                m[p] = 0
        elif s[h] == '-':
            m[p] -= 1
            if m[p] == -1:
                m[p] = 255
        elif s[h] == '.':
            out16 += format(m[p], '02X') + ' '
            outbytes += m[p].to_bytes(1, 'big')
        elif s[h] == '[':
            if m[p] == 0:
                c = 1
                while True:
                    h += 1
                    if h >= len(s):
                        exit_code = 1
                        er += '対応する]が見つかりません'
                        break
                    if s[h] == '[':
                        c += 1
                    elif s[h] == ']':
                        c -= 1
                    if c == 0:
                        break
        elif s[h] == ']':
            if m[p] != 0:
                c = -1
                while True:
                    h -= 1
                    if h < 0:
                        exit_code = 1
                        er += '対応する[が見つかりません'
                        break
                    if s[h] == '[':
                        c += 1
                    elif s[h] == ']':
                        c -= 1
                    if c == 0:
                        break
        h += 1
        if h == len(s):
            break
        if time.time() - start > 5:
            exit_code = 2
            er += '5秒を超えるプログラムは実行できません'
        if er:
            break
    if exit_code == 0:
        embed = discord.Embed(
            title='実行結果',
            description=f'終了ステータス：{exit_code}',
            color=0x008000
        )
        embed.add_field(
            name='標準出力(16進数表示)',
            value=f'```\n{out16}\n```'
        )
        try:
            outstr = outbytes.decode('utf-8')
        except UnicodeDecodeError:
            outstr = 'デコードできませんでした'
        embed.add_field(
            name='標準出力(UTF-8)',
            value=f'```\n{outstr}\n```'
        )
    else:
        embed = discord.Embed(
            title='実行結果',
            description=f'終了ステータス：{exit_code}',
            color=0xff0000
        )
        if exit_code == 1:
            embed.add_field(
                name='エラー',
                value=er
            )
        elif exit_code == 2:
            embed.add_field(
                name='タイムアウト',
                value='5秒を超えるプログラムは実行できません'
            )
    embed.set_author(
        name=message.author.name,
        icon_url=message.author.avatar_url
    )
    return await message.reply(embed=embed)
