<p align="center">   <img src="logo/logo.png" alt="Ninjemail logo"/> </p>

Ninjemail is a Python library designed to streamline the process of creating email accounts across various top email provider services. With Ninjemail, you can automate the creation of email accounts, saving time and effort. It provides an easy-to-use interface for creating accounts with customizable options.

- **Automated Account Creation:** Ninjemail streamlines the process of creating email accounts by automating the necessary steps.
- **Support for Major Email Providers:** Ninjemail supports a wide range of popular email service providers, giving you flexibility in choosing the provider that suits your needs.
- **Python Integration:** Ninjemail seamlessly integrates into Python projects, allowing for efficient automation of email account creation.
- **Auto-generated Account Details:** Generate random account details for username, password, first name, last name, country, and birthdate if not provided, allowing for quick creation of multiple accounts for testing or other purposes.
- **Customizable Options:** Customize account details such as username, password, first name, last name, country, and birthdate to meet your specific requirements.
- **Error Handling and Logging:** Ninjemail provides error handling capabilities and logs activities to facilitate debugging and tracking of account creation actions.
- **Open-Source and Extensible:** Being an open-source project, Ninjemail encourages contributions and allows for further extension and improvement of its functionalities.

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

## Usage

### Importing the Library

To use Ninjemail in your Python script, import the `Ninjemail` class from the `ninjemail` module:

```python
from ninjemail import Ninjemail
```

### Initializing Ninjemail

To create an instance of Ninjemail, call the `Ninjemail` class with optional parameters:

```python
ninja = Ninjemail(browser="firefox", captcha_keys={"capsolver": "YOUR_API_KEY"}, sms_key={"user": "USERNAME", "token": "TOKEN"})
```

The `browser` parameter specifies the browser to be used for automation. The default value is "firefox". Currently, **Firefox and Chrome are supported**.

The `captcha_keys` parameter is a dictionary that contains the **API keys for supported captcha solving services**, based on `config.toml`. The default value is an empty dictionary. You can provide API keys for specific captcha solving services if required. Currently, **"capsolver"** is supported.

The `sms_key` parameter is a dictionary that contains the **API key for the SMS service**, based on `config.toml`. The default value is an empty dictionary. You can provide an API key for the SMS service if required. Currently, **"getsmscode"** is supported.

### Creating Outlook Accounts

To create an Outlook/Hotmail account using Ninjemail, call the `create_outlook_account` method:

```python
ninja.create_outlook_account(username="", password="", first_name="", last_name="", country="", birthdate="", hotmail=False)
```

The `username` parameter is the desired username for the Outlook account. If not provided, a random username will be generated.

The `password` parameter is the desired password for the Outlook account. If not provided, a random password will be generated.

The `first_name` parameter is the first name of the account holder. If not provided, a random first name will be generated.

The `last_name` parameter is the last name of the account holder. If not provided, a random last name will be generated.

The `country` parameter is the country of residence for the account holder. If not provided, a random country will be selected.

The `birthdate` parameter is the birthdate of the account holder in the format "MM-DD-YYYY". If not provided, a random birthdate will be generated.

The `hotmail` parameter is a boolean flag indicating whether to create a Hotmail account. The default value is False (i.e., creates an Outlook account).

The method returns the email and password of the created account.

### Creating Gmail Accounts

To create a Gmail account using Ninjemail, call the `create_gmail_account` method:

```python
ninja.create_gmail_account(username="", password="", first_name="", last_name="", birthdate="")
```

The parameters are the same as for creating an Outlook account, except there is no `country` parameter.

The method returns the email and password of the created account.

### Logging

Ninjemail logs its activities to a file named `ninjemail.log` in the `logs` directory. The log file has a format of `[timestamp] [log_level]: log_message`. The log levels are: DEBUG, INFO, WARNING, ERROR, and CRITICAL.

## Example

Here's an example that shows how to use Ninjemail to create an Outlook account:

```python
from ninjemail import Ninjemail

# Replace "YOUR_API_KEY" with your actual API key
ninja = Ninjemail(captcha_keys={"capsolver": "YOUR_API_KEY"}, sms_key={"user": "USERNAME", "token": "TOKEN"})
email, password = ninja.create_outlook_account(username="testuser", password="testpassword", first_name="John", last_name="Doe", country="USA", birthdate="01-01-1990")

print(f"Email: {email}")
print(f"Password: {password}")
```

This will create an Outlook account with the provided information and print the email and password of the created account.

## Supported Providers

Ninjemail currently supports account creation for the following email providers:

- Gmail
- Outlook/Hotmail
- and more to come!

## Supported SMS Services

Ninjemail currently supports one SMS service provider for phone verification during account creation:

**getsmscode.com**

**Required Data:**

To use getsmscode.com with Ninjemail, you'll need to acquire the following information:

- **Username:** Your getsmscode.com username.
- **Token:** Your API token from getsmscode.com.

**Using getsmscode.com with Ninjemail:**

1. Include the `sms_key` argument when initializing the Ninjemail object:

   ```python
   ninja = Ninjemail(sms_key={"user": "YOUR_USERNAME", "token": "YOUR_TOKEN"})
   ```

   Replace `YOUR_USERNAME` with your getsmscode.com username and `YOUR_TOKEN` with your API token.

## Contribution

Contributions are welcome! If you have ideas for new features, encounter issues, or want to improve Ninjemail, feel free to contribute by opening issues and pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 
