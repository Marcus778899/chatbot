'''
telegram function
'''
import logging
from .typedef_for_bot import User
from .telegram_bot_config import bot

user_dict = {}

print("start register app!!")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hello! I'm a bot that can help you register your account.")
    bot.send_message(message.chat.id, "Please enter your username:")
    bot.register_next_step_handler(message, process_name)

def process_name(message):
    try:
        chat_id = message.chat.id
        name = message.text
        logging.info(f"user name is {name}")
        user = User(name)
        user_dict[chat_id] = user
        msg = bot.reply_to(message, "Please enter your email:")
        bot.register_next_step_handler(msg, process_email)
    except Exception as e:
        logging.error(e)

def process_email(message):

    def format_vaildate(email: str) -> bool:
        if "@" not in email:
            logging.error("email is not vaild")
            return False
        logging.info("email is vaild")
        return True

    try:
        chat_id = message.chat.id
        email = message.text
        if format_vaildate(email):
            user = user_dict[chat_id]
            user.email = email
            msg = bot.reply_to(message, "Please enter your phone number:")
            bot.register_next_step_handler(msg, process_phone)
        else:
            msg = bot.reply_to(message, "Please enter a valid email address:")
            bot.register_next_step_handler(msg, process_email)
    except Exception as e:
        logging.error(e)

def process_phone(message):
    try:
        chat_id = message.chat.id
        phone = message.text
        user = user_dict[chat_id]
        logging.info(f"user phone is {phone}")
        user.phone = phone
        msg = bot.reply_to(message, "Please enter your password:")
        bot.register_next_step_handler(msg, process_password)
    except Exception as e:
        bot.reply_to(message, "oooops phone error")
        logging.error(e)

def process_password(message):
    try:
        chat_id = message.chat.id
        password = message.text
        user = user_dict[chat_id]
        user.password = password
        bot.reply_to(message, "Registration successful!")
        logging.info(
            f"user {user.name} registered with email {user.email} and phone number {user.phone}"
        )
    except Exception as e:
        bot.reply_to(message, "oooops password error")
        logging.error(e)

@bot.message_handler(regexp='^(check|info)$')
def command_check(message):
    for index, value in user_dict.items():
        logging.info(f"index is {index} \n show content is {value.__dict__}")
        bot.send_message(
            index,
            f"Username: {value.name}\nEmail: {value.email}\nPhone: {value.phone}"
        )