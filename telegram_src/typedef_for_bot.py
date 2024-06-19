import logging
from . import CassandraDB

class User:
    def __init__(self, name:str) -> None:
        self.username = name
        self.email = None
        self.phone = None
        self.password = None
        self.level = None # when customer pay for subscription

    @staticmethod
    def validate_username(username:str) -> bool:
        action = CassandraDB()
        if action.check_the_username_exist(username):
            logging.error("Username already exists")
            return False
        logging.info("Username is valid")
        action.close_driver()
        return True

    @staticmethod
    def vaildate_email(email:str) -> bool:
        if "@" not in email:
            logging.error("Invalid email address")
            return False
        logging.info("Email address is valid")
        return True
    
    @staticmethod
    def validate_phone(phone:str) -> bool:
        if len(phone) != 10 or not phone.isdigit():
            logging.error("Invalid phone number")
            return False
        logging.info("Phone number is valid")
        return True
    
    @staticmethod
    def validate_password(password:str) -> bool:
        if len(password) < 6:
            logging.error("Password must be at least 8 characters long")
            return False
        logging.info("Password is valid")
        return True
        
class user_login:
    def __init__(self, username:str) -> None:
        self.username = username
        self.password = None

    @staticmethod
    def check_user_login(username: str):
        action = CassandraDB()
        information = action.selet_data(username)
        logging.info("User login information retrieved")
        action.close_driver()
        return information
    
    def check_account(self, login: dict) -> bool:
        '''
        login successful or not
        '''
        action = CassandraDB()
        result = action.check_the_account(login)
        action.close_driver()
        return result
    
    def display_information(self):
        action = CassandraDB()
        information = action.selet_data(self.username)
        logging.info("User information retrieved")
        action.close_driver()
        return information

