import time
from pathlib import Path
import logging
from urllib3.exceptions import ProtocolError
from requests.exceptions import ConnectionError, ReadTimeout
from telegram_src import bot

logging.basicConfig(
    filename = Path("logfile").absolute() / "log.txt",
    filemode='a',
    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
    datefmt='%H:%M:%S',
    level=logging.INFO
    )

def start_bot():
    retry_count = 0
    max_retires = 5

    while True:
        try:
            logging.info("Bot is running...")
            bot.enable_save_next_step_handlers(delay=2)
            bot.load_next_step_handlers()
            bot.infinity_polling(timeout=60,long_polling_timeout=60)
        except (ReadTimeout, ConnectionError, ProtocolError) as e:
            logging.error(f"Connect Error: {e}")
            retry_count += 1
            if retry_count > max_retires:
                logging.error("Max retries reached. Exiting...")
                break
            sleep_time = min(2 ** retry_count, 60)
            logging.info(f"Retrying in {sleep_time} seconds...")
            time.sleep(sleep_time)
        except Exception as e:
            logging.error(f"Unexcepted Error: {e}")
            time.sleep(5)
        else:
            retry_count = 0

if __name__ == '__main__':
    start_bot()