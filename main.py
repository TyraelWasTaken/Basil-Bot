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

  await member.add_roles(muted, reason=reason)
  if reason == None:
    reason = 'did something bad'
  await ctx.send(f"Hi I was told to mute {member.mention} because (s)he {reason}, I was also told to mute him for {length}")
  await member.send(f"Hi, you were muted in the server {guild.name} because {reason}, I was also told to mute you for {length}")
  await asyncio.sleep(flength)
  await member.remove_roles(muted)
  await ctx.send(f'{member.mention} has been unmuted (Yay!)')

@client.command()
@commands.has_permissions(kick_members=True)
async def unmute(ctx, member: discord.Member, reason=None):
  guild = ctx.guild
  muted = get(guild.roles, name='Muted')
  await member.remove_roles(muted, reason=reason)
  if reason == None:
    reason = 'did something good'
  await ctx.send(f"Hi I was told to unmute {member.mention} because (s)he {reason}")
  await member.send(f"Hi, you were unmuted in the server {guild.name} because you {reason}")

@client.command()
@commands.has_permissions(ban_members=True)
async def ban (ctx, member: discord.Member, reason=None):
  print('ver')
  
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
