import telebot  # importing part of the pyTelegramBotAPI library


with open("TOKEN.txt") as file:  # takes TOKEN code from TOKEN.txt file
    TOKEN = str(file.readline())


bot = telebot.TeleBot(TOKEN)  # defining bot TOKEN


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, f"Привет {message.from_user.first_name}! 💫 меня зовут todo bot и я умный помошник, "
                          f"который поможет тебе быть продуктивнее.")


'''@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)'''

bot.polling()
