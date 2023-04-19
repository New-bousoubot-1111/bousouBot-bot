import nextcord
from nextcord.ext import commands
import dhooks
import asyncio
import json
import os
from replit import db
import util

with open('json/config.json','r') as f:
	config = json.load(f)

color = nextcord.Colour(int(config['color'],16))

class global(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.Cog.listener()
  async def on_message(self,message):
    if message.author.bot:
      return
    if not message.reference == None:
      return
    guild_id = str(message.guild.id)
    try:
      channel = self.bot.get_channel(int(db[f'{guild_id}-globalchannel']))
    except KeyError:
      return
    if not message.channel == channel:
      return
    ban_users = []
    for user_id in db['globalban']:
      ban_users.append(user_id)
    if str(message.author.id) in ban_users:
      embed=nextcord.Embed(title="あなたはBANされています",description=f"あなたはてりほーのグローバルチャットからBANされています\n理由:{db['globalban'][str(message.author.id)]}",color=color)
      embed.set_footer(text="解除申請や異議申し立ての場合は作成者までご連絡ください")
      await message.reply(embed=embed)
      return
    hooks_url = util.webhook_loader(message,self.bot)
    hooks = []
    for hook_url in hooks_url:
      try:
        hook = dhooks.Webhook(
          str(hook_url),
          username=f"{message.author.name}#{message.author.discriminator}({message.author.id})",
          avatar_url=message.author.display_avatar.url
			  )
        hooks.append(hook)
      except:
        try:
          channel = self.bot.get_channel(int(db[f'{guild_id}-globalchannel']))
          embed=nextcord.Embed(title="WebHookが取得できません",description="グローバルチャット用のWebHookを取得できません\nもう一度セットアップをするまたは作成者までご連絡ください",color=color)
          await channel.send(embed=embed)
          return
        except KeyError:
          return
    token = util.token_check(message.content)
    if token == True:
      embed=nextcord.Embed(title="トークンを検出しました",description="トークンを検出したため処理を終了しました",color=color)
      try:
        await message.reply(embed=embed)
      except:
        pass
      return
    for hook in hooks:
      try:
        hook.send(message.clean_content)
      except:
        pass
      for attachment in message.attachments:
        hook.send(attachment.url)
        await asyncio.sleep(0.05) 
      await asyncio.sleep(0.1)

  @commands.Cog.listener("on_message")
  async def on_message_reply(self,message):
    if message.author.bot:
      return
    if message.reference == None:
      return
    guild_id = str(message.guild.id)
    try:
      channel = self.bot.get_channel(int(db[f'{guild_id}-globalchannel']))
    except KeyError:
      return
    if not message.channel == channel:
      return
    ban_users = []
    for user_id in db['globalban']:
      ban_users.append(user_id)
    if str(message.author.id) in ban_users:
      embed=nextcord.Embed(title="あなたはBANされています",description=f"あなたはてりほーのグローバルチャットからBANされています\n理由:{db['globalban'][str(message.author.id)]}",color=color)
      embed.set_footer(text="解除申請や異議申し立ての場合は作成者までご連絡ください")
      await message.reply(embed=embed)
      return
    hooks_url = util.webhook_loader(message,self.bot)
    hooks = []
    for hook_url in hooks_url:
      try:
        hook = dhooks.Webhook(
          str(hook_url),
          username=f"{message.author.name}#{message.author.discriminator}({message.author.id})",
          avatar_url=message.author.display_avatar.url
			  )
        hooks.append(hook)
      except:
        try:
          channel = self.bot.get_channel(int(db[f'{guild_id}-globalchannel']))
          embed=nextcord.Embed(title="WebHookが取得できません",description="グローバルチャット用のWebHookを取得できません\nもう一度セットアップをするまたは作成者までご連絡ください",color=color)
          await channel.send(embed=embed)
          return
        except KeyError:
          return
    reply_message = await util.get_reply_message(message)
    token = util.token_check(f"{message.content}\n{reply_message.content}")
    if token == True:
      embed=nextcord.Embed(title="トークンを検出しました",description="トークンを検出したため処理を終了しました",color=color)
      try:
        await message.reply(embed=embed)
      except:
        pass
      return
    for hook in hooks:
      try:
        if len(reply_message.content) > 0:
          hook.send(f"{reply_message.content}に返信\n{message.content}")
        else:
          hook.send(f"画像に返信\n{message.content}")
      except:
        pass
      for attachment in message.attachments:
        hook.send(attachment.url)
        await asyncio.sleep(0.05) 
      await asyncio.sleep(0.1)

  @commands.Cog.listener()
  async def on_guild_remove(self,guild):
    guild = guild
    guild_id = guild.id
    try:
      del db[f'{guild_id}-globalchannel']
      del db[f'{guild_id}-globalhook']
    except KeyError:
      return

def setup(bot):
  return bot.add_cog(global(bot))