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
    # محاولة استخدام النموذج الأساسي، وإذا واجه ضغط نجرب موديل بديل
    models_to_try = ['gemini-3.8-flash', 'gemini-2.0-flash', 'gemini-1.5-flash']
    
    reply = None
    for model_name in models_to_try:
        try:
            response = ai_client.models.generate_content(
                model=model_name,
                contents=message,
            )
            if response and response.text:
                reply = response.text
                break
        except Exception as e:
            continue
            
    if reply:
        await ctx.send(reply)
    else:
        await ctx.send("يا طويل العمر سيرفرات قوقل زحمة ضغط عالي، جرب بعد ثانية وتضبط!")

bot.run(os.getenv("DISCORD_TOKEN"))
