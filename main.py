import asyncio
import os
from importlib import import_module
import logging

import discord

from config import DISCORD_TOKEN, PREFIX
from reply import reply, message_id_to_author_id, user_message_id_to_bot_message


client = discord.Client()


@client.event
async def on_ready():
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
