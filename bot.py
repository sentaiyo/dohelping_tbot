import telebot  # importing part of the pyTelegramBotAPI library
from telebot import types

with open("TOKEN.txt") as file:  # takes TOKEN code from TOKEN.txt file
    TOKEN = str(file.readline())


bot = telebot.TeleBot(TOKEN)  # defining bot TOKEN


@bot.message_handler(commands=['help', 'start'])
def send_welcome(message):
    bot.reply_to(message, f"Привет {message.from_user.first_name}! 💫 меня зовут todo bot и я умный помошник, "
                          f"который поможет тебе быть продуктивнее.\nЕсли хочешь начать процесс создания новой цели 📈,"
                          f" пришли ок")
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("🪐ок🪐")
    markup.add(button1)

'''@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)'''

bot.polling()
