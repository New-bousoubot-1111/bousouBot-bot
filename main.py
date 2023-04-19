import nextcord
from nextcord.ext import commands
import traceback
import Levenshtein
import json
import util
from colorama import Fore
import os
import webserver

with open('json/config.json', 'r') as f:
    config = json.load(f)

intents = nextcord.Intents.all()
intents.members = True
intents.message_content = True
bot = commands.Bot(
	command_prefix=config['prefix'],
	help_command=None,
	intents=intents
)
for module in config['modules']:
    bot.load_extension(f"modules.{module}")

@bot.event
async def on_ready():
    print(Fore.GREEN + f"[Ready]\nbot:{bot.user.name}" + Fore.RESET)
    print(Fore.BLUE + "読み込みファイル" + Fore.RESET)
    print(Fore.BLUE + "----------------" + Fore.RESET)

@bot.event
async def on_guild_join(guild):
  for channel in guild.text_channels:
    if channel.permissions_for(guild.me).send_messages:
      em = nextcord.Embed(title="ぼうそうBOTのbotを追加していただき、ありがとうございます！\nbotのprefixは**b.**です。",color=0x08e2b7)
      await channel.send(embed=em)
      break

@bot.event
async def on_command_error(ctx, error:Exception):
    if isinstance(error, commands.errors.CommandNotFound):
        body = ctx.message.content.lstrip(ctx.prefix)
        res = []
        for i in bot.commands:
            check = Levenshtein.distance(str(i), str(body))
            if check <= 2:
                res.append(str(i))
        embed = nextcord.Embed(title="Error",
                               description=f"コマンドが見つかりません",
                               color=0xff0000)
        if not res == []:
            suggest = "".join([f'`{x}`\n' for x in res])
            embed.add_field(name="もしかして...", value=suggest)
        await ctx.send(embed=embed)
    elif isinstance(error, commands.errors.NotOwner):
        em = nextcord.Embed(title="このコマンドは使用できません",
                            description="このコマンドは管理者専用です",
                            color=0xff0000)
        await ctx.send(embed=em)
    else:
        format_error = "".join(traceback.TracebackException.from_exception(error).format())
        embed=nextcord.Embed(title="エラーが発生しました",description=f"Error ID:`{ctx.message.id}`\n```py\n{error}\n```",color=0xff0000)
        embed3=nextcord.Embed(title="Error Log",description=f"Error ID:`{ctx.message.id}`")
        embed3.add_field(name="実行コマンド",value=ctx.message.content)
        embed3.add_field(name="実行者",value=ctx.author)
        embed3.add_field(name="実行サーバー",value=ctx.guild.name)
        embed3.add_field(name="エラー内容(展開前)",value=f"```py\n{error}\n```")
        embed4=nextcord.Embed(title="エラー内容(展開後)",description=f"```py\n{format_error}\n```")
        
        await ctx.channel.send(embed=embed)
        Error_Log = 1073233143412301927
        channel = bot.get_channel(Error_Log)
        await channel.send(embed=embed3,view=util.open_error(embed3,embed4))
        error2 = "".join(
            traceback.TracebackException.from_exception(error).format())
        with open(f'errorlogs/{str(ctx.message.id)}.errorlog', 'w') as f:
            f.write(error2)
        print(Fore.RED + f"[Error]{error2}" + Fore.RESET)

webserver.start()
try:
    bot.run(os.getenv("token"))
except:
    os.system("kill 1")