from selenium import webdriver
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
import os
from urllib.parse import urlparse


def create_driver(browser, captcha_extension=False, proxy=None):
    if browser == 'firefox':
        custom_profile = FirefoxProfile()
        custom_profile.set_preference("extensions.ui.developer_mode", True)

        options = FirefoxOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        options.add_argument('--headless')

        # proxy
        if proxy:
            parsed_url = urlparse(proxy)

            ip_address = parsed_url.hostname
            port = parsed_url.port

            options.set_preference("network.proxy.type", 1)
            options.set_preference("network.proxy.http", ip_address)
            options.set_preference("network.proxy.http_port", port)
            options.set_preference('network.proxy.socks', ip_address)
            options.set_preference('network.proxy.socks_port', port)
            options.set_preference('network.proxy.socks_remote_dns', False)
            options.set_preference("network.proxy.ssl", ip_address)
            options.set_preference("network.proxy.ssl_port", port)

        options.profile = custom_profile

        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)
    elif browser == 'chrome':
        options = ChromeOptions()
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        options.add_argument('--headless=new')
        if proxy:
            options.add_argument(f'--proxy-server={proxy}')
        if captcha_extension:
            options.add_extension(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'captcha_solvers/capsolver_captcha_solver-1.10.4.crx'))

        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    else:
        raise ValueError('Unsupported browser')
    return driver
