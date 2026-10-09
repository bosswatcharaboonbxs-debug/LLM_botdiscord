import os
import discord
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

bot.run(token) # เริ่มเชื่อมต่อและรับเหตุการณ์จาก Discord
