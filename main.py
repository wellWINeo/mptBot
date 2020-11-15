#!/usr/bin/env python3
# -*- coding: UTF8-*-

from mptParser import mptShedule
from logs import log
import bot
import bot.core as core_bot
import time
import concurrent.futures

if __name__ == "__main__":
    ThreadPool = bot.sheduler.ThreadPool(bot.handlers.driverThread, 2)
    ThreadPool.start()
    core_bot.tg_bot.polling()
