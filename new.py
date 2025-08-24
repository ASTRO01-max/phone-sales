# n = 22
# m = bin(n)[2:]
# lst = []

# for i in m:
#     if i == "1":
#         lst.append(int(i))
# print(lst)

# n = 22
# m = bin(n)[2:]

# lst = []

# for i in m:
#     lst.append(i)
# print(lst)


# class Solution:
#     def binaryGap(self, n: int) -> int:
#         binary = list(bin(n)[2:])
#         indicies=[]
#         for i in range(len(binary)):
#             if (binary[i]=='1'):
#                 indicies.append(i)
#         distance=0
#         for i in range(1,len(indicies)):
#             if (indicies[i]-indicies[i-1]>distance):
#                 distance=indicies[i]-indicies[i-1]
#         return distance

# lst = [1, 2, 3]
# n = 0

# n = lst[-1]   # lst[-1] = 3
# n += 1        # n = 4

# lst[2] = n    # lst[2] ni 4 bilan almashtirdik

# print(lst)    # [1, 2, 4]

# @bot.callback_query_handler(func=lambda call: call.data == "iphone")
# def show_iphone_models(call):
#     markup = InlineKeyboardMarkup()
#     for model in phones.keys():
#         if "iPhone" in model:
#             btn = InlineKeyboardButton(model, callback_data=f"info_{model}")
#             markup.add(btn)
#     markup.add(InlineKeyboardButton("Orqaga🔙", callback_data="back_to_brands"))
#     bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
#                           text="iPhone modellari📱:", reply_markup=markup)

# @bot.callback_query_handler(func=lambda call: call.data == "samsung")
# def show_samsung_models(call):
#     markup = InlineKeyboardMarkup()
#     for model in phones.keys():
#         if "Samsung" in model:
#             btn = InlineKeyboardButton(model, callback_data=f"info_{model}")
#             markup.add(btn)
#     markup.add(InlineKeyboardButton("Orqaga🔙", callback_data="back_to_brands"))
#     bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
#                           text="Samsung modellari📱:", reply_markup=markup)

# @bot.callback_query_handler(func=lambda call: call.data == "xiaomi")
# def show_xiaomi_models(call):
#     markup = InlineKeyboardMarkup()
#     for model in phones.keys():
#         if "Xiaomi" in model:
#             btn = InlineKeyboardButton(model, callback_data=f"info_{model}")
#             markup.add(btn)
#     markup.add(InlineKeyboardButton("Orqaga🔙", callback_data="back_to_brands"))
#     bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
#                           text="XiaoMi modellari📱:", reply_markup=markup)

# @bot.callback_query_handler(func=lambda call: call.data.startswith("info_"))
# def show_phone_info(call):
#     bot.delete_message(call.message.chat.id, call.message.message_id)
#     model = call.data.split("_", 1)[1]
#     phone = phones.get(model)
#     photo = phone_PHOTOS.get(model)
#     markup = InlineKeyboardMarkup()
#     btn_back = InlineKeyboardButton("Orqaga🔙", callback_data="back_to_brands")
#     btn_order = InlineKeyboardButton("Buyurtma berish 🛒", callback_data=f"order_{model}")
#     markup.add(btn_order, btn_back)
#     if photo:
#         try:
#             with open(photo, "rb") as photo_file:
#                 bot.send_photo(call.message.chat.id, photo_file)
#         except FileNotFoundError:
#             bot.send_message(call.message.chat.id, f"{model} uchun rasm topilmadi.")
    
#     bot.send_message(call.message.chat.id,
#                      f"📱Model: {phone['📱Model']}\n"
#                      f"📲Xususiyatlari: {phone['📲Xususiyatlari']}\n"
#                      f"💾Xotira: {phone['💾Xotira']}\n"
#                      f"🎨Rangi: {phone['🎨Rangi']}\n"
#                      f"💰Narxi: {phone['💰Narxi']} USD",
#                      reply_markup=markup)




import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.client.default import DefaultBotProperties

TOKEN = "8047767402:AAFTQqDBCSW70gImz9VZR6HW4zk77oW9FAc"
dp = Dispatcher()

@dp.message(CommandStart())
async def command_start(message: Message):
    # start komandasiga javob
    await message.answer("Salom! Iltimos, 1 dan katta biror son yuboring, masalan: 5")


@dp.message(lambda message: message.text and message.text.isdigit())
async def send_buttons(message: Message):
    num = int(message.text)
    buttons = []
    k = 0
    for i in range(1, num):
        k += i
        buttons.append([KeyboardButton(text=str(k))])

    keyboard = ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True,
    )
    await message.answer("Quyidagi tugmalardan birini tanlang:", reply_markup=keyboard)


@dp.message()
async def echo_handler(message: Message) -> None:
    try:
        if message.text.lower() == "jinniman":
            await message.answer("Ha sen jinnisan 🤪")
        else:
            await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer("Nice try!")


async def main() -> None:
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())

