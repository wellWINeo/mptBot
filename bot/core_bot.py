import telebot
import time
import config
import bot_markup
import math
from mptParser.mptShedule import mptPage

users = {}
bot = telebot.TeleBot(config.bot_token)

mpt = mptPage()

class user():
    user_id = None
    name = ""
    group = None

    def __init__(self, _id, _name):
        self.user_id = _id
        self.name = _name


def bot_start():
    global users, bot
    users = []
    bot = telebot.TeleBot(config.bot_token)


def is_user_known(user_id):
    for user in users:
        if user.user_id == user_id:
            return True
    return False


@bot.message_handler(commands=['start'])
def start_msg(message):
    bot.reply_to(message, "Привет, бот запущен!\nЕго цель - удобноый просмотр рас    писания МПТ, \
а также он предупреждает о заменах.\n \
Для того чтобы узнать о комманда введите:\n \
/help")
    if not is_user_known(message.from_user.id):
        bot.send_message(message.chat.id, "Выберите направление: ",
            reply_markup=bot_markup.direction_choose_keyboard())

        new_user = user(message.chat.id, message.from_user.first_name)
        users.update({new_user.user_id : new_user})
        bot.set_update_listener(wait_for_dir_answer)
        
def wait_for_dir_answer(messages):
    for message in messages:
        if message.chat.id in users:
            if (users[message.chat.id]).group == None:
                bot.send_message(message.chat.id, "Выберите группу: ",
                        reply_markup=bot_markup.group_choose_keyboard(mpt, message.text))
                users[message.chat.id].group = "-"
            elif (users[message.chat.id]).group == "-":
                bot.send_message(message.chat.id, "Placeholder")

if __name__ == "__main__":
    bot.polling()




