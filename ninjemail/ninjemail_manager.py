import logging
import os
import sys
import random
sys.path.append(os.path.dirname(__file__))

from config import (
    CAPTCHA_SERVICES_SUPPORTED,
    DEFAULT_CAPTCHA_SERVICE,
    SMS_SERVICES_SUPPORTED,
    DEFAULT_SMS_SERVICE,
    SUPPORTED_SOLVERS_BY_EMAIL,
    SUPPORTED_BROWSERS
)
from email_providers import outlook, gmail, yahoo
from utils.webdriver_utils import create_driver
from utils import get_birthdate, generate_missing_info
from fp.fp import FreeProxy
from fp.errors import FreeProxyException


class Ninjemail():
    """
    Main class to create email accounts.

    Attributes:
        browser (str): The browser to be used for automation. Default is "firefox".
        captcha_keys (dict): The API keys for captcha solving services. Default is an empty dictionary.
        sms_keys (dict): The API keys for SMS services. Default is an empty dictionary.
        captcha_services_supported (list): The list of supported captcha solving services.
        default_captcha_service (str): The default captcha solving service.
        sms_services_supported (list): The list of supported SMS services.
        default_sms_service (str): The default SMS service.
        supported_solvers_by_email (dict): The dictionary containing supported captcha solvers by email providers.

    Methods:
        __init__(self, browser="firefox", captcha_keys={}, sms_keys={}, proxy=None, auto_proxy=False): Initializes a Ninjemail instance.
        setup_logging(self): Sets up the logging configuration for Ninjemail.
        get_proxy(self): Returns a proxy if user provided one or tries to get a free proxy if auto_proxy is enabled.
        get_captcha_key(self, email_provider): Retrieves the captcha key for the specified email provider if available.
        get_sms_key(self): Retrieves the SMS key for the default SMS service or a randomly chosen one if multiple provided.
        create_outlook_account(self, username="", password="", first_name="", last_name="", country="", birthdate="", hotmail=False, use_proxy=True): Creates an Outlook/Hotmail account using the provided information.
        create_gmail_account(self, username="", password="", first_name="", last_name="", birthdate="", use_proxy=True): Creates a Gmail account using the provided information.
        create_yahoo_account(self, username="", password="", first_name="", last_name="", birthdate="", myyahoo=False, use_proxy=True): Creates a Yahoo/Myyahoo account using the provided information.

    Logging:
        Logs are saved in the 'logs/ninjemail.log' file with a format of '[timestamp] [log_level]: log_message'.

    """
    def __init__(self,
                 browser="firefox",
                 captcha_keys={},
                 sms_keys={},
                 proxies=None,
                 auto_proxy=False
                 ):     
        """
        Initializes a Ninjemail instance.

        Args:
            browser (str, optional): The browser to be used for automation. Default is "firefox".
            captcha_keys (dict, optional): The API keys for captcha solving services. Default is an empty dictionary.
            sms_keys (dict, optional): The API keys for SMS services. Default is an empty dictionary.
            proxies (list, optional): List of proxies to use for the webdriver. Default is None.
            auto_proxy (bool, optional): Flag to indicate whether to use free proxies. Default is False.
        """
        if browser not in SUPPORTED_BROWSERS:
            raise ValueError(f"Unsupported browser '{browser}'. Supported browsers are: {', '.join(SUPPORTED_BROWSERS)}")
        self.browser = browser
        self.captcha_keys = captcha_keys
        self.sms_keys = sms_keys

        self.captcha_services_supported = CAPTCHA_SERVICES_SUPPORTED
        self.default_captcha_service = DEFAULT_CAPTCHA_SERVICE
        self.sms_services_supported = SMS_SERVICES_SUPPORTED
        self.default_sms_service = DEFAULT_SMS_SERVICE
        self.supported_solvers_by_email = SUPPORTED_SOLVERS_BY_EMAIL 
        
        self.proxies = proxies
        self.auto_proxy = auto_proxy

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

    def get_proxy(self):
        """
        Returns a proxy if user provided one or tries to get a free proxy if auto_proxy is enabled.
        """
        if self.proxies:
            return random.choice(self.proxies)
        elif self.auto_proxy:
            try:
                logging.info('Getting Free Proxy..')
                proxy = FreeProxy(country_id=['US']).get()
                return proxy
            except FreeProxyException:
                logging.info('There are no free proxies available.')
        return None

    def get_captcha_key(self, email_provider):
        """
        Retrieves the captcha key for the specified email provider if available.

        Raises a ValueError if no captcha key is provided for the email provider.
        """
        for solver in self.supported_solvers_by_email.get(email_provider.lower(), []):
            if solver in self.captcha_keys:
                return {"name": solver, "key": self.captcha_keys[solver]}
        logging.info(f'Supported captcha solving services for {email_provider} are: { self.supported_solvers_by_email[email_provider.lower()]}')
        raise ValueError(f"No captcha key provided for email provider: {email_provider}")

    def get_sms_key(self):
        """
        Retrieves the SMS key for the default SMS service or a randomly chosen one if multiple provided.

        Raises a ValueError if no SMS keys are provided.
        """
        if not self.sms_keys:
            raise ValueError("No SMS API keys provided for SMS verification.")

        if self.default_sms_service in self.sms_keys:
            return {"name": self.default_sms_service, "data": self.sms_keys[self.default_sms_service]}
        else:
            selected_service = random.choice(list(self.sms_keys.keys()))
            return {"name": selected_service, "data": self.sms_keys[selected_service]}

    def create_outlook_account(self, 
                               username="", 
                               password="", 
                               first_name="", 
                               last_name="",
                               country="",
                               birthdate="",
                               hotmail=False,
                               use_proxy=True):
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
            use_proxy (bool, optional): Flag indicating whether to use a proxy to create the account. Default is True.

        Returns:
            tuple: A tuple containing the username and password of the created account.

        """
        captcha_key = self.get_captcha_key('outlook')

        proxy = None
        if use_proxy:
            proxy = self.get_proxy()

        driver = create_driver(self.browser, captcha_extension=True, proxy=proxy, captcha_key=captcha_key)

        username, password, first_name, last_name, \
            country, birthdate = generate_missing_info(username, password, first_name, last_name, country, birthdate)
        month, day, year = get_birthdate(birthdate)

        return outlook.create_account(driver, 
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
                               birthdate="",
                               use_proxy=True):
        """
        Creates a Gmail account using the provided information.

        Args:
            username (str, optional): The desired username for the Gmail account.
            password (str, optional): The desired password for the Gmail account.
            first_name (str, optional): The first name of the account holder.
            last_name (str, optional): The last name of the account holder.
            birthdate (str, optional): The birthdate of the account holder in the format "MM-DD-YYYY".
            use_proxy (bool, optional): Flag indicating whether to use a proxy to create the account. Default is True.

        Returns:
            tuple: A tuple containing the username and password of the created account.

        """
        proxy = None
        if use_proxy:
            proxy = self.get_proxy()

        driver = create_driver(self.browser, proxy=proxy)

        username, password, first_name, last_name, \
            _, birthdate = generate_missing_info(username, password, first_name, last_name, '', birthdate)
        month, day, year = get_birthdate(birthdate)

        sms_key = self.get_sms_key()

        return gmail.create_account(driver, 
                                    sms_key,
                                    username, 
                                    password, 
                                    first_name, 
                                    last_name,
                                    month,
                                    day,
                                    year)

    def create_yahoo_account(self, 
                               username="", 
                               password="", 
                               first_name="", 
                               last_name="",
                               birthdate="",
                               use_proxy=True):
        """
        Creates a Yahoo/Myyahoo account using the provided information.

        Args:
            username (str, optional): The desired username for the Yahoo account.
            password (str, optional): The desired password for the Yahoo account.
            first_name (str, optional): The first name of the account holder.
            last_name (str, optional): The last name of the account holder.
            birthdate (str, optional): The birthdate of the account holder in the format "MM-DD-YYYY".
            use_proxy (bool, optional): Flag indicating whether to use a proxy to create the account. Default is True.

        Returns:
            dict: A dictionary containing the email and password of the created account.
        """
        captcha_key = self.get_captcha_key('yahoo')

        proxy = None
        if use_proxy:
            proxy = self.get_proxy()

        driver = create_driver(self.browser, captcha_extension=True, proxy=proxy, captcha_key=captcha_key)

        sms_key = self.get_sms_key()

        username, password, first_name, last_name, \
            _, birthdate = generate_missing_info(username, password, first_name, last_name, '', birthdate)
        month, day, year = get_birthdate(birthdate)

        return yahoo.create_account(driver, 
                                    sms_key,
                                    username, 
                                    password, 
                                    first_name, 
                                    last_name,
                                    month,
                                    day,
                                    year)
