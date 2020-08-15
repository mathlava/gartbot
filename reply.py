import logging
import os
from importlib import import_module

import discord

from config import PREFIX
from classes import LimitedSizeDict

message_id_to_author_id = LimitedSizeDict(size_limit=100)
user_message_id_to_bot_message = LimitedSizeDict(size_limit=100)

async def reply(message):

    # message主がbotならば無視
    if message.author.bot and not message.author.id == 614130545227726849:
        return

    if message.content.startswith(PREFIX):

        command = message.content.split()[0][len(PREFIX):]
        arg = message.content[len(PREFIX) + len(command):].lstrip()

        if os.path.exists(f'{os.path.dirname(os.path.abspath(__file__))}/commands/python/command_{command}.py'):

            tmp_module = import_module(f'commands.python.command_{command}')
            async with message.channel.typing():
                try:
                    sent_message = await tmp_module.main(message, arg)
                except discord.Forbidden:
                    return
                except Exception as e:
                    logging.exception(e)
                    embed = discord.Embed(
                        title='内部エラーが発生しました',
                        description='エラーが続く場合は公式サーバで報告してください\n'
                            + 'https://discord.gg/7gypE3Q',
                        color=0xff0000
                    )
                    embed.set_author(name=message.author.name, icon_url=message.author.avatar_url)
                    sent_message = await message.channel.send(embed=embed)
                message_id_to_author_id[sent_message.id] = message.author.id
                user_message_id_to_bot_message[message.id] = sent_message
                await sent_message.add_reaction('🚮')
        else:
            tmp_module = import_module('bots')
            async with message.channel.typing():
                try:
                    sent_messages = await tmp_module.loader(command, message, arg)
                except discord.Forbidden:
                    return
                except Exception as e:
                    logging.exception(e)
                    embed = discord.Embed(
                        title='内部エラーが発生しました',
                        description='エラーが続く場合は公式サーバで報告してください\n'
                            + 'https://discord.gg/7gypE3Q',
                        color=0xff0000
                    )
                    embed.set_author(name=message.author.name, icon_url=message.author.avatar_url)
                    sent_messages = [await message.channel.send(embed=embed)]
                for msg in sent_messages:
                    message_id_to_author_id[msg.id] = message.author.id
                    user_message_id_to_bot_message[message.id] = msg
                    await msg.add_reaction('🚮')
