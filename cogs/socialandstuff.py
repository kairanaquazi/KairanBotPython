import praw
import discord
from discord.ext import commands
import random
import time
import asyncio


class SocialAndStuff(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.cooldown(1, 5, commands.BucketType.guild)
    @commands.command(description="Dank memes or stuff")
    async def reddit(self, ctx, subred="dankmemes", length=5):
        print(ctx.command.is_on_cooldown(ctx))
        if ctx.command.is_on_cooldown(ctx):
            await ctx.send("Calm down")
            return
        length = int(length)
        assert(0 < length < 10)
        reddit = praw.Reddit('bot1')
        subreddit = reddit.subreddit(subred)
        message = ""
        for submission in subreddit.hot(limit=length):
            if submission.url.endswith(".jpg") or submission.url.endswith(".png"):
                message += submission.title + "\n" + submission.url + "\n\n\n"
        await ctx.send(message)
        await ctx.send(length)

    @commands.command(description="Webhook magic")
    async def updateme(self, ctx, webhook=None):
        if not webhook:
            await ctx.send("Please attach a webhook url")
            return
        file = open("hooks.txt", "a")
        file.write(webhook+"\n")
        file.close()


def setup(bot):
    bot.add_cog(SocialAndStuff(bot))
