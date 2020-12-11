import telebot
import config
from database import UsersData
import schedule
from threading import Thread
from time import sleep

# from telebot import types

bot = telebot.TeleBot(config.TOKEN)
difficulty = None
task = None
time = None
user_id = None


@bot.message_handler(commands=["start", "help"])
def start_replier(message):
    bot.send_message(message.chat.id, "Привет 💫, {0.first_name}!\nменя зовут toDoBot и я умный бот, который поможет "
                     "тебе быть продуктивнее".format(
                         message.from_user, bot.get_me()),
                     parse_mode='html')
    bot.send_message(message.chat.id, "/add - добавить новую задачу\n/del - удалить задачу\n/list - список всех задач")
    users_data = UsersData(config.table_path)
    users_data.add_user(message.from_user.id)


@bot.message_handler(commands=["add"])
def ask_difficulty(message):
    bot.send_message(message.chat.id, "отправь, пожалуйста, сложность своей задачи от 1 до 3")
    bot.register_next_step_handler(message, get_difficulty)


def get_difficulty(message):
    global difficulty
    difficulty = message.text  # добавляем сложность новой задачи
    bot.send_message(message.chat.id, "отправь, пожалуйста, текстовым сообщением новую задачу")
    bot.register_next_step_handler(message, get_task)


"""def add_task(message):
    bot.send_message(message.chat.id, "отправь, пожалуйста, текстовым сообщением новую задачу")
    bot.register_next_step_handler(message, get_task)"""


def get_task(message):
    global task
    global difficulty
    task = message.text
    users_data = UsersData(config.table_path)
    users_data.add_task(task, difficulty, message.from_user.id)  # добавляем task в бд к пользователю message.chat.id


@bot.message_handler(commands=['add_time'])
def add_new_time(message):
    bot.send_message(message.from_user.id, "Укажи время, когда ты свободен\n"
                                           "Например, утром, перед работой/учёбой или вечером после основных дел")
    bot.register_next_step_handler(message, add_new_user)


def add_new_user(message):
    global user_id
    global time
    user_id = message.from_user.id
    time = message.text
    users_data = UsersData(config.table_path)
    users_data.add_time(time, user_id)
    bot.reply_to(message, "Готово")
    Thread(target=schedule_checker(time)).start()


def schedule_checker(time):
    if time is not None:
        schedule.every().day.at(time).do(send_wakeup_message)
    while True:
        schedule.run_pending()
        sleep(1)


def send_wakeup_message():
    bot.send_message(user_id, "wakeup")


@bot.message_handler(commands=["del"])
def del_task(message):
    bot.send_message(message.chat.id, "отправь задачу, которую нужно удалить")
    bot.register_next_step_handler(message, remove_task_from_data_base)


def remove_task_from_data_base(message):
    global task
    task = message.text
    # удаляем task из бд пользователя message.chat.id


@bot.message_handler(commands=["list"])
def list_tasks(message):
    users_data = UsersData(config.table_path)
    task_list = users_data.get_tasks_for_user(message.from_user.id)
    bot.send_message(message.from_user.id, task_list)  # в list cписок всех задач пользователя


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)


if __name__ == '__main__':
     bot.infinity_polling()
