from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from os import environ


TOKEN = environ["TOKEN"]
BOT_USERNAME = environ["BOT_USERNAME"]
# Commands

async def start_command( update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello World")

async def help_command( update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Help Command")

# Responses
# aqui revisa si es una url o un magnet
def handle_response(text: str) -> str:
    return text

# logica de los mensajes
async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == 'group':
        if BOT_USERNAME in text:
            response = "group"
        else: return
    else:
        response = "chat"
    await update.message.reply_text(response)

if __name__ in "__main__":
    print("Starting Bot")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start",start_command))

    print("Polling")
    app.run_polling(poll_interval=10)

    