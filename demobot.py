import telebot  # library for working with telegram API
import config   # file with TOKEN and SOlite table path
from database import UsersData  # data from database
import schedule  # working with time
from threading import Thread  # running multiple operations simultaneously
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
                     "тебе быть продуктивнее, просто тыкни на то, что тебе нужно".format(
                         message.from_user, bot.get_me()),
                     parse_mode='html')
    send_menu(message)
    users_data = UsersData(config.table_path)  # adding user to database
    users_data.add_user(message.from_user.id)
    users_data.connection.close()


def send_menu(message):  # bot sends all possible commands
    bot.send_message(message.chat.id, "/add - добавить новую задачу👩‍💻\n"
                                      "/del - удалить задачу❌\n"
                                      "/list - список всех задач🌐\n"
                                      "/set_time - создать уведомление⏰\n")


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
    item2 = types.InlineKeyboardButton("Средняя", callback_data='2')
    item3 = types.InlineKeyboardButton("Сложная", callback_data='3')

    markup.add(item1, item2, item3)  # creating buttons

    bot.send_message(message.chat.id, "отправь, пожалуйста, сложность🤯 своей задачи", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)  # func answers button calls
def get_difficulty(call):
    try:
        if call.message:
            global task
            global difficulty
            global user_id
            difficulty = call.data  # gets button data
            users_data = UsersData(config.table_path)
            users_data.add_task(task, difficulty, user_id)  # add the task to the database to user message.chat.id
            # remove inline buttons
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="отправь, пожалуйста, сложность🤯 своей задачи",
                                  reply_markup=None)
            users_data.connection.close()
            set_time(call.message)  # making time notification
    except Exception as e:
        print(repr(e))


@bot.message_handler(commands=["set_time"])
def set_time(call):
    bot.send_message(call.chat.id, "Установи время⏰ на ближайшие сутки в 24 часовом формате через двоеточие, "
                                   "когда ты планируешь "
                                   "начать работу\n"
                                   "Например, утром, перед работой/учёбой или вечером после основных дел")
    bot.register_next_step_handler(call, add_new_time)


def add_new_time(message):
    global user_id
    global time
    user_id = message.from_user.id
    time = message.text  # takes time from user
    if len(time) == 4:
        time = "0" + time
    users_data = UsersData(config.table_path)
    users_data.add_time(time, user_id)     # sends time to table path
    users_data.connection.close()
    bot.reply_to(message, "Готово")
    send_menu(message)
    Thread(target=schedule_checker(time)).start()


def schedule_checker(time):  # sends wakeup message
    if time is not None:  # checks if the time is right
        schedule.every().day.at(time).do(send_wakeup_message)
    while True:
        schedule.run_pending()
        sleep(1)


def send_wakeup_message():
    bot.send_message(user_id, "🔥🔥🔥Время взяться за работу🔥🔥🔥\nначинай лучше со сложной задачи:")
    users_data = UsersData(config.table_path)  # takes data about task list in database and sends it
    task_list = users_data.get_tasks_for_user(user_id)
    bot.send_message(user_id, task_list)
    users_data.connection.close()


@bot.message_handler(commands=["del"])
def del_task(message):   # takes exact task to delete
    bot.send_message(message.from_user.id,
                     f'Список задач:\n{get_tasks_list(message.from_user.id)}')
    bot.send_message(message.chat.id, "отправь, пожалуйста, текстовым сообщением задачу, которую нужно удалить")
    bot.register_next_step_handler(message, remove_task_from_data_base)


def remove_task_from_data_base(message):
    global task
    task = message.text
    users_data = UsersData(config.table_path)
    users_data.delete_task(task)  # deletes task in database
    bot.send_message(message.from_user.id,
                     f'Готово, теперь список:\n{get_tasks_list(message.from_user.id)}')
    # удаляем task из бд пользователя message.chat.id
    users_data.connection.close()

    send_menu(message)


@bot.message_handler(commands=["list"])
def list_tasks(message):
    task_list = get_tasks_list(message.from_user.id)  # lists tasks from database
    bot.send_message(message.from_user.id, "начинать лучше со сложной задачи:")
    bot.send_message(message.from_user.id, task_list)
    # в list cписок всех задач пользователя
    send_menu(message)


def get_tasks_list(user_id):
    users_data = UsersData(config.table_path)
    task_list = users_data.get_tasks_for_user(user_id)  # task list is taken from database
    if len(task_list) == 0:
        task_list = 'список пуст'
    users_data.connection.close()
    return task_list


@bot.message_handler(func=lambda message: True) # bot answers messages that it doesnt understand
def echo_all(message):
    bot.reply_to(message, "я тебя не понимаю(((")
    send_menu(message)


if __name__ == '__main__':  # starting bot
     bot.infinity_polling()
