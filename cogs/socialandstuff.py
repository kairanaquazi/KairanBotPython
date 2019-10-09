import praw
import discord
from discord.ext import commands
import random
import time
import asyncio
import markovify

'''with open("trump.txt") as f:
    txt = f.readlines()

txt = [""]
mod = markovify.NewlineText(txt)'''


class SocialAndStuff(commands.Cog, name="Social Media and Stuff"):
    def __init__(self, bot):
        self.bot = bot

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
        await ctx.send("Added")

    '''@commands.command(description="Sentence from him")
    async def trump(self, ctx):
        msg = 'Tramp says: {0}'.format(mod.make_sentence())
        await ctx.send(msg)

    @commands.command(description="Tweet (<=140) from him")
    async def tweet(self, ctx):
        message = ctx.message
        msg = 'Tramp says: {0}'.format(mod.make_short_sentence(140))
        await ctx.send(msg)

    @commands.command(name='paragraph', aliases=['pgf'], description="Too much trump")
    async def pgf(self, ctx):
        """Generates 5-10 sentences generated from Trump's tweets."""
        message = ctx.message
        msg = 'Tramp says: {0}'.format(' '.join([mod.make_sentence() for i in range(random.randint(5, 10))]))
        await ctx.send(msg)'''


def setup(bot):
    bot.add_cog(SocialAndStuff(bot))
