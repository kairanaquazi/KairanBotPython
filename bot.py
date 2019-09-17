import discord
token = open("token.txt", "r").read()
client = discord.Client()
bannedWords = {}


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


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
    checksandbalances=0
    for i in bannedWords[server.id]:
        if i in message.content:
            checksandbalances=1
    if user.id != 589967187457081365 and not("removeBannedWord" in message.content) and bannedWords != [] and checksandbalances == 1:
        await message.delete()
    if message.content[0:2] == "k!":
        cmd = message.content[2:len(message.content)].split(" ")[0]
        args = message.content[2:len(message.content)].split(" ")[1:len(message.content)]
        if cmd == "echo":
            msg = ""
            for i in args:
                msg += i+" "
            await channel.send(msg)
        elif cmd == "addBannedWord":
            print(user.guild_permissions)


client.run(token)