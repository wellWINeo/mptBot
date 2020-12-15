#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# GitHub: wellWINeo

#########################
# Simple bot and parser #
# to simplify shedule & #
# changes viewing for   #
# students              #
#########################

import bot
import config
import logging
from mptParser import mptShedule
import sys
import time

#debug
if config.profiler:
    from guppy import hpy


# MAIN LOOP
if __name__ == "__main__":
    while True:
        try:
            if config.debug:
                log_level = logging.DEBUG
            else:
                log_level = logging.INFO
            
            if config.profiler:
                mem_heap = hpy()
            
            logging.basicConfig(level=log_level, filename=config.logs_path, filemode="w")
            
            logging.info("Bot started!")
         
            if config.profiler:
                print(mem_heap.heap())
            bot.core.tg_bot.polling(none_stop=True)
            logging.info("Bot stopped!")
        
        except KeyboardInterrupt:
            logging.warning("Exiting by KeyboardInterrupt")
            sys.exit()

        except:
            logging.error(f"Exception occured")
