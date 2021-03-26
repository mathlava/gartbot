'''
    GartBot - Discord Bot
    Copyright (C) 2021 Gakuto Furuya

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as
    published by the Free Software Foundation, either version 3 of the
    License, or (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''
import asyncio
import logging
import os
import secrets
import traceback
from collections import OrderedDict
from importlib import import_module

import discord

from config import DISCORD_TOKEN, PREFIX


# dictionary to adjust size automatically
class LimitedSizeDict(OrderedDict):


    def __init__(self, *args, **kwds):

        self.size_limit = kwds.pop("size_limit", None)
        OrderedDict.__init__(self, *args, **kwds)
        self._check_size_limit()

    def __setitem__(self, key, value):

        OrderedDict.__setitem__(self, key, value)
        self._check_size_limit()

    def _check_size_limit(self):

        if self.size_limit is not None:
            while len(self) > self.size_limit:
                self.popitem(last=False)


client = discord.Client()

# save the author of the message the bot sent
message_id_to_author_id = LimitedSizeDict(size_limit=100)
# link user's message to the bot's message
user_message_id_to_bot_message = LimitedSizeDict(size_limit=100)


@client.event
async def on_ready():
    print('It\'s activated.')


@client.event
async def on_message(message):

    await reply(message)
    await inside_joke(message)


@client.event
async def on_message_edit(before, after):

    # if the sent message is a call to the bot
    if before.id in user_message_id_to_bot_message:
        try:
            # delete the bot message
            await globals()['user_message_id_to_bot_message'][before.id].delete()
        except discord.errors.NotFound:
            pass
    # respond to the edited messege
    await reply(after)


@client.event
async def on_reaction_add(reaction, user):

    if user == client.user:
        return

    # if the reacted message is the bot's
    # and the person who reacted is the person who typed the command
    if reaction.message.author == client.user \
        and reaction.message.id in message_id_to_author_id \
        and user.id == message_id_to_author_id[reaction.message.id]:

        if str(reaction.emoji) in ('🚮', '✖️', '🗑️'):
            await reaction.message.delete()


# respond to the sent command
async def reply(message):

    # if the author is a bot other than PythonBot and botphilia
    if message.author.bot and not message.author.id in (614130545227726849, 674207357202464769):
        return

    if message.content.startswith(PREFIX):

        command = message.content.split()[0][len(PREFIX):]
        arg = message.content[len(PREFIX) + len(command):].lstrip()

        # if the command file exists atthe specified location
        if os.path.exists(f'{os.path.dirname(os.path.abspath(__file__))}/commands/command_{command}.py'):

            tmp_module = import_module(f'commands.command_{command}')
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
                global message_id_to_author_id
                global user_message_id_to_bot_message
                # save the author of the message the bot sent
                message_id_to_author_id[sent_message.id] = message.author.id
                # link user's message to the bot's message
                user_message_id_to_bot_message[message.id] = sent_message
                await sent_message.add_reaction('🚮')


async def inside_joke(message):

    if ':poponta:' in message.content or ':poponting:' in message.content:
        await message.add_reaction('🤔')
    
    if 'にゃーん' in message.content:
        await message.add_reaction('😿')

    if message.content.startswith('.OX'):

        def shobo_check(reaction, user):
            return user.id == 667746111808864262 # しょぼっと
        
        try:
            reaction, user = await client.wait_for('reaction_add', check=shobo_check, timeout=5.0)
            print(user)
        except asyncio.TimeoutError:
            await message.add_reaction(secrets.choice(('⭕', '❌')))
        else:
            if str(reaction.emoji) == '⭕':
                await reaction.message.add_reaction('❌')
            elif str(reaction.emoji) == '❌':
                await reaction.message.add_reaction('⭕')


client.run(DISCORD_TOKEN)
