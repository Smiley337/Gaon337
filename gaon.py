import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=["!", "가온아 "], intents=intents)

#봇이 켜지면 되는거래요?
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'{bot.user} 로 로그인 성공!')

@bot.event #가온이가 본인 이름을 인식함
async def on_message(message):
    if message.content.startswith("가온!"):
        await message.channel.send("네에?")

    await bot.process_commands(message)
"""
async def on_member_updat(before, after):
    ctx.send("{}님이 {}님이 되었어요!".format(before, after))

@bot.tree.command(name="hello", description="인사하기") #슬래시 커맨드에 tree라는걸로 등록이 됨
async def hello(interaction: discord.Interaction): #interaction 부분이 중요함
    await interaction.response.send_message("안녕하세요!")
"""
@bot.command(aliases=['ㅎㅇ', '가온아', 'hi']) #aliases는 안녕 대신에 쓸수있는 단어를 말함
async def 안녕(ctx):
    await ctx.send("안녕하세요! 👋")

@bot.command(aliases=['뭐해?', 'ㅁㅎ', '넌 뭐해?']) #물음표는 인식을 못해서 aliases에 넣어야함
async def 뭐해(ctx):
    await ctx.send("일리님을 보조하고 있어요.. 피곤해요. {}님은 뭐하고 계시나요?".format(ctx.author.name))

bot.run(TOKEN)













