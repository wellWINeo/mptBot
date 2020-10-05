from threading import Thread, Lock
import threading
from mptParser import mptShedule
import time


class updaterThread(Thread):
    
    def __init__(self, mptPageInstance):
        Thread.__init__(self)
        self.instance = mptPageInstance

    def run(self):
        print("Thread started")
        lock = Lock()
        while True:
            time.sleep(10)
            print("Thread set mutex")
            lock.acquire()
            if lock.locked(): 
                print(threading.current_thread)
            self.instance.update()
            lock.release()
            print("Thread unset mutex")
                    

if __name__ == "__main__":
    mpt = mptShedule.mptPage()
    thread = updaterThread(mpt)
    thread.start()