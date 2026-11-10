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
    # استخدام النموذج المتاح والمعتمد حالياً
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
    
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [{"parts": [{"text": message}]}]
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        res_json = response.json()
        
        if "candidates" in res_json:
            reply = res_json['candidates'][0]['content']['parts'][0]['text']
            await ctx.send(reply)
        else:
            error_msg = res_json.get('error', {}).get('message', 'خطأ غير معروف')
            await ctx.send(f"رد قوقل: {error_msg}")
            
    except Exception as e:
        await ctx.send(f"خطأ في النظام: {str(e)[:100]}")

bot.run(os.getenv("DISCORD_TOKEN"))
