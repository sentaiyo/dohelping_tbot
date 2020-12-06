import telebot
import config


from telebot import types

bot = telebot.TeleBot(config.TOKEN)


@bot.message_handler(commands=['start', 'help'])
def welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    item1 = types.InlineKeyboardButton("💫Создать новую цель💫", callback_data='new_goal')

    markup.add(item1)

    bot.send_message(message.chat.id,
                     "Привет 💫, {0.first_name}!\nменя зовут   и я умный бот, который поможет "
                     "тебе быть продуктивнее".format(
                         message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup)


    @bot.callback_query_handler(func=lambda call: True)
    def callback_inline(call):
        try:
            if call.message:
                if call.data == 'new_goal':

                    bot.send_message(call.message.chat.id, 'Для начала сформулируй цель, которую ты '
                                                  'хочешь достичь. Под целью понимается навык (играть на гитаре, '
                                                  'программировать на java, разговаривать по английски) или сложная задача '
                                                  '(поступить в вуз, сдать экзамен по математическому анализу, изучить '
                                                  'технологию/ фреймворк).')
                    bot.send_message(call.message.chat.id,
                                 "Пришли, пожалуйста, свою цель, формулировка должна содержать в себе "
                                 "глагол и быть четкой, чтобы ты мог оценить конкретный результат.")

                    @bot.message_handler(content_types=['text'])
                    def get_goal_name(message):

                        goal_name = message.text
                        bot.send_message(message.chat.id, '''Хорошо, твоя цель - ''' + goal_name)
                        markup = types.InlineKeyboardMarkup(row_width=2)
                        item1 = types.InlineKeyboardButton("💫ОК💫", callback_data='ok')

                        markup.add(item1)
                        bot.send_message(message.chat.id, "Теперь надо расписать три класса задач, которые ты будешь "
                                                          "выполнять на пути к цели. Никаких посторонних задач в классе "
                                                          "быть не должно\n1️⃣ Самые простые - они примерно занимают 15 "
                                                          "минут твоего времени и не требуют сильного умственного "
                                                          "напряжения (Посмотреть видео урок по C++, выучить песню "
                                                          "«группа крови» на гитаре, добавить комменты в проект, "
                                                          "установить библиотеку )\n2️⃣ Средней сложности - они примерно "
                                                          "занимают 30 минут (посмотреть 10 лекцию по алгебре, исправить "
                                                          "такой-то баг в таком-то проекте, решить такую-то задачку )\n3️⃣ "
                                                          "Сложные задачи - они занимают 1 час, требуют концентрации и "
                                                          "внимания (ботать листок, добавить фичу в проект, понять "
                                                          "такую-то главу по топологии)\nКонечно,  сложные задачи обычно "
                                                          "занимают намного больше времени, но любые отрезки из списка "
                                                          "задач ты можешь повторять сколь угодно раз. Например, сделать "
                                                          "2 сложные задачи подряд".format(
                         message.from_user, bot.get_me()),
                        parse_mode='html', reply_markup=markup)

                        @bot.callback_query_handler(func=lambda call: True)
                        def get_tasks(call):
                            try:
                                if call.message:
                                    if call.data == 'ok':
                                        bot.send_message(message.chat.id,"Тебе нужно прислать 2 задачи  1️⃣ "
                                                                         "класса, каждую в новой строке" )

                                        @bot.message_handler(content_types=['text'])
                                        def get_tasks1(message):
                                            bla = message.text
                            except Exception as e:
                                print(repr(e))

        except Exception as e:
            print(repr(e))



# RUN
bot.polling(none_stop=True)