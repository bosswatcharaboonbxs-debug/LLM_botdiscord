import os
import discord
import aiohttp
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("DISCORD_TOKEN")

if not token :
    raise RuntimeError("Please have DISCORD TOKEN in .env")

intents = discord.Intents.default() # กำหนดข้อมูลที่บอตต้องการรับ
intents.message_content = True

bot = commands.Bot(command_prefix="!" , intents=intents) # สร้างบอต โดยกำหนดให้คำสั่งขึ้นต้นด้วย !

@bot.event
async def on_ready() :
    print(f"บอตพร้อมแล้ว : {bot.user}")

@bot.command()
async def hello(ctx) :
    await ctx.send("สวััสดี!")
@bot.command()
async def say(ctx , *,message : str) :
    await ctx.send(
        message ,
        allowed_mentions = discord.AllowedMentions.none()
    )
@say.error
async def say_error(ctx,error) :
    if isinstance(error , commands.MissingRequiredArgument) :
        await ctx.send("ใช้แบบนี้ : !say [text]")
    else :
        raise error

@bot.command()
async def userinfo(ctx) :
    user = ctx.author

    await ctx.send(
        f"Name : {user.name}\n"
        f"ID : {user.id}\n"
        f"Account Date : {user.created_at:%d/%m/%Y}"
    )

async def ask_qwen(question) :
    timeout = aiohttp.ClientTimeout(total=180)

    async with aiohttp.ClientSession(timeout=timeout) as session :
        async with session.post(
            "http://127.0.0.1:11434/api/chat" ,
            json = {
                "model" : "qwen3:1.7b" ,
                "messages" : [
                    {"role" : "user" , "content" : question}
                ] ,
                "stream" : False ,
                "think" : False
            },
        ) as response :
            response.raise_for_status()
            data = await response.json()
    return data["message"]["content"]

@bot.command()
async def ask(ctx , * , question : str) :
    async with ctx.typing() :
        answer = await ask_qwen(question)

    for start in range(0, len(answer) , 1900) :
        await ctx.send(
            answer[start:start + 1900] ,
            allowed_mentions = discord.AllowedMentions.none() ,
        )

bot.run(token) # เริ่มเชื่อมต่อและรับเหตุการณ์จาก Discord
