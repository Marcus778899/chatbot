from telegram_src import bot

if __name__ == '__main__':
    bot.enable_save_next_step_handlers(delay=2)
    bot.load_next_step_handlers()
    bot.infinity_polling(interval=0, timeout=20)