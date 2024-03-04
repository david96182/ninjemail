import logging
import os
from config import (
    CAPTCHA_SERVICES_SUPPORTED,
    DEFAULT_CAPTCHA_SERVICE,
    SMS_SERVICES_SUPPORTED,
    DEFAULT_SMS_SERVICE,
    SUPPORTED_SOLVERS_BY_EMAIL,
    SUPPORTED_BROWSERS
)
from email_providers import outlook, gmail
from utils.webdriver_utils import create_driver
from utils import get_birthdate, generate_missing_info


class Ninjemail():
    """
    Main class to create email accounts.

    Attributes:
        browser (str): The browser to be used for automation. Default is "firefox".
        captcha_key (str): The API key for the captcha solving service. Default is an empty string.
        sms_key (dict): The API key for the SMS service. Default is an empty dict.
        captcha_services_supported (list): The list of supported captcha solving services.
        default_captcha_service (str): The default captcha solving service.
        sms_services_supported (list): The list of supported SMS services.
        default_sms_service (str): The default SMS service.

    Methods:
        __init__(self, browser="firefox", captcha_key="", sms_key=""): Initializes a Ninjemail instance.
        setup_logging(self): Sets up the logging configuration for Ninjemail.

    Logging:
        Logs are saved in the 'logs/ninjemail.log' file with a format of '[timestamp] [log_level]: log_message'.

    """
    def __init__(self,
                 browser="firefox",
                 captcha_keys={},
                 sms_key={} 
                 ):     
        """
        Initializes a Ninjemail instance.

        Args:
            browser (str, optional): The browser to be used for automation. Default is "firefox".
            captcha_key (dict, optional): The API key for the captcha solving service. Default is an empty string.
            sms_key (dict, optional): The API key for the SMS service. Default is an empty dict.
        """
        if browser not in SUPPORTED_BROWSERS:
            raise ValueError(f"Unsupported browser '{browser}'. Supported browsers are: {', '.join(SUPPORTED_BROWSERS)}")
        self.browser = browser
        self.captcha_keys = captcha_keys
        self.sms_key = sms_key

        self.captcha_services_supported = CAPTCHA_SERVICES_SUPPORTED
        self.default_captcha_service = DEFAULT_CAPTCHA_SERVICE
        self.sms_services_supported = SMS_SERVICES_SUPPORTED
        self.default_sms_service = DEFAULT_SMS_SERVICE
        self.supported_solvers_by_email = SUPPORTED_SOLVERS_BY_EMAIL 

        #Set up logging
        self.setup_logging()

    def setup_logging(self):
        """
        Sets up the logging configuration for Ninjemail.

        Logs are saved in the 'logs/ninjemail.log' file with a format of '[timestamp] [log_level]: log_message'.
        """
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
                               username="", 
                               password="", 
                               first_name="", 
                               last_name="",
                               country="",
                               birthdate="",
                               hotmail=False):
        """
        Creates an Outlook/Hotmail account using the provided information.

        Args:
            username (str, optional): The desired username for the Outlook account.
            password (str, optional): The desired password for the Outlook account.
            first_name (str, optional): The first name of the account holder.
            last_name (str, optional): The last name of the account holder.
            country (str, optional): The country of residence for the account holder.
            birthdate (str, optional): The birthdate of the account holder in the format "MM-DD-YYYY".
            hotmail (bool, optional): Flag indicating whether to create a Hotmail account. Default is False.

        Returns:
            Email and password of the created account.

        """
        api_key = None
        for solver in self.supported_solvers_by_email['outlook']:
            if solver in self.captcha_keys.keys():
                api_key = self.captcha_keys[solver]
        if not api_key:
            logging.error('API key for captcha solver service to solve captcha for Outlook was not provided.')
            logging.info(f'Supported captcha solving services for Outlook are: { self.supported_solvers_by_email["outlook"]}')
            raise ValueError('API key for captcha solver service to solve captcha for outlook was not provided.')
        driver = create_driver(self.browser, outlook=True)
        username, password, first_name, last_name, \
            country, birthdate = generate_missing_info(username, password, first_name, last_name, country, birthdate)
        month, day, year = get_birthdate(birthdate)

        return outlook.create_account(api_key,
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

    def create_gmail_account(self, 
                               username="", 
                               password="", 
                               first_name="", 
                               last_name="",
                               birthdate=""):
        """
        Creates an Gmail account using the provided information.

        Args:
            username (str, optional): The desired username for the Gmail account.
            password (str, optional): The desired password for the Gmail account.
            first_name (str, optional): The first name of the account holder.
            last_name (str, optional): The last name of the account holder.
            birthdate (str, optional): The birthdate of the account holder in the format "MM-DD-YYYY".

        Returns:
            Email and password of the created account.

        """
        
        driver = create_driver(self.browser)
        username, password, first_name, last_name, \
            _, birthdate = generate_missing_info(username, password, first_name, last_name, '', birthdate)
        month, day, year = get_birthdate(birthdate)
        if not self.sms_key.keys(): 
            logging.error('SMS API key for sms provider to verify account was not provided.')
            logging.info(f'Supported sms services for GMAIL are: { self.sms_services_supported}')
            raise ValueError('SMS API key for sms provider service to verify account for gmail was not provided.')
        else:
            self.sms_key.update({'project': 1})

        return gmail.create_account(driver, 
                                    self.sms_key,
                                    username, 
                                    password, 
                                    first_name, 
                                    last_name,
                                    month,
                                    day,
                                    year)
