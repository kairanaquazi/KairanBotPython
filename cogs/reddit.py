import praw
import discord
from discord.ext import commands
import random
import time
import asyncio


class Redit(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Try k!echo k!echo k!echo ... echo")
    async def update(self, ctx, subred="dankmemes", length=5):
        length = int(length)
        assert(0 < length < 10)
        reddit = praw.Reddit('bot1')
        subreddit = reddit.subreddit(subred)
        embed = discord.Embed(title=subreddit.title, description="wow", color=0x00ffd9)
        message = ""
        for submission in subreddit.hot(limit=5):
            message += submission.title + "\n" + submission.url + "\n\n\n"
        await ctx.send(message)


def setup(bot):
    bot.add_cog(Redit(bot))
