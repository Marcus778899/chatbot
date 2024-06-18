import time
import logging
from telegram_src import bot

def start_bot():
    while True:
        try:
            bot.enable_save_next_step_handlers(delay=2)
            bot.load_next_step_handlers()
            bot.infinity_polling(timeout=60,long_polling_timeout=60)
            logging.info("Bot is running...")
        except Exception as e:
            logging.error(e)
            time.sleep(5)

if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    start_bot()