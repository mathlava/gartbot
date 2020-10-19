import discord


async def main(message, arg):
    embed = discord.Embed(
        title='コマンドが見つかりません',
        description=f'```\ntexpdfコマンドは廃止されました\n```',
        color=0xff0000
        )
    embed.set_author(name=message.author.name, icon_url=message.author.avatar_url)
    return await message.channel.send(embed=embed)
