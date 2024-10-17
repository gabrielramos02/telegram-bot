from asyncio import sleep
from telegram import Update
from telegram.ext import ContextTypes
from responses.api_request import request_info

async def start_command( update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("Command: Start")
    await update.message.reply_text("Hello World")