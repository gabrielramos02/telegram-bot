from curses.ascii import CAN
from time import sleep
from telegram import Message, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from .barra_progreso import barra_progreso
from .api_request import request_info, request_torrent_info

CANCEL_MARKUP = InlineKeyboardMarkup(
    [[InlineKeyboardButton("Cancel", callback_data="Cancel",)]]
)

async def button_tap(update: Update, context: CallbackContext):

    # print(update.callback_query.message.reply_to_message.text)

    data = update.callback_query.data
    text = update.callback_query.message.reply_to_message.text
    markup = None
    print(data)
    await update.callback_query.answer(text="")
    if data == "Cancel" and text != "Cancelado":
        await update.callback_query.edit_message_text("Cancelado")
    if data == "Info":
        await progress_menu(text, update, context)
    



async def progress_menu(text: str, update: Update, context: CallbackContext):
    torrent_list = request_info()
    torrent = dict()
    message = Message(
        message_id=update.callback_query.message.id,
        date=update.callback_query.message.date,
        chat=update.callback_query.message.from_user.id,
    )

    for t in torrent_list:
        if t.get("magnet_uri") == text:

            torrent = t

            break

    while True:
        info = request_torrent_info(torrent.get("hash"))
        if info == "404":
            message = await update.callback_query.edit_message_text(
                "Torrent no encontrado"
            )
            break
        while info == []:
            if message.text != "Descargando Metadata":
                message = await update.callback_query.edit_message_text(
                    "Descargando Metadata",
                    reply_markup=CANCEL_MARKUP,
                )
                sleep(8)
            info = request_torrent_info(torrent.get("hash"))
            sleep(8)

        progress = 0
        is_seed = True
        # print(info)

        for file in info:
            if file.get("is_seed"):
                # print(file.get("is_seed"))
                pass
            else:
                is_seed = False
            progress = progress + file.get("progress")

        # print(is_seed)
        # print(info.get("completion_date"))
        if is_seed:
            # Torrent Completado
            message = await update.callback_query.edit_message_text(
                "Completado",
                reply_markup=CANCEL_MARKUP,
            )
            break
        # print(update.message.id)
        percent = progress * 100

        # print(f'Downloaded: {info.get("total_downloaded")}, Total: {info.get("total_size")} ')
        # print(percent)
        text = barra_progreso(percent)

        #print(message.text)

        message_text = f"Progreso\n\n{text}   {percent}%"

        if message.text != message_text:
            message = await update.callback_query.edit_message_text(
                message_text,
                parse_mode="html",
                reply_markup=CANCEL_MARKUP
            )
        sleep(8)
        # await update.message.edit_text("En Proceso")

        # percent = torrent.
        # barra_progreso()
