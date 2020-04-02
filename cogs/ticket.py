import discord
from discord.ext import commands
import asyncio
import redis
import json
import pymongo
with open("options.json") as f:
    options = json.loads(f.read())

class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db=redis.Redis(password=options["redispassword"])

    @commands.command()
    async def sendticket(self, ctx:discord.Context, level, *, text):
        channel = ctx.channel
        message = ctx.message
        await message.delete()
        mods=self.db.lrange(str(ctx.guild.id),0,-1)
        guild = ctx.author.guild
        if mods:
            pass
        else:
            author = ctx.author
            if author.dm_channel is None:
                author.create_dm()
            dmchan = author.dm_channel
            msg = f'''Sorry, this server does not have modmail enabled.'''
            await dmchan.send(msg)

        for mod in mods:
            curmod = guild.get_member(mod)
            if curmod.dm_channel is None:
                await curmod.create_dm()
            dmchan = curmod.dm_channel
            msg = f'''{ctx.author.display_name} has filed a mod report with level: {level} \nthat states:\n{text}\nIt has id {ticketid}'''
            await dmchan.send(msg)

    @commands.command()
    async def getticket(self, ticketid):
        
