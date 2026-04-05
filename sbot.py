import telebot
import requests

# သင်၏ Telegram Bot Token
TOKEN = "8754953424:AAG1-wKJ7uJVdMNk9s-KFThkPnLL5RSAgEA"
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "မင်္ဂလာပါ! ကျွန်တော်က Chat AI Bot ပါ။ သိချင်တာတွေကို စာရိုက်ပြီး မေးမြန်းနိုင်ပါတယ်ဗျာ။")

@bot.message_handler(func=lambda message: True)
def chat_ai(message):
    user_query = message.text
    # အဖြေရှာနေစဉ် ခဏစောင့်ရန် အသိပေးခြင်း
    status_msg = bot.reply_to(message, "🔍 အဖြေရှာပေးနေပါတယ်... ခဏစောင့်ပါ...")
    
    try:
        # AI API သို့ ချိတ်ဆက်မေးမြန်းခြင်း (အခမဲ့ AI စနစ်)
        api_url = f"https://nexra.aryahcr.cc/api/ai/chatgpt?prompt={user_query}&model=gpt-4"
        response = requests.get(api_url, timeout=30)
        
        if response.status_code == 200:
            ai_answer = response.json().get('gpt', 'နားမလည်နိုင်ဖြစ်နေပါတယ်ဗျာ။')
            bot.edit_message_text(ai_answer, message.chat.id, status_msg.message_id)
        else:
            bot.edit_message_text("⚠️ AI Server အလုပ်မလုပ်သေးပါ။", message.chat.id, status_msg.message_id)
            
    except Exception as e:
        bot.edit_message_text(f"❌ Error: {str(e)}", message.chat.id, status_msg.message_id)

bot.infinity_polling()
