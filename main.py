import os
import discord
from discord.ext import commands
import requests

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"البوت اشتغل وصار جاهز باسم: {bot.user}")

@bot.command(name="سولف")
async def chat(ctx, *, message: str):
    api_key = os.getenv("GEMINI_API_KEY")
    # استخدام الرابط المباشر للنموذج الأسرع والأكثر استقراراً
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [{"parts": [{"text": message}]}]
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        res_json = response.json()
        
        # استخراج الرد من استجابة قوقل
        reply = res_json['candidates'][0]['content']['parts'][0]['text']
        await ctx.send(reply)
    except Exception as e:
        # لو حصل أي خطأ نطبع الخطأ عشان نعرفه، ونرد برسالة واضحة
        await ctx.send(f"عذراً، صار خطأ تقريبي: {str(e)[:100]}")

bot.run(os.getenv("DISCORD_TOKEN"))
