from threading import Thread, Lock
import threading
import mptShedule

class updaterThread(Thread):
    
    def __init__(self, mptPageInstance):
        Thread.__init__(self)
        self.instance = mptPageInstance

    def run(self):
        lock = Lock()
        lock.acquire()
        #self.mptPageInstance.update()
        lock.release()

if __name__ == "__main__":
    thread = updaterThread()
    thread.start()

