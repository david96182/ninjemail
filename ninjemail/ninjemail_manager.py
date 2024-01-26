import logging
import os
from config import (
    CAPTCHA_SERVICES_SUPPORTED,
    DEFAULT_CAPTCHA_SERVICE,
    SMS_SERVICES_SUPPORTED,
    DEFAULT_SMS_SERVICE,
)


class Ninjemail():
    """
    Main class to create email accounts
    """
    def __init__(self,
                 browser="",
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
            level=logging.DEBUG,
            format='%(asctime)s [%(levelname)s]: %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )

