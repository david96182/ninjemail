import pytest
import requests

from ..sms_services.fivesim import FiveSim, APIError

# Mocking requests.post
@pytest.fixture
def mock_requests_get(mocker):
    mock = mocker.patch("requests.get")
    mock.return_value.raise_for_status.return_value = None
    mock.return_value.json.return_value = {"success": True}
    return mock

# Mocking time.sleep
@pytest.fixture
def mock_time_sleep(mocker):
    return mocker.patch("time.sleep")

# Fixture to create an instance of FiveSim
@pytest.fixture
def fivesim():
    return FiveSim(service="service_id", token="api_key", country="usa")

def test_request_success(mock_requests_get, fivesim):
    response = fivesim.request("some_command")
    assert response == {"success": True}
    mock_requests_get.assert_called_once_with(
        "https://5sim.net/v1/user/some_command",
        headers = {
                'Authorization': 'Bearer ' + 'api_key',
                }
    )

def test_request_failure(mock_requests_get, fivesim):
    mock_requests_get.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError
    with pytest.raises(APIError):
        fivesim.request("some_command")

def test_get_phone(mock_requests_get, fivesim):
    mock_requests_get.return_value.json.return_value = {
        "phone": "+1234567890",
        "id": "order123"
    }
    phone, order_id = fivesim.get_phone()
    assert phone == "234567890"
    assert order_id == "order123"

def test_get_code(mock_requests_get, fivesim):
    mock_requests_get.return_value.json.return_value = {
        "sms": [{"code" :"12345"}]
    }
    code = fivesim.get_code("order123")
    assert code == "12345"

def test_get_phone_with_prefix(mock_requests_get, fivesim):
    mock_requests_get.return_value.json.return_value = {
        "phone": "+1234567890",
        "id": "order123"
    }
    phone, order_id = fivesim.get_phone(send_prefix=True)
    assert phone == "1234567890"
    assert order_id == "order123"

def test_request_error_response(mock_requests_get, fivesim):
    mock_requests_get.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError
    with pytest.raises(APIError):
        fivesim.request("some_command")

def test_get_phone_error_response(mock_requests_get, fivesim):
    mock_requests_get.return_value.raise_for_status.side_effect = requests.exceptions.HTTPError

    with pytest.raises(APIError):
        fivesim.get_phone()

def test_request_error_no_free_phones(mock_requests_get, fivesim):
    mock_response = mock_requests_get.return_value
    mock_response.text = "no free phones"

    with pytest.raises(APIError) as exc_info:
        fivesim.request('no_phone')
    assert str(exc_info.value) == '5Sim has no free phones'

def test_request_error_not_enough_balance(mock_requests_get, fivesim):
    mock_response = mock_requests_get.return_value
    mock_response.text = "not enough user balance"

    with pytest.raises(APIError) as exc_info:
        fivesim.request('no_balance')
    assert str(exc_info.value) == 'Not enough balance'

def test_get_code_error_response(mock_requests_get, mock_time_sleep, fivesim):
    mock_time_sleep.side_effect = Exception("Test exception")
    mock_requests_get.return_value.json.return_value = {
        "status": "CANCELLED",
        "sms": []
    }
    with pytest.raises(Exception) as exc_info:
        fivesim.get_code("order123")
    assert str(exc_info.value) == "Test exception"

