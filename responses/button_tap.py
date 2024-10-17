from asyncio import sleep
from telegram import Message, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

from .barra_progreso import barra_progreso
from .api_request import delete_magnet, request_info, request_torrent_info

CANCEL_MARKUP = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                "Cancel",
                callback_data="Cancel",
            )
        ]
    ]
)


async def button_tap(update: Update, context: CallbackContext):

    # print(update.callback_query.message.reply_to_message.text)

    data = update.callback_query.data
    text = update.callback_query.message.reply_to_message.text
    markup = None
    print(data)
    await update.callback_query.answer(text="")
    if data == "Cancel" and text != "Cancelado":
        torrent = await get_torrent(text)
        await delete_magnet(torrent.get("hash"))
        await update.callback_query.edit_message_text("Cancelado")
    if data == "Info":
        await progress_menu(text, update, context)


async def progress_menu(text: str, update: Update, context: CallbackContext):
    torrent = await get_torrent(text)
    # torrent_list = await request_info()
    # torrent = dict()
    message = Message(
        message_id=update.callback_query.message.id,
        date=update.callback_query.message.date,
        chat=update.callback_query.message.from_user.id,
    )

    # for t in torrent_list:

    #     if t.get("magnet_uri") == text:

    #         torrent = t

    #         break

    while True:
        info = await request_torrent_info(torrent.get("hash"))
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
                await sleep(3)
            info = await request_torrent_info(torrent.get("hash"))

        descargado = 0
        total = 0
        is_seed = True
        # print(info)
        #print(info)
        for file in info:
            #print(file.get("is_seed"))
            if file.get("is_seed"):
                break
            else:
                is_seed = False
            descargado = descargado + file.get("progress") * file.get("size")
            total = total + file.get("size")

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
        percent = descargado * 100 / total

        # print(f'Downloaded: {info.get("total_downloaded")}, Total: {info.get("total_size")} ')
        # print(percent)
        text = barra_progreso(percent)

        # print(message.text)

        message_text = f"Progreso\n\n{text}   {percent}%"

        if message.text != message_text:
            message = await update.callback_query.edit_message_text(
                message_text, parse_mode="html", reply_markup=CANCEL_MARKUP
            )
        await sleep(8)
        # await update.message.edit_text("En Proceso")

        # percent = torrent.
        # barra_progreso()


async def get_torrent(text):
    torrent_list = await request_info()
    torrent = dict()
    for t in torrent_list:

        if t.get("magnet_uri") == text:
            
            torrent = t
            
            break
    return torrent
