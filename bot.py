import discord
import discord.utils
from discord.ext import commands
import os
import subprocess
import shlex
import random
import asyncpg
import asyncio

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
async def pong(ctx):
    await ctx.send('<https://www.youtube.com/watch?v=dQw4w9WgXcQ>')

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
        user = dict(await client.pg_con.fetchrow("SELECT * FROM playerdata WHERE id = $1", str(ctx.author.id)))
        if user:
            await client.pg_con.execute("UPDATE ONLY playerdata SET currpunishment = 'banned' WHERE $1 = ign", name)
        await ctx.send(f'{name} has been banned')
    else:
        await ctx.send('You do not have permission to use that command')

@client.command()
async def unban(ctx, name):
    staff = discord.utils.get(ctx.author.guild.roles, id=662708083264585733)
    if staff in ctx.author.roles:
        b = open("blacklist.txt")
        output = []
        string=f'{name}'
        for line in b:
            if not line.startswith(string):
                output.append(line)
        b.close()
        b = open("blacklist.txt", 'w')
        b.writelines(output)
        b.close()
        subprocess.call(shlex.split(f'./whitelist.sh "{name}"'))
        user = dict(await client.pg_con.fetchrow("SELECT * FROM playerdata WHERE id = $1", str(ctx.author.id)))
        if user:
           await client.pg_con.execute("UPDATE ONLY playerdata SET currpunishment = 'none' WHERE $1 = ign", name)
        await ctx.send(f"{name} has been unbanned")
    else:
        await ctx.send('You do not have permission to use that command')

def check(author):
    def inner_check(message): 
        if message.author != author:
            return False
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
async def tp(ctx, name1, name2:str=''):
    if name2 == '':
        user = dict(await client.pg_con.fetchrow("SELECT * FROM playerdata WHERE id = $1", str(ctx.author.id)))
        if user:
            ign = user.get("ign")
            v2 = random.randint(1111,9999)
            subprocess.call(shlex.split(f'./verify.sh "{name1}" {v2}'))
            await ctx.send(f'{name1}, a 4-digit code has been sent to you in game, copy it here to continue')
            msg2 = await client.wait_for('message',check = check2(ctx.author), timeout=60)
            attempt2 = msg2.content
            if int(attempt2) == v2:
                await ctx.send(f'Code Accepted for {name1}, Teleporting {ign} to {name1}')
                subprocess.call(shlex.split(f'./teleport.sh "{ign}" "{name1}"'))
            else:
                await  ctx.send('That is the incorrect code, check your minecraft chat for a 4 digit number sent to you, if not and you think this is a bug please message a staff member')
        else:
            await ctx.send("You are not verified!, make sure you specify bot people who are teleporting")
    else:
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
async def spawn(ctx, name:str = ''):
    if name == '':
        user = dict(await client.pg_con.fetchrow("SELECT * FROM playerdata WHERE id = $1", str(ctx.author.id)))
        if user:
            ign = user.get("ign")
            await ctx.send(f'Teleporting {ign} to spawn now')
            subprocess.call(shlex.split(f'./tspawn.sh "{ign}"'))
        else:
            await ctx.send('You are not a verified user! try `!p verify [your ign]`')
    else:
        user = dict(await client.pg_con.fetchrow("SELECT * FROM playerdata WHERE id = $1", str(ctx.author.id)))
        ign = user.get("ign")
        if user:
            await ctx.send(f'{ign} is already a verified account!, next time try just doing `!p spawn`')
        v1 = random.randint(1111,9999)
        subprocess.call(shlex.split(f'./verify.sh "{name}" {v1}'))
        await ctx.send(f'{name} A 4-digit code has been sent to you in game, copy it here to continue')
        msg = await client.wait_for('message', check=check(ctx.author), timeout=60)
        attempt1 = msg.content
        if int(attempt1) == v1:
            await ctx.send(f'Teleporting {name} to spawn now')
            subprocess.call(shlex.split(f'./tspawn.sh "{name}"'))
        else:
            await ctx.send("That code is incorrect!, try the command again")

@client.command()
async def rtp(ctx, name:str=''):
    if name == '':
        user = dict(await client.pg_con.fetchrow("SELECT * FROM playerdata WHERE id = $1", str(ctx.author.id)))
        if user:
            ign = user.get("ign")
            x = random.randrange(100000) - 50000
            y = random.randrange(100000) - 50000
            await ctx.send(f'Randomly Teleporting {ign} now')
            subprocess.call(shlex.split(f'./rtp.sh "{ign}" {x} {y}'))
        else:
            await ctx.send('You are not a verified user! try `!p verify [your ign]`')
    else:
        user = dict(await client.pg_con.fetchrow("SELECT * FROM playerdata WHERE id = $1", str(ctx.author.id)))
        ign = user.get("ign")
        if user:
            await ctx.send(f'{ign} is already a verified account!, next time try just doing `!p spawn`')
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
        else:
            await ctx.send("That code is incorrect!, try the command again")


@client.command()
async def banlist(ctx):
    staff = discord.utils.get(ctx.author.guild.roles, id=662708083264585733)
    if staff in ctx.author.roles:
        b = open("blacklist.txt")
        await ctx.send(b.readlines())
    else:
        await ctx.send('You do not have permission to use that command')

@client.command()
async def verify(ctx, ign):
    author = ctx.message.author
    role = discord.utils.get(author.guild.roles, id=715668348217851964)
    staff = discord.utils.get(author.guild.roles, id=662708083264585733)
    donator = discord.utils.get(author.guild.roles, id=715971753607823360)
    if role in author.roles:
        await ctx.send('You are already verified!, if you need to switch accounts contact a staff member')
    else:
        user = await client.pg_con.fetch("SELECT * FROM playerdata WHERE ign = $1", str(ign))
        if user:
            await ctx.send("That minecraft account is already linked, if this is wrong ask a staff member for help!")
        else:
            v1 = random.randint(1111,9999)
            subprocess.call(shlex.split(f'./verify.sh "{ign}" {v1}'))
            await ctx.send(f'{ign} A 4-digit code has been sent to you in game, copy it here to be verified!')
            msg = await client.wait_for('message', check=check(ctx.author), timeout=60)
            attempt1 = msg.content
            if int(attempt1) == v1:
                if staff in author.roles:
                    rank = 'Staff'
                else:
                    if donator in author.roles:
                        rank = 'Donator'
                    else:
                        rank = 'Player'
                await client.pg_con.execute("INSERT INTO playerdata (id, ign, homenum, currpunishment, rank, home1, home2, home3) VALUES ($1, $2, 0, 'none', $3, 'none', 'none', 'none')", str(author.id), str(ign), rank)
                await ctx.send("You are now verified!")
                await author.add_roles(role)
                await author.edit(nick = ign)
            else:
                await ctx.send("That code is incorrect!, try the command again")

@client.command()
async def info(ctx, name):
    staff = discord.utils.get(ctx.author.guild.roles, id=662708083264585733)
    if staff in ctx.author.roles:
        if name[0] == '<':
            d_id = name[3:21]
            user = dict(await client.pg_con.fetchrow("SELECT * FROM playerdata WHERE id = $1", str(d_id)))
        else:
            user = dict(await client.pg_con.fetchrow("SELECT * FROM playerdata WHERE ign = $1", str(name)))
        if user:
            embed = discord.Embed(title="Playerinfo", description="player information for verified users", color=0x00ff00)
            for key in user:
                embed.add_field(name=f"{key}", value=f'{user.get(key)}', inline=False)
            await ctx.send(embed=embed)
        else:
            await ctx.send('That is not a verified user')
    else:
        await ctx.send('You do not have permission to use that command')

@client.command()
async def sethome(ctx, name:str='home1'):
    author = ctx.message.author
    user = dict(await client.pg_con.fetchrow("SELECT ign FROM playerdata WHERE id = $1", str(author.id)))
    if user:
        ign = user.get('ign')
        subprocess.call(shlex.split(f'./sethome.sh "{ign}"'))
        await ctx.send('Please wait ~10 seconds while your home is set!')
        await asyncio.sleep(10)
        lineList = [line.rstrip('\n') for line in open('../1.14.60.5/log.txt')]
        logLen = len(lineList)
        log = str(lineList[logLen-1])
        if str(ign) in log:
            nameLen = len(ign)
            coords = log[nameLen + 15:]
            if name == 'home1':
                await client.pg_con.execute("UPDATE ONLY playerdata SET home1 = $1 WHERE ign = $2", str(coords), ign)
                await ctx.send('Your home has been set')
            else:
                sponsor = discord.utils.get(ctx.author.guild.roles, id=716155240319287316)
                donator = discord.utils.get(ctx.author.guild.roles, id=715971753607823360)
                staff = discord.utils.get(ctx.author.guild.roles, id=662708083264585733)
                if name == 'home2':
                    if sponsor in author.roles or donator in author.roles or staff in author.roles:
                        await client.pg_con.execute("UPDATE ONLY playerdata SET home2 = $1 WHERE ign = $2", str(coords), ign)
                        await ctx.send('Your home has been set')
                    else:
                        await ctx.send("You must be a Donator, Sponsor, or a Staff member to set a second home!")
                else:
                    if name == 'home3':
                        if sponsor in author.roles or staff in author.roles:
                            await client.pg_con.execute("UPDATE ONLY playerdata SET home3 = $1 WHERE ign = $2", str(coords), ign)
                            await ctx.send('Your home has been set')
                        else:
                            await ctx.send('You must be a Sponsor or a Staff member to set a third home!')
                    else:
                        await ctx.send(f'{name} is not a vaild home name, must be "home1", "home2", or "home3"')

        else:
            await ctx.send('Home set failed, make sure you are on the server and please try again')
    else:
        await ctx.send("You are not verified, try using `!p verify [your name]` to use this command")

@client.command()
async def home(ctx, name:str='home1'):
    author = ctx.message.author
    user = dict(await client.pg_con.fetchrow("SELECT * FROM playerdata WHERE id = $1", str(author.id)))
    if user:
        ign = user.get('ign')
        home = user.get(name)
        if home != 'none':
            homeArr = home.split(', ')
            subprocess.call(shlex.split(f'./thome.sh "{ign}" {homeArr[0]} {homeArr[1]} {homeArr[2]}'))
            await ctx.send(f'Sent {ign} to {name}!')
        else:
            await ctx.send(f'{name} is not set!, try using `!p sethome [home]`')
    else:
        await ctx.send("You are not verified!, do `!p verify [your name]`")
    

client.loop.run_until_complete(create_db_pool())
client.run(botKey)