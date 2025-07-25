from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "WEKA_HAPA_BOT_TOKEN_YAKO"

user_data = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_data[user.id] = {"gt_balance": 0, "taps": 0}
    keyboard = [
        [InlineKeyboardButton("👉 TAP 👈", callback_data="tap")],
        [InlineKeyboardButton("📊 Balance", callback_data="balance")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Karibu kwenye GTTapBot! Bonyeza TAP ili upate GT Token:", reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user = query.from_user
    await query.answer()

    if user.id not in user_data:
        user_data[user.id] = {"gt_balance": 0, "taps": 0}

    if query.data == "tap":
        user_data[user.id]["gt_balance"] += 0.12
        user_data[user.id]["taps"] += 1
        await query.edit_message_text(text=f"Umebonyeza TAP! 🎉\nGT Token zako: {user_data[user.id]['gt_balance']:.2f}")
    elif query.data == "balance":
        balance = user_data[user.id]["gt_balance"]
        taps = user_data[user.id]["taps"]
        await query.edit_message_text(text=f"📊 BALANCE 📊\nGT Token: {balance:.2f}\nTaps: {taps}")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    print("Bot inaendeshwa...")
    app.run_polling()

if __name__ == "__main__":
    main()