import discord

import os
import json

with open(os.path.dirname(__file__) + '/../config.json', 'r') as f:
    config_dict = json.load(f)

PREFIX = config_dict['prefix']

async def main(message, arg):

    embed = discord.Embed(
        title='がーとぼっと',
        description='コマンド一覧'
    )
    embed.add_field(
        name=f'`{PREFIX}run 言語名\nコード`',
        value='プログラムを実行できます'
    )
    embed.add_field(
        name=f'`{PREFIX}tex LaTeXの数式`',
        value='数式を画像にできます'
    )
    embed.add_field(
        name=f'`{PREFIX}stex LaTeXの数式`',
        value='数式をスポイラー付き画像にできます'
    )
    embed.add_field(
        name=f'`{PREFIX}texp LaTeXの文章`',
        value='LaTeXで書かれた文章を画像にできます'
    )
    embed.add_field(
        name=f'`{PREFIX}texpdf LaTeXのコード(プリアンブル含む)`',
        value='LaTeXで書かれた文章をpdfにできます'
    )
    embed.add_field(
        name=f'`{PREFIX}ad 複素数`',
        value='素微分します'
    )
    embed.add_field(
        name=f'`{PREFIX}ai 正整数`',
        value='素微分するとその整数になる整数のうち' \
            + ' [1, 10000000) の範囲にあるものを出力します'
    )
    embed.add_field(
        name=f'`{PREFIX}bf コード`',
        value='BrainF\*ck のプログラムを実行できます'
    )
    embed.add_field(
        name=f'`{PREFIX}escape (エスケープしたいメッセージに返信)`',
        value=r'Discordの修飾(\*, \_, \\, ...)をエスケープして表示します'
    )

    embed.set_author(
        name=message.author.name,
        icon_url=message.author.avatar_url
    )
    return await message.reply(embed=embed)
