import logging
import time
from typing import Optional, Tuple
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException, NoAlertPresentException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.common.keys import Keys
from sms_services import get_sms_instance

logger = logging.getLogger(__name__)

# Centralized selector configuration
SELECTORS = {
    "first_name": (By.ID, 'firstName'),
    "last_name": (By.ID, 'lastName'),
    "month": (By.ID, 'month'),
    "day": (By.XPATH, '//input[@name="day"]'),
    "year": (By.ID, 'year'),
    "gender": (By.ID, 'gender'),
    "how_to_set_username": (By.ID, 'selectionc3'),
    "username": (By.NAME, 'Username'),
    "password": (By.NAME, 'Passwd'),
    "password_confirm": (By.NAME, 'PasswdAgain'),
    "phone_input": (By.ID, 'phoneNumberId'),
    "verification_code": (By.ID, 'code'),
    "error_message": (By.XPATH, "//div[contains(text(), 'Sorry, we could not create your Google Account.')]"),
    "phone_error": (By.XPATH, "//div[@class='Ekjuhf Jj6Lae']"),
    "final_buttons": (By.TAG_NAME, 'button')
}

NEXT_BUTTON_SELECTORS = [
    (By.XPATH, "//span[contains(text(),'Skip')]"),
    (By.CSS_SELECTOR, "div.VfPpkd-RLmnJb"),
    (By.CSS_SELECTOR, "div.VfPpkd-Jh9lGc"),
    (By.CSS_SELECTOR, "span.VfPpkd-vQzf8d"),
    (By.XPATH, "//span[contains(text(), 'Next')]"),
    (By.XPATH, "//span[contains(text(),'I agree')]"),
    (By.XPATH, "//div[contains(text(),'I agree')]"),
    (By.CLASS_NAME, "VfPpkd-LgbsSe"),
    (By.XPATH, "//button[contains(text(),'Next')]"),
    (By.XPATH, "//button[contains(text(),'I agree')]"),
]

WAIT_TIMEOUT = 10
RETRY_ATTEMPTS = 3

class AccountCreationError(Exception):
    """Base exception for account creation failures"""
    pass

def safe_click(element: WebElement) -> None:
    """Click element with JavaScript as fallback"""
    try:
        element.click()
    except WebDriverException:
        pass

def wait_and_click(driver: WebDriver, by: Tuple[str, str], timeout: int = WAIT_TIMEOUT) -> None:
    """Wait for element to be clickable and click it"""
    element = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable(by)
    )
    safe_click(element)

def next_button(driver: WebDriver) -> None:
    """Click the next button with improved reliability"""
    for selector in NEXT_BUTTON_SELECTORS:
        try:
            current_page = driver.current_url
            wait_and_click(driver, selector, timeout=5)
            time.sleep(1)  # Brief pause for page transition
            if current_page != driver.current_url:
                return
        except (TimeoutException, NoSuchElementException):
            continue
    raise AccountCreationError("Failed to find next button")

def set_how_to_set_username(driver: WebDriver) -> None:
    """Set how to set username"""
    try:
        how_to_set_username = WebDriverWait(driver, WAIT_TIMEOUT).until(EC.element_to_be_clickable((By.ID, 'selectionc3')))
        how_to_set_username.click()
    except:
        pass

def set_input_value(driver: WebDriver, selector: Tuple[str, str], value) -> None:
    """Set input value with JavaScript to ensure proper update"""
    element = WebDriverWait(driver, WAIT_TIMEOUT).until(
        EC.presence_of_element_located(selector)
    )
    driver.execute_script("arguments[0].value = arguments[1];", element, value)

def handle_errors(driver: WebDriver) -> None:
    """Check for common error conditions"""
    try:
        error_element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(SELECTORS["error_message"])
        )
        logger.error("Google account creation failed: %s", error_element.text)
        raise AccountCreationError(f"Google error: {error_element.text}")
    except TimeoutException:
        pass

def fill_personal_info(driver: WebDriver, first_name: str, last_name: str) -> None:
    """Fill in personal information section"""
    try:
        set_input_value(driver, SELECTORS["first_name"], first_name)
        set_input_value(driver, SELECTORS["last_name"], last_name)
        next_button(driver)
    except TimeoutException as e:
        logger.error("Failed to fill personal info")
        raise AccountCreationError("Personal info section timed out") from e

def fill_birthdate(driver: WebDriver, month, day, year) -> None:
    """Fill in birthdate information"""
    try:
        # Select month from dropdown
        month_select = Select(WebDriverWait(driver, WAIT_TIMEOUT).until(
            EC.element_to_be_clickable(SELECTORS["month"])
        ))
        month_select.select_by_index(int(month))
        
        # Set day and year
        set_input_value(driver, SELECTORS["day"], day)
        set_input_value(driver, SELECTORS["year"], year)
        
        # Select gender (index 3 = 'Rather not say')
        gender_select = Select(driver.find_element(*SELECTORS["gender"]))
        gender_select.select_by_index(3)
        
        next_button(driver)
    except (NoSuchElementException, TimeoutException) as e:
        logger.error("Failed to fill birthdate info")
        raise AccountCreationError("Birthdate section failed") from e

def handle_phone_verification(driver: WebDriver, sms_key, sms_provider) -> dict:
    """Handle phone number verification process"""
    try:
        phone_info = {}
        if sms_key['name'] == 'getsmscode':
            phone = sms_provider.get_phone(send_prefix=True)
            phone_info.update({'phone': phone})
        elif sms_key['name'] in ['smspool', '5sim']:
            phone, order_id = sms_provider.get_phone(send_prefix=True)
            phone_info.update({'phone': phone, 'order_id': order_id})
        
        phone_input = WebDriverWait(driver, WAIT_TIMEOUT).until(
            EC.element_to_be_clickable(SELECTORS["phone_input"])
        )
        phone_input.send_keys('+' + str(phone) + Keys.ENTER)
        
        # Check for phone number rejection
        try:
            error_element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located(SELECTORS["phone_error"])
            )
            logger.error("Phone number rejected: %s", error_element.text)
            raise AccountCreationError(f"Phone rejected: {error_element.text}")
        except TimeoutException:
            pass

        return phone_info
    except Exception as e:
        logger.error("Phone verification failed: %s", str(e))
        raise AccountCreationError("Phone verification step failed") from e

def handle_sms_code(driver: WebDriver, sms_key, sms_provider, phone_info: dict) -> None:
    """Handle SMS code entry"""
    try:
        if sms_key['name'] == 'getsmscode':
            code = sms_provider.get_code(phone_info['phone'])
        elif sms_key['name'] in ['smspool', '5sim']:
            code = sms_provider.get_code(phone_info['order_id'])
        code_input = WebDriverWait(driver, WAIT_TIMEOUT).until(
            EC.element_to_be_clickable(SELECTORS["verification_code"])
        )
        code_input.send_keys(str(code) + Keys.ENTER)
        time.sleep(2)  # Allow time for code verification
    except Exception as e:
        logger.error("SMS code entry failed: %s", str(e))
        raise AccountCreationError("SMS verification failed") from e

def confirm_alert(driver: WebDriver) -> None:
    """Confirm the alert popup"""
    try:
        WebDriverWait(driver, 10).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        alert.accept()
    except NoAlertPresentException:
        logging.info("No alert present")

def create_account(
    driver,
    sms_key,
    username,
    password,
    first_name,
    last_name,
    month,
    day,
    year
) -> Tuple[Optional[str], Optional[str]]:
    """
    Create a new Gmail account with improved reliability and error handling
    
    Returns:
        Tuple: (email, password) or (None, None) on failure
    """
    try:
        logger.info('Starting Gmail account creation process')
        driver.get('https://accounts.google.com/signup/v2/createaccount?flowName=GlifWebSignIn&flowEntry=SignUp')
        
        # Initial information
        fill_personal_info(driver, first_name, last_name)
        fill_birthdate(driver, month, day, year)
        
        # Username and password
        set_how_to_set_username(driver)
        set_input_value(driver, SELECTORS["username"], username)
        next_button(driver)
        set_input_value(driver, SELECTORS["password"], password)
        set_input_value(driver, SELECTORS["password_confirm"], password)
        next_button(driver)

        handle_errors(driver)
        
        time.sleep(2)
        if driver.find_elements(By.ID, "phoneNumberId"):
            # Phone verification
            sms_provider = get_sms_instance(sms_key, 'google')
            phone_info = handle_phone_verification(driver, sms_key, sms_provider)
            handle_sms_code(driver, sms_key, sms_provider, phone_info)
        
        for _ in range(3):
            next_button(driver)
            time.sleep(2)

        confirm_alert(driver)
        
        # Agree to terms
        agree_button = WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.CSS_SELECTOR, "button span.VfPpkd-vQzf8d")))
        agree_button.click()

        # Log successful creation
        logger.info("Gmail account created successfully")
        logger.debug("Account details: %s@gmail.com", username)
        return f"{username}@gmail.com", password

    except Exception as e:
        logger.error("Account creation failed: %s", str(e))
        raise AccountCreationError("Account creation process failed") from e
    finally:
        driver.quit()
