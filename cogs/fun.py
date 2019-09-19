import discord
from discord.ext import commands
import random
import time


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def echo(self, ctx, *, echo: str):
        if echo == "echo":
            return
        async with ctx.typing():
            # do expensive stuff here
            time.sleep(2)
            await ctx.send(echo)

    @commands.command()
    async def add(self, ctx, *, echo: str):
        async with ctx.typing():
            time.sleep(random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]))
            await ctx.send(int(echo[0])+int(echo[2]))


def setup(bot):
    bot.add_cog(Fun(bot))
