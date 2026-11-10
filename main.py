import os
import discord
from discord.ext import commands
from google import genai

# إعداد قوقل جيميناي بنموذج سريع ومستقر
ai_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"البوت اشتغل وصار جاهز باسم: {bot.user}")

@bot.command(name="سولف")
async def chat(ctx, *, message: str):
    # إرسال الرسالة باستخدام نموذج خفيف وسريع الاستجابة
    response = ai_client.models.generate_content(
        model='gemini-1.5-flash',
        contents=message,
    )
    await ctx.send(response.text)

bot.run(os.getenv("DISCORD_TOKEN"))
