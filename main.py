from mptParser import mptShedule

if __name__ == "__main__":
    mpt = mptShedule.mptPage()
    print(mpt.getSheduleByDay("П50-2-19", 1))