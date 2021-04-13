import discord

async def main(message: discord.Message, arg: str):

    embed = discord.Embed(
        title='がーとぼっと',
        description='latexコマンドはtexpコマンドに改名しました'
    )
    embed.set_author(
        name=message.author.name,
        icon_url=message.author.avatar_url
    )
    return await message.reply(embed=embed)
