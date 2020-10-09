from mptParser import mptShedule
from logs import log
import time

if __name__ == "__main__":
    mpt = mptShedule.mptPage()
    while True:
        time.sleep(5)
        print(mpt.getSheduleByDay("П50-2-19", 2))
