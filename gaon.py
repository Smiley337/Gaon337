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
    await ctx.send("일리님을 보조하고 있어요.. 피곤해요. {}님은 뭐하고 계시나요?".format(ctx.author.display_name))

#음성 채널 기능들


#입장하기 
@bot.command(aliases=['들어와','통화방 와','연결'])
async def join(ctx):
    channel = ctx.author.voice.channel #유저가 있는 통화방을 channel이라는 값에 입력함

    if ctx.author.voice is None: #만약 유저가 통화방에 들어가있지 않다면,
        await ctx.send("어.. 어디 계시나요? 못찾겠어요..")
        return #돌아가 새끼야
    
    if ctx.voice_client is not None:
        await ctx.send("별 등장!")
        print("음성 채널 정보: {0.author.voice}".format(ctx))
        print("음성 채널 이름: {0.author.voice.channel}".format(ctx))
        return await ctx.voice_client.move_to(channel)

    await channel.connect()
#퇴장
@bot.command(aliases=['나가', '꺼져'])
async def out(ctx):

    if ctx.voice_client is None:
        await ctx.send("저는 거기 없어요!!")
        return

    await ctx.voice_client.disconnect()
    await ctx.send("가온이 {0.author.voice.channel}에서 나갔어요!".format(ctx))



bot.run(TOKEN)

















