import pytest
from selenium.webdriver import Firefox, Chrome
import undetected_chromedriver as uc
from ..utils.webdriver_utils import create_driver

@pytest.fixture(autouse=True)
def mock_driver_manager_installations(monkeypatch):
    def mock_gecko_install(*args, **kwargs):
        return 'gecko_driver_path'

    def mock_chrome_install(*args, **kwargs):
        return 'chrome_driver_path'

    def mock_firefox_service(*args, **kwargs):
        return None

    def mock_chrome_service(*args, **kwargs):
        return None

    def mock_firefox(*args, **kwargs):
        pass

    def mock_chrome(*args, **kwargs):
        pass

    def mock_firefox_quit(self):
        pass

    def mock_chrome_quit(self):
        pass

    monkeypatch.setattr('webdriver_manager.firefox.GeckoDriverManager.install', mock_gecko_install)
    monkeypatch.setattr('webdriver_manager.chrome.ChromeDriverManager.install', mock_chrome_install)
    monkeypatch.setattr('selenium.webdriver.firefox.service.Service.__init__', mock_firefox_service)
    monkeypatch.setattr('selenium.webdriver.chrome.service.Service.__init__', mock_chrome_service)
    monkeypatch.setattr('selenium.webdriver.Firefox.__init__', mock_firefox)
    monkeypatch.setattr('selenium.webdriver.Chrome.__init__', mock_chrome)
    monkeypatch.setattr('undetected_chromedriver.Chrome.__init__', mock_chrome)
    monkeypatch.setattr('selenium.webdriver.Firefox.quit', mock_firefox_quit)
    monkeypatch.setattr('selenium.webdriver.Chrome.quit', mock_chrome_quit)
    monkeypatch.setattr('undetected_chromedriver.Chrome.quit', mock_chrome_quit)


def test_create_firefox_driver_no_proxy_no_captcha():
    driver = create_driver('firefox')
    assert isinstance(driver, Firefox)
    driver.quit()


def test_create_chrome_driver_no_proxy_no_captcha():
    driver = create_driver('chrome')
    assert isinstance(driver, Chrome)
    driver.quit()

def test_create_undetected_chrome_driver():
    driver = create_driver('undetected-chrome')
    assert isinstance(driver, uc.Chrome)
    driver.quit()

def test_create_undetected_chrome_driver_with_proxy_and_captcha():
    driver = create_driver('undetected-chrome', captcha_extension=True, proxy='http://10.10.10.1:2020')
    assert isinstance(driver, uc.Chrome)
    driver.quit()


def test_create_firefox_driver_with_proxy():
    proxy_url = 'http://127.0.0.1:8080'

    driver = create_driver('firefox', proxy=proxy_url)
    assert isinstance(driver, Firefox)

    driver.quit()


def test_create_chrome_driver_with_proxy():
    proxy_url = 'http://127.0.0.1:8080'

    driver = create_driver('chrome', proxy=proxy_url)
    assert isinstance(driver, Chrome)
    driver.quit()


def test_create_firefox_driver_with_captcha_extension():

    driver = create_driver('firefox', captcha_extension=True)
    assert isinstance(driver, Firefox)
    driver.quit()


def test_unsupported_browser():
    with pytest.raises(ValueError):
        create_driver('safari')
