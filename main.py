from discord.ext import commands 
import discord
import asyncio
from discord.utils import get
from keep_alive import keep_alive
import random
import time
import os
import sys
from discord import Intents
import re

client = commands.Bot(command_prefix='?')

@client.command()
async def test(ctx):
  print('command recieved')

@client.command()
@commands.has_permissions(kick_members=True)
async def mute(ctx, member: discord.Member, length, reason=None):
  guild = ctx.guild
  muted = get(guild.roles, name='Muted')
  member = get(guild.roles, name='member')

  dater = re.split('(\D+)',length)
  
  numbers = ' '.join(dater[:1])
  letter = ' '.join(dater[1:2])
  
  flength = 0

  if letter == 's':
    flength = int(numbers)
  
  elif letter == 'm':
    flength = int(numbers) * 60
  
  elif letter == 'h':
    flength = int(numbers) * 60 * 60
  
  elif letter == 'd':
    flength = int(numbers) * 60 * 60 * 24

  elif letter == 'w':
    flength = int(numbers) * 60 * 60 * 24 * 7
  
  elif letter == 'mon':
    flength = int(numbers) * 60 * 60 * 24 * 7 * 30
  
  elif letter == 'y':
    flength = int(numbers) * 60 * 60 * 24 * 7 * 30 * 12
  
  elif letter == 'dec':
    flength = int(numbers) * 60 * 60 * 24 * 7 * 30 * 12 * 100


  if not muted:
    muted = await guild.create_role(name='Muted')

    for channel in guild.channels:
      await channel.set_premissions(muted, speak=False, send_messages=False)

  await member.remove_roles(member)
  await member.add_roles(muted, reason=reason)
  if reason == None:
    reason = 'did something bad'
  await ctx.send(f"Hi I was told to mute {member.mention} because (s)he {reason}, I was also told to mute him for {length}")
  await member.send(f"Hi, you were muted on the server {guild.name} because {reason}, I was also told to mute you for {length}")
  await asyncio.sleep(flength)
  await member.remove_roles(muted)
  await member.add_roles(member)
  await ctx.send(f'{member.mention} has been unmuted (Yay!)')

@client.command()
@commands.has_permissions(kick_members=True)
async def unmute(ctx, member: discord.Member, reason=None):
  guild = ctx.guild
  member = get(guild.roles, name='member')
  muted = get(guild.roles, name='Muted')
  await member.remove_roles(muted, reason=reason)
  await member.add_roles(member)
  if reason == None:
    reason = 'did something good'
  await ctx.send(f"Hi I was told to unmute {member.mention} because (s)he {reason}")
  await member.send(f"Hi, you were unmuted on the server {guild.name} because you {reason}")

@client.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, reason=None):
  guild = ctx.guild
  if reason == None:
    reason = 'did something bad'
  await ctx.send(f"Hi I was told to kick {member.mention} because (s)he {reason}")
  await member.send(f"Hi, you were kicked on the server {guild.name} because you {reason}")
  await member.kick()

@client.command()
@commands.has_permissions(create_instant_invite = True)
async def invite(ctx, member: discord.Member, message):
  invite = await discord.abc.GuildChannel.create_invite(ctx.message.channel, max_uses=1)
  await member.send(f'Hi {ctx.author.name} sent you an invite! \nHe said: \n{message} \n {invite}')


@client.command()
@commands.has_permissions(ban_members=True)
async def ban (ctx, member: discord.Member, reason=None):
  
  if member == None or member == ctx.message.author:
    await ctx.channel.send("You cannot ban yourself")
    return
  
  if reason is None:
    await member.send(f'Hi, you have been banned from {ctx.guild.name}. They didn\'t say why :(.')
    await ctx.channel.send(f'Hi, {member.name} has been banned by {ctx.author.name} for no particular reason.')
    await member.ban()

  else:
    await member.send(f'Hi, {member.name} , you have been banned from {ctx.guild.name()}. The reason for this was {reason}.')
    await ctx.channel.send(f'Hi, {member.name} has been banned by {ctx.author.name} the reason specified was {reason}.')
    await member.ban()


@client.event
async def on_message(message):
  ctx = await client.get_context(message)
  guild = ctx.guild
  memberrole = get(guild.roles, name='member')
  muted = get(guild.roles, name='Muted')
  counter = 0 
  author = ctx.message.author
  with open("list.txt", "r+") as file:
      for lines in file:
          if lines.strip("\n") == str (message.author.id):
              counter+=1 

      file.writelines(f"{str(message.author.id)}\n")
      if counter > 5:
        if not muted:
          muted = await guild.create_role(name='Muted')
          
          for channel in guild.channels:
            await channel.set_premissions(muted, speak=False, send_messages=False)
        
        await author.add_roles(muted, reason='Spam')
        await author.remove_roles(memberrole)
        await ctx.send(f"Hi I was told to mute {author.mention} because (s)he spammed, I was also told to mute him for 5 minutes")
        await author.send(f"Hi, you were muted on the server {guild.name} because spammed, I was also told to mute you for 5 minutes")
        await asyncio.sleep(300)
        await author.remove_roles(muted)
        await author.add_roles(memberrole)
        await ctx.send(f'{author.mention} has been unmuted (Yay!)')
  
  await client.process_commands(message)


@client.command()
@commands.has_permissions(administrator=True)
async def shutdown(ctx):
  await client.close()

@client.event
async def on_command_error(ctx, error):
    print(error)
    if str(error) == 'You are missing Mute Members permission(s) to run this command.':
      await ctx.send('Sorry (s)he is already muted ')
    elif isinstance(error, commands.MissingPermissions):
      await ctx.send(f"Sorry but you're not allowed to do that, ok? <:Basil_smile:996486112442863686>") 
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please remember to put everything in your sentence or I can\'t understand it <:Basil_smile:996486112442863686>')

@client.event
async def on_ready():
    print("Everything is going to be ok")
    while True:
      await asyncio.sleep(10)
      with open("list.txt", "r+") as file:
          file.truncate(0)

keep_alive()
client.run(os.environ["key"])
