import nextcord
import json
import os
import sys

with open('json/help.json','r') as f:
	help = json.load(f)
with open('json/config.json','r') as f:
	config = json.load(f)

color = nextcord.Colour(int(config['color'],16))
    
#再起動実行
class restart_button(nextcord.ui.View):
  def __init__(self):
    super().__init__(timeout=None)
  @nextcord.ui.button(label="再起動",style=nextcord.ButtonStyle.green)
  async def button_click(self,button:nextcord.ui.Button,interaction:nextcord.Interaction):
    if interaction.user.id in config['owners']:
      embed=nextcord.Embed(title="再起動",description="Botを再起動します\n再起動終了まで時間がかかる場合があります",color=color)
      await interaction.response.send_message(embed=embed)
      self.stop()
      res = sys.executable
      os.execl(res,res,*sys.argv)
    else:
      embed=creator_only()
      await interaction.response.send_message(embed=embed,ephemeral=True)
      
#エラー展開
class page_creator(nextcord.ui.View):
  def __init__(self,embeds,ctx,author):
    super().__init__(timeout=None)
    self.embeds = embeds
    self.ctx = ctx
    self.author = author
    self.page = 0
  @nextcord.ui.button(emoji="⬅️",style=nextcord.ButtonStyle.grey,disabled=True)
  async def back(self, button:nextcord.ui.Button,click:nextcord.Interaction):
    self.page -= 1
    embed = self.embeds[self.page]
    if self.page == 0:
      button.disabled = True
    if self.page < len(self.embeds):
      self.next.disabled = False
    await click.response.edit_message(embed=embed,view=self)

  @nextcord.ui.button(emoji="➡️", style=nextcord.ButtonStyle.grey,disabled=False)
  async def next(self,button:nextcord.ui.Button,click:nextcord.Interaction):
    self.page += 1
    embed = self.embeds[self.page]
    if self.page > 0:
      self.back.disabled = False
    if self.page == len(self.embeds) - 1:
      button.disabled = True
    await click.response.edit_message(embed=embed,view=self)

  @nextcord.ui.button(label="閉じる",emoji="❌",style=nextcord.ButtonStyle.red)
  async def delete(self,button:nextcord.ui.Button,click:nextcord.Interaction):
    if self.author.id == click.user.id:
      await click.response.edit_message(view=None)
    else:
      await click.response.send_message("これはあなたのメッセージではないためこの動作は実行できません",ephemeral=True)

class open_error(nextcord.ui.View):
  def __init__(self,embed,embed2):
    super().__init__(timeout=None)
    self.value = None
    self.embed = embed
    self.embed2 = embed2

  @nextcord.ui.button(label="エラーを展開",style=nextcord.ButtonStyle.red)
  async def open_the_error(self,button:nextcord.ui.Button,interaction:nextcord.Interaction):
    await interaction.response.edit_message(embed=self.embed2,view=close_error(self.embed,self.embed2))

class close_error(nextcord.ui.View):
  def __init__(self,embed,embed2):
    super().__init__(timeout=None)
    self.value = None
    self.embed = embed
    self.embed2 = embed2

  @nextcord.ui.button(label="エラーを閉じる",style=nextcord.ButtonStyle.red)
  async def close_the_error(self,button:nextcord.ui.Button,interaction:nextcord.Interaction):
    await interaction.response.edit_message(embed=self.embed,view=open_error(self.embed,self.embed2))
    
#ページボタン
class page_button(nextcord.ui.View):
  def __init__(self,embed,embed2):
    super().__init__(timeout=None)
    self.value = None
    self.embed = embed
    self.embed2 = embed2

  @nextcord.ui.button(label="情報",style=nextcord.ButtonStyle.green)
  async def close_the_error(self,button:nextcord.ui.Button,interaction:nextcord.Interaction):
    await interaction.response.edit_message(embed=self.embed)

  @nextcord.ui.button(label="コマンド",style=nextcord.ButtonStyle.green)
  async def open_the_error(self,button:nextcord.ui.Button,interaction:nextcord.Interaction):
    await interaction.response.edit_message(embed=self.embed2)
    
#管理者
def creator_only():
  embed=nextcord.Embed(title="Error",description="このコマンドは管理者専用です",color=0xff0000)
  return embed
  
#起動時間
def sec_formatter(times):
  times = round(int(times))
  if times > 0:
    minutes, seconds = divmod(times, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)

  times = []
  times.append(f"{days}日")
  times.append(f"{hours}時間")
  times.append(f"{minutes}分")
  times.append(f"{seconds}秒")
  times = ''.join(times)
  return times