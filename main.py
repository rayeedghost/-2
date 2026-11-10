import os
import discord
from discord.ext import commands
from google import genai

# تشغيل العميل بالطريقة الرسمية الجديدة
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
        # استخدام الطريقة الآمنة الرسمية اللي تختصر وجع رأس الروابط
        response = ai_client.models.generate_content(
            model='gemini-2.5-flash',
            contents=message,
        )
        await ctx.send(response.text)
    except Exception as e:
        # لو واجهنا أي ضغط أو خطأ، نجرب النموذج البديل الفوري
        try:
            response = ai_client.models.generate_content(
                model='gemini-2.0-flash',
                contents=message,
            )
            await ctx.send(response.text)
        except Exception as ex:
            await ctx.send("يا طويل العمر سيرفرات قوقل زحمة اليوم، جرب مرة ثانية بعد شوي!")

bot.run(os.getenv("DISCORD_TOKEN"))
