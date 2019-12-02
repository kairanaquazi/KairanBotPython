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
    vc = await ctx.author.voice.channel.connect()
    vc.play(discord.FFmpegPCMAudio('testing.mp3'), after=lambda e: print('done', e))
    vc.is_playing()
    vc.pause()
    vc.resume()
    vc.stop()
    await ctx.send(f"Joined")


@client.command(pass_context=True)
async def leave(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
    await voice.disconnect()
    await ctx.send(f"Left {channel}")
client.run(token)
