import discord
from discord.ext.commands import *
from jishaku.help_command import DefaultPaginatorHelp
import json
import yaml
import os
import random
import asyncio
import aiohttp
import praw
import datetime
import requests
import threading
import keep_alive
from locallog.scripts.logger import Logger, MimicLogger
print(discord.__version__)
with open("token.txt", "r") as f:
    TOKEN = f.read()
client = discord.Client()
bannedWords = {}
with open("options.json") as f:
    options = json.loads(f.read())
with open("censor.yaml") as f:
    opyaml = yaml.load(f.read(), Loader=yaml.SafeLoader)

logger = MimicLogger()
if options["logging"]:
    del logger
    logger = Logger()

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
        self.http2 = None
        self.bg_task = self.loop.create_task(self.playingstatus())
        self.reddit_task = self.loop.create_task(self.redditupdate())
        self.change_status = True
        self.games = ["Fortnite", "with a kitten", "Secret Hitler", "with toys", "with Kairan", "Kill the Fascists"]
        self.reddit = praw.Reddit('bot1')
        self.subreddit = self.reddit.subreddit("dankmemes")
        open("lastred.txt", "a").close()
        with open("lastred.txt", "r") as fo:
            self.lastsent = "".join(fo.readlines())
        if options["repeatreddit"]:
            self.lastsent = 0
        self.invite = 0
        if not self.http2:
            self.http2 = aiohttp.ClientSession()
        self.restart = datetime.datetime.now()

    async def on_ready(self):
        self.invite = discord.utils.oauth_url(self.user.id, discord.Permissions(permissions=8))
        print('Logged in as')
        print(client.user.name)
        print(client.user.id)
        print("Playing: {}".format(game))
        self.restart = datetime.datetime.now()
        print(self.restart)
        print("OAuth link: ", self.invite)
        print('------')

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

    async def on_member_ban(self, guild, user):
        print(f"By golly, {user.name} go banned!!!!")
        if guild.id == 554826709082570760:  # insert your guild (or remove this if you dont want a custom message)
            await guild.get_channel(554826709510258698).send(f"By golly, {user.name} was banned!\nF in the chat :(")

    async def logout(self):
        if not self.http2.closed:
            await self.http2.close()
            await asyncio.sleep(0)
        with open("lastred.txt", "w") as fooo:
            fooo.write(str(self.lastsent))
        logger.close()
        await super().logout()

    async def on_command_error(self, ctx, error):
        await ctx.send(error)
        logger.log("ERROR", "Command: "+ctx.message.content+" by "+ctx.message.author.name+" failed")
        if error == CommandNotFound:
            pass
        key = await self.post_to_hastebin(str(error))
        print(key)
        if key == "":
            return
        await ctx.send(key)

    async def post_to_hastebin(self, data):
        data = data.encode("utf-8")
        site = "http://hastebin.com"
        if options["haste"] == 2:
            return ""
        if not options["haste"]:
            site = "http://localhost"
        async with self.http2.post(site+"/documents", data=data) as resp:
            out = await resp.json()

        assert "key" in out

        '''print("Requesting Haste")
        response = requests.post('http://hastebin.com/documents', data="hello")
        if response.status_code == 200:
            print(response.json()['key'])
        print(response.status_code)'''
        return f"{site}/" + out["key"]

    async def process_commands(self, message):
        logger.log("INFO", "Command used")
        await super().process_commands(message)

    async def playingstatus(self):

        await self.wait_until_ready()
        while self.is_ready() and self.change_status:
            status = random.choice(self.games)
            status += f" | Hiding in {len(self.guilds)} servers and spying on {len(self.users)} users... "
            status += f"last restarted at {self.restart.strftime('%d-%b-%Y (%H:%M:%S)')}"
            await self.change_presence(activity=discord.Game(name=status), status=discord.Status.online)
            await asyncio.sleep(120)

    async def redditupdate(self):

        await self.wait_until_ready()
        print("Started")
        sendchannel = ""
        for i in self.guilds[1].channels:
            if i.id == 631635939558424596:
                sendchannel = i
                break
        self.lastsent = 0
        while self.is_ready() and self.change_status:
            # self.subreddit.hot(limit=options["length"])
            print("Y")
            for i in self.subreddit.hot(limit=options["length"]):
                newtitle = i.title
                for curse in opyaml["censor"]:
                    newtitle = newtitle.replace(curse, opyaml["censor"][curse])
                # Resume here
                if i.url != self.lastsent:
                    await sendchannel.send(newtitle + "\n" + i.url + "\n\n\n")
                    self.lastsent = i.url
                    with open("lastred.txt", "w") as foo:
                        foo.write(self.lastsent)
                else:
                    pass
            await asyncio.sleep(120)


games = ["Fortnite", "with a kitten", "Secret Hitler", "with toys", "with Kairan", "Kill the Fascists"]
game = "Fortnite"+" | k!help"
print(when_mentioned_or("k!"))
client = KairanBot(prefix=when_mentioned_or("k!"),
                   pm_help=True if 'pm_help' not in options else options['pm_help'],
                   activity=discord.Game('nothing. Serving Ioun.' if 'game' not in options else game),
                   help_command=DefaultPaginatorHelp())


'''@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print("Playing: {}".format(game))
    print(datetime.datetime.now())
    print('------')'''

for file in os.listdir("cogs"):
    if file.endswith(".py") and not(file in options["disabledCogs"]):
        name = file[:-3]
        try:
            client.load_extension(f"cogs.{name}")
        except:
            print(f"Failed to load cogs.{name}")
        print(name)

client.load_extension("jishaku")
keep_alive.keep_alive()
hm = 0
client.run(TOKEN)

