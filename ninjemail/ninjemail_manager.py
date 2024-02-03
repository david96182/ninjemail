import logging
import os
from config import (
    CAPTCHA_SERVICES_SUPPORTED,
    DEFAULT_CAPTCHA_SERVICE,
    SMS_SERVICES_SUPPORTED,
    DEFAULT_SMS_SERVICE,
)
from email_providers import outlook
from utils.webdriver_utils import create_driver
from utils import get_birthdate


class Ninjemail():
    """
    Main class to create email accounts
    """
    def __init__(self,
                 browser="firefox",
                 captcha_key="",
                 sms_key="" 
                 ):     
        self.browser = browser
        self.captcha_key = captcha_key
        self.sms_key = sms_key

        self.captcha_services_supported = CAPTCHA_SERVICES_SUPPORTED
        self.default_captcha_service = DEFAULT_CAPTCHA_SERVICE
        self.sms_services_supported = SMS_SERVICES_SUPPORTED
        self.default_sms_service = DEFAULT_SMS_SERVICE

        #Set up logging
        self.setup_logging()

    def setup_logging(self):
        # Create logs directory if it doesn't exist
        logs_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
        os.makedirs(logs_dir, exist_ok=True)

        # Set up logging configuration
        logging.basicConfig(
            filename=os.path.join(logs_dir, 'ninjemail.log'),
            level=logging.INFO,
            format='%(asctime)s [%(levelname)s]: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

    def create_outlook_account(self, 
                               username, 
                               password, 
                               first_name, 
                               last_name,
                               country,
                               birthdate,
                               hotmail=False):
        """
        Creates an Outlook/Hotmail account using the provided information.

        Args:
            username (str): The desired username for the Outlook account.
            password (str): The desired password for the Outlook account.
            first_name (str): The first name of the account holder.
            last_name (str): The last name of the account holder.
            country (str): The country of residence for the account holder.
            birthdate (str): The birthdate of the account holder in the format "MM/DD/YYYY".
            hotmail (bool, optional): Flag indicating whether to create a Hotmail account. Default is False.

        Returns:
            None

        """
        driver = create_driver(self.browser)
        month, day, year = get_birthdate(birthdate)

        return outlook.create_account(self.captcha_key,
                                      driver, 
                                      username, 
                                      password, 
                                      first_name, 
                                      last_name,
                                      country,
                                      month,
                                      day,
                                      year,
                                      hotmail)

