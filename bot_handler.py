from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    ContextTypes,
    filters,
    CommandHandler
)
import asyncio
from telegram.constants import ParseMode
import os
from dotenv import load_dotenv
from validator import is_valid_url
from bypass_service import bypass_url
from user_client import client
from queue_state import lock, request_counter
from logger import logger
from telegram.error import TimedOut, NetworkError, RetryAfter


load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
active_users = set()


def create_bot():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    return app

async def start_command(update: Update, context):
    user = update.message.from_user

    user_id = user.id
    username = f"@{user.username}" if user.username else "N/A"

    logger.info(
        f"user_id={user_id} | username={username} | command=/start"
    )
    
    text = (
        "👋 *Welcome to Bypass Bot!*\n\n"
        "🔗 *What this bot does:*\n"
        "Send any supported short link and I’ll try to bypass it for you.\n\n"
        "🛠 *How to use:*\n"
        "1️⃣ Send a short URL (example: `https://xyz.in/abc`)\n"
        "2️⃣ Your request will be added to a queue\n"
        "3️⃣ Please wait while your link is processed\n"
        "4️⃣ You’ll receive the bypassed link or an error\n\n"
        "⚠️ *Notes:*\n"
        "• Some links may not be supported\n"
        "• Requests are processed one by one\n"
        "• Please don’t spam\n\n"
        "🚀 *Just send a link to begin!*"
    )

    await update.message.reply_text(
        text,
        parse_mode=ParseMode.MARKDOWN
    )


async def handle_message(update, context):
    user = update.message.from_user

    user_id = user.id
    username = f"@{user.username}" if user.username else "N/A"
    text = update.message.text

    logger.info(
        f"user_id={user_id} | username={username} | text={text}"
    )



    text = update.message.text

    if not is_valid_url(text):
        await update.message.reply_text("❌ Please send a valid URL")
        return

    

    if user_id in active_users:
        await update.message.reply_text(
                "⏳ You already have a request in progress. Please wait."
            )
        return

    active_users.add(user_id)


    async with lock:
        context.application.bot_data["request_counter"] += 1
        my_position = (
            context.application.bot_data["request_counter"]
            - context.application.bot_data["processed_counter"]
        )

    status_message = await update.message.reply_text(
        f"⏳ Your link is added to queue\n"
        f"📌 Queue position: {my_position}"
    )

    await context.application.bot_data["queue"].put(
        (update, context, text, status_message)
    )


        
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    error = context.error

    if isinstance(error, RetryAfter):
        wait_time = error.retry_after
        print(f"⏳ Flood control hit. Sleeping for {wait_time} seconds...")
        await asyncio.sleep(wait_time)
        return

    if isinstance(error, (TimedOut, NetworkError)):
        print("⚠️ Network/Telegram timeout occurred, ignored.")
        return

    print("❌ Unexpected error:", error)
