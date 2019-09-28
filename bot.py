import discord
from discord.ext.commands import *
from jishaku.help_command import DefaultPaginatorHelp
import json
import os
import random
import asyncio

TOKEN = open("token.txt", "r").read()
client = discord.Client()
bannedWords = {}
with open("options.json") as f:
    options = json.loads(f.read())

'''@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')
    game = discord.Game("with a kitten | Prefix is currently k!")
    await client.change_presence(activity=game)



@client.event
async def on_message(message):
    channel = message.channel
    server = channel.guild
    user = message.author

    try:
        bannedWords[server.id]
    except KeyError:
        print("Creating BannedWords for {0}".format(server.id))
        bannedWords[server.id] = []
    che = 0
    for i in bannedWords[server.id]:
        if i in message.content:
            che = 1
    if user.id != 589967187457081365 and not("removeBannedWord" in message.content) and bannedWords != [] and che == 1:
        await message.delete()
    if message.content[0:2] == "k!":
        cmd = message.content[2:len(message.content)].split(" ")[0]
        args = message.content[2:len(message.content)].split(" ")[1:len(message.content)]
        if cmd == "echo":
            if user.id == 589967187457081365:
                return
            msg = ""
            for i in args:
                msg += i+" "
            await channel.send(msg)
        elif cmd == "addBannedWord":
            if user.guild_permissions.manage_messages:
                for i in args:
                    bannedWords[server.id].append(i)
            await channel.send("Add these banned words")
        elif cmd == "removeBannedWord":
            if user.guild_permissions.manage_messages:
                for i in args:
                    bannedWords[server.id].remove(i)
            await channel.send("Removed these banned words")
        elif cmd == "clearBannedWords":
            if user.guild_permissions.manage_messages:
                bannedWords[server.id] = []
            await channel.send("Cleared the banned word list")
        elif cmd == "listBannedWords":
            msg = ""
            for i in bannedWords[server.id]:
                msg += i + "\n"
            await channel.send(msg)
        elif cmd == "eval":
            msg = ""
            for i in args:
                msg += i+" "
            eval(msg)

client.run(token)'''


class KairanBot(Bot):
    def __init__(self, *args, prefix=None, **kwargs):
        super().__init__(prefix, *args, **kwargs)

    async def on_message(self, msg: discord.Message):
        ctx = await self.get_context(msg)
        if msg.author.id in options["Blacked"] and "k!" in msg:
            await ctx.send("Banned lol")
        try:
            await self.process_commands(msg)
            if 'delete_orig' in options and options['delete_orig'] and isinstance(ctx, Context) and ctx.valid:
                await msg.delete()
        except BaseException as e:
            print(e)

    async def on_command_error(self, ctx, error):
        await ctx.send(error)


games = ["Fortnite", "with a kitten", "Secret Hitler", "with toys", "with Kairan", "Kill the Fascists"]
game = random.choice(games)+" | k!help"
client = KairanBot(prefix=when_mentioned_or('!' if 'prefix' not in options else options['prefix']),
                   pm_help=True if 'pm_help' not in options else options['pm_help'],
                   activity=discord.Game('nothing. Serving Ioun.' if 'game' not in options else game),
                   help_command=DefaultPaginatorHelp())


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print("Playing: {}".format(game))
    print('------')

for file in os.listdir("cogs"):
    if file.endswith(".py") and not(file in options["disabledCogs"]):
        name = file[:-3]
        client.load_extension(f"cogs.{name}")
        print(name)

client.load_extension("jishaku")

client.run(TOKEN)

