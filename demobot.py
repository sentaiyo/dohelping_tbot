import telebot
import config
from database import UsersData

# from telebot import types

bot = telebot.TeleBot(config.TOKEN)
difficulty = None
task = None


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
    difficulty = message.text
    print(difficulty)  # добавляем сложность новой задачи
    bot.send_message(message.chat.id, "отправь, пожалуйста, текстовым сообщением новую задачу")
    bot.register_next_step_handler(message, get_task)


"""def add_task(message):
    bot.send_message(message.chat.id, "отправь, пожалуйста, текстовым сообщением новую задачу")
    bot.register_next_step_handler(message, get_task)"""


def get_task(message):
    global task
    global difficulty
    task = message.text
    print(task)
    users_data = UsersData('C:/Users/Admin/tables/table1.sqlite')
    users_data.add_task(task, difficulty, message.from_user.id)  # добавляем task в бд к пользователю message.chat.id


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
    bot.reply_to(message, task_list)  # в list cписок всех задач пользователя


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)


if __name__ == '__main__':
     bot.infinity_polling()