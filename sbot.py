import telebot
import requests
import os
from flask import Flask
from threading import Thread

# ၁။ Render အတွက် Port ဖွင့်ပေးမည့် Flask App တည်ဆောက်ခြင်း
app = Flask('')

@app.route('/')
def home():
    return "Chat AI Bot is Online!"

def run():
    # Render ကပေးသော Port ကိုယူရန် (မရှိလျှင် 8080 ကိုသုံးရန်)
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# ၂။ Bot မ Run ခင် Keep Alive စနစ်ကို အရင်စတင်ခြင်း
keep_alive()

# ၃။ Telegram Bot Settings
TOKEN = "8754953424:AAG1-wKJ7uJVdMNk9s-KFThkPnLL5RSAgEA" # သင့် Token အမှန်ဖြစ်ရမည်
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "မင်္ဂလာပါ! ကျွန်တော်က Chat AI Bot ပါ။ သိချင်တာရှိရင် စာရိုက်ပြီး မေးမြန်းနိုင်ပါတယ်ဗျာ။")

@bot.message_handler(func=lambda message: True)
def chat_ai(message):
    query = message.text
    try:
        # Chat AI API သို့ မေးမြန်းခြင်း
        api_url = f"https://nexra.aryahcr.cc/api/ai/chatgpt?prompt={query}&model=gpt-4"
        response = requests.get(api_url, timeout=30).json()
        
        # AI ထံမှရရှိသော အဖြေကို ပြန်ပို့ခြင်း
        bot.reply_to(message, response.get('gpt', 'နားမလည်ပါဗျာ။ နောက်တစ်ခေါက် ပြန်မေးကြည့်ပေးပါ။'))
        
    except Exception as e:
        bot.reply_to(message, "ခေတ္တစောင့်ဆိုင်းပြီးမှ ပြန်မေးပေးပါဗျာ။")

# ၄။ Bot ကို အမြဲတမ်း ပွင့်နေစေရန် Run ခြင်း
if name == "main":
    print("Bot is starting on Render...")
    bot.infinity_polling()
