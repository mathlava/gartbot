import discord
import sympy as sy

async def sobibun(value):

    factors = sy.factorint(int(value))
    memo = {j: value * j for j in factors.values()}
    wa = [memo[factors[i]] // i for i in factors.keys()]
    return sum(wa)

async def main(message, arg):

    n = sy.simplify(arg)
    if n == 0:
        result = 'undefined'
    elif n.is_Integer:
        d = await sobibun(sy.sign(n) * n)
        result = str(sy.sign(n) * d)
    elif n.is_real:
        n_nu = sy.fraction(n)[0] * sy.sign(n)
        n_de = sy.fraction(n)[1]
        while n_nu != sy.floor(n_nu):
            n_nu *= 10
            n_de *= 10
        d_nu = await sobibun(n_nu)
        d_de = await sobibun(n_de)
        d = sy.sign(n) * (d_nu * n_de - n_nu * d_de) / n_de ** 2
        result = str(d)
    else:
        n_norm2 = sy.re(n) ** 2 + sy.im(n) ** 2
        n_nu = sy.fraction(n_norm2)[0]
        n_de = sy.fraction(n_norm2)[1]
        d_nu = await sobibun(n_nu)
        d_de = await sobibun(n_de)
        d = n * (d_nu * n_de - n_nu * d_de) / n_de ** 2 / n_norm2
        result = str(d)
    embed = discord.Embed(description=result)
    embed.set_author(
        name=message.author.name,
        icon_url=message.author.avatar_url
    )
    return await message.channel.send(embed=embed)
