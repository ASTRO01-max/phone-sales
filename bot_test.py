import telebot
from telebot import types

API_TOKEN = '8047119512:AAHOGhPKa1CJioPt1xEHpnR4EOj-b-C9U-4'
bot = telebot.TeleBot(API_TOKEN)

phones = {
    "iPhone": [
        {
            "model": "iPhone xs max",
            "price": "900 USD",
            "features": "6.1 dyuymli Super Retina XDR displey, Face ID, A14 Bionic chip",
            "storage": "256gb",
            "color": "Oq rang",
            "image": r"C:\Users\hp\Desktop\iPhones\ip 14 pro max.jpg"
        }
    ]
}

# Start komandasi
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup()
    for brand in phones:
        btn = types.InlineKeyboardButton(brand, callback_data=brand)
        markup.add(btn)
    bot.send_message(message.chat.id, "Assalomu alaykum!\nBotimizga xush kelibsiz!🤝\n\nSmartfon turini tanlang:", reply_markup=markup)

# Brend tanlansa
@bot.callback_query_handler(func=lambda call: call.data in phones.keys())
def show_models(call):
    brand = call.data
    markup = types.InlineKeyboardMarkup()
    for phone in phones[brand]:
        btn = types.InlineKeyboardButton(phone['model'], callback_data=f"show_{brand}_{phone['model']}")
        markup.add(btn)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=f"{brand} modellari:", reply_markup=markup)

# Telefon tafsiloti va rasmi
@bot.callback_query_handler(func=lambda call: call.data.startswith("show_"))
def show_phone(call):
    _, brand, model = call.data.split("_", 2)
    for phone in phones[brand]:
        if phone["model"] == model:
            caption = (
                f"📱 <b>Model:</b> {phone['model']} (Yangi)\n"
                f"🔧 <b>Xususiyatlari:</b> {phone['features']}\n"
                f"💾 <b>Xotira:</b> {phone['storage']}\n"
                f"🎨 <b>Rangi:</b> {phone['color']}\n"
                f"💲 <b>Narxi:</b> {phone['price']}"
            )

            markup = types.InlineKeyboardMarkup()
            markup.add(
                types.InlineKeyboardButton("Buyurtma berish 🛒", callback_data=f"order_{brand}_{model}"),
                types.InlineKeyboardButton("Orqaga 🔙", callback_data=brand)
            )

            with open(phone['image'], 'rb') as photo_file:
                bot.send_photo(chat_id=call.message.chat.id, photo=photo_file, caption=caption,
                               reply_markup=markup, parse_mode="HTML")
            return



@bot.callback_query_handler(func=lambda call: call.data.startswith("order_"))
def order_phone(call):
    _, brand, model = call.data.split("_", 2)
    username = call.from_user.username or call.from_user.first_name
    bot.send_message(call.message.chat.id, f"✅ {model} uchun buyurtmangiz qabul qilindi, {username}!\nTez orada siz bilan bog'lanamiz.📞")

print("Bot ishlayapti...")
bot.infinity_polling() 
