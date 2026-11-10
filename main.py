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
    
    # الخطوة 1: جلب الموديلات المتاحة لمفتاحك تلقائياً من قوقل
    list_url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    
    try:
        models_res = requests.get(list_url).json()
        available_model = None
        
        # البحث عن أول موديل يدعم التوليد (generateContent)
        if "models" in models_res:
            for m in models_res["models"]:
                methods = m.get("supportedGenerationMethods", [])
                if "generateContent" in methods:
                    # نأخذ اسم النموذج ونظفه من كلمة models/ لو وجدت
                    available_model = m["name"].replace("models/", "")
                    break
        
        # إذا ما لقينا، نحط الاحتياطي الحديث
        if not available_model:
            available_model = "gemini-2.5-flash" # أو أي اسم متاح حالياً
            
        # الخطوة 2: إرسال الرسالة للموديل الشغال فعلياً
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{available_model}:generateContent?key={api_key}"
        
        headers = {"Content-Type": "application/json"}
        data = {
            "contents": [{"parts": [{"text": message}]}]
        }
        
        response = requests.post(url, json=data, headers=headers)
        res_json = response.json()
        
        if "candidates" in res_json:
            reply = res_json['candidates'][0]['content']['parts'][0]['text']
            await ctx.send(reply)
        else:
            error_msg = res_json.get('error', {}).get('message', 'خطأ غير معروف')
            await ctx.send(f"رد قوقل ({available_model}): {error_msg}")
            
    except Exception as e:
        await ctx.send(f"خطأ في الاتصال: {str(e)[:100]}")

bot.run(os.getenv("DISCORD_TOKEN"))
