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
        # نستخدم نموذج واحد ونخليه يركز ويعطيك رد حقيقي بدون هبد
        response = ai_client.models.generate_content(
            model='gemini-2.0-flash',
            contents=message,
        )
        if response and response.text:
            await ctx.send(response.text)
        else:
            await ctx.send("قُمّ صامت... قوقل ما رجعت نص بالرد.")
    except Exception as e:
        # نطبع جزء من الخطأ الحقيقي عشان نعرف هل هي زحمة ولا مفتاح ولا ايش بالضبط
        error_str = str(e)
        if "429" in error_str or "ResourceExhausted" in error_str:
            await ctx.send("خلصت حصة الـ API المجانية المؤقتة، اصبر دقيقة وتعال!")
        else:
            await ctx.send(f"خطأ قوقل: {error_str[:120]}")

bot.run(os.getenv("DISCORD_TOKEN"))
