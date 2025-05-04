import os
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler
from src.database import SessionLocal, User

load_dotenv()

TELEGRAM_API_TOKEN = os.getenv("TELEGRAM_API_TOKEN")

async def start(update, context):
    chat_id = str(update.message.chat_id)
    username = update.message.from_user.chat_id

    if not username:
        await update.message.reply_text("⚠️ You must set a Telegram username in your settings to use price alerts.")
        print(f"User with chat_id {chat_id} has no username")
        return
    
    db = SessionLocal()
    existing_user = db.query(User).filter(User.chat_id == chat_id).first()

    if existing_user is None:
        user = User(chat_id=chat_id, username=username)
        db.add(user)
        db.commit()
        await update.message.reply_text(f"✅ You are successfully subscribed as @{username}!")
        print(f"User @{username} ({chat_id}) subscribed and added to DB.")
    else:
        await update.message.reply_text("⚠️ You're already subscribed for alerts.")
        print(f"User @{username} ({chat_id}) already exists.")

    db.close()

def main():
    app = ApplicationBuilder().token(TELEGRAM_API_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()

if __name__ == "__main__":
    main()
