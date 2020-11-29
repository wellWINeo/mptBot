from threading import Thread, RLock
from mptParser import mptShedule
import time
import config

class updaterThread(Thread):
    
    def __init__(self, mptPageInstance, mutex):
        Thread.__init__(self)
        self.instance = mptPageInstance
        self.mutex = mutex
    

    def run(self):
        #print("Thread started")
        while True:
            time.sleep(config.parser_update_time)
            #print("Thread set mutex")
            self.mutex.acquire()
            self.instance.update()
            self.mutex.release()
            #print("Thread unset mutex")
         


if __name__ == "__main__":
    mpt = mptShedule.mptPage()
    thread = updaterThread(mpt)
    thread.start()
