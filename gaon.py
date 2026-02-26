import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

#봇이 켜지면 되는거래요?
@bot.event
async def on_ready():
    print(f'{bot.user} 로 로그인 성공!')
    
""" @bot.command()
async def 안녕(ctx):
    await ctx.send("안녕하세요! 👋")
 """
@bot.command(name="안녕", help="인사말", aliases=["인사", "하이"])
async def hello(ctx):
  hi = random.randrange(1,4)
  if hi == 1:
    await ctx.channel.send("안녕하세요")
  elif hi == 2:
    await ctx.channel.send("안녕")
  elif hi == 3:
    await ctx.channel.send("네, 안녕하세요")

bot.run(TOKEN)

