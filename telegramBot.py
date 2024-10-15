from pydoc import resolve
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from os import environ
from commands.start import start_command
from commands.help import help_command
from responses.handle_magnet import handle_magnet
from responses.handle_url import handle_url
import re

TOKEN = environ["TOKEN"]
BOT_USERNAME = environ["BOT_USERNAME"]

# Responses
# aqui revisa si es una url o un magnet
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text
    magnet_regex = "^magnet:"
    #url_regex = "https?:\/\/(www\.)?[a-zA-Z0-9@:%._\\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\\+.~#?&//=]*)?"

    magnet_match = re.search(string=text,pattern=magnet_regex)
    #url_match = re.search(string=text,pattern=url_regex)

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == 'group':
        return
    else:
        if magnet_match:
            response = handle_magnet(text)
        #elif url_match:
            #response = handle_url(text)
        else: 
            response = "URL con formato incorrecto"
    await update.message.reply_text(response)


#App Initial
if __name__ in "__main__":
    print("Starting Bot")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start",start_command))

    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    print("Polling")
    app.run_polling(poll_interval=3)

    