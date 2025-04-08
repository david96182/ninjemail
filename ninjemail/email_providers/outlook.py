import logging
from typing import Optional, Tuple
from utils.web_helpers import wait_and_click, set_input_value
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait, Select

logger = logging.getLogger(__name__)

# Centralized selector configuration
SELECTORS = {
    "email_switch": (By.ID, 'liveSwitch'),
    "username_input": (By.ID, 'usernameInput'),
    "domain_select": (By.ID, 'domainSelect'),
    "next_button": (By.ID, 'nextButton'),
    "show_password": (By.ID, 'ShowHidePasswordCheckbox'),
    "optin_email": (By.ID, 'iOptinEmail'),
    "password_input": (By.ID, 'Password'),
    "first_name_input": (By.ID, 'firstNameInput'),
    "last_name_input": (By.ID, 'lastNameInput'),
    "country_select": (By.ID, 'countryRegionDropdown'),
    "birth_month": (By.ID, 'BirthMonth'),
    "birth_day": (By.ID, 'BirthDay'),
    "birth_year": (By.ID, 'BirthYear'),
    "captcha_frame": (By.ID, "enforcementFrame"),
    "captcha_reload": (By.XPATH, "//button[contains(text(), 'Reload Challenge')]"),
    "success_message": (By.XPATH, "//span[contains(text(), 'A quick note about your Microsoft account')]"),
    "ok_button": (By.ID, "id__0")
}

WAIT_TIMEOUT = 10
MAX_CAPTCHA_RETRIES = 3
CAPTCHA_RETRY_DELAY = 60

class AccountCreationError(Exception):
    """Base exception for account creation failures"""
    pass

def select_dropdown(driver: WebDriver, by: Tuple[str, str], value: str) -> None:
    """Select an option from a dropdown menu"""
    element = WebDriverWait(driver, WAIT_TIMEOUT).until(
        EC.presence_of_element_located(by)
    )
    Select(element).select_by_visible_text(value)

def select_dropdown_by_index(driver: WebDriver, by: Tuple[str, str], index: int) -> None:
    """Select a dropdown option by index"""
    element = WebDriverWait(driver, WAIT_TIMEOUT).until(
        EC.presence_of_element_located(by)
    )
    Select(element).select_by_index(index)

def handle_captcha(driver: WebDriver) -> None:
    """Handle Microsoft account captcha challenge"""
    success = False
    try:
        # Switch to captcha frames
        WebDriverWait(driver, WAIT_TIMEOUT).until(
            EC.frame_to_be_available_and_switch_to_it(SELECTORS["captcha_frame"])
        )
        WebDriverWait(driver, WAIT_TIMEOUT).until(
            EC.frame_to_be_available_and_switch_to_it((By.TAG_NAME, "iframe"))
        )
        WebDriverWait(driver, WAIT_TIMEOUT).until(
            EC.frame_to_be_available_and_switch_to_it((By.ID, "game-core-frame"))
        )
        
        # Initial captcha click
        wait_and_click(driver, (By.CSS_SELECTOR, "div#root > div > div > button"))
        
        # Handle potential retries
        for _ in range(MAX_CAPTCHA_RETRIES):
            try:
                WebDriverWait(driver, CAPTCHA_RETRY_DELAY).until(
                    EC.url_contains('privacynotice')
                )
                if 'privacynotice' in driver.current_url:
                    success = True
                    break
            except TimeoutException:
                continue
        if not success:
            raise AccountCreationError("The captcha was not solved")
    except Exception as e:
        logger.error("Captcha handling failed: %s", str(e))
        raise AccountCreationError("Captcha challenge failed") from e
    finally:
        driver.switch_to.default_content()

def verify_account_creation(driver: WebDriver) -> bool:
    """Verify successful account creation and complete final steps"""
    try:
        WebDriverWait(driver, WAIT_TIMEOUT).until(
            EC.visibility_of_element_located(SELECTORS["success_message"])
        )
        
        # Complete post-creation steps
        wait_and_click(driver, SELECTORS["ok_button"])
        
        return True
    except TimeoutException:
        logger.error("Account creation verification timeout")
        return False

def create_account(
    driver: WebDriver,
    username: str,
    password: str,
    first_name: str,
    last_name: str,
    country: str,
    month: str,
    day: str,
    year: str,
    hotmail: bool
) -> Tuple[Optional[str], Optional[str]]:
    """
    Create a new Microsoft account (Outlook/Hotmail) with enhanced reliability
    
    Returns:
        Tuple: (email, password) or (None, None) on failure
    """
    try:
        logger.info('Starting Microsoft account creation process')
        driver.get('https://signup.live.com/signup')

        # Initial email setup
        wait_and_click(driver, SELECTORS["email_switch"])
        driver.implicitly_wait(2)
        set_input_value(driver, SELECTORS["username_input"], username)

        if hotmail:
            select_dropdown_by_index(driver, SELECTORS["domain_select"], 1)

        wait_and_click(driver, SELECTORS["next_button"])

        # Password setup
        try:
            wait_and_click(driver, SELECTORS["show_password"])
            wait_and_click(driver, SELECTORS["optin_email"])
        except TimeoutException:
            logger.debug("Optional password visibility elements not found")
        
        set_input_value(driver, SELECTORS["password_input"], password)
        wait_and_click(driver, SELECTORS["next_button"])

        # Personal information
        set_input_value(driver, SELECTORS["first_name_input"], first_name)
        set_input_value(driver, SELECTORS["last_name_input"], last_name)
        wait_and_click(driver, SELECTORS["next_button"])

        # Demographic information
        select_dropdown(driver, SELECTORS["country_select"], country)
        select_dropdown_by_index(driver, SELECTORS["birth_month"], int(month))
        select_dropdown_by_index(driver, SELECTORS["birth_day"], int(day))
        set_input_value(driver, SELECTORS["birth_year"], year)
        wait_and_click(driver, SELECTORS["next_button"])

        # Captcha handling
        handle_captcha(driver)

        # Final verification
        if not verify_account_creation(driver):
            raise AccountCreationError("Account creation verification failed")

        # Log successful creation
        logger.info(f"{"Hotmail" if hotmail else "Outlook"} account created successfully")
        logger.debug("Account details: %s@%s.com", username, "hotmail" if hotmail else "outlook")
        
        return f"{username}@{'hotmail' if hotmail else 'outlook'}.com", password

    except Exception as e:
        logger.error("Account creation failed: %s", str(e))
        raise AccountCreationError("Microsoft account creation process failed") from e
    finally:
        driver.quit()
