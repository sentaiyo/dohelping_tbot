import telebot
import config


#from telebot import types

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=["start", "help"])
def start_replier(message):
    bot.send_message(message.chat.id, "Привет 💫, {0.first_name}!\nменя зовут toDoBot и я умный бот, который поможет "
                     "тебе быть продуктивнее".format(
                         message.from_user, bot.get_me()),
                     parse_mode='html')
    bot.send_message(message.chat.id, "/add - добавить новую задачу\n/del - удалить задачу")


@bot.message_handler(commands=["add"])
def add_task(message):
    bot.send_message(message.chat.id, "отправь, пожалуйста, новую задачу")
    bot.register_next_step_handler(message, get_task)


def get_task(message):
    task = message.text
    #добавляем task в бд к пользователю message.chat.id


@bot.message_handler(commands=["del"])
def del_task(message):
    bot.send_message(message.chat.id, "отправь задачу, которую нужно удалить")
    bot.register_next_step_handler(message, remove_task_from_data_base)


def remove_task_from_data_base(message):
    task = message.text
    # удаляем task из бд пользователя message.chat.id


@bot.message_handler(commands=["list"])
def list_tasks(message):
    bot.reply_to(message, message.text)


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)


if __name__ == '__main__':
     bot.infinity_polling()