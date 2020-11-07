import telebot
import time
import config
import bot_markup
from mptParser.mptShedule import mptPage

users = []
tg_bot = telebot.TeleBot(config.bot_token)
mpt = mptPage()

commands_tree = {
        "START": ["start", "/start"],
        "SHEDULE": ["shedule", "/shedule", "расписание", "/расписание"],
        "CHANGES": ["changes", "/changes", "замены", "/замены"],
        "HELP": ["help", "/help", "помощь", "/помощь"]}


class user():
    user_id = None
    name = ""
    group = None

    def __init__(self, _id, _name):
        self.user_id = _id
        self.name = _name

def recognize_user(id_):
    for user in users:
        if user.user_id == id_:
            return user
    return False


@tg_bot.message_handler(func=lambda message: 
                        True if message.text in commands_tree["START"] 
                        else False)
def start_handler(message):
    tg_bot.reply_to(message, "Привет, бот запущен!\nЕго цель - удобный просмотр расписания МПТ, \
а также он предупреждает о заменах.\n \
Для того чтобы узнать о комманда введите:\n \
/help")
    if recognize_user(message.from_user.id) == False:
        tg_bot.send_message(message.chat.id, "Выберите направление: ",
            reply_markup=bot_markup.direction_choose_keyboard())

        new_user = user(message.from_user.id, message.from_user.first_name)
        users.append(new_user) 
        tg_bot.set_update_listener(wait_for_dir_answer)

def wait_for_dir_answer(messages):
    
    for message in messages:
        gen = (user for user in users if user.user_id == message.from_user.id)
        for user in gen:       
            if user.group == None: 
                tg_bot.send_message(message.chat.id, "Выберите группу: ",
                                    reply_markup=bot_markup.group_choose_keyboard(mpt, message.text))
                user.group = "-"

            elif user.group == "-": 
                tg_bot.send_message(message.chat.id, "Отличо! Группа выбрана и сохранена")
                user.group = message.text 


@tg_bot.message_handler(func=lambda message:
                        True if message.text in commands_tree["HELP"]
                        else False)
def help_handler(message):
    tg_bot.send_message(message.chat.id, "help_placeholder")


@tg_bot.message_handler(func=lambda message:
                        True if message.text in commands_tree["SHEDULE"]
                        else False)
def shedule_handler(message):
    tg_bot.send_message(message.chat.id, "Выберите на какой срок: ", 
            reply_markup=bot_markup.choose_shedule_date())


@tg_bot.callback_query_handler(func=lambda call: 
                               True if call.data[:3] == "cb_" 
                               else False)
def callback_query(call):
    cur_user = recognize_user(call.from_user.id)
    
    if call.data == "cb_today":
        tg_bot.answer_callback_query(call.id, "Расписание на сегодня")
        tg_bot.send_message(call.message.chat.id, "Today_placeholder {0}".format(cur_user.group))
    
    elif call.data == "cb_tomorrow":
        tg_bot.answer_callback_query(call.id, "Расписание на завтра")
        tg_bot.send_message(call.message.chat.id, "Tommorow_placeholer {0}".format(cur_user.group))
    
    elif call.data == "cb_week":
        tg_bot.answer_callback_query(call.id, "Расписание на неделю")
        tg_bot.send_message(call.message.chat.id, "Weak_placeholder {0}".format(cur_user.group))

    else:
        tg_bot.answer_callback_query(call.id, "Internal callback function error")


if __name__ == "__main__":
    tg_bot.polling()
