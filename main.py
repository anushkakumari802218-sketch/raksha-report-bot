import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

logging.basicConfig(level=logging.INFO)
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🛡️ *Raksha Report Bot*\n\n"
        "Aap yaha gumnam tarike se report bhej sakte hai.\n"
        "Bas apna message likh ke bhejiye, main admin tak pahuncha dungi.\n\n"
        "Aapki pehchan gupt rahegi.",
        parse_mode="Markdown"
    )

async def handle_report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text
    # User ko confirmation
    await update.message.reply_text("✅ Aapki report surakshit mil gayi. Dhanyavaad! 🙏\nAapki pehchan gupt rahegi.")

    # Admin ko bhejo agar ID hai to
    if ADMIN_ID and BOT_TOKEN:
        try:
            admin_text = f"🚨 *New Raksha Report*\n\n{user_msg}\n\n_Anonymous_"
            await context.bot.send_message(chat_id=ADMIN_ID, text=admin_text, parse_mode="Markdown")
        except Exception as e:
            logging.error(e)

def main():
    if not BOT_TOKEN:
        logging.error("BOT_TOKEN nahi mila!")
        return
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_report))
    app.run_polling()

if __name__ == "__main__":
    main()