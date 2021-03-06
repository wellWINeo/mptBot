import telebot
import time
import config
from mptParser.schedule import mptPage
import logging

# hack to fix circular deps
tg_bot = telebot.AsyncTeleBot(config.bot_token)

import bot.markup as bot_markup
import bot.user as users
import bot.utils as utils

db = users.users_db(config.db_path)

#----------------
# COMMANDS
#----------------
commands_tree = {
        "START": ("start", "/start"),
        "SHEDULE": ("schedule", "/schedule", "расписание", "/расписание", "Расписание"),
        "CHANGES": ("changes", "/changes", "замены", "/замены", "Замены"),
        "HELP": ("help", "/help", "помощь", "/помощь", "Помощь"),
        "PING": ("ping", "/ping", "Ping", "пинг", "Пинг"),
        "DEL": ("/del", "del", "delete", "/delete"),
        "ABOUT": ("/about", "about", "About", "О боте"),
        "ME": ("/me", "/Me", "me", "Me", "Обо мне")}


#----------------
# BOT FEATURES
#----------------
@tg_bot.message_handler(func=lambda message: 
                        True if message.text in commands_tree["START"] 
                        else False)
def start_handler(message):
    logging.debug("[" + str(message.from_user.id) + "] " + "Bot received \"start\" command")
    tg_bot.reply_to(message, "Привет, бот запущен!\nЕго цель — удобный просмотр "\
                             "расписания МПТ, а также он предупреждает о заменах.\n "\
                             "Для того чтобы узнать о комманда введите:\n " \
                             "/help")
    logging.debug("[" + str(message.from_user.id) + "] " + "Initial answer on \"start\" command sent")
    if db.get_user(message.from_user.id) is None:
        logging.debug("[" + str(message.from_user.id) + "] " + "User not present in db")
        tg_bot.send_message(message.chat.id, "Выберите направление: ",
            reply_markup=bot_markup.direction_choose_keyboard())
        logging.debug("[" + str(message.from_user.id) + "] " + "Bot send keyboard markup")

        new_user = users.user(message.from_user.id, message.from_user.first_name)
        db.add_user(new_user)
    else:
        tg_bot.send_message(message.chat.id, "Вы уже есть в базе данных",
                            reply_markup=bot_markup.main_menu_keyboard())
        


#----------------
# Receiving anwer about
# user's group direction
#----------------
@tg_bot.message_handler(func=lambda message: 
                        True if db.get_user(message.from_user.id) != None and 
                        db.get_user(message.from_user.id).status < users.status.ANON
                        else False)
def answer_message_handler(message):
    logging.debug(f"[{message.from_user.id}] Received answer on dir choosing")
    user = db.get_user(message.from_user.id)

    if user != None:
        if user.status == users.status.UNKNOWN:
            groups = utils.mpt.get_groups_by_dir(message.text)
            if len(groups) == 0:
                logging.debug(f"[{user.user_id}] Invalid dir")
                tg_bot.send_message(message.chat.id, "Некорректный ответ, " \
                                                     "попробуйте еще раз",
                                    reply_markup=bot_markup.direction_choose_keyboard())
            else:
                utils.wait_group_choose(message, groups)
                logging.debug(f"[{message.from_user.id}] User hasn't group")
                user.status = users.status.NO_GROUP
                user.group = message.text
                db.update(user)

        elif user.status == users.status.NO_GROUP:
            groups = utils.mpt.get_groups_by_dir(user.group)
            logging.debug(f"[{message.from_user.id}] User fields completed")
            
            if message.text not in groups:
                logging.debug(f"[{user.user_id}] Invalid group")
                tg_bot.send_message(message.chat.id, "Некорректный номер группы," \
                                                     "выберите, используя клавиатуру")
            else:
                utils.group_choosed(message)
                user.group = message.text
                user.status = users.status.COMPLETE
                db.update(user)
                tg_bot.send_message(message.chat.id, "Вы успешно добавлены в бд",
                                    reply_markup=bot_markup.main_menu_keyboard())
    else:
        tg_bot.send_message(message.chat.id, "Something went wrong")


#----------------
# HELP
#----------------
@tg_bot.message_handler(func=lambda message:
                        True if message.text in commands_tree["HELP"]
                        else False)
def help_handler(message):
    logging.debug(f"[{message.from_user.id})] help command")
    tg_bot.send_message(message.chat.id, "Здесь представлены основные команды бота: \n"\
                                         "\t/start — запускает бота и регистрирует " \
                                         "пользователя, если он еще не зарегистрирован\n"\
                                         "\t/расписание - отправляет сообщение с меню "\
                                         "выбора дня для показа расписания\n"\
                                         "\t/замены - отправляет список замен (если есть)" \
                                         "на текущий день\n"
                                         "\t/ping - просто проверка, что бот еще жив\n" \
                                         "\t/del - удаление пользователя из базы данных\n" \
                                         "\t/about - увидеть доп. информацию о боте\n"
                                         "\t/help - чтобы увидеть еще раз это сообщение\n"
                                         "P.S. некоторые команды допускают несколько " \
                                         "вариантов написания, для более подробной информации " \
                                         "смотрите \'commands_tree\' в bot/core.py")


#----------------
# PING
#----------------
@tg_bot.message_handler(func=lambda message:
                        True if message.text in commands_tree["PING"]
                        else False)
def ping_handler(message):
    tg_bot.send_message(message.chat.id, "Еще здесь <3")
    tg_bot.send_message(message.chat.id,
                        reply_markup=bot_markup.main_menu_keyboard())
    

#----------------
# DELETE
# user from db
#----------------
@tg_bot.message_handler(func=lambda message:
                        True if message.text in commands_tree["DEL"]
                        else False)
def delete_handler(message):
    try:
        db.del_user(message.from_user.id)
        tg_bot.send_message(message.chat.id, "Вас больше нет в базе данных")
    except:
        tg_bot.send_message(message.chat.id, "Не удалось удалить, возможно, вас нет в базе данных")
    tg_bot.send_message(message.chat.id,
                        reply_markup=bot_markup.main_menu_keyboard())


#----------------
# ABOUT
#----------------
@tg_bot.message_handler(func=lambda message:
                        True if message.text in commands_tree["ABOUT"]
                        else False)
def about_handler(message):
    logging.debug("Handling /about command")
    tg_bot.send_message(message.chat.id, "mptBot - свободный телеграмм бот с открытым " \
                                         "исходным кодом под лицензией MPL 2.0 для " \
                                         "расписания МПТ, которое парсится с сайта.\n"
                                         f"Версия: {config.version}\n" \
                                         "Исходный код: github.com/wellWINeo/mptBot \n"
                                         "В случае обнаружения ошибок, просьба сообщить, " \
                                         "создав issue \n" \
                                         "Чтобы увидеть список команд: /help")
    tg_bot.send_message(message.chat.id,
                        reply_markup=bot_markup.main_menu_keyboard())


#----------------
# Send info
# about user
#----------------
@tg_bot.message_handler(func=lambda message:
                        True if message.text in commands_tree["ME"]
                        else False)
def me_handler(message):
    logging.debug("Handling /me command")
    
    cur_user = db.get_user(message.from_user.id)

    if cur_user != None:
        tg_bot.send_message(message.chat.id, f"Имя - {cur_user.name}\n" \
                                             f"ID - {cur_user.user_id}\n" \
                                             f"Группа - {cur_user.group}")
    else:
        tg_bot.send_message(message.chat.id, "Вас еще нет в базе данных")
    
    tg_bot.send_message(message.chat.id,
                        reply_markup=bot_markup.main_menu_keyboard())

#----------------
# Sending callback
# for schedule day
# choosing
#----------------
@tg_bot.message_handler(func=lambda message:
                        True if message.text.split()[0] in commands_tree["SHEDULE"]
                        else False)
def schedule_handler(message):
    logging.debug("[{message.from_user.id}] Shedule command")
    cur_user = db.get_user(message.from_user.id)
    if len(message.text.split()) > 1:
        if cur_user == None:
            db.add_user(users.user(message.from_user.id, 
                                   message.from_user.first_name,
                                   _group=" ".join(message.text.split()[1:]),
                                   _status=users.status.ANON))
        else:
            cur_user.comm = cur_user.group
            cur_user.group = " ".join(message.text.split()[1:])
            cur_user.status = users.status.ANOTHER
            db.update(cur_user)
    
    utils.schedule_date(message)
    tg_bot.send_message(message.chat.id,
                        reply_markup=bot_markup.main_menu_keyboard())


#----------------
# Receiving & handling
# callback
#----------------
@tg_bot.callback_query_handler(func=lambda call: 
                               True if call.data[:3] == "cb_" 
                               else False)
def callback_query(call):
    logging.debug("[" + str(call.message.from_user.id) + "] " + "Callback query received")
    utils.schedule_handler(call)
    tg_bot.send_message(call.message.chat.id, "Test",
                        reply_markup=bot_markup.main_menu_keyboard())


#----------------
# Sending changes
#----------------
@tg_bot.message_handler(func=lambda message:
                        True if message.text in commands_tree["CHANGES"]
                        else False)
def changes_handler(message):
    logging.debug("[" + str(message.from_user.id) + "] " + "Changes command")
    utils.changes_handler(message)
    tg_bot.send_message(message.chat.id,
                        reply_markup=bot_markup.main_menu_keyboard())
