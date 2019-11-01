import discord


def isowner(user):
    if type(user) == discord.User:
        user = user.id
    if type(user) == discord.Member:
        user = user.id

