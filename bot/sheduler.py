import threading
#from mptParser.mptShedule import mptPage
import queue
from enum import Enum
import bot.handlers as handlers

shedule_mutex = threading.RLock()
shedule_event = threading.Event()
pipeline = queue.Queue() 

# Creating mptShedule intstance
#mpt = mptPage()


#bot = core_bot.tg_bot

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
    group = None
    
    def __init__(self, action, message = None, call = None):
        if (message == None) and (call != None):
            self.call = call
            self.message = call.message
        else:
            self.message = message
        self.group = handlers.recognize_user(self.message.from_user.id).group
        self.action = action



class ThreadPool:
    pool = []
    thread_class = None

    def __init__(self, thread_class, threads_count):
        self.thread_class = thread_class
        for i in range(0, threads_count):
            self.create_thread()
    
    def create_thread(self):
        self.pool.append(self.thread_class())    
    
    def demonize(self):
        for t in self.pool:
            t.setDaemon()

    def start(self):
        for t in self.pool:
            t.start()

    def stop(self):
        for t in self.pool:
            t.join()
