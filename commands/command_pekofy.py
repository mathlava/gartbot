import discord
from sudachipy import tokenizer
from sudachipy import dictionary

async def main(message: discord.Message, arg: str):

    tokenizer_obj = dictionary.Dictionary().create()
    mode = tokenizer.Tokenizer.SplitMode.C
    if message.reference:
        referenced_message = await message.channel.fetch_message(message.reference.message_id)
        sentences = referenced_message.content
    else:
        sentences = arg
    if len(sentences) == 0:
        embed = discord.Embed(
            title='エラー',
            description='文章が含まれるメッセージに返信するか引数に指定してください',
            color=0xff0000
        )
        embed.set_author(
            name=message.author.name,
            icon_url=message.author.avatar_url
        )
        return await message.reply(embed=embed)
    for sentence in sentences.splitlines():
        tokens = tokenizer_obj.tokenize(sentence, mode)
        pekofied_sentences = ''
        pekofied_sentence = ''
        final_form_flag = False
        for t in tokens:
            if noun_flag:
                if t.part_of_speech()[1] == '句点':
                    pekofied_sentence += 'ぺこ' + t.surface()
                elif t.part_of_speech()[1] == '終助詞':
                    pekofied_sentence += 'ぺこ' + t.surface()
                else:
                    pekofied_sentence += t.surface()
                noun_flag = False
            elif final_form_flag:
                if t.part_of_speech()[0] == '助動詞':
                    pekofied_sentence += t.surface()
                elif t.part_of_speech()[1] == '終助詞':
                    if t.dictionary_form() == 'じゃん':
                        pekofied_sentence += 'ぺこ' + t.surface()
                    else:
                        pekofied_sentence += t.surface()
                elif t.part_of_speech()[1] == '接続助詞':
                    if t.dictionary_form() == 'と':
                        pekofied_sentence += t.surface()
                    else:
                        pekofied_sentence += 'ぺこだ' + t.surface()
                else:
                    pekofied_sentence += 'ぺこ' + t.surface()
                final_form_flag = False
            elif t.part_of_speech()[0] == '名詞':
                pekofied_sentence += t.surface()
                noun_flag = True
            elif '終止形' in t.part_of_speech()[5]:
                pekofied_sentence += t.surface()
                final_form_flag = True
            else:
                pekofied_sentence += t.surface()
        if final_form_flag:
            pekofied_sentence += 'ぺこ'
        pekofied_sentences += pekofied_sentence + '\n'
    embed = discord.Embed(
        description=pekofied_sentences
    )
    embed.set_author(
        name=message.author.name,
        icon_url=message.author.avatar_url
    )
    return await message.reply(embed=embed)
