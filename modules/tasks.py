import nextcord
from nextcord.ext import commands,tasks
import json
import aioschedule
from colorama import Fore

with open('json/config.json','r') as f:
	config = json.load(f)

color = nextcord.Colour(int(config['color'],16))

class tasks(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
		
  @commands.Cog.listener()
  async def on_ready(self):
    print(Fore.BLUE + "|tasks         |" + Fore.RESET)
    print(Fore.BLUE + "----------------" + Fore.RESET)
    self.status.start()

  @tasks.loop(minutes=3)
  async def status(self):
    await self.bot.change_presence(activity=nextcord.Game(name=f"{config['prefix']}help"))

def setup(bot):
  return bot.add_cog(tasks(bot))