from mptParser import mptShedule
from logs import log
import bot
import bot.core_bot as core_bot
import time
import concurrent.futures

if __name__ == "__main__":
    # threads_pool = concurrent.futures.ThreadPoolExecutor(max_workers=2)
    # threads_pool.submit(bot.sheduler.msg_handler, bot.sheduler.pipeline)
    # try:
    #     bot.tg_bot.polling()
    # except:
    #     threads_pool.shutdown()

    ThreadPool = bot.utils.sheduler.ThreadPool(bot.utils.sheduler.msg_handler, 2)
    ThreadPool.start()
    core_bot.tg_bot.polling()
