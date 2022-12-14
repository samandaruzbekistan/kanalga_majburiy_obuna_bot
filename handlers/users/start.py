from aiogram import types
from loader import bot,dp
from aiogram.dispatcher.filters.builtin import CommandStart
from data.config import CHANNELS
from keyboards.inline.subscription import check_button
from loader import dp
from utils.misc import subscription


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    text = ""
    for channel in CHANNELS:
        chat = await bot.get_chat(channel)
        invite_link = await chat.export_invite_link()
        # logging.info(invite_link) https://t.me/samandar_sariboyev
        text += f"👉 <a href='{invite_link}'>{chat.title}</a>\n"

    await message.answer(f"Quyidagi kanallarga obuna bo'ling: \n"
                         f"{text}",
                         reply_markup=check_button,
                         disable_web_page_preview=True)

@dp.callback_query_handler(text="check_subs")
async def checker(call: types.CallbackQuery):
    await call.answer()
    result = ""
    s = 0
    count = len(CHANNELS)
    for channel in CHANNELS:
        status = await subscription.check(user_id=call.from_user.id,
                                          channel=channel)
        channel = await bot.get_chat(channel)
        if status:
            s += 1
            result += f"<b>{channel.title}</b> kanaliga obuna bo'lgansiz!\n\n"
        else:
            invite_link = await channel.export_invite_link()
            result += (f"<b>{channel.title}</b> kanaliga obuna bo'lmagansiz. "
                       f"<a href='{invite_link}'>Obuna bo'ling</a>\n\n")
    if s != count:
        await call.message.answer("Botdan foydalana olmaysiz")
    else:
        await call.message.answer("Botdan foydalanishingiz mumkin")
    await call.message.answer(result, disable_web_page_preview=True)