import discord
from subprocess import TimeoutExpired, check_output, CalledProcessError, STDOUT
from os.path import dirname
from os import listdir
from proto import cmdin_pb2, cmdout_pb2, help_pb2
from config import PREFIX

def count_bquates(st):
    mx = 0
    i = 0
    for x in st:
        if x == '`':
            i += 1
            if mx < i:
                mx = i
        else:
            i = 0
    return mx

async def loader(cmd, message, arg):

    in_pb: cmdin_pb2.Input = cmdin_pb2.Input()
    in_pb.prefix = PREFIX
    buf = cmdin_pb2.InputMedia()
    buf.type = buf.UTF8
    buf.data = arg.encode(encoding='utf-8')
    in_pb.media.append(buf)
    stdin = in_pb.SerializeToString()

    if not cmd in listdir(dirname(__file__) + '/bin'):
        return []
    cmd_path = dirname(__file__) + '/bin/' + cmd
    out_pb = cmdout_pb2.Output()
    try:
        out_bin = check_output([cmd_path], timeout=5, input=stdin, stderr=STDOUT)
        out_pb.ParseFromString(out_bin)
    except TimeoutExpired:
        out_msg = cmdout_pb2.BotMsg()
        buf = cmdout_pb2.OutputMedia()
        buf.type = buf.UTF8
        buf.data = 'timeout'.encode(encoding='utf-8')
        buf.error = 1
        out_msg.medias.append(buf)
        out_pb.msgs.append(out_msg)
    except CalledProcessError as e:
        out_msg = cmdout_pb2.BotMsg()
        buf = cmdout_pb2.OutputMedia()
        buf.type = buf.UTF8
        err = e.output
        buf.data = err
        buf.error = 1
        out_msg.medias.append(buf)
        out_pb.msgs.append(out_msg)

    result = []
    for msg_pb in out_pb.msgs:
        fields = []
        f = {'title': '','val': ''}

        error = False
        for i, media in enumerate(msg_pb.medias):
            error = error or media.error
            if media.type == media.UTF8:
                if media.level == 0:
                    line = '' if f['val'] == '' else '\n'
                    line += media.data.decode(encoding='utf-8')
                    if media.long_code:
                        line = '```' + line.replace('```', ' `` ') + '```'
                    elif media.short_code:
                        qs = '`' * (count_bquates(line) + 1)
                        bf = line
                        line = qs
                        if bf[0] == '`':
                            line += ' '
                        line += bf
                        if line[-1] == '`':
                            line += ' '
                        line += qs
                    elif media.spoiled:
                        line = '||' + line.replace('||', '\\|\\|') + '||'
                    f['val'] += line
                else:
                    f['title'] += media.data.decode(encoding='utf-8')
                    continue
            if i == len(msg_pb.medias) or not media.extend_field:
                fields.append(f)
                f = {'title': '','val': ''}

        embed = discord.Embed()
        if len(fields) == 1 and fields[0]['title'] == '':
            embed.description = fields[0]['val']
        else:
            for f in fields:

                embed.add_field(name=cmd if f['title'] == '' else f['title'] , value=f['val'])
        embed.color = msg_pb.color & 0x00ffffff
        if error:
            embed.color = 0xff0000
            embed.title = 'Error'
        embed.set_author(
            name=message.author.name,
            icon_url=message.author.avatar_url
        )
        result.append(await message.channel.send(embed=embed))

    return result
