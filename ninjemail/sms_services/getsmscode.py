import logging
import random
import re
import time

import requests

PREFIXES = {
        "us":"1",
        "hk": "852",
        }

class APIError(Exception):
    pass

class GetsmsCode:
    """
    This class provides functionalities to interact with the GetsmsCode API to obtain phone numbers and SMS verification codes.

    Attributes:
        user (str): Your GetsmsCode username.
        token (str): Your GetsmsCode token.
        project (str): GetsmsCode project ID.
        country (str, optional): The country code for the phone number. Defaults to 'hk'.
        prefix (str): The phone number prefix for the specified country.
        API_URL (str): The base URL for the GetsmsCode API.

    Methods:
        _generate_generic(): Generates a random 7-digit phone number.
        get_endpoint(ccode): Returns the appropriate GetsmsCode API endpoint based on the provided country code.
        request(kwargs): Sends a POST request to the GetsmsCode API with the provided arguments.
        get_phone(send_prefix=False): Retrieves a phone number from the GetsmsCode API.
            - send_prefix (bool, optional): Specifies whether to return the phone number with or without the prefix. Defaults to False.
        get_code(phone): Retrieves the SMS verification code sent to the provided phone number.

    Exceptions:
        APIError: Raised when an error occurs while interacting with the GetsmsCode API.
    """

    _last_phone = None
    code_patt = re.compile(r"([0-9]{5,6})")

    def __init__(
            self,
            project,
            user,
            token,
            country="hk",
            ):
        self.user = user
        self.token = token
        self.project = project
        self.country = country
        self.prefix = PREFIXES.get(self.country) or ''
        self.API_URL = f"http://api.getsmscode.com/{self.get_endpoint(country)}.php"

    def _generate_generic(self):
        """
        Generates a random 7-digit phone number starting with "52".

        Returns:
            str: The generated phone number.
        """
        return "52" + str(random.randint(234562, 777777))

    def get_endpoint(self, ccode):
        """
        Returns the appropriate GetsmsCode API endpoint based on the provided country code.

        Args:
            ccode (str): The country code for the phone number.

        Returns:
            str: The corresponding GetsmsCode API endpoint.
        """
        if ccode in {
                "hk",
                }:
            return "vndo"
        if ccode in {
                "us",
                }:
            return "usdo"
        return "do"

    def request(self, **kwargs):
        """
        Sends a POST request to the GetsmsCode API with the provided arguments.

        Args:
            kwargs (dict): Additional arguments to be included in the request body.

        Returns:
            str: The API response text.

        Raises:
            APIError: If the API returns an error message.
        """
        if self.country not in {"us", "cn"}:
            kwargs["cocode"] = self.country

        res = requests.post(
                self.API_URL,
                data=dict(
                    username=self.user,
                    token=self.token,
                    pid=self.project,
                    **kwargs,
                    )
                )
        res.raise_for_status()

        text = res.text
        if "Message" in text:
            raise APIError(text)

        return text

    def get_phone(self, send_prefix=False):
        """
        Retrieves a phone number from the GetsmsCode API.

        Args:
            send_prefix (bool, optional): Specifies whether to return the phone number with or without the prefix. Defaults to False.

        Returns:
            str: The retrieved phone number, optionally with the prefix removed.

        Raises:
            APIError: If an error occurs while retrieving the phone number.
        """
        logging.info("Getting a phone number")

        data = {
                "action": "getmobile",
                }

        data = self.request(**data)

        self._last_phone = data
        logging.info("Got phone: %s", data)

        if not send_prefix:
            data = data.removeprefix(self.prefix)
        return data.strip()

    def get_code(self, phone):
        """
        Retrieves the SMS verification code sent to the provided phone number.

        Args:
            phone (str): The phone number to retrieve the code for.

        Returns:
            str: The extracted SMS verification code.

        Raises:
            APIError: If an error occurs while retrieving the code.
            AssertionError: If no code is found in the API response.
        """
        logging.info("Getting the code with phone %s", phone)

        data = {
                "action": "getsms",
                "mobile": phone,
                }
        while True:
            try:
                text = self.request(**data)
            except APIError as exc:
                logging.info("Retrying...")
                time.sleep(10)
            else:
                break
        match = re.search(self.code_patt, text.split("|")[1])
        assert match, f"No code in {text}"

        logging.info("Got code %s", match.group())
        return match.groups()[0]
