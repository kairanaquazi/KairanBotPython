import discord
from discord.ext import commands


def canban(ctx, member: discord.Member):
    return member.permissions_in(ctx.channel).ban_members


def cankick(ctx, member: discord.Member):
    return member.permissions_in(ctx.channel).kick_members


def candelete(ctx, member: discord.Member):
    return member.permissions_in(ctx.channel).manage_messages


class ModerationTools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def words(self, ctx):
        if ctx.invoked_subcommand is None:
            open(f'cogs/bannedwords/{str(ctx.guild.id)}.txt', 'a').close()
            await ctx.send(open(f"cogs/bannedwords/{ctx.guild.id}.txt", "r").readlines())

    @words.command(description="Do it, I dare you")
    async def add(self, ctx, *args: str):
        author = ctx.author
        if not candelete(ctx, author):
            return
        file = open(f'cogs/bannedwords/{str(ctx.guild.id)}.txt', 'a')
        for i in args:
            file.write(i+"\n")
        file.close()
        await ctx.send(f"Addded {args} to the banned word list for {ctx.guild.id}")

    @words.command(description="Do it, I dare you")
    async def remove(self, ctx, *args: str):
        author = ctx.author
        if not candelete(ctx, author):
            return
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
        await ctx.send(f"Removed {args} from the list")

    @words.command(description="Do it, I dare you")
    async def clear(self, ctx):
        author = ctx.author
        if not candelete(ctx, author):
            return
        open(f"cogs/bannedwords/{ctx.guild.id}.txt", "w")
        await ctx.send("Cleared")

    @words.command(description="Do it, I dare you")
    async def list(self, ctx):
        open(f'cogs/bannedwords/{str(ctx.guild.id)}.txt', 'a').close()
        await ctx.send(open(f"cogs/bannedwords/{ctx.guild.id}.txt", "r").readlines())

    @commands.command()
    async def ban(self, ctx, member: discord.Member, reason=""):
        author = ctx.author
        if canban(ctx, author):
            await member.ban(reason=reason)
        else:
            text = "You do not have sufficient permissions to execute this command"
            text += ", if you believe this is in error, please contact either thepronoobkq#3751 (owner of the bot) by "
            text += "DM, or contact a server admin or owner (to get you perms)"
            await ctx.send(text)

    @commands.command()
    async def unban(self, ctx, member: discord.Member, reason=""):
        author = ctx.author
        if canban(ctx, author):
            await member.unban(reason=reason)
        else:
            text = "You do not have sufficient permissions to execute this command"
            text += ", if you believe this is in error, please contact either thepronoobkq#3751 (owner of the bot) by "
            text += "DM, or contact a server admin or owner (to get you perms)"
            await ctx.send(text)

    @commands.command()
    async def kick(self, ctx, member: discord.Member, reason=""):
        author = ctx.author
        if cankick(ctx, author):
            await member.kick(reason=reason)
        else:
            text = "You do not have sufficient permissions to execute this command"
            text += ", if you believe this is in error, please contact either thepronoobkq#3751 by "
            text += "DM, or contact a server admin or owner"
            await ctx.send(text)


def setup(bot):
    bot.add_cog(ModerationTools(bot))
