import asyncio
import os
from collections import OrderedDict
from importlib import import_module
import logging

import discord

from config import DISCORD_TOKEN, PREFIX
from reply import reply


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


@client.event
async def on_ready():

    global message_id_to_author_id
    message_id_to_author_id = LimitedSizeDict(size_limit=100)

    global user_message_id_to_bot_message
    user_message_id_to_bot_message = LimitedSizeDict(size_limit=100)

    print('起動しました')


@client.event
async def on_message(message):
    await reply(message)
    if 'にゃーん' in message.content:
        await message.add_reaction('😿')


@client.event
async def on_message_edit(before, after):

    if before.id in user_message_id_to_bot_message:
        try:
            await globals()['user_message_id_to_bot_message'][before.id].delete()
        except discord.errors.NotFound:
            pass

    await reply(after)


@client.event
async def on_reaction_add(reaction, user):

    if user == client.user:
        return

    if reaction.message.author == client.user \
        and reaction.message.id in message_id_to_author_id \
        and user.id == message_id_to_author_id[reaction.message.id]:

        if str(reaction.emoji) in ('🚮', '✖️', '🗑️'):
            await reaction.message.delete()


client.run(DISCORD_TOKEN)
