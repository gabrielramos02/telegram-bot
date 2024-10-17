from time import sleep
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes, CallbackContext
from .api_request import send_magnet, request_info, request_torrent_info
from .handle_url import handle_url
from .barra_progreso import barra_progreso
import re

MENU = "<b>Progress</b>\n\nA beautiful menu with a shiny inline button."
MENU_MARKUP = InlineKeyboardMarkup(
    [[InlineKeyboardButton("Info", callback_data="Info")]]
)
# Responses
# aqui revisa si es una url o un magnet


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text
    magnet_regex = "^magnet:"
    # url_regex = "https?:\/\/(www\.)?[a-zA-Z0-9@:%._\\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\\+.~#?&//=]*)?"

    magnet_match = re.search(string=text, pattern=magnet_regex)
    # url_match = re.search(string=text,pattern=url_regex)

    print(f'User ({update.message.chat.id}) in {message_type}: "{text}"')

    if message_type == "group":
        return
    else:
        if magnet_match:
            if await send_magnet(text):
                response = "Agregado Correctamente"

                await context.bot.send_message(
                    update.message.from_user.id,
                    response,
                    reply_markup=MENU_MARKUP,
                    reply_to_message_id=update.message.id,
                )
                # await update.message.reply_text(response, reply_markup=MENU_MARKUP)
        # elif url_match:
        # response = handle_url(text)
        else:
            response = "URL con Formato Incorrecto"
            await update.message.reply_text(response)
            return
