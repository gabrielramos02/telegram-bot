from asyncio import sleep
from telegram import Update
from telegram.ext import ContextTypes

async def start_command( update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("Command: Start")
    await sleep(15)
    await update.message.reply_text("Hello World")