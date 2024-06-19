'''
telegram function
'''
import logging
from .typedef_for_bot import User,user_login
from .telegram_bot_config import bot
from . import CassandraDB

user_dict = {}

def insert_customer_information(information: User):
    action = CassandraDB()
    try:
        data = information.__dict__
        print(information)
        action.insert_into_customer_data(data)
    except Exception as e:
        logging.error(e)
    finally:
        action.close_driver()

print("start register app!!")

@bot.message_handler(commands=['register'])
def send_welcome(message):
    bot.reply_to(message, "Hello! I'm a bot that can help you register your account.")
    bot.send_message(message.chat.id, "Please enter your username:")
    bot.register_next_step_handler(message, process_name)

def process_name(message):
    try:
        chat_id = message.chat.id
        username = message.text
        if User.validate_username(username):
            logging.info(f"user {username} start register")
            user = User(username)
            user_dict[chat_id] = user
            msg = bot.reply_to(message, "Please enter your email:")
            bot.register_next_step_handler(msg, process_email)
        else:
            msg = bot.reply_to(message, "Duplicate username. Please enter new username:")
            bot.register_next_step_handler(msg, process_name)

    except Exception as e:
        logging.error(e)

def process_email(message):
    try:
        chat_id = message.chat.id
        email = message.text
        if User.vaildate_email(email):
            user = user_dict[chat_id]
            user.email = email
            msg = bot.reply_to(message, "Please enter your phone number:")
            bot.register_next_step_handler(msg, process_phone)
        else:
            msg = bot.reply_to(message, "Invalid email address. Please enter a valid email:")
            bot.register_next_step_handler(msg, process_email)
    except Exception as e:
        logging.error(e)

def process_phone(message):
    try:
        chat_id = message.chat.id
        phone = message.text
        if User.validate_phone(phone):
            user = user_dict[chat_id]
            user.phone = phone
            msg = bot.reply_to(message, "Please enter your password:")
            bot.register_next_step_handler(msg, process_password)
        else:
            msg = bot.reply_to(message, "Invalid phone number. Please enter a valid phone number:")
            bot.register_next_step_handler(msg, process_phone)
    except Exception as e:
        logging.error(e)

def process_password(message):
    try:
        chat_id = message.chat.id
        password = message.text
        if User.validate_password(password):
            logging.info(f"password vaild!")
            user = user_dict[chat_id]
            user.password = password
            bot.send_message(chat_id, "Registration successful!")
            insert_customer_information(user)
            logging.info(
                f"Customer information is save to Cassandra"
            )

        else:
            bot.reply_to(message, "Invalid password. Please enter a valid password:")
    except Exception as e:
        bot.reply_to(message, "oooops password error")
        logging.error(e)

@bot.message_handler(regexp='^(check|info)$')
def command_check(message):
    bot.send_message(message.chat.id, "Please enter your username:")
    bot.register_next_step_handler(message, process_username_check)
    logging.info(f"{message.chat.id} check info")

def process_username_check(message):
    try:
        username = message.text
        bot.send_message(
            message.chat.id,
            "Please enter your password"
        )
        bot.register_next_step_handler_by_chat_id(message.chat.id, process_password_check,username)
    except Exception as e:
        logging.error(e)

def process_password_check(message, username):
    try:
        password = message.text
        login = user_login(username)
        login_dict = {
            'username': username, 
            'password': password
        }
        if login.check_account(login_dict):
            user_info = login.display_information()
            response = f"Username: {user_info[0].username}\nEmail: {user_info[0].email}\nPhone: {user_info[0].phone}\nLevel: {user_info[0].level}"
            bot.send_message(message.chat.id, response)
        else:
            bot.send_message(message.chat.id, "Invalid username or password.")
    except Exception as e:
        logging.error(e)
        
            
            
        
        
