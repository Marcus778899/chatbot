import logging

class User:
    def __init__(self, name:str) -> None:
        self.username = name
        self.email = None
        self.phone = None
        self.password = None
        self.level = None # when customer pay for subscription

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
        
