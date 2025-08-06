import os
from telegram import Update, ChatPermissions
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from datetime import timedelta

TOKEN = os.getenv("TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Botul este online și gata de moderare!")

async def warn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.reply_to_message.from_user if update.message.reply_to_message else None
    if user:
        await update.message.reply_text(f"⚠️ Avertisment pentru {user.mention_html()}.", parse_mode="HTML")
    else:
        await update.message.reply_text("❗ Trebuie să răspunzi la un mesaj pentru a avertiza.")

async def ban(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.reply_to_message.from_user if update.message.reply_to_message else None
    if user:
        await context.bot.ban_chat_member(update.effective_chat.id, user.id)
        await update.message.reply_text(f"⛔ {user.mention_html()} a fost banat.", parse_mode="HTML")
    else:
        await update.message.reply_text("❗ Trebuie să răspunzi la un mesaj pentru a bana.")

async def mute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.reply_to_message.from_user if update.message.reply_to_message else None
    if user:
        until_date = update.message.date + timedelta(minutes=10)
        permissions = ChatPermissions(can_send_messages=False)
        await context.bot.restrict_chat_member(update.effective_chat.id, user.id, permissions, until_date=until_date)
        await update.message.reply_text(f"🔇 {user.mention_html()} a fost amuțit 10 minute.", parse_mode="HTML")
    else:
        await update.message.reply_text("❗ Trebuie să răspunzi la un mesaj pentru a da mute.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("warn", warn))
    app.add_handler(CommandHandler("ban", ban))
    app.add_handler(CommandHandler("mute", mute))
    app.run_polling()
