import os
import sys
import argparse
import logging
import random
import string

from ninjemail import Ninjemail

logger = logging.getLogger(__name__)


def rand_username(prefix="ninjatest", length=6):
    return prefix + ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))


def main():
    parser = argparse.ArgumentParser(description="Run a Gmail creation flow using Ninjemail (CI runner)")
    parser.add_argument("--headless", default="true", help="Run browser headless (true/false)")
    args = parser.parse_args()

    headless = str(args.headless).lower() in ("1", "true", "yes")

    # Read secrets from environment (CI should set these as repository secrets)
    CAPSOLVER_KEY = os.environ.get("CAPSOLVER_KEY")
    SMS_5SIM_TOKEN = os.environ.get("SMS_5SIM_TOKEN")
    HTTP_PROXY = os.environ.get("HTTP_PROXY")

    if not CAPSOLVER_KEY or not SMS_5SIM_TOKEN:
        logger.error("Missing required secrets: ensure CAPSOLVER_KEY and SMS_5SIM_TOKEN are set in the workflow environment")
        sys.exit(2)

    # Configure Ninjemail
    captcha_keys = {"capsolver": CAPSOLVER_KEY}
    sms_keys = {"5sim": {"token": SMS_5SIM_TOKEN}}

    try:
        # Create Ninjemail instance. The constructor may accept extra options; keep this minimal and robust.
        ninja = Ninjemail(browser="firefox", captcha_keys=captcha_keys, sms_keys=sms_keys, auto_proxy=False)

        # Generate credentials (or use provided test password)
        username = rand_username()
        password = os.environ.get("GMAIL_TEST_PASSWORD") or ("P@ssw0rd!" + ''.join(random.choices(string.ascii_letters + string.digits, k=6)))

        logger.info("Starting Gmail creation: headless=%s username=%s", headless, username)

        email, pw = ninja.create_gmail_account(
            username=username,
            use_proxy=False,
            first_name="CI",
            last_name="Runner",
            birthdate="01-01-1990",
        )

        # Print only the created email to stdout (avoid leaking secrets)
        if email:
            print(email)
            logger.info("Created account: %s", email)
            sys.exit(0)
        else:
            logger.error("Account creation returned no email")
            sys.exit(1)

    except Exception:
        logger.exception("Gmail runner failed")
        # Non-zero exit signals workflow failure; logs include stack trace but secrets are not printed
        sys.exit(1)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")
    main()



