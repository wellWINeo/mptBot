from mptParser import mptShedule
from logs import log
import time

if __name__ == "__main__":
    mpt = mptShedule.mptPage()
    direction = "09.02.07"
    groups = mpt.get_groups_by_dir(direction)
    print(groups)
