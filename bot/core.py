import telebot
import time
import config
from mptParser.mptShedule import mptPage
import logging

#hack to fix circular deps
tg_bot = telebot.AsyncTeleBot(config.bot_token)

import bot.markup as bot_markup
import bot.db as db
import bot.utils as utils 
from bot.user import user


#----------------
# COMMANDS
#----------------
commands_tree = {
        "START": ("start", "/start"),
        "SHEDULE": ("shedule", "/shedule", "расписание", "/расписание", "Расписание"),
        "CHANGES": ("changes", "/changes", "замены", "/замены", "Замены"),
        "HELP": ("help", "/help", "помощь", "/помощь", "Помощь"),
        "PING": ("ping", "/ping", "Ping", "пинг", "Пинг"),
        "DEL": ("/del", "del", "delete", "/delete")}


#----------------
# BOT FEATURES
#----------------
@tg_bot.message_handler(func=lambda message: 
                        True if message.text in commands_tree["START"] 
                        else False)
def start_handler(message):
    logging.debug("[" + str(message.from_user.id) + "] " + "Bot received \"start\" command")
    tg_bot.reply_to(message, "Привет, бот запущен!\nЕго цель - удобный просмотр расписания МПТ, \
а также он предупреждает о заменах.\n \
Для того чтобы узнать о комманда введите:\n \
/help")
    logging.debug("[" + str(message.from_user.id) + "] " + "Initial answer on \"start\" command sent")
    if utils.recognize_user(message.from_user.id) == False:
        logging.debug("[" + str(message.from_user.id) + "] " + "User not present in db")
        tg_bot.send_message(message.chat.id, "Выберите направление: ",
            reply_markup=bot_markup.direction_choose_keyboard())
        logging.debug("[" + str(message.from_user.id) + "] " + "Bot send keyboard markup")

        new_user = user(message.from_user.id, message.from_user.first_name)
        utils.users.append(new_user)
        db.add_user(new_user)

#----------------
# Receiving anwer about
# user's group direction
#----------------
@tg_bot.message_handler(func= lambda message: utils.is_msg_answer(message))
def answer_message_handler(message):
    logging.debug("[" + str(message.from_user.id) + "] " + "Received answer on dir choosing")

    user = utils.recognize_user(message.from_user.id)
    
    if user:
        if user.group == "":
            utils.wait_group_choose(message)
            logging.debug("[" + str(message.from_user.id) + "] " + "User hasn't group")
            user.group = "-"
            db.users_db.update({"group" : "-"}, db.User.user_id == user.user_id)

        elif user.group == "-":
            logging.debug("[" + str(message.from_user.id) + "] " + "User filled")
            utils.group_choosed(message)
            user.group = message.text
            db.users_db.update({"group" : message.text},
                                db.User.user_id == user.user_id)
    else:
        tg_bot.send_message(message.chat.id, "Something went wrong")


#----------------
# HELP
#----------------
@tg_bot.message_handler(func=lambda message:
                        True if message.text in commands_tree["HELP"]
                        else False)
def help_handler(message):
    logging.debug("[" + str(message.from_user.id) + "]" +"help command")
    tg_bot.send_message(message.chat.id, "help_placeholder")



#----------------
# PING
#----------------
@tg_bot.message_handler(func=lambda message:
                        True if message.text in commands_tree["PING"]
                        else False)
def ping_handler(message):
    tg_bot.send_message(message.chat.id, "Еще здесь <3")
    

#----------------
# DELETE
# user from db
#----------------
@tg_bot.message_handler(func=lambda message:
                        True if message.text in commands_tree["DEL"]
                        else False)
def delete_handler(message):
    try:
        db.remove_user(message.from_user.id)
        utils.users.remove(utils.recognize_user(message.from_user.id))
        tg_bot.send_message(message.chat.id, "Вас больше нет в базе данных")
    except:
        tg_bot.send_message(message.chat.id, "Не удалось удалить, возможно вас нет в базе данных")


#----------------
# Sending callback
# for shedule day
# choosing
#----------------
@tg_bot.message_handler(func=lambda message:
                        True if message.text in commands_tree["SHEDULE"]
                        else False)
def shedule_handler(message):
    logging.debug("[" + str(message.from_user.id) + "] " +"Shedule command")
    utils.shedule_date(message)


#----------------
# Receiving & handling
# callback
#----------------
@tg_bot.callback_query_handler(func=lambda call: 
                               True if call.data[:3] == "cb_" 
                               else False)
def callback_query(call):
    logging.debug("[" + str(call.message.from_user.id) + "] " + "Callback query received")
    utils.shedule_handler(call)


#----------------
# Sending changes
#----------------
@tg_bot.message_handler(func=lambda message:
                        True if message.text in commands_tree["CHANGES"]
                        else False)
def changes_handler(message):
    logging.debug("[" + str(message.from_user.id) + "] " + "Changes command")
    utils.changes_handler(message)
