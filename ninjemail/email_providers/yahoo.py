import logging
from typing import Optional, Tuple
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait, Select
from sms_services import get_sms_instance
from utils.web_helpers import safe_click, wait_and_click, set_input_value

logger = logging.getLogger(__name__)

# Constants
URL = 'https://login.yahoo.com/account/create'
WAIT_TIMEOUT = 25
MAX_CAPTCHA_RETRIES = 3
CAPTCHA_SOLVE_TIMEOUT = 120

# Centralized selector configuration
SELECTORS = {
    "username": (By.ID, 'usernamereg-userId'),
    "password": (By.ID, 'usernamereg-password'),
    "first_name": (By.ID, 'usernamereg-firstName'),
    "last_name": (By.ID, 'usernamereg-lastName'),
    "birth_month": (By.ID, 'usernamereg-month'),
    "birth_day": (By.ID, 'usernamereg-day'),
    "birth_year": (By.ID, 'usernamereg-year'),
    "submit_button": (By.ID, 'reg-submit-button'),
    "phone_input": (By.ID, 'usernamereg-phone'),
    "recaptcha_frame": (By.ID, "recaptcha-iframe"),
    "funcaptcha_frame": (By.ID, "arkose-iframe"),
    "verification_code": (By.ID, "verification-code-field"),
    "success_page": (By.XPATH, "//h1[contains(., 'Account created')]")
}

class AccountCreationError(Exception):
    """Base exception for Yahoo account creation failures"""
    pass

def handle_captcha(driver: WebDriver) -> None:
    """Handle Yahoo's captcha challenges with retries"""
    try:
        # Try reCAPTCHA first
        WebDriverWait(driver, CAPTCHA_SOLVE_TIMEOUT).until(
            EC.frame_to_be_available_and_switch_to_it(SELECTORS["recaptcha_frame"])
        )
        try:
            complete_btn = WebDriverWait(driver, CAPTCHA_SOLVE_TIMEOUT).until(
                EC.element_to_be_clickable((By.ID, "recaptcha-submit"))
            )
            safe_click(complete_btn)
        finally:
            driver.switch_to.default_content()
            
    except TimeoutException:
        # Fallback to FunCaptcha
        try:
            WebDriverWait(driver, WAIT_TIMEOUT).until(
                EC.frame_to_be_available_and_switch_to_it(SELECTORS["funcaptcha_frame"])
            )
            WebDriverWait(driver, CAPTCHA_SOLVE_TIMEOUT).until(
                EC.visibility_of_element_located((By.XPATH, "//h2[contains(., 'Security check complete')]"))
            )
            safe_click(driver.find_element(By.ID, 'arkose-submit'))
        finally:
            driver.switch_to.default_content()

def handle_phone_submission(driver: WebDriver, sms_key, sms_provider) -> dict:
    """Handle phone verification process"""
    phone_info = {}
    next_button_selectors = [
        (By.ID, 'reg-sms-button'),
        (By.ID, 'reg-submit-button')
    ]
    try:
        if sms_key['name'] == 'getsmscode':
            phone = sms_provider.get_phone(send_prefix=False)
            phone_info.update({'phone': phone})
        elif sms_key['name'] in ['smspool', '5sim']:
            phone, order_id = sms_provider.get_phone(send_prefix=False)
            phone_info.update({'phone': phone, 'order_id': order_id})

        set_input_value(driver, SELECTORS["phone_input"], str(phone_info.get('phone')))

        for selector in next_button_selectors:
            try:
                wait_and_click(driver, selector, timeout=10)
                return phone_info
            except (TimeoutException, NoSuchElementException):
                continue

        raise TimeoutException("No valid next button found after phone entry")
    except Exception as e:
        logger.error("Phone submission failed: %s", str(e))
        raise AccountCreationError("Phone verification step failed") from e

def verify_phone(driver: WebDriver, sms_key, sms_provider, phone_info: dict) -> None:
    """Handle SMS verification process"""
    try:
        if sms_key['name'] == 'getsmscode':
            code = sms_provider.get_code(phone_info['phone'])
        elif sms_key['name'] in ['smspool', '5sim']:
            code = sms_provider.get_code(phone_info['order_id'])
        code_input = WebDriverWait(driver, WAIT_TIMEOUT).until(
            EC.element_to_be_clickable(SELECTORS["verification_code"])
        )
        code_input.send_keys(str(code) + Keys.ENTER)
    except Exception as e:
        logger.error("SMS verification failed: %s", str(e))
        raise AccountCreationError("Phone verification failed") from e

def create_account(
    driver: WebDriver,
    sms_key: dict,
    username: str,
    password: str,
    first_name: str,
    last_name: str,
    month: str,
    day: str,
    year: str,
) -> Tuple[Optional[str], Optional[str]]:
    """
    Create a new Yahoo account with improved reliability
    
    Returns:
        Tuple: (email, password) or (None, None) on failure
    """
    try:
        logger.info('Starting Yahoo account creation process')
        driver.get(URL)

        # Account basics
        set_input_value(driver, SELECTORS["username"], username)
        set_input_value(driver, SELECTORS["password"], password)
        set_input_value(driver, SELECTORS["first_name"], first_name)
        set_input_value(driver, SELECTORS["last_name"], last_name)

        # Birthdate
        Select(WebDriverWait(driver, WAIT_TIMEOUT).until(
            EC.presence_of_element_located(SELECTORS["birth_month"])
        )).select_by_index(int(month))
        
        set_input_value(driver, SELECTORS["birth_day"], day)
        set_input_value(driver, SELECTORS["birth_year"], year)

        wait_and_click(driver, SELECTORS["submit_button"])

        # Phone verification
        sms_provider = get_sms_instance(sms_key, 'yahoo')
        phone_info = handle_phone_submission(driver, sms_key, sms_provider)

        # Captcha handling
        if not 'phone-verify' in driver.current_url:
            handle_captcha(driver)

        # SMS verification
        verify_phone(driver, sms_key, sms_provider, phone_info)

        # Verify success state
        WebDriverWait(driver, WAIT_TIMEOUT).until(
            EC.any_of(
                EC.url_contains("create/success"),
                EC.url_contains("account/upsell/webauth")
            )
        )

        # Log successful creation
        logger.info("Yahoo account created successfully")
        logger.debug("Account details: %s@yahoo.com", username)
        
        return f"{username}@yahoo.com", password

    except Exception as e:
        logger.error("Account creation failed: %s", str(e))
        raise AccountCreationError("Yahoo account creation failed") from e
    finally:
        driver.quit()

