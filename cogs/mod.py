import discord
from discord.ext import commands


def canban(ctx, member: discord.Member):
    return member.permissions_in(ctx.channel).ban_members


def cankick(ctx, member: discord.Member):
    return member.permissions_in(ctx.channel).kick_members


class ModerationTools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(description="Do it, I dare you")
    async def addBannedWord(self, ctx, *args: str):
        file = open(f'cogs/bannedwords/{str(ctx.guild.id)}.txt', 'a')
        for i in args:
            file.write(i+"\n")
        file.close()
        await ctx.send(f"Addded {args} to the banned word list for {ctx.guild.id}")

    @commands.command(description="Do it, I dare you")
    async def removeBannedWord(self, ctx, *args: str):
        file = open(f"cogs/bannedwords/{str(ctx.guild.id)}.txt", "r")
        added = []
        for i in file.readlines():
            if "".join(i.split()) in args:
                pass
            else:
                added.append(i)
        file.close()
        del file
        file = open(f"cogs/bannedwords/{str(ctx.guild.id)}.txt", "w")
        file.writelines(added)
        print(added)
        file.close()

    @commands.command(description="Do it, I dare you")
    async def clearBannedWords(self, ctx):
        open(f"cogs/bannedwords/{ctx.guild.id}.txt", "w")
        await ctx.send("Cleared")

    @commands.command(description="Do it, I dare you")
    async def listBannedWords(self, ctx):
        open(f'cogs/bannedwords/{str(ctx.guild.id)}.txt', 'a').close()
        await ctx.send(open(f"cogs/bannedwords/{ctx.guild.id}.txt", "r").readlines())

    @commands.command()
    async def ban(self, ctx, member: discord.Member, reason=""):
        author = ctx.author
        if canban(ctx, author):
            await member.ban(reason=reason)

    @commands.command()
    async def kick(self, ctx, member: discord.Member, reason=""):
        author = ctx.author
        if cankick(ctx, author):
            await member.kick(reason=reason)


def setup(bot):
    bot.add_cog(ModerationTools(bot))
