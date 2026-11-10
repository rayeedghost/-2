import os
import discord
from discord.ext import commands
from google import genai

ai_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"البوت اشتغل وصار جاهز باسم: {bot.user}")

@bot.command(name="سولف")
async def chat(ctx, *, message: str):
    try:
        # استخدام موديل 1.5 الفلاش المعتمد والمستقر
        response = ai_client.models.generate_content(
            model='gemini-1.5-flash',
            contents=message,
        )
        if response and response.text:
            await ctx.send(response.text)
        else:
            await ctx.send("البوت رد بس بدون نص!")
    except Exception as e:
        await ctx.send(f"خطأ: {str(e)[:120]}")

bot.run(os.getenv("DISCORD_TOKEN"))
