import telebot
import requests
import os
from flask import Flask
from threading import Thread

# Flask App for Keep Alive
app = Flask('')
@app.route('/')
def home():
    return "Bot is alive!"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

keep_alive()

# Telegram Bot Setup
TOKEN = "8754953424:AAG1-wKJ7uJVdMNk9s-KFThkPnLL5RSAgEA"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(func=lambda message: True)
def chat_ai(message):
    query = message.text
    try:
        # ပိုစိတ်ချရသော AI API သို့ ပြောင်းလဲအသုံးပြုခြင်း
        api_url = f"https://endpoint.onrender.com/chatgpt?text={query}"
        response = requests.get(api_url, timeout=20)
        
        # API ကနေ စာသားအတိုင်းပြန်ပေးရင် ဒါကိုသုံးပါ
        ai_reply = response.text 
        
        bot.reply_to(message, ai_reply)
        
    except Exception as e:
        bot.reply_to(message, "ခဏလေးနော်... AI ဆီက အဖြေမလာလို့ပါ။")

if __name__ == "__main__":
    bot.infinity_polling()
