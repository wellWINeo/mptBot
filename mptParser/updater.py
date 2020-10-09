from threading import Thread, Lock
import threading
from mptParser import mptShedule
import time


class updaterThread(Thread):
    
    def __init__(self, mptPageInstance, mutex):
        Thread.__init__(self)
        self.instance = mptPageInstance
        print(mutex.locked())
        self.mutex = mutex
    

    def run(self):
        print("Thread started")
        #lock = threading.Lock()
        while True:
            time.sleep(10)
            print("Thread set mutex")
            
            self.mutex.acquire()
            print("mutexed")
            self.instance.update()
            self.mutex.release()
            print("Thread unset mutex")
         


if __name__ == "__main__":
    mpt = mptShedule.mptPage()
    thread = updaterThread(mpt)
    thread.start()
