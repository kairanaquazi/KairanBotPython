import discord
from discord.ext import commands
import random
import time
import asyncio


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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
        if ctx.message.author.id != self.bot.owner.user.id:
            return
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

    @commands.command(aliases=["invite"])
    async def link(self, ctx):
        await ctx.send(self.bot.invite)

    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        channel = member.guild.system_channel
        if channel is not None:
            await channel.send('Welcome {0.mention}.'.format(member))
        if member.bot and (member.guild.id == 554826709082570760 or member.guild.id == 659933426039914516):
            role = discord.utils.get(member.guild.roles, name="BOT")
            await member.add_roles(role)


def setup(bot):
    bot.add_cog(Fun(bot))
