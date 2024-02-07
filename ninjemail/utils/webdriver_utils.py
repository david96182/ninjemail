from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile


def create_driver(browser):
    if browser == 'firefox':
        custom_profile = FirefoxProfile()
        custom_profile.set_preference("extensions.ui.developer_mode", True)

        options = FirefoxOptions()
        options.add_argument('--no-sandbox')
        # options.add_argument("disable-popup-blocking")
        # options.add_argument("disable-notifications")
        # options.add_argument("disable-popup-blocking")
        # options.add_argument('--ignore-ssl-errors=yes')
        # options.add_argument('--ignore-certificate-errors')
        # options.add_argument('--headless')
        # options.add_argument("--incognito")
        options.profile = custom_profile

        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
    else:
        raise ValueError('Unsupported browser')
    return driver
