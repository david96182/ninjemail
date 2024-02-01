import logging
import deathbycaptcha

def solve_funcaptcha(api_key, url, sitekey):
    """
    Solves a Funcaptcha using Death By Captcha service.

    Args:
        api_key (str): The API key for Death By Captcha service in the format "username:password".
        url (str): The URL of the page containing the Funcaptcha.
        sitekey (str): The public key for the Funcaptcha.

    Returns:
        str or False: The solved text of the Funcaptcha if successful, False otherwise.

    Raises:
        deathbycaptcha.AccessDeniedException: If unable to access Death By Captcha service due to invalid credentials or insufficient balance.

    """
    logging.info('Solving funcaptcha with Death By Captcha')
    username, password = api_key.split(':')
    client = deathbycaptcha.SocketClient(username, password)
    captcha_dict = {
        'publickey': sitekey,
        'pageurl': url
    }
    try:
        captcha = client.decode(type=6, funcaptcha_params=captcha_dict)
        if captcha:
            return captcha['text']
        else:
            return False
    except deathbycaptcha.AccessDeniedException:
        logging.error("Unable to access Death By Captcha, check balance or credentials")

