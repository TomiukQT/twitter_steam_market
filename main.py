from bot.bot import TwitterBot
from my_logger.logger import ConsoleLogger

import schedule
import time


def job(bot: TwitterBot):
    messages = bot.scan_messages()
    bot.process_new_messages(messages)


def main():
    bot = TwitterBot()
    schedule.every(2).minutes.do(job, bot=bot)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    main()
