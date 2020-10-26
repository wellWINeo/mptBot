from mptParser import mptShedule
from logs import log
import time

if __name__ == "__main__":
    mpt = mptShedule.mptPage()
    print(mpt.get_groups_by_dir("09.02.01"))
