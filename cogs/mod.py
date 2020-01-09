import discord
from discord.ext import commands
import asyncio,json

permerrortext = "You do not have sufficient permissions to execute this command"
permerrortext += ", if you believe this is in error, please contact either thepronoobkq#3751 (owner of the bot) by "
permerrortext += "DM, or contact a server admin or owner (to get you perms)"


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
    async def ban(self, ctx, member: discord.Member, *, reason=""):
        author = ctx.author
        if canban(ctx, author):
            await member.ban(reason=reason)
            await ctx.send("Banned")
        else:
            await ctx.send(permerrortext)

    @commands.command()
    async def unban(self, ctx, member: discord.User, *, reason=""):
        author = ctx.author
        if canban(ctx, author):
            await ctx.guild.unban(member, reason=reason)
            await ctx.send("Unbanned")
        else:
            await ctx.send(permerrortext)

    @commands.command()
    async def kick(self, ctx, member: discord.Member, *, reason=""):
        author = ctx.author
        if cankick(ctx, author):
            await member.kick(reason=reason)
            await ctx.send("Kicked")
        else:
            await ctx.send(permerrortext)

    @commands.command()
    async def softban(self, ctx, member: discord.Member, *, reason=""):
        author = ctx.author
        if canban(ctx, author):
            await member.ban(reason=reason)
            await member.unban(reason=reason)
            await ctx.send("Softbanned")
        else:
            await ctx.send(permerrortext)

    @commands.command()
    async def bans(self, ctx, limit=10):  # mainly a debug tool for finding who a "deleted user" is
        async for entry in ctx.guild.audit_logs(action=discord.AuditLogAction.ban, limit=limit):
            await ctx.send('{0.user} banned {0.target}'.format(entry))
            await asyncio.sleep(0.5)

    @commands.command()
    async def mailmod(self, ctx, type, *, text):
        channel = ctx.channel
        message = ctx.message
        message.delete()
        with open("modsoptions.json") as f:
            mods = json.loads(f.read())
        guild = ctx.author.guild
        mods = mods[guild.id]
        for mod in mods:
            curmod = guild.get_member(mod)
            if curmod.dm_channel == None:
                await curmod.create_dm()
            dmchan = curmod.dm_channel
            msg=f'''{ctx.author.display_name} has filed a mod report that states:\ntext\n please DM the other mods and pick who takes the report.'''
            dmchan.send(msg)


def setup(bot):
    bot.add_cog(ModerationTools(bot))
