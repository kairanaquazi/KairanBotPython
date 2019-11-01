import discord
from discord.ext import commands

with open("token.txt", "r") as f:
    token = f.read()

client = commands.Bot(command_prefix="k!")


@client.event
async def on_ready():
    print("online")


@client.command(pass_context=True)
async def join(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        try:
            voice = await channel.connect()
        except:
            await voice.move_to(channel)
    await ctx.send(f"Joined {channel}")


@client.command(pass_context=True)
async def leave(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    await voice.disconnect()
    await ctx.send(f"Left {channel}")
client.run(token)
