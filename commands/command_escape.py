import discord

async def main(message: discord.Message, arg: str):
    
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
    if len(usr_msg.content) == 0:
        embed = discord.Embed(
            title='エラー',
            description='文章が含まれるメッセージに返信してください',
            color=0xff0000
        )
        embed.set_author(
            name=message.author.name,
            icon_url=message.author.avatar_url
        )
        return await message.reply(embed=embed)
    new_str = discord.utils.escape_markdown(usr_msg.content)
    if len(new_str) > 2000:
        embed = discord.Embed(
            title='エラー',
            description='結果が2000文字を超えました',
            color=0xff0000
        )
        embed.set_author(
            name=message.author.name,
            icon_url=message.author.avatar_url
        )
        return await message.reply(embed=embed)
    return await message.reply(new_str)
