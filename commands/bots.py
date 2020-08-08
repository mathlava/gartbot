import discord
from proto import cmdin_pb2, cmdout_pb2, help_pb2

async def main(message, arg):

    result = ""
    embed = discord.Embed(description=result)
    embed.set_author(
        name=message.author.name,
        icon_url=message.author.avatar_url
    )
    return await message.channel.send(embed=embed)
    