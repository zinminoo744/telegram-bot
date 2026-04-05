import telebot
import requests
import os
from flask import Flask
from threading import Thread

# ၁။ Render အိပ်မပျော်စေရန် Flask App တည်ဆောက်ခြင်း
app = Flask('')
@app.route('/')
def home():
    return "Bot is running online!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

keep_alive()

# ၂။ Telegram Bot Setup
TOKEN = "8754953424:AAG1-wKJ7uJVdMNk9s-KFThkPnLL5RSAgEA"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda message: True)
def chat_ai(message):
    query = message.text
    try:
        # ၃။ ပိုမိုကောင်းမွန်သော Chat AI API သို့ ချိတ်ဆက်ခြင်း
        api_url = f"https://api.pawan.krd/cosmosrp/v1/chat/completions"
        headers = {"Content-Type": "application/json"}
        data = {
            "model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": query}]
        }
        
        # API link အဟောင်းအစား ဤနေရာတွင် အခြား အခမဲ့ API တစ်ခုခုဖြင့် စမ်းသပ်နိုင်သည်
        # လောလောဆယ် "Not Found" ဖြစ်နေသော API အစား တိုက်ရိုက်အဖြေပေးမည့် link ကို သုံးပါမည်
        fallback_api = f"https://nexra.aryahcr.cc/api/ai/chatgpt?prompt={query}&model=gpt-4"
        response = requests.get(fallback_api, timeout=30).json()
        
        # API အဖြေကို ထုတ်ယူခြင်း
        ai_reply = response.get('gpt', 'ခဏလေးနော်... အဖြေရှာမတွေ့လို့ပါ။')
        bot.reply_to(message, ai_reply)
        
    except Exception as e:
        bot.reply_to(message, "စနစ် အနည်းငယ် ချို့ယွင်းနေပါတယ်။ ခဏနေမှ ပြန်မေးပေးပါ။")

if __name__ == "__main__":
    bot.infinity_polling()
