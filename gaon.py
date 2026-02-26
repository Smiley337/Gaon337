import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents=intents)

#봇이 켜지면 되는거래요?
@bot.event
async def on_ready():
    print(f'{bot.user} 로 로그인 성공!')
"""
async def on_member_updat(before, after):
    ctx.send("{}님이 {}님이 되었어요!".format(before, after))
"""
@bot.command(aliases=['ㅎㅇ', '가온아', 'hi']) #aliases는 안녕 대신에 쓸수있는 단어를 말함
async def 안녕(ctx):
    await ctx.send("안녕하세요! 👋")

bot.run(TOKEN)





