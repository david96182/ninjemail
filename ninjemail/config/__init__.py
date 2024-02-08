import toml
import os

# Load configuration from the TOML file
config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'config.toml')
config = toml.load(config_path)

# Expose configuration variables as module-level variables
CAPTCHA_SERVICES_SUPPORTED = config.get("CAPTCHA_SERVICES_SUPPORTED", [])
DEFAULT_CAPTCHA_SERVICE = config.get("DEFAULT_CAPTCHA_SERVICE", "")
SMS_SERVICES_SUPPORTED = config.get("SMS_SERVICES_SUPPORTED", [])
DEFAULT_SMS_SERVICE = config.get("DEFAULT_SMS_SERVICE", "")
SUPPORTED_BROWSERS = config.get("SUPPORTED_BROWSERS", [])

SUPPORTED_SOLVERS_BY_EMAIL = {}
for item in config['SUPPORTED_SOLVERS_BY_EMAIL']:
    email_service = item['email_service']
    solvers = item['solvers']
    SUPPORTED_SOLVERS_BY_EMAIL[email_service] = solvers
