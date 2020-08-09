import discord

async def main(message, arg):

    embed = discord.Embed(
        title='がーとぼっと',
        description='コマンド一覧'
    )
    embed.add_field(
        name='`)run 言語名\nコード`',
        value='プログラムを実行できます'
    )
    embed.add_field(
        name='`)tex LaTeXの数式`',
        value='数式を画像にできます'
    )
    embed.add_field(
        name='`)stex LaTeXの数式`',
        value='数式をスポイラー付き画像にできます'
    )
    embed.add_field(
        name='`)latex LaTeXの文章`',
        value='LaTeXで書かれた文章を画像にできます'
    )
    embed.add_field(
        name='`)texpdf LaTeXのコード(プリアンブル含む)`',
        value='LaTeXで書かれた文章をpdfにできます'
    )
    embed.add_field(
        name='`)ad 複素数`',
        value='素微分します'
    )
    embed.add_field(
        name='`)ai 正整数`',
        value='素微分するとその整数になる整数のうち' \
            + ' [1, 10000000) の範囲にあるものを出力します'
    )
    embed.add_field(
        name='`)bf コード`',
        value='BreainF\*ck のプログラムを実行できます'
    )
    embed.set_author(
        name=message.author.name,
        icon_url=message.author.avatar_url
    )
    return await message.channel.send(embed=embed)
