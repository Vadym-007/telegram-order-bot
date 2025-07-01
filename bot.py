
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import os

orders = {}
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[KeyboardButton("☕ Зробити замовлення")]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Привіт! Натисни кнопку або напиши замовлення ☕", reply_markup=reply_markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user.full_name
    text = update.message.text
    if text == "☕ Зробити замовлення":
        await update.message.reply_text("Введи замовлення:")
        return
    orders[user] = text
    await update.message.reply_text(f"✅ Замовлення прийнято, {user}!")

async def list_orders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not orders:
        await update.message.reply_text("Немає замовлень.")
    else:
        await update.message.reply_text("🧾 Замовлення:
" + "\n".join(f"- {u}: {o}" for u, o in orders.items()))

async def send_orders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not orders:
        await update.message.reply_text("Список порожній.")
    else:
        await update.message.reply_text("📤 Зведення:
" + "\n".join(f"- {u}: {o}" for u, o in orders.items()))

async def clear_orders(update: Update, context: ContextTypes.DEFAULT_TYPE):
    orders.clear()
    await update.message.reply_text("🗑️ Замовлення очищено.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("list", list_orders))
    app.add_handler(CommandHandler("send", send_orders))
    app.add_handler(CommandHandler("clear", clear_orders))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("✅ Бот запущено")
    app.run_polling()
