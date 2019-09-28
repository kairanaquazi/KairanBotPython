import discord
from discord.ext import commands
import random
import time
import asyncio


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Try k!echo k!echo k!echo ... echo")
    async def echo(self, ctx, *, echo: str):
        if echo == "echo":
            return
        await ctx.send(echo)

    @commands.command(description="Addition")
    async def add(self, ctx, num1, num2):
        async with ctx.typing():
            await asyncio.sleep(random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]))
            await ctx.send(int(num1)+int(num2))

    @commands.command(descripion="All of them!!!")
    async def members(self, ctx):
        msg = ""
        for i in ctx.guild.members:
            msg += i.name + "\n"
        await ctx.send(msg)

    @commands.command(description="Pong", aliases=["delay"])
    async def ping(self, ctx):
        before = time.monotonic()
        message = await ctx.send("Pong!")
        ping = (time.monotonic() - before) * 1000
        await message.edit(content=f"Pong!  `{int(ping)}ms`")

    @commands.command(description="Get a new activity")
    async def stat(self, ctx):
        await ctx.send(self.bot.activity)

    @commands.command()
    async def umm(self, ctx, *name: str):
        n = name
        name = ""
        for i in n:
            name += i+" "
        await ctx.send("Start")
        for i in ctx.guild.members:
            test = 0
            try:
                await i.edit(nick=name)
            except BaseException as e:
                await ctx.send(f"Fail at {i}")
                await ctx.send(f"Reason: {e}")
                test = 1
                pass
            if not test:
                await ctx.send(f"Success at {i}")
            if i.id == 589967187457081365:
                await i.edit(nick="KairanBot")
        await ctx.send("Done")
        return


def setup(bot):
    bot.add_cog(Fun(bot))
