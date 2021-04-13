import discord
import sympy as sy

class TooLargeNumber(Exception):
    pass

async def sobibun(value: int):

    if value > 100000000:
        raise TooLargeNumber()
    factors = sy.factorint(int(value))
    memo = {j: value * j for j in factors.values()}
    wa = [memo[factors[i]] // i for i in factors.keys()]
    return sum(wa)

async def main(message: discord.Message, arg: str):

    try:
        n = sy.sympify(arg.replace('i', 'I'))
    except sy.SympifyError:
        result = '式の読み込みに失敗しました\n' \
            'ヒント：掛け算の記号 * は省略できません'
        embed = discord.Embed(
            title='エラー',
            description=result,
            color=0xff0000
            )
        embed.set_author(
            name=message.author.name,
            icon_url=message.author.avatar_url
        )
        return await message.reply(embed=embed)
    try:
        if n == 0:
            result = 'undefined'
        elif n.is_Integer:
            d = await sobibun(sy.sign(n) * n)
            result = str(sy.sign(n) * d)
        elif n.is_real:
            n_numerator = sy.fraction(n)[0] * sy.sign(n)
            n_denominator = sy.fraction(n)[1]
            while n_numerator != sy.floor(n_numerator):
                n_numerator *= 10
                n_denominator *= 10
            d_numerator = await sobibun(n_numerator)
            d_denominator = await sobibun(n_denominator)
            d = sy.sign(n) * (d_numerator * n_denominator - n_numerator * d_denominator) / n_denominator ** 2
            result = str(d)
        else:
            n_norm2 = sy.re(n) ** 2 + sy.im(n) ** 2
            n_numerator = sy.fraction(n_norm2)[0]
            n_denominator = sy.fraction(n_norm2)[1]
            d_numerator = await sobibun(n_numerator)
            d_denominator = await sobibun(n_denominator)
            d = n * (d_numerator * n_denominator - n_numerator * d_denominator) / (2 * n_denominator * n_numerator)
            result = str(d)
    except TooLargeNumber:
        embed = discord.Embed(
            title='エラー',
            description='値が大きすぎるか複雑すぎます',
            color=0xff0000
            )
        embed.set_author(
            name=message.author.name,
            icon_url=message.author.avatar_url
        )
        return await message.reply(embed=embed)
    embed = discord.Embed(description=result.replace('I', 'i'))
    embed.set_author(
        name=message.author.name,
        icon_url=message.author.avatar_url
    )
    return await message.reply(embed=embed)
