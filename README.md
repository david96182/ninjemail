<p align="center">   <img src="logo/logo.png" alt="Ninjemail logo"/> </p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.11-blue.svg?style=flat-square" alt="Python Badge">
  <img src="https://img.shields.io/badge/code%20style-pep8-orange.svg?style=flat-square" alt="PEP8 Badge">
  <img src="https://hits.dwyl.com/david96182/ninjemail.svg?style=flat-square&show=unique&color=blue" alt="HitCount Badge">
  <img src="https://img.shields.io/github/license/david96182/ninjemail?style=flat-square" alt="GitHub License Badge">
  <img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square&color=purple" alt="PRs Welcome Badge">
</p>


------

Ninjemail is a Python library designed to streamline the process of creating email accounts across various top email provider services. With Ninjemail, you can automate the creation of email accounts, saving time and effort. It provides an easy-to-use interface for creating accounts with customizable options.

## Features

- **Automated Account Creation:** Ninjemail streamlines the process of creating email accounts by automating the necessary steps.
- **Support for Major Email Providers:** Ninjemail supports a wide range of popular email service providers including Gmail, Outlook and Yahoo, giving you flexibility in choosing the provider that suits your needs.
- **Python Integration:** Ninjemail seamlessly integrates into Python projects, allowing for efficient automation of email account creation.
- **Auto-generated Account Details:** Generate random account details for username, password, first name, last name, country, and birthdate if not provided, allowing for quick creation of multiple accounts for testing or other purposes.
- **Customizable Options:** Customize account details such as username, password, first name, last name, country, and birthdate to meet your specific requirements.
- **Error Handling and Logging:** Ninjemail provides error handling capabilities and logs activities to facilitate debugging and tracking of account creation actions.
- **Open-Source and Extensible:** Being an open-source project, Ninjemail encourages contributions and allows for further extension and improvement of its functionalities.
- **Proxy Support:** Ninjemail includes proxy support, giving users the option to use their own proxies for account creation. This feature allows for enhanced privacy, security, and flexibility during the email account creation process.
- **Free Proxy Option:** Additionally, Ninjemail offers an option to automatically retrieve and use free proxies. This feature provides users with a convenient solution for proxy usage, eliminating the need for purchasing or configuring proxies separately.

## Installation

To install Ninjemail, you can follow these steps:

1. Clone the Ninjemail repository from GitHub using the following command:

   Copy

   ```bash
   git clone https://github.com/david96182/ninjemail.git
   ```

2. Change your current directory to the cloned repository:

   Copy

   ```bash
   cd ninjemail
   ```

3. Install the required dependencies using pip:

   ```bash
   pip install -r requirements.txt
   ```

You can then proceed to use Ninjemail as described in the next instructions.

## Testing

To ensure the reliability and correctness of this project, tests have been implemented using [pytest](https://pytest.org/). The test suite covers various aspects of the codebase and helps maintain the desired functionality as the project evolves.

### Running Tests

1. Make sure you have the project's dependencies installed.

2. Navigate to the project's root directory.

3. Run the following command to execute the test suite:

   ```bash
   pytest
   ```

### Test Coverage

Comprehensive test coverage is prioritized to minimize bugs and regressions. The current code coverage can be measured using pytest-cov. To generate a coverage report, users can execute the following command:

```bash
pytest --cov
```

The coverage report will be displayed in the terminal.

### Writing Tests

When adding new features or fixing bugs, it's important to include corresponding test cases to validate the changes. Tests should be placed in the `tests/` directory, following a naming convention such as `test_module.py` or `test_class.py`. You can organize the tests based on the project's structure.

## Usage

### Importing the Library

To use Ninjemail in your Python script, import the `Ninjemail` class from the `ninjemail` module:

```python
from ninjemail import Ninjemail
```

### Initializing Ninjemail

To create an instance of Ninjemail, call the `Ninjemail` class with optional parameters:

```python
ninja = Ninjemail(
    	browser="firefox", 
    	captcha_keys={"capsolver": "YOUR_API_KEY"}, 
    	sms_keys={"service_name": {"user": "USERNAME", "token": "TOKEN"}},
    	proxy='http://ip:port',
    	auto_proxy=True
)
```

The `browser` parameter specifies the browser to be used for automation. The default value is "firefox". Currently, **Firefox and Chrome are supported**.

The `captcha_keys` parameter is a dictionary that contains the **API keys for supported captcha solving services**, based on `config.toml`. The default value is an empty dictionary. You can provide API keys for specific captcha solving services if required. Currently, **"capsolver"** is supported.

The `sms_keys` parameter is a dictionary that contains the **API key/s for the SMS service/s**, based on `config.toml`. The default value is an empty dictionary. You can provide an API key or keys for the SMS services if required. Currently, **"getsmscode"** and **"smspool"** are supported.

The `proxy` parameter specifies the proxy server to be used for the creation of the email accounts. It should be a string in the format "http://ip:port" where "ip" is the IP address of the proxy server and "port" is the port number. 

The `auto_proxy` parameter is a boolean flag that determines whether Ninjemail should automatically obtain and rotate free proxies during automation tasks. If `auto_proxy` is set to `True`, Ninjemail will handle the process of acquiring and managing free proxies internally.

Please note that when `auto_proxy` is enabled, Ninjemail will handle the management of proxies, but the availability and reliability of free proxies may vary. It's important to consider the limitations and potential risks associated with using free proxy services.

### Creating Outlook Accounts

To create an Outlook/Hotmail account using Ninjemail, call the `create_outlook_account` method:

```python
ninja.create_outlook_account(
    		username="", 
    		password="", 
    		first_name="", 
    		last_name="", 
    		country="", 
    		birthdate="", 
    		hotmail=False,
    		use_proxy=True
)
```

The `username` parameter is the desired username for the Outlook account. If not provided, a random username will be generated.

The `password` parameter is the desired password for the Outlook account. If not provided, a random password will be generated.

The `first_name` parameter is the first name of the account holder. If not provided, a random first name will be generated.

The `last_name` parameter is the last name of the account holder. If not provided, a random last name will be generated.

The `country` parameter is the country of residence for the account holder. If not provided, a random country will be selected.

The `birthdate` parameter is the birthdate of the account holder in the format "MM-DD-YYYY". If not provided, a random birthdate will be generated.

The `hotmail` parameter is a boolean flag indicating whether to create a Hotmail account. The default value is False (i.e., creates an Outlook account).

The `use_proxy` parameter determines whether to use a proxy for the process of creating an Outlook account. If `use_proxy` is set to `True`, a proxy will be utilized during the account creation process. Default is `True`.

The method returns the email and password of the created account.

### Creating Gmail Accounts

To create a Gmail account using Ninjemail, call the `create_gmail_account` method:

```python
ninja.create_gmail_account(
    		username="", 
    		password="", 
    		first_name="", 
    		last_name="", 
    		birthdate="",
    		use_proxy=True
)
```

The parameters are the same as for creating an Outlook account, except there is no `country` parameter.

The method returns the email and password of the created gmail account.

### Creating Yahoo Accounts

To create a Yahoo account using Ninjemail, call the `create_yahoo_account` method:

```python
ninja.create_yahoo_account(
    		username="", 
    		password="", 
    		first_name="", 
    		last_name="", 
    		birthdate="",
    		myyahoo=False
    		use_proxy=True
)
```

The parameters are the same as for creating an Outlook account, except there is no 'country' parameter, and there is a specific parameter for a Yahoo account that is `myyahoo`. The `myyahoo` parameter is a boolean flag indicating whether to create a Myyahoo account. The default value is False (creates a Yahoo account).

The method returns the email and password of the created account.

### Logging

Ninjemail logs its activities to a file named `ninjemail.log` in the `logs` directory. The log file has a format of `[timestamp] [log_level]: log_message`. The log levels are: DEBUG, INFO, WARNING, ERROR, and CRITICAL.

## Example

Here's an example that shows how to use Ninjemail to create an Outlook account:

```python
from ninjemail import Ninjemail

# Replace "YOUR_API_KEY", "USERNAME" and "TOKEN" with your actual keys
ninja = Ninjemail(
    		captcha_keys={"capsolver": "YOUR_API_KEY"},
    		sms_keys={"getsmscode": {"user": "USERNAME", "token": "TOKEN"}},
			auto_proxy=True)
email, password = ninja.create_outlook_account(
    					username="testuser", 
    					password="testpassword", 
    					first_name="John", 
    					last_name="Doe", 
    					country="USA", 
    					birthdate="01-01-1990"
)

print(f"Email: {email}")
print(f"Password: {password}")
```

This will create an Outlook account with the provided information and print the email and password of the created account.

Here's an example that demonstrates how to use Ninjemail to create a Yahoo account without providing any user information. Ninjemail will generate all the necessary data for you, including name, birthdate, etc. This example utilizes smspool as the SMS service and chrome as the web browser:

```python
from ninjemail import Ninjemail

# Replace "YOUR_API_KEY" and "TOKEN" with your actual API keys
ninja = Ninjemail(
    	    browser="chrome",
    		captcha_keys={"capsolver": "YOUR_API_KEY"},
    		sms_keys={"smspool": {"token": "TOKEN"}},
			auto_proxy=True)
email, password = ninja.create_yahoo_account(
    					use_proxy=False
)

print(f"Email: {email}")
print(f"Password: {password}")
```

This will create a Yahoo account with auto-generated information and will print the email and password of the created account.

## Supported Providers

Ninjemail currently supports account creation for the following email providers:

- Gmail
- Outlook/Hotmail
- Yahoo/Myyahoo
- and more to come!

## Supported SMS Services

Ninjemail currently supports two SMS services providers for phone verification during account creation:

**getsmscode.com**

**Required Data:**

To use getsmscode.com with Ninjemail, you'll need to acquire the following information:

- **Username:** Your getsmscode.com username.
- **Token:** Your API token from getsmscode.com.

**Using getsmscode.com with Ninjemail:**

1. Include the `sms_keys` argument when initializing the Ninjemail object:

   ```python
   ninja = Ninjemail(sms_keys={"getsmscode": {"user": "YOUR_USERNAME", 
                              		"token": "YOUR_TOKEN"}})
   ```
   
   Replace `YOUR_USERNAME` with your getsmscode.com username and `YOUR_TOKEN` with your API token.

**[smspool.net](https://smspool.net/?refferal=aumBFOq90I)**

**Required Data:**

To use smspool with Ninjemail, you'll need to acquire the following information:

- **Token:** Your API token from smspool.

**Using smspool.net with Ninjemail:**

1. Include the `sms_keys` argument when initializing the Ninjemail object:

   ```python
   ninja = Ninjemail(sms_keys={"smspool": {"token": "YOUR_TOKEN"}})
   ```

   Replace `token` with your smspool API key.

## Contribution

Contributions are welcome! If you have ideas for new features, encounter issues, or want to improve Ninjemail, feel free to contribute by opening issues and pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 

## Disclaimer

Ninjemail is provided solely for educational and informational purposes. It is explicitly stated that the intention behind Ninjemail is not to promote or engage in any illegal activities, including hacking or any other unauthorized actions.

While using Ninjemail, it is crucial to understand and abide by the terms of service of each email provider you choose to utilize. Creating accounts that violate these terms of service may lead to the suspension or termination of your account by the respective email provider.

To ensure responsible and lawful usage of Ninjemail, please consider the following additional points:

1. Unethical Use: Under no circumstances should Ninjemail be employed for malicious or unethical activities, including but not limited to spamming, phishing, or identity theft. Such actions are strictly prohibited.
2. Legal Compliance: You are solely responsible for ensuring that your use of Ninjemail is in full compliance with all applicable laws and regulations within your jurisdiction. Any misuse that violates the law is strictly discouraged.

By choosing to use Ninjemail, you acknowledge and accept the aforementioned disclaimers and agree to utilize this service only for educational and lawful purposes. Any misuse or illegal activities conducted using Ninjemail are entirely the responsibility of the user, and the developers and providers of Ninjemail bear no liability for such actions.
