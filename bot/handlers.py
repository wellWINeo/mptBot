from threading import Thread
import bot.sheduler as sheduler
import bot.core as bot
import bot.markup as markup
import bot.handlers as handlers
import bot.db as db
import telebot
from mptParser.mptShedule import mptPage

class user():
    user_id = None
    name = ""
    group = None

    def __init__(self, _id, _name, _group=None):
        self.user_id = _id
        self.name = _name
        self.group = _group

users = db.load()
mpt = mptPage()
bot = bot.tg_bot

def recognize_user(id_):
    for user in users:
        return user
    return False

def is_msg_answer(message):
    for user in (user for user in users if user.user_id == message.from_user.id):
        if (user.group == None) or (user.group == "-"):
            return True
    return False


class driverThread(Thread):
    
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        while True:
            if sheduler.shedule_event.is_set():
                context = sheduler.pipeline.get()
                if context.action == sheduler.actions.WAIT_GROUP_CHOOSE:
                    bot.send_message(context.message.chat.id,
                                    "Выберите группу: ",
                                    reply_markup=markup.group_choose_keyboard(mpt, context.message.text))
                elif context.action == sheduler.actions.WAIT_GROUP_ALREADY_CHOOSED:
                    bot.send_message(context.message.chat.id,
                                    "Отлично! Группа выбрана и сохранена",
                                    reply_markup=telebot.types.ReplyKeyboardRemove())
                    
                elif context.action == sheduler.actions.SHEDULE_HANDLER:
                    bot.send_message(context.message.chat.id, 
                                    "Выберите на какой срок: ",
                                    reply_markup=markup.choose_shedule_date())
                
                elif context.action == sheduler.actions.CALLBACK_QUERY:
                    cur_user = handlers.recognize_user(context.call.from_user.id)

                    if context.call.data == "cb_today":
                        bot.answer_callback_query(context.call.id, "Расписание на сегодня")
                        bot.send_message(context.message.chat.id,
                                        "Today_placeholder {0}".format(cur_user.group))

                    if context.call.data == "cb_tomorrow":
                        bot.answer_callback_query(context.call.id, "Расписание на завтра")
                        bot.send_message(context.message.chat.id,
                                        "Tomorrow_placeholder {0}".format(cur_user.group))

                    if context.call.data == "cb_week":
                        bot.answer_callback_query(context.call.id, "Расписание на неделю")
                        bot.send_message(context.message.chat.id,
                                        "Weak_placeholder {0}".format(cur_user.group))
                    else:
                        bot.answer_callback_query(context.call.id,
                                                 "Internal callback function error")

                elif context.action == sheduler.actions.CHANGES_HANDLER:
                    cur_user = handlers.recognize_user(context.message.from_user.id)

                    if cur_user:
                        bot.send_message(context.message.chat.id,
                                                    "Changes placeholder - " + \
                                                    str(cur_user.group))
                if (sheduler.pipeline.qsize()) == 0:
                    sheduler.shedule_event.clear()
            else:
                 sheduler.shedule_event.wait()
