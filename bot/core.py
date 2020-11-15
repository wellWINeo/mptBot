import telebot
import time
import config
from mptParser.mptShedule import mptPage

#hack to fix circular deps
tg_bot = telebot.TeleBot(config.bot_token)

import bot.markup as bot_markup
import bot.sheduler as sheduler
import bot.handlers as handlers

mpt = mptPage()

commands_tree = {
        "START": ["start", "/start"],
        "SHEDULE": ["shedule", "/shedule", "расписание", "/расписание", "Расписание"],
        "CHANGES": ["changes", "/changes", "замены", "/замены", "Замены"],
        "HELP": ["help", "/help", "помощь", "/помощь", "Помощь"]}


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
    sheduler.pipeline.put(sheduler.context(sheduler.actions.SHEDULE_HANDLER, message))
    sheduler.shedule_event.set()

@tg_bot.callback_query_handler(func=lambda call: 
                               True if call.data[:3] == "cb_" 
                               else False)
def callback_query(call):
    sheduler.pipeline.put(sheduler.context(sheduler.actions.CALLBACK_QUERY, call=call))
    sheduler.shedule_event.set()

@tg_bot.message_handler(func=lambda message:
                        True if message.text in commands_tree["CHANGES"]
                        else False)
def changes_handler(message):
    sheduler.pipeline.put(sheduler.context(sheduler.actions.CHANGES_HANDLER, message))
    sheduler.shedule_event.set()

if __name__ == "__main__":
    tg_bot.polling()