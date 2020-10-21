from mptParser import mptShedule
from logs import log
import time

if __name__ == "__main__":
    mpt = mptShedule.mptPage()
    for i in range(0, 10):
        time.sleep(1)
        print(mpt.getSheduleByDay("П50-2-19", 2))

    del mpt
