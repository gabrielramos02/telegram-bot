from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler, CallbackContext, ApplicationBuilder
from os import environ
from commands.start import start_command
from commands.help import help_command
from responses.handle_message import handle_message
from responses.button_tap import button_tap

TOKEN = environ["TOKEN"]
BOT_USERNAME = environ["BOT_USERNAME"]

async def cancel(update: Update, context: CallbackContext):
    print("hola")


#App Initial
if __name__ in "__main__":
    print("Starting Bot")
    app = Application.builder().token(TOKEN).concurrent_updates(True).build()

    app.add_handler(CommandHandler("start",start_command,block=False))

    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    app.add_handler(CallbackQueryHandler(pattern="Cancel",callback=cancel))
    app.add_handler(CallbackQueryHandler(pattern="Info",callback=button_tap))
        
    print("Polling")
    app.run_polling()
    
    

    