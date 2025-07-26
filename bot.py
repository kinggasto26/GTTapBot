from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler

TOKEN = "8364907543:AAH7qJQIX2cuVUHsMg1wKVfIbooblXtAPy8"

user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_data[user.id] = {"gt_balance": 0, "taps": 0}
    keyboard = [
        [InlineKeyboardButton("👉 TAP 👈", callback_data='tap')],
        [InlineKeyboardButton("📊 Balance", callback_data='balance')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Karibu kwenye GTTapBot!", reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user
    if user.id not in user_data:
        user_data[user.id] = {"gt_balance": 0, "taps": 0}

    if query.data == 'tap':
        user_data[user.id]["taps"] += 1
        user_data[user.id]["gt_balance"] += 0.12
        await query.answer("Umetap!")
    elif query.data == 'balance':
        taps = user_data[user.id]["taps"]
        balance = user_data[user.id]["gt_balance"]
        await query.answer()
        await query.edit_message_text(f"Taps zako: {taps}\nGT Balance: {balance:.2f}")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(button))
app.run_polling()