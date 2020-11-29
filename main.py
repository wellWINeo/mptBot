#!/usr/bin/env python3
# -*- coding: UTF8 -*-

from mptParser import mptShedule
from logs import log
import bot
import bot.core as core_bot
import time
import concurrent.futures
import logging
import config

if __name__ == "__main__":
    if config.debug:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO

    logging.basicConfig(level=log_level, filename=config.logs_path, filemode="a")
    
    logging.info("Bot started!")
    ThreadPool = bot.sheduler.ThreadPool(bot.handlers.driverThread, config.exec_threads)
    ThreadPool.start()
    core_bot.tg_bot.polling()
    logging.info("Bot stopped!")
