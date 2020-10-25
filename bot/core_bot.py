import telebot
import time
import config
import bot_markup

users = []
bot = telebot.TeleBot(config.bot_token)


class user():
    user_id = None
    name = ""
    group = ""
    is_complete = None

    def __init__(self, _id, _name, _group = None, not_complete = False):
        self.user_id = _id
        self.name = _name
        if not_complete == False:
            self.group = _group
            is_complete = True
        else:
            is_complete = False
        

def bot_start():
    global users, bot
    users = []
    bot = telebot.TeleBot(config.bot_token)

def is_user_known(user_id):
    for user in users:
        if user.user_id == user_id:
            return True
    return False


@bot.message_handler(commands='start')
def start_msg(message):
    bot.reply_to(message, "Привет, бот запущен!\nЕго цель - удобноый просмотр рас    писания МПТ, \
а также он предупреждает о заменах.\n \
Для того чтобы узнать о комманда введите:\n \
/help")
    if not is_user_known(message.from_user.id):
        bot.send_message(message.chat.id, "Выберите направление: ",
            reply_markup=bot_markup.direction_choose_keyboard())
        new_user = user(message.chat.id, message.from_user.first_name, 
            not_complete=True)
        users.append(new_user)

def wait_for_dir_answer(messages, instance):
    for message in messages:
        if message.chat.id == instance.user_id:
            bot.send_message(message.chat.id, "Выберите группу: ")

if __name__ == "__main__":
    bot.polling()




