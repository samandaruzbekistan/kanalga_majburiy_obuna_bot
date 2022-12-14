from aiogram import types
import wikipedia
from utils.misc import subscription
from data.config import CHANNELS
from loader import dp
wikipedia.set_lang("uz")

# Echo bot
@dp.message_handler(state=None)
async def bot_echo(message: types.Message):
    s = 0
    count = len(CHANNELS)
    for channel in CHANNELS:
        status = await subscription.check(user_id=message.from_user.id,
                                          channel=channel)
        if status:
            s += 1
    if s == count:
        try:
            await message.answer(wikipedia.summary(message.text, sentences=20))
            try:
                await message.answer_photo(wikipedia.page(message.text).images[0])
            except:
                pass
        except:
            await message.answer("Malumot topilmadi")
    else:
        await message.answer("Botdan foydalana olmaysiz. /start ni bosib kanallarga obuna bo'ling")