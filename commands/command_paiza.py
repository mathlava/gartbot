import discord

async def main(message, arg):

    embed = discord.Embed(
        title='がーとぼっと',
        description='paizaコマンドはなくなりました\n' \
            + '代わりに以下のコマンドをお使いください'
    )
    embed.add_field(
        name=')run 言語名\nコード',
        value='プログラムを実行できます'
    )
    embed.set_author(
        name=message.author.name,
        icon_url=message.author.avatar_url
    )
    return await message.channel.send(embed=embed)
