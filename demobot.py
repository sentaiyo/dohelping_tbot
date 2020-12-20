import telebot  # library for working with telegram API
import config   # file with TOKEN and SQlite table path
from database import UsersData  # data from database
import schedule  # working with time
from threading import Thread
from time import sleep  # func for timer
from telebot import types  # module for bot configuration


bot = telebot.TeleBot(config.TOKEN)  # creating bot
difficulty = None
task = None    # global variables
time = None
user_id = None


@bot.message_handler(commands=["start", "help"])  # bot answers /start /help
def start_replier(message):
    bot.send_message(message.chat.id, "Привет 💫, {0.first_name}!\nменя зовут toDoBot и я бот, который поможет "
                     "тебе быть продуктивнее".format(
                         message.from_user, bot.get_me()),
                     parse_mode='html')
    send_menu(message)
    users_data = UsersData(config.table_path)  # adding user to database
    users_data.add_user(message.from_user.id)


def send_menu(message): # bot sends all possible commands
    bot.send_message(message.chat.id, "/add - добавить новую задачу👩‍💻\n"
                                      "/del - удалить задачу❌\n"
                                      "/list - список всех задач🌐\n"
                                      "/set_time - создать уведомление✅")


@bot.message_handler(commands=["add"])  # function for adding new goal
def ask_difficulty(message):
    bot.send_message(message.chat.id, "отправь, пожалуйста, текстовым сообщением новую задачу🛩")
    bot.register_next_step_handler(message, get_task)


def get_task(message):  # function takes goal information from user
    global task
    global user_id
    task = message.text
    user_id = message.from_user.id
    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton("Простая", callback_data='1')
    item2 = types.InlineKeyboardButton("Не очень", callback_data='2')
    item3 = types.InlineKeyboardButton("Сложная", callback_data='3')

    markup.add(item1, item2, item3)

    bot.send_message(message.chat.id, "отправь, пожалуйста, сложность🤯 своей задачи", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def get_difficulty(call):
    try:
        if call.message:
            global task
            global difficulty
            global user_id
            difficulty = call.data
            users_data = UsersData(config.table_path)
            users_data.add_task(task, difficulty, user_id)  # добавляем task в бд к пользователю message.chat.id
            # remove inline buttons
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="отправь, пожалуйста, сложность🤯 своей задачи",
                                  reply_markup=None)
            set_time(call.message)
    except Exception as e:
        print(repr(e))


@bot.message_handler(commands=["set_time"])
def set_time(call):
    bot.send_message(call.chat.id, "Установи время⏰ на ближайшие сутки в 24 часовом формате через двоеточие, когда ты планируешь "
                                   "начать работу\n"
                                   "Например, утром, перед работой/учёбой или вечером после основных дел")
    bot.register_next_step_handler(call, add_new_time)


def add_new_time(message):
    global user_id
    global time
    user_id = message.from_user.id
    time = message.text
    users_data = UsersData(config.table_path)
    users_data.add_time(time, user_id)
    bot.reply_to(message, "Готово")
    send_menu(message)
    Thread(target=schedule_checker(time)).start()


def schedule_checker(time):
    if time is not None:
        schedule.every().day.at(time).do(send_wakeup_message)
    while True:
        schedule.run_pending()
        sleep(1)


def send_wakeup_message():
    bot.send_message(user_id, "🔥🔥🔥Время взяться за работу🔥🔥🔥\nнайчинай лучше со сложной задачи:")
    users_data = UsersData(config.table_path)
    task_list = users_data.get_tasks_for_user(user_id)
    bot.send_message(user_id, task_list)


@bot.message_handler(commands=["del"])
def del_task(message):
    bot.send_message(message.from_user.id,
                     f'Список задач:\n{get_tasks_list(message.from_user.id)}')
    bot.send_message(message.chat.id, "отправь, пожалуйста, текстовым сообщением задачу, которую нужно удалить")
    bot.register_next_step_handler(message, remove_task_from_data_base)


def remove_task_from_data_base(message):
    global task
    task = message.text
    users_data = UsersData(config.table_path)
    users_data.delete_task(task)
    bot.send_message(message.from_user.id,
                     f'Готово, теперь список:\n{get_tasks_list(message.from_user.id)}')
    # удаляем task из бд пользователя message.chat.id

    send_menu(message)


@bot.message_handler(commands=["list"])
def list_tasks(message):
    task_list = get_tasks_list(message.from_user.id)
    bot.send_message(message.from_user.id, task_list)
    # в list cписок всех задач пользователя
    send_menu(message)


def get_tasks_list(user_id):
    users_data = UsersData(config.table_path)
    task_list = users_data.get_tasks_for_user(user_id)
    if len(task_list) == 0:
        task_list = 'список пуст'
    return task_list


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)
    send_menu(message)


if __name__ == '__main__':
     bot.infinity_polling()
