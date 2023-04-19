import nextcord
from nextcord.ext import commands
import json
import requests
from colorama import Fore
import util

with open('json/config.json','r') as f:
	config = json.load(f)
with open('json/help.json','r') as f:
	help = json.load(f)

color = nextcord.Colour(int(config['color'],16))

class command(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
		
  @commands.Cog.listener()
  async def on_ready(self):
    print(Fore.BLUE + "|command       |" + Fore.RESET)		
    
  #ping
  @commands.command()
  async def ping(self,ctx):
        embed=nextcord.Embed(title="ping", description=f"BOTのpingは**{round(self.bot.latency *1000)}**です。",color=color)
        await ctx.send(embed=embed)
    
  #eew
  @commands.command()
  async def eew(self,ctx):
    request = requests.get(f'https://api.p2pquake.net/v2/history?codes=551&limit=1')
    response = request.json()[0]
    data = response['earthquake']
    hypocenter = data['hypocenter']
    if request.status_code == 200:
      embed=nextcord.Embed(title="地震情報",color=color)
      embed.add_field(name="震源地",value=hypocenter['name'],inline=False)
      embed.add_field(name="最大震度",value=round(data['maxScale']/10),inline=False)
      embed.add_field(name="発生時刻",value=data['time'],inline=False)
      embed.add_field(name="マグニチュード",value=hypocenter['magnitude'],inline=False)
      embed.add_field(name="震源の深さ",value=f"{hypocenter['depth']}Km",inline=False)
      await ctx.send(embed=embed)
    else:
      await ctx.send("APIリクエストでエラーが発生しました")
  #eew2
  @commands.command()
  async def eew2(self,ctx):
    request = requests.get("https://api.p2pquake.net/v2/history?codes=551&limit=1")
    response = request.json()[0]
    data = response['earthquake']
    hypocenter = data['hypocenter']
    if request.status_code == 200:
      embed=nextcord.Embed(title="地震情報",color=color)
      embed.add_field(name=f"{data['time']}頃、**{hypocenter['name']}**で地震がありました",value=f"最大震度は**{round(data['maxScale']/10)}**、震源の深さは**{hypocenter['depth']}Km**、マグニチュードは**{hypocenter['magnitude']}**です",inline=False)
      await ctx.send(embed=embed)
    else:
      await ctx.send("APIリクエストでエラーが発生しました")
  
  @commands.command()
  async def item(self,ctx,search=None,lang=(config['lang'])):
    if search == None:
      embed=nextcord.Embed(title="アイテム名を入力してください",description="検索したいアイテム名を入力してください",color=color)
      await ctx.send(embed=embed)
    else:
      count = 0      
      name_search = requests.get(f"https://fortnite-api.com/v2/cosmetics/br/search/all?name={search}&matchMethod=contains&language={lang}&searchLanguage={lang}").json()
      if name_search["status"] == 200:  
        for item in name_search['data']:
            embed = nextcord.Embed(title=item['type']['displayValue'],colour=color)
            embed.add_field(name="アイテム名",value=f"{item['name']}")
            embed.add_field(name="ID",value=f"{item['id']}")
            embed.add_field(name="説明", value=f"{item['description']}")
            embed.add_field(name="レアリティ", value=f"{item['rarity']['displayValue']}")
            try:
              embed.add_field(name="導入シーズン",value=f"{item['introduction']['text']}")
            except:
              pass
            try:
              embed.add_field(name="セット",value=f"{item['set']['text']}")
            except:
              pass								
            if item['images']['icon'] != None:
                embed.set_thumbnail(url=item['images']['icon'])
            await ctx.send(item['id'],embed=embed)
            count += 1
            if count == int(config['search_max']):
              item_count = len(name_search['data'])
              embed = nextcord.Embed(title="検索数の最大値に到達しました",description=f"残り{item_count - max}個のアイテムがあります",color=color)
              await ctx.send(embed=embed)
              return
            elif name_search['status'] == 404:
              embed = nextcord.Embed(title="アイテムが見つかりません",color=color)
              await ctx.send(embed=embed)
  
  @commands.command()
  async def help(self,ctx):
    creators = []
    for creator in help['owners']:
      creators.append(await self.bot.fetch_user(int(creator)))
    creators = "".join(f"\n`{x}`" for x in creators)
    commands_list = "".join(f"`{help['prefix']}{x}` " for x in help['commands_list'])
    embed=nextcord.Embed(title="情報",color=color)
    embed.add_field(name=f"作成者",value=f"{creators}")
    embed.add_field(name=f"言語",value="Python")
    embed.add_field(name="",value="\n[公式サイト](https://discord.gg/3VFpmSEugD)")

    embed2=nextcord.Embed(title="コマンド",description=f"***{commands_list}***",color=color)
    await ctx.channel.send(embed=embed,view=util.page_button(embed,embed2))

  @commands.command()
  async def eew_setup(self,ctx):
    if ctx.author.guild_permissions.manage_messages:
      with open('json/eew_channel.json','r') as a:
        ch = json.load(a)
        ch[str(ctx.guild.id)] = str(ctx.channel.id)
      with open('json/eew_channel.json','w') as a:
        json.dump(ch,a,indent=4)
      embed=nextcord.Embed(description=f"{ctx.channel.mention}を地震チャンネルに設定しました",color=color)
      await ctx.send(embed=embed)
    else:
      embed=nextcord.Embed(title="このコマンドを実行するためにはメッセージ管理の権限が必要です",color=color)
      await ctx.send(embed=embed)

  @commands.command()
  async def eew_remove(self,ctx):
    if ctx.author.guild_permissions.manage_messages:
      try:
        with open('json/eew_channel.json','r') as a:
          ch = json.load(a)
          ch.pop(str(ctx.guild.id))
        with open('json/eew_channel.json','w') as a:
          json.dump(ch,a,indent=4)
        embed=nextcord.Embed(title=f"このサーバーの地震チャンネルを解除しました",color=color)
        await ctx.send(embed=embed)
      except KeyError:
        embed=nextcord.Embed(title=f"このサーバーに地震チャンネルはありません",color=color)
        await ctx.send(embed=embed)
    else:
      embed=nextcord.Embed(title="このコマンドを実行するためにはメッセージ管理の権限が必要です",color=colors)
      await ctx.send(embed=embed)

def setup(bot):
  return bot.add_cog(command(bot))