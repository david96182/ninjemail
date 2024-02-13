from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
import os


def create_driver(browser, outlook=False):
    if browser == 'firefox':
        custom_profile = FirefoxProfile()
        custom_profile.set_preference("extensions.ui.developer_mode", True)

        options = FirefoxOptions()
        options.add_argument('--no-sandbox')
        #options.add_argument('--proxy-server=http://20.111.54.16:8123')
        # options.add_argument("disable-popup-blocking")
        # options.add_argument("disable-notifications")
        # options.add_argument("disable-popup-blocking")
        # options.add_argument('--ignore-ssl-errors=yes')
        # options.add_argument('--ignore-certificate-errors')
        # options.add_argument('--headless')
        # options.add_argument("--incognito")
        options.profile = custom_profile

        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
    elif browser == 'chrome':
        options = ChromeOptions()
        options.add_argument('--no-sandbox')
        if outlook:
            options.add_extension(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'captcha_solvers/capsolver_captcha_solver-1.10.4.crx'))
        # options.add_argument('--headless')

        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    else:
        raise ValueError('Unsupported browser')
    return driver
