import telebot
from telebot.types import *
import os
from datetime import datetime
from phone import *
from phonePhotos import *
import time

API_TOKEN = '8047119512:AAHOGhPKa1CJioPt1xEHpnR4EOj-b-C9U-4'
bot = telebot.TeleBot(API_TOKEN)

user_orders = {}  

def save_order_to_file(username, phone_model, price):
    file_path = "buyurtmalar.txt"
    with open(file_path, "a") as file:
        order_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        file.write(f"Foydalanuvchi: {username}, Buyurtma: {phone_model}, Narxi: {price}, Vaqt: {order_time}\n")
    print(f"Buyurtma saqlandi: {username} - {phone_model}, Narx: {price}, Vaqt: {order_time}")

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, """Assalomu alekum!\nBotimizga Xush kelibsiz!""")
    time.sleep(1)
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("iPhone telefonlari", callback_data="iphone"))
    markup.add(InlineKeyboardButton("Samsung telefonlari", callback_data="samsung"))
    markup.add(InlineKeyboardButton("XiaoMi telefonlari", callback_data="xiaomi"))
    bot.send_message(message.chat.id, "Telefon markalarini tanlang📲:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "iphone")
def show_iphone_models(call):
    markup = InlineKeyboardMarkup()
    for model in phones.keys():
        if "iPhone" in model:
            btn = InlineKeyboardButton(model, callback_data=f"info_{model}")
            markup.add(btn)
    markup.add(InlineKeyboardButton("Orqaga🔙", callback_data="back_to_brands"))
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="iPhone modellari📱:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "samsung")
def show_samsung_models(call):
    markup = InlineKeyboardMarkup()
    for model in phones.keys():
        if "Samsung" in model:
            btn = InlineKeyboardButton(model, callback_data=f"info_{model}")
            markup.add(btn)
    markup.add(InlineKeyboardButton("Orqaga🔙", callback_data="back_to_brands"))
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Samsung modellari📱:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "xiaomi")
def show_xiaomi_models(call):
    markup = InlineKeyboardMarkup()
    for model in phones.keys():
        if "Xiaomi" in model:
            btn = InlineKeyboardButton(model, callback_data=f"info_{model}")
            markup.add(btn)
    markup.add(InlineKeyboardButton("Orqaga🔙", callback_data="back_to_brands"))
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="XiaoMi modellari📱:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("info_"))
def show_phone_info(call):
    bot.delete_message(call.message.chat.id, call.message.message_id)
    model = call.data.split("_")[1]
    phone = phones.get(model)
    photo = phone_PHOTOS.get(model)
    markup = InlineKeyboardMarkup()
    btn_back = InlineKeyboardButton("Orqaga🔙", callback_data="back_to_brands")
    btn_order = InlineKeyboardButton("Buyurtma berish 🛒", callback_data=f"order_{model}")
    markup.add(btn_order, btn_back)
    if photo:
        try:
            with open(photo, "rb") as photo_file:
                bot.send_photo(call.message.chat.id, photo_file)
        except FileNotFoundError:
            bot.send_message(call.message.chat.id, f"{model} uchun rasm topilmadi.")
    
    bot.send_message(call.message.chat.id,
                     f"📱Model: {phone['📱Model']}\n"
                     f"📲Xususiyatlari: {phone['📲Xususiyatlari']}\n"
                     f"💾Xotira: {phone['💾Xotira']}\n"
                     f"🎨Rangi: {phone['🎨Rangi']}\n"
                     f"💰Narxi: {phone['💰Narxi']} USD",
                     reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "back_to_brands")
def back_to_brands(call):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("iPhone telefonlari", callback_data="iphone"))
    markup.add(InlineKeyboardButton("Samsung telefonlari", callback_data="samsung"))
    markup.add(InlineKeyboardButton("XiaoMi telefonlari", callback_data="xiaomi"))
    
    bot.send_message(call.message.chat.id, "Telefon markalarini tanlang📱:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("order_"))
def order_phone(call):
    _, model = call.data.split("_", 1)
    username = call.from_user.username or "Ismi ko'rsatilmagan"
    phone = phones[model]

    if username not in user_orders:
        user_orders[username] = []

    if not any(order['model'] == phone['📱Model'] for order in user_orders[username]):
        user_orders[username].append({"model": phone['📱Model'], "price": int(phone['💰Narxi'])})
        save_order_to_file(username, phone['📱Model'], phone['💰Narxi'])
        bot.send_message(call.message.chat.id, f"📱 {phone['📱Model']} uchun buyurtmangiz qabul qilindi!")
    else:
        bot.send_message(call.message.chat.id, f"📱 {phone['📱Model']} avvaldan buyurtma ro'yxatida mavjud!")

    markup = InlineKeyboardMarkup()
    btn_new_order = InlineKeyboardButton("Ha", callback_data="new_order")
    btn_no_order = InlineKeyboardButton("Yo'q", callback_data="no_order")
    markup.add(btn_new_order, btn_no_order)

    bot.send_message(call.message.chat.id, "Yana buyurtma berishni xohlaysizmi?", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "new_order")
def new_order(call):
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("iPhone telefonlari", callback_data="iphone"))
    markup.add(InlineKeyboardButton("Samsung telefonlari", callback_data="samsung"))
    markup.add(InlineKeyboardButton("Xiaomi telefonlari", callback_data="xiaomi"))
    bot.send_message(call.message.chat.id, "Yangi buyurtma berish uchun telefon markalarini tanlang📱",
                     reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "no_order")
def show_cart(call):
    username = call.from_user.username or "Ismi ko'rsatilmagan"
    chat_id = call.message.chat.id

    if username in user_orders and user_orders[username]:
        total_price = 0
        orders_message = "Sizning tanlagan telefonlaringiz:\n"
        for order in user_orders[username]:
            orders_message += f"📱 {order['model']} - 💰 {order['price']} USD\n"
            total_price += order['price']
        orders_message += f"\n💰 Jami narx: {total_price} USD"

        checkout_markup = InlineKeyboardMarkup()
        checkout_btn = InlineKeyboardButton("Sotib olish💰", callback_data="checkout")
        checkout_markup.add(checkout_btn)

        bot.send_message(chat_id, orders_message, reply_markup=checkout_markup)
    else:
        bot.send_message(chat_id, "Hali hech qanday buyurtma tanlanmagan.")

@bot.callback_query_handler(func=lambda call: call.data == "checkout")
def checkout(call):
    username = call.from_user.username or "Ismi ko'rsatilmagan"
    chat_id = call.message.chat.id

    if username in user_orders and user_orders[username]:
        total_price = sum(order['price'] for order in user_orders[username])
        orders_message = " Sizning buyurtmalaringiz:\n\n"

        for order in user_orders[username]:
            orders_message += f"📱 {order['model']} - 💰 {order['price']} USD\n"

        orders_message += f"\n💰 Jami: {total_price} USD"
        markup = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        markup.add(KeyboardButton("Aloqa telefon no'merni yuborish ", request_contact=True))
        markup.add(KeyboardButton("Geolokatsiya yuborish ", request_location=True))
        bot.send_message(chat_id, orders_message, reply_markup=markup)
    else:
        bot.send_message(chat_id, "Hali buyurtmalar mavjud emas.")

    bot.send_message(chat_id, "Iltimos telefon no'meringizni yuboring.")
    
    del user_orders[username]

@bot.message_handler(content_types=['contact'])
def handle_contact(message):
    if message.contact is not None:
        chat_id = message.chat.id
        if chat_id not in user_orders:
            user_orders[chat_id] = {}
        user_orders[chat_id]['phone'] = message.contact.phone_number
        markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
        location_button = KeyboardButton("Geolokatsiyani yuborish ", request_location=True)
        markup.add(location_button)
        bot.send_message(chat_id, "Iltimos geolokatsiyangizni yuboring.", reply_markup=markup)

@bot.message_handler(content_types=['location'])
def handle_location(message):
    if message.location is not None:
        chat_id = message.chat.id
        username = message.from_user.username or "Ismi ko'rsatilmagan"
        latitude = message.location.latitude
        longitude = message.location.longitude

        if chat_id not in user_orders:
            user_orders[chat_id] = {}
        user_orders[chat_id]['location'] = (latitude, longitude)

        bot.send_message(
            chat_id,
            f"Rahmat, {username}!\nSizning buyurtmangiz qabul qilindi va yaqin orada yetkazib beriladi.\n\n"
            f"Manzil: kenglik {latitude}, uzunlik {longitude}.",
        )
        markup = InlineKeyboardMarkup()
        admin_button = InlineKeyboardButton("Admin🧑🏻‍💻", callback_data="admins")
        contact_button = InlineKeyboardButton("Aloqa 📞", callback_data="contact")
        markup.add(contact_button, admin_button)
        bot.send_message(chat_id, "To'liq ma'lumot olish uchun biz bilan bog'laning.", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "contact")
def contact_info(call):
    bot.send_message(call.message.chat.id, "Biz bilan bog'lanish uchun📞: +998998071134")

@bot.callback_query_handler(func=lambda call: call.data == "admins")
def admin_info(call):
    bot.send_message(call.message.chat.id, "Biz bilan bog'lanish uchun🧑🏻‍💻: @martin_0_001")

print("Bot ishlayapti...")
bot.infinity_polling() 


