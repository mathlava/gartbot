import discord

async def main(message, arg):
    
    if message.reference == None:
        embed = discord.Embed(
            title='エラー',
            description='エスケープしたいメッセージに返信してください',
            color=0xff0000
        )
        embed.set_author(
            name=message.author.name,
            icon_url=message.author.avatar_url
        )
        return await message.reply(embed=embed)
    try:
        usr_msg = await message.channel.fetch_message(message.reference.message_id)
    except discord.errors.NotFound:
        embed = discord.Embed(
            title='エラー',
            description='そのメッセージは見つかりませんでした',
            color=0xff0000
        )
        embed.set_author(
            name=message.author.name,
            icon_url=message.author.avatar_url
        )
        return await message.reply(embed=embed)
    new_str = discord.utils.escape_markdown(usr_msg.content)
    return await message.reply(new_str)
