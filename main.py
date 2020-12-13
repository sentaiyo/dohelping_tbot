import telebot
from datetime import datetime
import schedule
from threading import Thread
from time import sleep

now = datetime.now()
current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time)

TOKEN = '1494234926:AAGrHyvPpoLtz8NYKX0hpw6y2wysKcZgOig'
bot = telebot.TeleBot(TOKEN)
message_id = None
your_time = None


@bot.message_handler(commands=['start'])
def send_welcome(message):
    global message_id
    message_id = message.chat.id
    bot.reply_to(message, "choose time you want to wake up")


@bot.message_handler(content_types=["text"])
def get_time(message):
    global your_time
    your_time = message.text
    bot.send_message(message.chat.id, 'Hello')
    Thread(target=schedule_checker(your_time)).start()


def schedule_checker(my_time):
    if your_time is not None:
        schedule.every().day.at(my_time).do(send_message)
        while True:
            schedule.run_pending()
            sleep(1)


def send_message():
    bot.send_message(message_id, 'Wake up!!!')

if __name__ == "__main__":
    bot.polling(none_stop=True, interval=0)

