from threading import Thread
import bot.sheduler as sheduler
import bot.core as bot
import bot.markup as markup
import bot.handlers as handlers
import bot.db as db
import telebot
import datetime
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


# Functions
# for handling
# commands


class driverThread(Thread):

    context = None

    def __init__(self):
        Thread.__init__(self)
    
    def handle_shedule(self, date):
        text = ""
        if date != "week":
            
            if date == "today":
                day_num = datetime.datetime.today()
            elif date == "tomorrow":
                day_num = datetime.datetime.today() + datetime.timedelta(days=1)
            
            shedule_tree = mpt.getSheduleByDay(self.context.group, day_num.isoweekday())
            text += str(day_num.date()) + "\n"
            text += "------------" + "\n"
            for i in shedule_tree:
                text += "[" + i[0] + "] " + i[1] + ", " + i[2] + "\n"
            bot.send_message(self.context.message.chat.id, text=text)
        else:
            for d in range(1, 6):
                shedule_tree = mpt.getSheduleByDay(self.context.group, d)
                text = "Day: " + str(d) + "\n"
                text += "------------" + "\n"
                for i in shedule_tree:
                    text += "[" + i[0] + "] " + i[1] + ", " + i[2] + "\n\n"
                bot.send_message(self.context.message.chat.id, text=text)


    def run(self):
        while True:
            if sheduler.shedule_event.is_set():
                self.context = sheduler.pipeline.get()

                # If bot wait group in answr
                if self.context.action == sheduler.actions.WAIT_GROUP_CHOOSE:
                    bot.send_message(self.context.message.chat.id,
                                    "Выберите группу: ",
                                    reply_markup=markup.group_choose_keyboard(mpt, 
                                                            self.context.message.text))
                # If user already choose group
                elif self.context.action == sheduler.actions.WAIT_GROUP_ALREADY_CHOOSED:
                    bot.send_message(self.context.message.chat.id,
                                    "Отлично! Группа выбрана и сохранена",
                                    reply_markup=telebot.types.ReplyKeyboardRemove())
                
                # Send shedule to user    
                elif self.context.action == sheduler.actions.SHEDULE_HANDLER:
                    bot.send_message(self.context.message.chat.id, 
                                    "Выберите на какой срок: ",
                                    reply_markup=markup.choose_shedule_date())
                
                # Answer on callback
                elif self.context.action == sheduler.actions.CALLBACK_QUERY:
                    cur_user = handlers.recognize_user(self.context.call.from_user.id)
                    
                    # Today
                    if self.context.call.data == "cb_today":
                        bot.answer_callback_query(self.context.call.id, "Расписание на сегодня")
                        bot.send_message(self.context.message.chat.id,
                                        "Today_placeholder {0}".format(cur_user.group))
                        self.handle_shedule("today")
                    # Tomorrow
                    if self.context.call.data == "cb_tomorrow":
                        bot.answer_callback_query(self.context.call.id, "Расписание на завтра")
                        bot.send_message(self.context.message.chat.id,
                                        "Tomorrow_placeholder {0}".format(cur_user.group))
                        self.handle_shedule("tomorrow")
                    # All weak
                    if self.context.call.data == "cb_week":
                        bot.answer_callback_query(self.context.call.id, "Расписание на неделю")
                        bot.send_message(self.context.message.chat.id,
                                        "Weak_placeholder {0}".format(cur_user.group))
                        self.handle_shedule("week")
                   
                    else:
                        bot.answer_callback_query(self.context.call.id,
                                                 "Internal callback function error")
                
                # Send shedule changes to user
                elif self.context.action == sheduler.actions.CHANGES_HANDLER:
                    cur_user = handlers.recognize_user(self.context.message.from_user.id)

                    if cur_user:
                        bot.send_message(self.context.message.chat.id,
                                        "Changes placeholder - " + str(cur_user.group))
                if (sheduler.pipeline.qsize()) == 0:
                    sheduler.shedule_event.clear()
            else:
                print("Thread locked")
                sheduler.shedule_event.wait()



