#!/usr/bin/env python3
# -*- coding: UTF8 -*-

# GitHub: wellWINeo
###################
# Simple bot and parser 
# to simplify shedule & 
# changes viewing for
# students

from mptParser import mptShedule
from logs import log
import bot
import bot.core as core_bot
import time
import concurrent.futures
import logging
import config

#debug
if config.debug:
    from guppy import hpy


# MAIN LOOP
if __name__ == "__main__":
    if config.debug:
        mem_heap = hpy()
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO

    logging.basicConfig(level=log_level, filename=config.logs_path, filemode="w")
    
    logging.info("Bot started!")
    #ThreadPool = bot.sheduler.ThreadPool(bot.handlers.driverThread, config.exec_threads)
    #ThreadPool.start()
    if config.debug:
        print(mem_heap.heap())
    core_bot.tg_bot.polling(none_stop=True)
    logging.info("Bot stopped!")
