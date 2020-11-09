import discord

async def main(message, arg):

    embed = discord.Embed(
        title='がーとぼっと',
        description='latexコマンドはtexpコマンドに改名しました'
    )
    embed.set_author(
        name=message.author.name,
        icon_url=message.author.avatar_url
    )
    return await message.channel.send(embed=embed)
