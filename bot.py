import discord
import discord.utils
from discord.ext import commands
import os
import subprocess
import shlex

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


@client.command()
async def whitelist(ctx, name):
    b = open("blacklist.txt", "r")
    bMembers = b.read().splitlines()
    print(bMembers)
    if name in bMembers:
        await ctx.send(f'{name} is currently banned')
    else:    
        try:
            subprocess.call(shlex.split(f'./whitelist.sh {name}'))
            await ctx.send(f'{name} has been whitelisted')
        except:
            await ctx.send('Whitelist failed')

@client.command()
async def ban(ctx, name):
    staff = discord.utils.get(ctx.author.guild.roles, id=662708083264585733)
    if staff in ctx.author.roles:
        b = open("blacklist.txt", "a")
        b.write('\n')
        b.write(f'{name}')
        subprocess.call(shlex.split(f'./unwhitelist.sh {name}'))
        await ctx.send(f'{name} has been banned')
    else:
        await ctx.send('You do not have permission to use that command')

@client.command()
async def unban(ctx, name):
    staff = discord.utils.get(ctx.author.guild.roles, id=662708083264585733)
    if staff in ctx.author.roles:
        b = open("blacklist.txt")
        output = []
        str=f'{name}'
        for line in b:
            if not line.startswith(str):
                output.append(line)
        b.close()
        b = open("blacklist.txt", 'w')
        b.writelines(output)
        b.close()
        await ctx.send(f"{name} has been unbanned")
    else:
        await ctx.send('You do not have permission to use that command')

@client.command()
async def banlist(ctx):
    b = open("blacklist.txt")
    await ctx.send(b.readlines())

client.run(botKey)