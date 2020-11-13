import telebot
import time
import config
from mptParser.mptShedule import mptPage

#hack to fix circular deps
tg_bot = telebot.TeleBot(config.bot_token)

import bot.utils.bot_markup as bot_markup
import bot.utils.sheduler as sheduler
import bot.utils.handlers as handlers

mpt = mptPage()

commands_tree = {
        "START": ["start", "/start"],
        "SHEDULE": ["shedule", "/shedule", "расписание", "/расписание"],
        "CHANGES": ["changes", "/changes", "замены", "/замены"],
        "HELP": ["help", "/help", "помощь", "/помощь"]}


@tg_bot.message_handler(func=lambda message: 
                        True if message.text in commands_tree["START"] 
                        else False)
def start_handler(message):
    tg_bot.reply_to(message, "Привет, бот запущен!\nЕго цель - удобный просмотр расписания МПТ, \
а также он предупреждает о заменах.\n \
Для того чтобы узнать о комманда введите:\n \
/help")
    if handlers.recognize_user(message.from_user.id) == False:
        tg_bot.send_message(message.chat.id, "Выберите направление: ",
            reply_markup=bot_markup.direction_choose_keyboard())

        new_user = handlers.user(message.from_user.id, message.from_user.first_name)
        handlers.users.append(new_user)

@tg_bot.message_handler(func= lambda message: handlers.is_msg_answer(message))
def answer_message_handler(message):
    user = handlers.recognize_user(message.from_user.id)
    
    if user:
        if user.group == None:
            sheduler.pipeline.put(sheduler.context(sheduler.actions.WAIT_GROUP_CHOOSE, message))
            sheduler.shedule_event.set()
            user.group = "-"

        elif user.group == "-":
            sheduler.pipeline.put(sheduler.context(sheduler.actions.WAIT_GROUP_ALREADY_CHOOSED, message))
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
    cur_user = handlers.recognize_user(call.from_user.id)
    
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

@tg_bot.message_handler(func=lambda message:
                        True if message.text in commands_tree["CHANGES"]
                        else False)
def changes_handler(message):
    cur_user = handlers.recognize_user(message.from_user.id)
    if cur_user:
        tg_bot.send_message(message.chat.id, "Changes placeholder for user in group: " + str(cur_user.group))


if __name__ == "__main__":
    tg_bot.polling()
