from threading import Thread, RLock
from mptParser import schedule 
import time
import config


class updaterThread(Thread):
 
    def __init__(self, mptPageInstance, mutex):
        Thread.__init__(self)
        self.instance = mptPageInstance
        self.mutex = mutex
    
    def run(self):
        while True:
            time.sleep(config.parser_update_time)
            self.mutex.acquire()
            self.instance.update()
            self.mutex.release()
