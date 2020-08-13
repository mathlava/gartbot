import discord

async def main(message, arg):
    
    try:
        usr_msg = await message.channel.fetch_message(int(arg.split()[0]))
    except ValueError:
        embed = discord.Embed(
            title='エラー',
            description='`)escape メッセージID`と入力してください\n' \
                'メッセージIDの取得の方法は' \
                '[こちら](https://support.discord.com/hc/ja/articles/206346498-ユーザー-サーバー-メッセージIDはどこで見つけられる-)',
            color=0xff0000
        )
        embed.set_author(
            name=message.author.name,
            icon_url=message.author.avatar_url
        )
        return await message.channel.send(embed=embed)
    except discord.errors.NotFound:
        embed = discord.Embed(
            title='エラー',
            description='このチャンネルにそのメッセージは見つかりませんでした',
            color=0xff0000
        )
        embed.set_author(
            name=message.author.name,
            icon_url=message.author.avatar_url
        )
        return await message.channel.send(embed=embed)
    new_str = discord.utils.escape_markdown(usr_msg.content)
    return await message.channel.send(new_str)
