import discord
from sudachipy import tokenizer
from sudachipy import dictionary

async def main(message: discord.Message, arg: str):

    tokenizer_obj = dictionary.Dictionary().create()
    mode = tokenizer.Tokenizer.SplitMode.C
    if message.reference:
        referenced_message = await message.channel.fetch_message(message.reference.message_id)
        sentence = referenced_message.content
    else:
        sentence = arg
    tokens = tokenizer_obj.tokenize(sentence, mode)
    pekofied_sentence = ''
    flag = False
    for t in tokens:
        if flag:
            if t.part_of_speech()[1] == '終助詞':
                pekofied_sentence += t.surface()
            elif t.part_of_speech()[1] == '接続助詞':
                if t.dictionary_form() == 'と':
                    pekofied_sentence += t.surface()
                else:
                    pekofied_sentence += 'ぺこだ' + t.surface()
            else:
                pekofied_sentence += 'ぺこ' + t.surface()
            flag = False
        elif '終止形' in t.part_of_speech()[5]:
            pekofied_sentence += t.surface()
            flag = True
        else:
            pekofied_sentence += t.surface()
    if flag:
        pekofied_sentence += 'ぺこ'
    return await message.reply(pekofied_sentence)
