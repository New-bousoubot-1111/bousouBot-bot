import nextcord
from nextcord.ext import commands,tasks
import json
import asyncio
import requests
from colorama import Fore
from replit import db
import util

with open('json/config.json','r') as f:
	config = json.load(f)

color = nextcord.Colour(int(config['color'],16))

class earthquake(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
		
  @commands.Cog.listener()
  async def on_ready(self):
    print(Fore.BLUE + "|earthquake    |" + Fore.RESET)
    self.eew_info.start()

  #地震情報
  @tasks.loop(seconds=2)
  async def eew_info(self):
    with open('json/eew.json','r') as f:
      eew_id = json.load(f)['eew_id']
      data = requests.get(f'https://api.p2pquake.net/v2/history?codes=551&limit=1').json()[0]["points"]
      if data[0]["isArea"] is False:
        isArea = "この地震による津波の心配はありません"
      if data[0]["isArea"] is True:
        isArea = "この地震で津波が発生する可能性があります"
    request = requests.get(f'https://api.p2pquake.net/v2/history?codes=551&limit=1')
    response = request.json()[0]
    data = response['earthquake']
    hypocenter = data['hypocenter']
    if request.status_code == 200:
      if eew_id != response['id']:
        embed=nextcord.Embed(title="地震情報",color=color)
        embed.add_field(name="発生時刻",value=data['time'],inline=False)
        embed.add_field(name="震源地",value=hypocenter['name'],inline=False)
        embed.add_field(name="最大震度",value=round(data['maxScale']/10),inline=False)
        embed.add_field(name="マグニチュード",value=hypocenter['magnitude'],inline=False)
        embed.add_field(name="震源の深さ",value=f"{hypocenter['depth']}Km",inline=False)
        embed.add_field(name="",value=isArea,inline=False)
        embed.set_footer(text=data['time'])
        with open('json/eew_channel.json','r') as r:
          load = json.load(r)
          for guild in load:
            channel = self.bot.get_channel(int(load[guild]))
            await channel.send(embed=embed)
        with open('json/eew.json','r') as f:
          eew_id = json.load(f)
          eew_id['eew_id'] = response['id']
        with open('json/eew.json','w') as f:
          json.dump(eew_id,f,indent=2)
      else:
        return

def setup(bot):
  return bot.add_cog(earthquake(bot))