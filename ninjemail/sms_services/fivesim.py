import logging
import re
import time

import requests

PREFIXES = {
        "usa":"1",
        }

class APIError(Exception):
    pass

class FiveSim:
    """
    This class provides functionalities to interact with the 5Sim API to obtain phone numbers and SMS verification codes.

    Attributes:
        token (str): Your 5Sim api key.
        service (str): 5Sim service name.
        country (str, optional): The country name for the phone number. Defaults to 'usa'.

    Methods:
        request(kwargs): Sends a GET request to the 5Sim API with the provided arguments.
        get_phone(send_prefix=False): Purchases a phone number from the 5Sim API.
            - send_prefix (bool, optional): Specifies whether to return the phone number with or without the prefix. Defaults to False.
        get_code(phone): Retrieves the SMS verification code sent to the provided phone number.

    Exceptions:
        APIError: Raised when an error occurs while interacting with the 5Sim API.
    """

    _last_phone = None
    code_patt = re.compile(r"([0-9]{5,6})")

    def __init__(
            self,
            service,
            token,
            country='usa',
            ):
        self.token = token
        self.service = service
        self.country = country
        self.prefix = PREFIXES.get(self.country) or ''
        self.API_URL = "https://5sim.net/v1/user/"

    def request(self, cmd):
        """
        Sends a GET request to the 5Sim API with the provided arguments.

        Args:
            kwargs (dict): Additional arguments to be included in the request body.

        Returns:
            str: The API response text.

        Raises:
            APIError: If the API returns an error message.
        """
        headers = {
                'Authorization': 'Bearer ' + self.token,
                } 

        res = requests.get(
                self.API_URL + cmd,
                headers=headers,
                )
        try:
            res.raise_for_status()
        except requests.exceptions.HTTPError as err:
            raise APIError(str(err))

        if res.text == "no free phones":
            raise APIError('5Sim has no free phones')
        if res.text == "not enough user balance":
            raise APIError("Not enough balance")

        return res.json()

    def get_phone(self, send_prefix=False):
        """
        Purchases a phone number from the 5Sim API.

        Args:
            send_prefix (bool, optional): Specifies whether to return the phone number with or without the prefix. Defaults to False.

        Returns:
            str: The retrieved phone number, optionally with the prefix removed and the order id of the purchased phone number.

        Raises:
            APIError: If an error occurs while retrieving the phone number.
        """
        logging.info("Getting a phone number")

        cmd = 'buy/activation/' + self.country + '/any/' + self.service
        data = self.request(cmd=cmd)

        self._last_phone = data
        phone_number = data['phone'] 
        phone_number = phone_number.removeprefix('+')
        order_id = data['id']

        logging.info("Got phone: %s", phone_number)

        if not send_prefix:
            phone_number = phone_number.removeprefix('1')
        return phone_number, order_id

    def get_code(self, order_id):
        """
        Retrieves the SMS verification code sent to the provided phone number.

        Args:
            order_id (str): The order_id to retrieve the code for the sms.

        Returns:
            str: The extracted SMS verification code.

        Raises:
            APIError: If an error occurs while retrieving the code.
            AssertionError: If no code is found in the API response.
        """
        logging.info("Getting the verification code")

        cmd = '/check/' + str(order_id)
        received = False
        while not received:
            res = self.request(cmd=cmd)
            if res['sms']:
                received = True
            elif res['status'] in ['CANCELED', 'TIMEOUT', 'BANNED']:
                raise APIError('Error getting verification code, order status: %s' % res['status'])
            else:
                logging.info("Retrying...")
                time.sleep(10)

        sms = res['sms']
        code = sms[0]['code']

        logging.info("Got code %s", code)
        return code


