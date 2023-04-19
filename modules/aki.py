import nextcord
from nextcord.ext import commands
from nextcord import Embed
import asyncio
import akinator as ak
import random
from colorama import Fore

m = 0xe3fbff
e = 0xe5ff00
s = 0x00ff00

class aki(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
      
    @commands.Cog.listener()
    async def on_ready(self):
      print(Fore.BLUE + "|aki           |" + Fore.RESET)

    @commands.command(usage="aki\nアキネーターで遊べます")
    async def aki(self,ctx):
      async with ctx.typing():
        intro = nextcord.Embed(description=f"どうも私はアキネーターです\n私は{ctx.author.mention}が思い浮かべたものを当てて見せます",color=m)
        bye = nextcord.Embed(description=f"じゃあね{ctx.author.mention}くん", color=m)
        await ctx.send(embed=intro)

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower() in ["y", "n", "p",
                                                                                                       "b",
                                                                                                       "yes", "no",
                                                                                                       "probably",
                                                                                                       "idk",
                                                                                                       "back"]

        try:
            aki = ak.Akinator()
            q = aki.start_game(language="jp")
            while aki.progression <= 80:
                question = nextcord.Embed(title="質問", description=q, color=m)
                question.set_footer(text="y/n/p/idk/bで答えてね(はい/いいえ/多分そう(そうでもない)/わからない/一つ戻る)")
                await ctx.send(embed=question)
                try:
                  msg = await self.bot.wait_for("message", check=check, timeout=30)
                except asyncio.TimeoutError:
                    await ctx.send("30秒間返信がなかったから終了するね")
                    await ctx.send(embed=bye)
                    return
                if msg.content.lower() in ["b", "back"]:
                    try:
                        q = aki.back()
                    except ak.CantGoBackAnyFurther as e:
                        await ctx.send(e)
                        continue
                else:
                    try:
                        q = aki.answer(msg.content.lower())
                    except ak.InvalidAnswerError as e:
                        await ctx.send(e)
                        continue
            aki.win()
            answer = nextcord.Embed(title=aki.first_guess['name'], description=aki.first_guess['description'],color=m)
            answer.add_field(name="ランキング",value=f"{aki.first_guess['ranking']}位")
            answer.set_image(url=aki.first_guess['absolute_picture_path'])
            answer.set_footer(text="これで合っていますか?(y/n)")
            await ctx.send(embed=answer)
            try:
              correct = await self.bot.wait_for("message", check=check, timeout=30)
            except asyncio.TimeoutError:
                await ctx.send("30秒間返信がなかったから終了するね")
                await ctx.send(embed=bye)
                return
            if correct.content.lower() == "y":
                yes = nextcord.Embed(description="やったぜ！\nアキネーターはなんでも分かるのさ", color=m)
                await ctx.send(embed=yes)
            else:
                no = nextcord.Embed(description="まじかよ\nまた遊んでくれよな", color=m)
                await ctx.send(embed=no)
            await ctx.send(embed=bye)
        except Exception as e:
            await ctx.send(e)

    
def setup(bot):
    return bot.add_cog(aki(bot))