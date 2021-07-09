from discord.ext import commands
from datetime import datetime
from urllib import parse, request
from pytz import timezone
import os
import time
import asyncio
import datetime
import discord
import random
from keep_alive import keep_alive

whitelist = ["717153131170889740"]

bot = commands.Bot(command_prefix ='$',description = "I'm an antispam bot")

@bot.event
async def on_ready():
    print("AntiSpamBot esta listo") 
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="your messages"))


async def mute(ctx, member: discord.Member, time_muted: int):
  if ctx.message.author.id not in whitelist or not ctx.message.author.guild_permissions.administrator:
    print(ctx.message.author.guild_permissions.administrator)
    roleMute = discord.utils.get(member.guild.roles, name = 'Muted')
    await member.add_roles(roleMute)

    embedMuted = discord.Embed(title = ":mute: Spam",
    description = "**{0}** fue silenciado durante **{1} segundos**".format(member.mention,time_muted),
    color = discord.Color.red())
        
    await ctx.send(embed=embedMuted)

    await asyncio.sleep(time_muted)

    await unmute(ctx,member)


async def unmute(ctx, member: discord.Member):
  mutedRole = discord.utils.get(ctx.guild.roles, name = "Muted")

  await member.remove_roles(mutedRole)
  embedUnmuted = discord.Embed(title =":white_check_mark: Unmute", description = f"{member.mention} ya no está silenciado",
  color = discord.Color.green())

  await ctx.send(embed=embedUnmuted)


cooldown = commands.CooldownMapping.from_cooldown(5,6,commands.BucketType.member)

@bot.event
async def on_message(message):
    ctx = await bot.get_context(message)

    if message.author.bot:
      return
    
    retry_after = cooldown.update_rate_limit(message)
    print(retry_after)
    if retry_after:
      def check(msgb):
        return msgb.author.id == message.author.id

      await message.channel.purge(limit = 7,check = check, before = None)
      await mute(ctx,message.author,120)

    await bot.process_commands(message)

keep_alive()
bot.run("DISCORD_TOKEN")
