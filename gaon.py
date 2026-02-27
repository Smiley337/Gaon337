import discord
import yt_dlp 
import asyncio

from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(
    command_prefix=commands.when_mentioned_or("!", "가온아 "),
    intents=intents
)

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

    if ctx.author.voice is None: #만약 유저가 통화방에 들어가있지 않다면,
        await ctx.send("어.. 어디 계시나요? 못찾겠어요..")
        return #돌아가 새끼야
    
    channel = ctx.author.voice.channel #유저가 있는 통화방을 channel이라는 값에 입력함
    
    if ctx.voice_client is not None:
        if channel == ctx.voice_client.channel:
            await ctx.send("이미 같이 있어요!")
        else :
            await ctx.send("별 이동!")
            print("음성 채널 정보: {0.author.voice}".format(ctx))
            print("이동 음성 채널 이름: {0.author.voice.channel}".format(ctx))
            return await ctx.voice_client.move_to(channel)

    await channel.connect()
    await ctx.send("별 입장! ✨")
    print("음성 채널 정보: {0.author.voice}".format(ctx))
    print("음성 채널 이름: {0.author.voice.channel}".format(ctx))

#퇴장

@bot.command(aliases=['나가', '꺼져'])
async def out(ctx):

    if ctx.voice_client is None:
        await ctx.send("저는 거기 없어요!!")
        return
    
    if ctx.author.voice is None: #만약 유저가 통화방에 들어가있지 않다면,
        await ctx.send("이씨 장난치지 말아요! 같이 있지도 않으면서!")
        return #돌아가 새끼야
    
    channel = ctx.author.voice.channel #유저가 있는 통화방을 channel이라는 값에 입력함
    
    if channel != ctx.voice_client.channel:
        await ctx.send("같은 곳에 있을 때만 내보낼 수 있어요!")
        return


    await ctx.voice_client.disconnect()
    await ctx.send("가온이 {0.author.voice.channel}에서 퇴장! 👋")
    


# =========================
# yt-dlp 기본 설정 부분
# =========================

# 유튜브 오디오 추출 옵션
ytdl_format_options = {
    'format': 'bestaudio/best',  # 최고 음질 오디오 선택
    'noplaylist': True,          # 플레이리스트 무시
    'quiet': True,               # 콘솔 로그 최소화
    'default_search': 'auto',    # 검색어만 입력해도 검색 가능
    'source_address': '0.0.0.0', # IPv4 강제 (Railway에서 안정적)
}

# ffmpeg 실행 옵션
ffmpeg_options = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',  # 끊기면 재연결
    'options': '-vn',  # 영상은 무시하고 오디오만
}

# yt-dlp 객체 생성
ytdl = yt_dlp.YoutubeDL(ytdl_format_options)


# =========================
# 🎵 유튜브 소스 클래스
# =========================
class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=True):
        loop = loop or asyncio.get_event_loop()

        # yt-dlp를 별도 스레드에서 실행 (봇 멈춤 방지)
        data = await loop.run_in_executor(
            None,
            lambda: ytdl.extract_info(url, download=not stream)
        )

        # 플레이리스트일 경우 첫 곡만 선택
        if 'entries' in data:
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)

        return cls(
            discord.FFmpegPCMAudio(filename, **ffmpeg_options),
            data=data
        )


# =========================
# 🎵 음악 기능 Cog
# =========================
class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ▶️ 음악 재생
    @commands.command(aliases=['불러줘'])
    async def play(self, ctx, *, url):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                return await ctx.send("먼저 음성 채널에 들어가 주세요!")

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop=self.bot.loop)
            ctx.voice_client.play(
                player,
                after=lambda e: print(f'Player error: {e}') if e else None
            )

        await ctx.send(f'🎶 가온이는 지금 이 노래를 부르고 있어요: {player.title}')

    #볼륨 조절
    @commands.command(aliases=['소리', '소리 조절'])
    async def volume(self, ctx, volume: int):
        if ctx.voice_client is None:
            return await ctx.send("연결하고 훈수질해요!")

        ctx.voice_client.source.volume = volume / 100
        await ctx.send(f"목소리를 {volume}% 로 바꿨어요.")

    # 일시정지
    @commands.command(aliases=['멈춰', '기다려'])
    async def pause(self, ctx):
        if ctx.voice_client.is_playing():
            ctx.voice_client.pause()
            await ctx.send("네? 잠깐 멈췄어요!")
        else:
            await ctx.send("히잉.. 노래 안부르고 있는데,,")

    # 다시재생
    @commands.command(aliases=['계속 불러', '다시재생', '다시 불러'])
    async def resume(self, ctx):
        if ctx.voice_client.is_paused():
            ctx.voice_client.resume()
            await ctx.send("다시 계속 부를게요!")
        else:
            await ctx.send("..?? 아무것도 안부르고 있었는걸요..")

bot.add_cog(Music(bot))
bot.run(TOKEN)































