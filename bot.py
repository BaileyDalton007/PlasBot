import discord
import discord.utils
from discord.ext import commands

commands = discord.ext.commands
f = open("botkey.txt", "r")
botKey = f.read()

client = commands.Bot(command_prefix = ("!p ", "!p", "!"), case_insensitive = True, help_command=None)

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game('with your feelings'))
    print("Bot has successfully started")

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("That is an invalid command!")
    else:
        print(error)

@client.command()
async def ping(ctx):
    await ctx.send(f'Bot latency is {round(client.latency * 1000)}ms')

client.run(botKey)