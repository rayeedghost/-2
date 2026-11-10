import os
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"تم تسجيل الدخول بنجاح، البوت شغال باسم: {bot.user}")

@bot.command(name="سولف")
async def chat(ctx, *, message: str):
    await ctx.send(f"أهلاً بك! وصلني كلامك: '{message}'، وجاهز أسولف معك.")

bot.run(os.getenv("DISCORD_TOKEN"))
