import ninjemail
import pytest
from unittest.mock import MagicMock, patch
from unittest import mock

from ..ninjemail_manager import Ninjemail
from ..email_providers import outlook
from fp.errors import FreeProxyException



def test_init_valid_browser():
  """Tests Ninjemail initialization with a valid browser."""
  manager = Ninjemail()
  assert manager.browser == "firefox"

def test_init_valid_browser_undetected_chrome():
  """Tests Ninjemail initialization with a valid browser."""
  manager = Ninjemail(browser="undetected-chrome")
  assert manager.browser == "undetected-chrome"

def test_init_invalid_browser():
  """Tests Ninjemail initialization with an invalid browser."""
  with pytest.raises(ValueError) as excinfo:
    Ninjemail(browser="invalid_browser")
  assert "Unsupported browser" in str(excinfo.value)


@patch('ninjemail_manager.FreeProxy.get')  # Patching FreeProxy.get for mocking
def test_get_proxy_with_provided_proxy(mocker):
  """Tests get_proxy with a user-provided proxy."""
  proxy = "http://myproxy:8080"
  manager = Ninjemail(proxies=[proxy])
  assert manager.get_proxy() == proxy
  mocker.assert_not_called()  # Assert FreeProxy.get wasn't called


@patch('ninjemail_manager.FreeProxy.get')  # Patching FreeProxy.get for mocking
def test_get_proxy_with_auto_proxy_success(mocker):
  """Tests get_proxy with auto_proxy and successful free proxy retrieval."""
  manager = Ninjemail(auto_proxy=True)
  mock_proxy = {"http": "http://freeproxy:3128"}
  mocker.return_value = mock_proxy
  assert manager.get_proxy() == mock_proxy


@patch('ninjemail_manager.FreeProxy.get')  # Patching FreeProxy.get for mocking
def test_get_proxy_with_auto_proxy_failure(mocker):
  """Tests get_proxy with auto_proxy and free proxy retrieval failure."""
  manager = Ninjemail(auto_proxy=True)
  mocker.side_effect = FreeProxyException("No free proxies available")
  assert manager.get_proxy() is None


def test_get_captcha_key_valid_provider(mocker):
  """Tests get_captcha_key with a valid email provider and key."""
  mocker.patch.dict('ninjemail_manager.SUPPORTED_SOLVERS_BY_EMAIL', {'outlook': ['solver1']})
  manager = Ninjemail(captcha_keys={"solver1": "key"})
  assert manager.get_captcha_key('outlook') == {"name" : "solver1", "key": "key"}


def test_get_captcha_key_invalid_provider():
  """Tests get_captcha_key with an invalid email provider (won't pass)."""
  manager = Ninjemail()
  with pytest.raises(KeyError):  # Expecting KeyError here
    manager.get_captcha_key('invalid_provider')


def test_get_captcha_key_no_key_for_provider(mocker):
  """Tests get_captcha_key with a valid provider but no key."""
  mocker.patch.dict('ninjemail_manager.SUPPORTED_SOLVERS_BY_EMAIL', {'outlook': ['solver1']})
  manager = Ninjemail()
  with pytest.raises(ValueError) as excinfo:
    manager.get_captcha_key('outlook')
  assert "No captcha key provided for email provider: outlook" in str(excinfo.value)


def test_get_sms_key_with_keys(mocker):
  """Tests get_sms_key with multiple SMS keys provided."""
  manager = Ninjemail(sms_keys={"service1": "key1", "service2": "key2"})
  selected_service = manager.get_sms_key()
  assert selected_service["name"] in ["service1", "service2"]


def test_get_sms_key_no_keys():
  """Tests get_sms_key with no SMS keys provided."""
  manager = Ninjemail()
  with pytest.raises(ValueError) as excinfo:
    manager.get_sms_key()
  # Check both type and message
  assert isinstance(excinfo.value, ValueError)
  assert str(excinfo.value) == "No SMS API keys provided for SMS verification."


@pytest.fixture(autouse=True)
def mock_create_account_methods(monkeypatch):
    def mock_outlook(*args, **kwargs):
        return "outlook_username", "outlook_password"

    def mock_gmail(*args, **kwargs):
        return "gmail_username", "gmail_password"

    def mock_yahoo(*args, **kwargs):
        return "yahoo_username", "yahoo_password"

    monkeypatch.setattr('email_providers.outlook.create_account', mock_outlook)
    monkeypatch.setattr('email_providers.gmail.create_account', mock_gmail)
    monkeypatch.setattr('email_providers.yahoo.create_account', mock_yahoo)

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
    monkeypatch.setattr('selenium.webdriver.Firefox.quit', mock_firefox_quit)
    monkeypatch.setattr('selenium.webdriver.Chrome.quit', mock_chrome_quit)

def test_create_outlook_account():

    manager = Ninjemail(browser='chrome', captcha_keys={'capsolver': 'token'})
    username, password = manager.create_outlook_account(
        username="testuser", 
        password="testpassword",
        first_name="Test",
        last_name="User",
        country="US",
        birthdate="01-01-2000"
    )

    assert username == "outlook_username"
    assert password == "outlook_password"

def test_create_outlook_account_no_info():

    manager = Ninjemail(browser='chrome', captcha_keys={'capsolver': 'token'})
    username, password = manager.create_outlook_account(
    )

    assert username == "outlook_username"
    assert password == "outlook_password"

def test_create_outlook_account_with_proxy():

    manager = Ninjemail(browser='chrome', captcha_keys={'capsolver': 'token'}, proxies=['http://127.0.0.1:8080'])
    username, password = manager.create_outlook_account(
    )

    assert username == "outlook_username"
    assert password == "outlook_password"

def test_create_outlook_account_no_captcha_key():

    manager = Ninjemail()
    with pytest.raises(ValueError) as excinfo:
        manager.create_outlook_account(
            username="testuser", 
            password="testpassword",
            first_name="Test",
            last_name="User",
            country="US",
            birthdate="01-01-2000"
        )
    assert isinstance(excinfo.value, ValueError)
    assert str(excinfo.value) == "No captcha key provided for email provider: outlook"

def test_create_gmail_account():

    manager = Ninjemail(sms_keys={'smspool': {'token': 'aaaaaaaa'}})
    username, password = manager.create_gmail_account(
        username="testuser", 
        password="testpassword",
        first_name="Test",
        last_name="User",
        birthdate="01-01-2000"
    )

    assert username == "gmail_username"
    assert password == "gmail_password"

def test_create_gmail_account_no_info():

    manager = Ninjemail(sms_keys={'smspool': {'token': 'aaaaaaaa'}})
    username, password = manager.create_gmail_account(
    )

    assert username == "gmail_username"
    assert password == "gmail_password"

def test_create_gmail_account_with_proxy():

    manager = Ninjemail(sms_keys={'smspool': {'token': 'aaaaaaaa'}}, proxies=['http://127.0.0.1:8080'])
    username, password = manager.create_gmail_account(
    )

    assert username == "gmail_username"
    assert password == "gmail_password"

def test_create_gmail_account_no_sms_key():

    manager = Ninjemail()
    with pytest.raises(ValueError) as excinfo:
        manager.create_gmail_account(
            username="testuser", 
            password="testpassword",
            first_name="Test",
            last_name="User",
            birthdate="01-01-2000"
        )
    assert isinstance(excinfo.value, ValueError)
    assert str(excinfo.value) == "No SMS API keys provided for SMS verification."
    
def test_create_yahoo_account():

    manager = Ninjemail(browser='chrome', captcha_keys={'capsolver': 'token'},
                        sms_keys={'smspool': {'token': 'bbbbbb'}})
    username, password = manager.create_yahoo_account(
        username="testuser", 
        password="testpassword",
        first_name="Test",
        last_name="User",
        birthdate="01-01-2000"
    )

    assert username == "yahoo_username"
    assert password == "yahoo_password"

def test_create_yahoo_account_no_info():

    manager = Ninjemail(browser='chrome', captcha_keys={'capsolver': 'token'},
                        sms_keys={'smspool': {'token': 'bbbbbb'}})
    username, password = manager.create_yahoo_account(
    )

    assert username == "yahoo_username"
    assert password == "yahoo_password"

def test_create_yahoo_account_with_proxy():

    manager = Ninjemail(browser='chrome', captcha_keys={'capsolver': 'token'},
                        sms_keys={'smspool': {'token': 'bbbbbb'}}, proxies=['http://127.0.0.1:8080'])
    username, password = manager.create_yahoo_account(
    )

    assert username == "yahoo_username"
    assert password == "yahoo_password"

def test_create_yahoo_account_no_captcha_key():

    manager = Ninjemail(sms_keys={'smspool': {'token': 'bbbbbb'}})
    with pytest.raises(ValueError) as excinfo:
        manager.create_yahoo_account(
            username="testuser", 
            password="testpassword",
            first_name="Test",
            last_name="User",
            birthdate="01-01-2000"
        )
    assert isinstance(excinfo.value, ValueError)
    assert str(excinfo.value) == "No captcha key provided for email provider: yahoo"

def test_create_yahoo_account_no_sms_key():

    manager = Ninjemail(browser='chrome', captcha_keys={'capsolver': 'token'})
    with pytest.raises(ValueError) as excinfo:
        manager.create_yahoo_account(
            username="testuser", 
            password="testpassword",
            first_name="Test",
            last_name="User",
            birthdate="01-01-2000"
        )
    assert isinstance(excinfo.value, ValueError)
    assert str(excinfo.value) == "No SMS API keys provided for SMS verification."
