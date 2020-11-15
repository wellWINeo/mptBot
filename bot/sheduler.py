import threading
from mptParser.mptShedule import mptPage
import queue
from enum import Enum
import bot.core as core_bot
import bot.handlers as handlers
import bot.markup as bot_markup
import telebot

shedule_mutex = threading.RLock()
shedule_event = threading.Event()
pipeline = queue.Queue() 

# Creating mptShedule intstance
mpt = mptPage()


bot = core_bot.tg_bot

class actions(Enum):
    WAIT_GROUP_CHOOSE = 1
    WAIT_GROUP_ALREADY_CHOOSED = 2
    SHEDULE_HANDLER = 3
    CALLBACK_QUERY = 4
    CHANGES_HANDLER = 5

class context:
    action = None
    message = None
    call = None

    def __init__(self, action, message = None, call = None):
        if (message == None) and (call != None):
            self.call = call
            self.message = call.message
        else:
            self.message = message
        self.action = action



class ThreadPool:
    pool = []
    exec_fn = None

    def __init__(self, exec_fn, threads_count):
        self.exec_fn = exec_fn
        for i in range(0, threads_count):
            self.create_thread()
    def create_thread(self):
        self.pool.append(threading.Thread(target=self.exec_fn))    
    
    def start(self):
        for t in self.pool:
            t.start()

    def stop(self):
        for t in self.pool:
            t.join()

def msg_handler():
    while True:
        if shedule_event.is_set():
            context = pipeline.get()

            if context.action == actions.WAIT_GROUP_CHOOSE:
                bot.send_message(context.message.chat.id,
                                "Выберите группу: ",
                                reply_markup=bot_markup.group_choose_keyboard(mpt, context.message.text))
            elif context.action == actions.WAIT_GROUP_ALREADY_CHOOSED:
                bot.send_message(context.message.chat.id,
                                "Отлично! Группа выбрана и сохранена",
                                reply_markup=telebot.types.ReplyKeyboardRemove())
                
            elif context.action == actions.SHEDULE_HANDLER:
                bot.send_message(context.message.chat.id, 
                                "Выберите на какой срок: ",
                                reply_markup=bot_markup.choose_shedule_date())
            
            elif context.action == actions.CALLBACK_QUERY:
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

            elif context.action == actions.CHANGES_HANDLER:
                cur_user = handlers.recognize_user(context.message.from_user.id)

                if cur_user:
                    bot.send_message(context.message.chat.id,
                                                "Changes placeholder - " + \
                                                str(cur_user.group))
            if (pipeline.qsize()) == 0:
                shedule_event.clear()

        # else:
        #     shedule_event.wait()
