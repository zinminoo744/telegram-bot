from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler, CallbackQueryHandler,
    ContextTypes
)
from duckduckgo_search import DDGS
from keep_alive import keep_alive

# ✅ Web Search Function
def search_web(query):
    with DDGS() as ddgs:
        results = ddgs.text(query, max_results=3)
        return "\n\n".join([f"{r['title']}\n{r['href']}" for r in results]) or "No results found."

# ✅ /start Command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Search 🔍", callback_data='search')],
        [InlineKeyboardButton("Movie(use vpn) 🍿", callback_data='movie')],
        [InlineKeyboardButton("Book 📚", callback_data='book')],
        [InlineKeyboardButton("Contact 📩", callback_data='contact')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Welcome! ကြိုက်ရာရွေးပြီး သုံးနိုင်ပါတယ်💖:", reply_markup=reply_markup)

# ✅ /search Command
async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args:
        query = " ".join(context.args)
        result = search_web(query)
        await update.message.reply_text(result)
    else:
        await update.message.reply_text("Usage: /search your query")

# ✅ /movie Command
async def movie(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎬 Visit Channel Myanmar: https://channelmyanmar.org")

# ✅ /book Command
async def book(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📚 Browse Myanmar Books: https://www.shwenarsin.com/category")

# ✅ /contact Command
async def contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📩 You can contact @mgzim anytime.")

# ✅ Handle Inline Buttons
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'search':
        await query.message.reply_text("Please use /search <your query>")
    elif query.data == 'movie':
        await movie(query, context)
    elif query.data == 'book':
        await book(query, context)
    elif query.data == 'contact':
        await contact(query, context)

# ✅ Bot Setup
def main():
    keep_alive()

    app = ApplicationBuilder().token("7988888713:AAGnQn4CFnX7NGaN6a7YzL0AvEfDExEtfsI").build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("search", search))
    app.add_handler(CommandHandler("movie", movie))
    app.add_handler(CommandHandler("book", book))
    app.add_handler(CommandHandler("contact", contact))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()
