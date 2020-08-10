import discord

async def command_escape(message, arg):
    
    usr_msg = await message.channel.fetch_message(int(arg.split()[0]))
    new_str = discord.utils.escape_markdown(usr_msg.content)
    return await message.channel.send(new_str)
