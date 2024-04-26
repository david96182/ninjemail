import logging
import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from sms_services import getsmscode, smspool, fivesim
import undetected_chromedriver as uc

URL = 'https://login.yahoo.com/account/create'
WAIT = 25

def create_account(captcha_key,
                   driver, 
                   sms_key,
                   username, 
                   password, 
                   first_name, 
                   last_name,
                   month,
                   day,
                   year,
                   myyahoo):
    """
    Automatically creates a Yahoo  account.

    Args:
        captcha_key (str): The API key for the captcha solving service.
        driver (WebDriver): The Selenium WebDriver instance for the configured browser.
        sms_key(dict): The data of the SMS service.
        username (str): The desired username for the email account.
        password (str): The desired password for the email account.
        first_name (str): The first name for the account holder.
        last_name (str): The last name for the account holder.
        month (str): The birth month for the account holder.
        day (str): The birth day for the account holder.
        year (str): The birth year for the account holder.
        myyahoo (bool): Flag indicating whether to create a Myyahoo account.

    Returns:
        tuple: Email and password of the created account.

    """
    SMS_SERVICE = sms_key['name']

    if SMS_SERVICE == 'getsmscode':
        data = sms_key['data'] 
        data.update({'project': 15,
                     'country': 'us'})
        sms_provider = getsmscode.GetsmsCode(**data)
    elif SMS_SERVICE == 'smspool':
        data = sms_key['data']
        data.update({'service': 1034})
        sms_provider = smspool.SMSPool(**data)
    elif SMS_SERVICE == '5sim':
        data = sms_key['data']
        data.update({'service': 'yahoo'})
        sms_provider = fivesim.FiveSim(**data)

    if type(driver) is webdriver.Firefox:
        driver.install_addon(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'captcha_solvers/capsolver_captcha_solver-1.10.4.xpi'))
        driver.get('https://www.google.com')
        capsolver_src = driver.find_element(By.XPATH, '/html/script[2]')
        capsolver_src = capsolver_src.get_attribute('src')
        capsolver_ext_id = capsolver_src.split('/')[2]
        driver.get(f'moz-extension://{capsolver_ext_id}/www/index.html#/popup')
        time.sleep(5)
        
        api_key_input = driver.find_element(By.XPATH, '//input[@placeholder="Please input your API key"]')
        api_key_input.send_keys(captcha_key)
        driver.find_element(By.ID, 'q-app').click()
        
        # solve recaptcha by token
        #token_recaptcha = driver.find_element(By.XPATH, '/html/body/div/div/div/main/div[2]/div[2]/div[1]/div[1]/div[3]/div[2]/div[1]/div[1]/span')
        #token_recaptcha.click()
        time.sleep(5)
    elif type(driver) is webdriver.Chrome or type(driver) is uc.Chrome:
        driver.get('https://www.google.com')
        capsolver_src = driver.find_element(By.XPATH, '/html/script[2]')
        capsolver_src = capsolver_src.get_attribute('src')
        capsolver_ext_id = capsolver_src.split('/')[2]
        driver.get(f'chrome-extension://{capsolver_ext_id}/www/index.html#/popup')
        time.sleep(5)
        
        api_key_input = driver.find_element(By.XPATH, '//input[@placeholder="Please input your API key"]')
        api_key_input.send_keys(captcha_key)
        driver.find_element(By.ID, 'q-app').click()

        # solve recaptcha by token
        #token_recaptcha = driver.find_element(By.XPATH, '/html/body/div/div/div/main/div[2]/div[2]/div[1]/div[1]/div[3]/div[2]/div[1]/div[1]/span')
        #token_recaptcha.click()
        time.sleep(5)

    logging.info('Creating Yahoo account')

    driver.get(URL)
    driver.implicitly_wait(2)

    # insert username
    username_input = WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.ID, 'usernamereg-userId')))
    username_input.send_keys(username)
    time.sleep(1)

    # select myyahoo if myyahoo is True
    if myyahoo:
        email_domain_combobox = Select(WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.ID, 'yid-domain-selector'))))
        email_domain_combobox.select_by_index(1)

    # insert password
    password_input = WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.ID, 'usernamereg-password')))
    password_input.send_keys(password)
    time.sleep(2)

    # insert First and Last name
    first_name_input = WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.ID, 'usernamereg-firstName')))
    first_name_input.send_keys(first_name)

    last_name_input = WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.ID, 'usernamereg-lastName')))
    last_name_input.send_keys(last_name)
    time.sleep(2)

    # birthdate
    month_combobox = Select(WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.ID, 'usernamereg-month'))))
    month_combobox.select_by_index(int(month))
    time.sleep(1)

    day_combobox = WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.ID, 'usernamereg-day')))
    day_combobox.send_keys(int(day))

    year_input = WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.ID, 'usernamereg-year')))
    year_input.send_keys(year)

    driver.implicitly_wait(2)

    next_button = driver.find_element(By.ID, 'reg-submit-button')
    next_button.click()

    # get and insert phone
    if SMS_SERVICE == 'getsmscode':
        phone = sms_provider.get_phone(send_prefix=False)
    elif SMS_SERVICE == 'smspool' or SMS_SERVICE == '5sim':
        phone, order_id = sms_provider.get_phone(send_prefix=False)
    time.sleep(2)
    WebDriverWait(driver, WAIT).until(EC.element_to_be_clickable((By.ID, "usernamereg-phone"))).send_keys(str(phone) + Keys.ENTER)

    wait = WebDriverWait(driver, 5) # wait for capsolver extension to solve the captcha
    try:
        # recaptcha challenge
        WebDriverWait(driver, WAIT).until(EC.frame_to_be_available_and_switch_to_it((By.ID, "recaptcha-iframe")))
        time.sleep(10)
        try:
            complete_recaptcha = WebDriverWait(driver, 120).until(EC.element_to_be_clickable((By.ID, "recaptcha-submit")))

            driver.switch_to.default_content()
            WebDriverWait(driver, WAIT).until(EC.frame_to_be_available_and_switch_to_it((By.ID, "recaptcha-iframe")))
            continue_button = driver.find_element(By.ID, 'recaptcha-submit')
            continue_button.click()

            complete_recaptcha.click()

            driver.switch_to.default_content()
        except:
            pass
    except:
        # funcaptcha challenge
        try:
            WebDriverWait(driver, WAIT).until(EC.frame_to_be_available_and_switch_to_it((By.ID, "arkose-iframe")))
            while True:
                try:
                    h2_element = wait.until(EC.visibility_of_element_located((By.XPATH, "//h2[contains(text(), 'Security check')]")))
                except:
                    break
        
            challenge_complete = wait.until(EC.visibility_of_element_located((By.XPATH, "//h2[contains(text(), 'Security check complete')]")))
            continue_button = driver.find_element(By.ID, 'arkose-submit')
            continue_button.click()
        except:
            logging.error("Captcha was not solved.")

    # check if captcha was not correctly solved
    current_url = driver.current_url
    if "challenge/fail" in current_url:
        logging.error("Error after solve captcha. Too many failed attempts.")
        driver.quit()
        return None, None

    # verify sms
    try:
        if SMS_SERVICE == 'getsmscode':
            code = sms_provider.get_code(phone)
        elif SMS_SERVICE == 'smspool' or  SMS_SERVICE == '5sim':
            code = sms_provider.get_code(order_id) 
        WebDriverWait(driver, WAIT).until(EC.element_to_be_clickable((By.ID, "verification-code-field"))).send_keys(str(code) + Keys.ENTER)
    except:
        logging.error("Error confirming phone number.")
        return None, None

    # check if account was created successfully
    try:
        current_url = driver.current_url
        if "/create/success" in current_url:
            done = WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.TAG_NAME, 'button'))) 
            done.click()
            time.sleep(5)
            driver.quit
    except:
        logging.error("Error verificating the account.")
        return None, None

    logging.info(f'{"Myyahoo" if myyahoo else "Yahoo"} email account created successfully.')
    logging.info("Account Details:")
    logging.info(f"Email:      {username}@{'myyahoo' if myyahoo else 'yahoo'}.com")
    logging.info(f"Password:      {password}")
    logging.info(f"First Name:    {first_name}")
    logging.info(f"Last Name:     {last_name}")
    logging.info(f"Date of Birth: {month}/{day}/{year}")
    driver.quit()
    return f"{username}@{'myyahoo' if myyahoo else 'yahoo'}.com", password

