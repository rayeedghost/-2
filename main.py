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
    reply = None
    
    # نجرب أولاً النموذج السريع
    try:
        response = ai_client.models.generate_content(
            model='gemini-2.0-flash',
            contents=message,
        )
        if response and response.text:
            reply = response.text
    except Exception as e:
        pass

    # إذا ما رد، نجرب النموذج البديل فوراً
    if not reply:
        try:
            response = ai_client.models.generate_content(
                model='gemini-1.5-flash',
                contents=message,
            )
            if response and response.text:
                reply = response.text
        except Exception as e:
            pass

    if reply:
        await ctx.send(reply)
    else:
        await ctx.send("يا طويل العمر سيرفرات قوقل قافلة اليوم، جرب مرة ثانية بعد شوي!")

bot.run(os.getenv("DISCORD_TOKEN"))
