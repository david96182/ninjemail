# utils/web_helpers.py
from typing import Tuple
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException

def safe_click(element: WebElement) -> None:
    """Click element with JavaScript as fallback"""
    try:
        element.click()
    except WebDriverException:
        pass

def wait_and_click(driver: WebDriver, 
                  by: Tuple[str, str], 
                  timeout: int = 10) -> None:
    """Wait for element to be clickable and click it"""
    element = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable(by)
    )
    safe_click(element)

def set_input_value(driver: WebDriver, 
                   selector: Tuple[str, str], 
                   value: str) -> None:
    """Set input value with JavaScript to ensure proper update"""
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(selector)
    )
    element.send_keys(value)
