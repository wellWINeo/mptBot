import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
import time
import config

class user():
    user_id = None
    name = ""
    group = ""

    def __init__(self, _id, _name, _group):
        self.user_id = _id
        self.name = _name
        self.group = _group
        print("id: " + str(self.user_id) + "\nname: " + self.name + "\ngroup: " + self.group)

users = []

bot = telebot.TeleBot(config.bot_token)

choose_group_markup = telebot.types.ReplyKeyboardMarkup(row_width=3)
button1 = telebot.types.KeyboardButton("1")
button2 = telebot.types.KeyboardButton("2")
button3 = telebot.types.KeyboardButton("3")
choose_group_markup.add(button1, button2, button3)

def gen_markup_shedule():
    markup = InlineKeyboardMarkup()
    markup.add( InlineKeyboardButton("На сегодня", callback_data="cb_today"),
                InlineKeyboardButton("На завтра", callback_data="cd_tomorrow"),
                InlineKeyboardButton("На неделю", callback_data="cb_week"))
    return markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Привет, бот запущен!\nЕго цель - удобноый просмотр расписания МПТ, \
а также он предупреждает о заменах.\n \
Для того чтобы узнать о комманда введите:\n \
/help")
    bot.send_message(message.chat.id, "Выберите направление: ", reply_markup=choose_group_markup)
    new_user = user(message.from_user.id, message.from_user.first_name, "TestGroup")
    users.append(new_user)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "cb_today":
        bot.answer_callback_query(call.id, time.localtime())
        bot.send_message(call.message.chat.id, "Today") 
    elif call.data == "cb_tomorrow":
        bot.answer_callback_query(call.id, "Расписание на завтра")
    elif call.data == "cb_weak":
        bot.answer_callback_query(call.id, "Расписание на неделю")
    else:
        bot.answer_callback_query(call.id, "Internal error occured")

@bot.message_handler(commands='замены')
def changes_handler(message):
    print(message)
    bot.send_message(message.chat.id, "Замены на сегодня, " + message.from_user.first_name)

@bot.message_handler(commands='расписание')
def shedule_handler(message):
    bot.send_message(message.chat.id, "На какой срок?", reply_markup=gen_markup_shedule())

@bot.message_handler(commands='users')
def show_users(message):
    print(users)

if __name__ == "__main__":
    bot.polling()
