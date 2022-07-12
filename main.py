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
  
  elif letter == 'mon':
    flength = int(numbers) * 60 * 60 * 24 * 30
  
  elif letter == 'y':
    flength = int(numbers) * 60 * 60 * 24 * 30 * 12
  
  elif letter == 'dec':
    flength = int(numbers) * 60 * 60 * 24 * 30 * 12 * 100


  if not muted:
    muted = await guild.create_role(name='Muted')

    for channel in guild.channels:
      await channel.set_premissions(muted, speak=False, send_messages=False)

  await member.add_roles(muted, reason=reason)
  await ctx.send(f"Server Muted {member.mention} \nReason: {reason} \nLength: {length}")
  await member.send(f"You were server muted in the server {guild.name} for reason {reason} for {length}") #\\\\\\FIX
  await asyncio.sleep(flength)
  await member.remove_roles(muted)
  await ctx.send(f'{member.mention} has been unmuted')

@client.command()
@commands.has_permissions(ban_members=True)
async def ban (ctx, member: discord.Member, reason=None):
  print('ver')
  
  if member == None or member == ctx.message.author:
    await ctx.channel.send("You cannot ban yourself")
    return
  
  if reason is None:
    await member.send(f'Hello, you have been banned from {ctx.guild.name}. There was no specified reason for this ban.')
    await ctx.channel.send(f'user {member.name} has been banned by {ctx.author.name} for no specified reason.')
    await member.ban()

  else:
    await member.send(f'Hello {member.name} , you have been banned from {ctx.guild.name()}. The reason specified for this was {reason}.')
    await ctx.channel.send(f'user {member.name} has been banned by {ctx.author.name} the reason specified was {reason}.')
    await member.ban()

@client.command()
@commands.has_permissions(administrator=True)
async def shutdown(ctx):
  await ctx.bot.logout()
  ctx.channel.send('logging out')

@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please pass in all requirements :rolling_eyes:.')
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("You dont have all the requirements :angry:")

@client.event
async def on_ready():
    print("ready")
    while True:
      await asyncio.sleep(10)
      with open("list.txt", "r+") as file:
          file.truncate(0)

keep_alive()
client.run(os.environ["key"])
