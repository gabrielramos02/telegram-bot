from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from os import environ
from commands.start import start_command
from commands.help import help_command
from responses.handle_message import handle_message
from responses.button_tap import button_tap
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TOKEN = environ["TOKEN"]
BOT_USERNAME = environ["BOT_USERNAME"]


#App Initial
if __name__ in "__main__":
   
    app = Application.builder().token(TOKEN).concurrent_updates(True).build()

    app.add_handler(CommandHandler("start",start_command,block=False))

    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    app.add_handler(CallbackQueryHandler(button_tap))
        
    app.run_polling()
    
    

    