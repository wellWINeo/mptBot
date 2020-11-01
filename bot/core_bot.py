import telebot
import time
import config
import bot_markup
import math
from mptParser.mptShedule import mptPage

users = {}
bot = telebot.TeleBot(config.bot_token)
bot_command=["start", "расписание"]
mpt = mptPage()

class user():
    user_id = None
    name = ""
    group = None

    def __init__(self, _id, _name):
        self.user_id = _id
        self.name = _name

def is_user_known(user_id):
    for user in users:
        print(user)
        print(type(user))
        if type(user) != 'int' and user.user_id == user_id:
            return True
    return False


@bot.message_handler(commands=["start"])
def start_handler(message):
    bot.reply_to(message, "Привет, бот запущен!\nЕго цель - удобный просмотр расписания МПТ, \
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
                bot.send_message(message.chat.id, "Отличо! Группа выбрана и сохранена")
                users[message.chat.id].group = message.text
            
            #else:
            #   bot.send_message(message.chat.id, "Такой команды я не знаю(")


@bot.message_handler(commands=["расписание"])
def shedule_handler(message):
    bot.send_message(message.chat.id, "Выберите на какой срок: ", 
            reply_markup=bot_markup.choose_shedule_date())

@bot.callback_query_handler(func= lambda call: True if call.data[:3] == "cb_" else False)
def callback_query(call):
    if call.data == "cb_today":
        bot.answer_callback_query(call.id, "Расписание на сегодня")
        bot.send_message(call.message.chat.id, "Today_placeholder")
    
    elif call.data == "cb_tomorrow":
        bot.answer_callback_query(call.id, "Расписание на завтра")
        bot.send_message(call.message.chat.id, "Tommorow_placeholer")
    
    elif call.data == "cb_week":
        bot.answer_callback_query(call.id, "Расписание на неделю")
        bot.send_message(call.message.chat.id, "Weak_placeholder " + users[call.message.chat.id].group)

    else:
        bot.answer_callback_query(call.id, "Internal callback function error")


#@bot.message_handler(func= lambda message: True if message not in bot_command else False)
#def incorrect_command_handler(message):
#    bot.send_message(message.chat.id, "Такой команы я не знаю(")


if __name__ == "__main__":
    bot.polling()




