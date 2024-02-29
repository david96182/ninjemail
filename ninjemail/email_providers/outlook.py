import logging
import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium import webdriver

URL = 'https://signup.live.com/signup'
WAIT = 25

def create_account(captcha_key,
                   driver, 
                   username, 
                   password, 
                   first_name, 
                   last_name,
                   country,
                   month,
                   day,
                   year,
                   hotmail):
    """
    Automatically creates an outlook/hotmail account.

    Args:
        captcha_key (str): The API key for Death By Captcha service in the format "username:password".
        driver (WebDriver): The Selenium WebDriver instance for the configured browser.
        username (str): The desired username for the email account.
        password (str): The desired password for the email account.
        first_name (str): The first name for the account holder.
        last_name (str): The last name for the account holder.
        country (str): The country for the account holder.
        month (str): The birth month for the account holder.
        day (str): The birth day for the account holder.
        year (str): The birth year for the account holder.
        hotmail (bool): Flag indicating whether to create a Hotmail account.

    Returns:
        None

    """
    logging.info('Creating outlook account')

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
        time.sleep(5)
    elif type(driver) is webdriver.Chrome:
        driver.get('https://www.google.com')
        capsolver_src = driver.find_element(By.XPATH, '/html/script[2]')
        capsolver_src = capsolver_src.get_attribute('src')
        capsolver_ext_id = capsolver_src.split('/')[2]
        driver.get(f'chrome-extension://{capsolver_ext_id}/www/index.html#/popup')
        time.sleep(5)
        
        api_key_input = driver.find_element(By.XPATH, '//input[@placeholder="Please input your API key"]')
        api_key_input.send_keys(captcha_key)
        driver.find_element(By.ID, 'q-app').click()
        time.sleep(5)
    else:
        print("The WebDriver is not an instance of Firefox.")

    driver.set_window_size(800, 600)
    driver.get(URL)

    # Select create email
    email_input = WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.ID, 'liveSwitch')))
    email_input.click()

    driver.implicitly_wait(2)

    # Insert username
    username_input = WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.ID, 'MemberName')))
    username_input.send_keys(username)

    # Select hotmail if hotmail is True
    if hotmail:
        email_domain_combobox = Select(WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.ID, 'LiveDomainBoxList'))))
        email_domain_combobox.select_by_index(1)

    driver.find_element(By.ID, 'iSignupAction').click()
    driver.implicitly_wait(2)

    # Insert password and dismark notifications
    show_password_checkbox = WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.ID, 'ShowHidePasswordCheckbox')))
    show_password_checkbox.click()
    driver.find_element(By.ID, 'iOptinEmail').click()
    driver.find_element(By.ID, 'PasswordInput').send_keys(password)
    password_next = WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.ID, 'iSignupAction')))
    password_next.click()
    
    driver.implicitly_wait(2)

    # Insert First and Last name
    first_name_input = WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.ID, 'FirstName')))
    first_name_input.send_keys(first_name)
    last_name_input = WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.ID, 'LastName')))
    last_name_input.send_keys(last_name)
    driver.find_element(By.ID, 'iSignupAction').click()

    # Insert Country and birthdate
    country_combobox = Select(WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.ID, 'Country'))))
    country_combobox.select_by_visible_text(country)
    month_combobox = Select(WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.ID, 'BirthMonth'))))
    month_combobox.select_by_index(int(month))
    day_combobox = Select(WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.ID, 'BirthDay'))))
    day_combobox.select_by_index(int(day))
    year_input = WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.ID, 'BirthYear')))
    year_input.send_keys(year)
    driver.find_element(By.ID, 'iSignupAction').click()

    driver.implicitly_wait(2)

    # captcha next button
    WebDriverWait(driver, WAIT).until(EC.frame_to_be_available_and_switch_to_it((By.ID, "enforcementFrame")))
    WebDriverWait(driver, WAIT).until(EC.frame_to_be_available_and_switch_to_it((By.TAG_NAME, "iframe")))
    WebDriverWait(driver, WAIT).until(EC.frame_to_be_available_and_switch_to_it((By.ID, "game-core-frame")))
    next_button = WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div#root > div > div > button")))
    next_button.click()

    wait = WebDriverWait(driver, 60) # wait for capsolver extension to solve the captcha
    while True:
        try:
            h2_element = wait.until(EC.visibility_of_element_located((By.XPATH, "//h2[contains(text(), 'Something went wrong. Please reload the challenge to try again.')]")))

            if h2_element:
                button = driver.find_element(By.XPATH, "//button[contains(text(), 'Reload Challenge')]")
                button.click()
        except:
            break 

    time.sleep(5)
    try:
        acc_created_text = wait.until(EC.visibility_of_element_located((By.XPATH, "//span[contains(text(), 'A quick note about your Microsoft account')]")))
        if acc_created_text:
            logging.info(f'{"Hotmail" if hotmail else "Outlook"} email account created successfully.')
            logging.info("Account Details:")
            logging.info(f"Email:      {username}@{'hotmail' if hotmail else 'outlook'}.com")
            logging.info(f"Password:      {password}")
            logging.info(f"First Name:    {first_name}")
            logging.info(f"Last Name:     {last_name}")
            logging.info(f"Country:       {country}")
            logging.info(f"Date of Birth: {month}/{day}/{year}")
            driver.quit()
            return f"{username}@{'hotmail' if hotmail else 'outlook'}.com", password
    except:
        logging.error(f"There was an error creating the {'Hotmail' if hotmail else 'Outlook'} account.")

    driver.quit()

