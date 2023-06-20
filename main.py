import telebot
from nltk.tokenize import word_tokenize
import nltk

nltk.download('punkt')

bot = telebot.TeleBot("5880664554:AAEiCndxs69oWLV9JTy70Xc3H4Wj4BhYGL0")


@bot.message_handler(commands=['start'])

def send_welcome(message):
    bot.reply_to(message, "Привет, я доставлю для тебя вкуснейшую пиццу, но перед этим мне нужно узнать твоё имя.")
    bot.register_next_step_handler(message, get_name)

def get_name(message):
    name = message.text
    bot.reply_to(message, "Большую, среднюю или маленькую пиццу вы хотите? - выбирите.", reply_markup=create_pizza_buttons())
    bot.register_next_step_handler(message, get_pizza, name)

def create_pizza_buttons():
    markup = telebot.types.ReplyKeyboardMarkup(row_width=3)
    markup.add(telebot.types.KeyboardButton("Большую"), telebot.types.KeyboardButton("Среднюю"), telebot.types.KeyboardButton("Маленькую"))
    return markup

def get_pizza(message, name):
    pizza_size = message.text.lower()
    if "большую" in pizza_size:
        pizza_size = "Большую"
    elif "среднюю" in pizza_size:
        pizza_size = "Среднюю"
    elif "маленькую" in pizza_size:
        pizza_size = "Маленькую"
    else:
        bot.reply_to(message, "Выберите пожалуйста корректный размер пиццы: 'большую', 'среднюю' или 'маленькую'")
        return

    bot.reply_to(message, "Какой способ оплаты вы будете использовать?", reply_markup=create_payment_buttons())
    bot.register_next_step_handler(message, get_payment, name, pizza_size)

def create_payment_buttons():
    markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
    markup.add(telebot.types.KeyboardButton("Наличными"), telebot.types.KeyboardButton("Картой"))
    return markup

def get_payment(message, name, pizza_size):
    payment_method = message.text.lower()
    bot.reply_to(message, "Куда доставить пиццу?(Напишите пожалуйста адрес вручную)")
    bot.register_next_step_handler(message, confirm_order, name, pizza_size, payment_method)

def confirm_order(message, name, pizza_size, payment_method):
    address = message.text

    if payment_method in ('нал', 'налич', 'наличка'):
        if pizza_size == "Большую":
            order = f"Вы хотите большую пиццу, оплата – наличными, доставить по адресу {address}. Вы подтверждаете заказ?"
        elif pizza_size == "Среднюю":
            order = f"Вы хотите среднюю пиццу, оплата – наличными, доставить по адресу {address}. Вы подтверждаете заказ?"
        else:
            order = f"Вы хотите маленькую пиццу, оплата – наличными, доставить по адресу {address}. Вы подтверждаете заказ?"
    elif payment_method in ('без', 'безнал'):
        if pizza_size == "Большую":
            order = f"Вы хотите большую пиццу, оплата – картой, доставить по адресу {address}. Вы подтверждаете заказ?"
        elif pizza_size == "Среднюю":
            order = f"Вы хотите среднюю пиццу, оплата – картой, доставить по адресу {address}. Вы подтверждаете заказ?"
        else:
            order = f"Вы хотите маленькую пиццу, оплата – картой, доставить по адресу {address}. Вы подтверждаете заказ?"
    else:
        order = "Выберите способ оплаты корректно: 'нал', 'налич', 'наличка' или 'без', 'безнал'"

    markup = telebot.types.ReplyKeyboardMarkup(row_width=2)
    markup.add(telebot.types.KeyboardButton("Да"), telebot.types.KeyboardButton("Нет"))

    bot.reply_to(message, order, reply_markup=markup)
    bot.register_next_step_handler(message, place_order, name, pizza_size, payment_method, address)

def place_order(message, name, pizza_size, payment_method, address):
    confirmation = message.text.lower()
    if confirmation == "да":
        bot.reply_to(message, f"Спасибо за заказ, {name}! Ожидайте самую вкусную пиццу в вашей жизни)))"
                              f"")
    else:
        bot.reply_to(message, "Хорошо, начнем заново.")
        bot.send_message(message.chat.id, "Как вас зовут?")
        bot.register_next_step_handler(message, get_name)

bot.polling(none_stop=True)