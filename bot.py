import discord
import discord.utils
from discord.ext import commands
import os
import subprocess
import shlex
import random
import asyncpg

commands = discord.ext.commands
f = open("botkey.txt", "r")
botKey = f.read()
p = open("password.txt", "r")
password = p.read()
d = open("ip.txt", "r")
address = d.read()

client = commands.Bot(command_prefix = ("!p ", "!p", "!"), case_insensitive = True, help_command=None)

async def create_db_pool():
    client.pg_con = await asyncpg.create_pool(host=address, database='bedrockdb', user='postgres', password=password)


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
    if name in bMembers:
        await ctx.send(f'{name} is currently banned')
    else:    
        try:
            subprocess.call(shlex.split(f'./whitelist.sh "{name}"'))
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
        subprocess.call(shlex.split(f'./unwhitelist.sh "{name}"'))
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
        subprocess.call(shlex.split(f'./whitelist.sh "{name}"'))

        await ctx.send(f"{name} has been unbanned")
    else:
        await ctx.send('You do not have permission to use that command')

def check(author):
    def inner_check(message):
        if message.author != author:
            return False
        else:
            try: 
                int(message.content) 
                return True 
            except ValueError: 
                return False
        return inner_check

def check2(author):
    def inner_check(message):
        try: 
            int(message.content) 
            return True 
        except ValueError: 
            return False
    return inner_check

@client.command()
async def tp(ctx, name1, name2):
    v1 = random.randint(1111,9999)
    subprocess.call(shlex.split(f'./verify.sh "{name1}" {v1}'))
    await ctx.send(f'{name1} A 4-digit code has been sent to you in game, copy it here to continue')
    msg = await client.wait_for('message', check=check(ctx.author), timeout=60)
    attempt1 = msg.content
    if int(attempt1) == v1:
        await ctx.send(f'Code Accepted for {name1}')
        v2 = random.randint(1111,9999)
        subprocess.call(shlex.split(f'./verify.sh "{name2}" {v2}'))
        await ctx.send(f'{name2}, a 4-digit code has been sent to you in game, copy it here to continue')
        msg2 = await client.wait_for('message',check = check2(ctx.author), timeout=60)
        attempt2 = msg2.content
        if int(attempt2) == v2:
            await ctx.send(f'Code Accepted for {name2}, Teleporting {name1} to {name2}')
            subprocess.call(shlex.split(f'./teleport.sh "{name1}" "{name2}"'))
        else:
            await  ctx.send('That is the incorrect code, check your minecraft chat for a 4 digit number sent to you, if not and you think this is a bug please message a staff member')
    else:
        await ctx.send('That is the incorrect code, check your minecraft chat for a 4 digit number sent to you, if not and you think this is a bug please message a staff member')

@client.command()
async def spawn(ctx, name):
    v1 = random.randint(1111,9999)
    subprocess.call(shlex.split(f'./verify.sh "{name}" {v1}'))
    await ctx.send(f'{name} A 4-digit code has been sent to you in game, copy it here to continue')
    msg = await client.wait_for('message', check=check(ctx.author), timeout=60)
    attempt1 = msg.content
    if int(attempt1) == v1:
        await ctx.send(f'Teleporting {name} to spawn now')
        subprocess.call(shlex.split(f'./tspawn.sh "{name}"'))

@client.command()
async def rtp(ctx, name):
    v1 = random.randint(1111,9999)
    x = random.randrange(100000) - 50000
    y = random.randrange(100000) - 50000
    subprocess.call(shlex.split(f'./verify.sh "{name}" {v1}'))
    await ctx.send(f'{name} A 4-digit code has been sent to you in game, copy it here to continue')
    msg = await client.wait_for('message', check=check(ctx.author), timeout=60)
    attempt1 = msg.content
    if int(attempt1) == v1:
        await ctx.send(f'Randomly Teleporting {name} now')
        subprocess.call(shlex.split(f'./rtp.sh "{name}" {x} {y}'))


@client.command()
async def banlist(ctx):
    staff = discord.utils.get(ctx.author.guild.roles, id=662708083264585733)
    if staff in ctx.author.roles:
        b = open("blacklist.txt")
        await ctx.send(b.readlines())
    else:
        await ctx.send('You do not have permission to use that command')

client.loop.run_until_complete(create_db_pool())
client.run(botKey)