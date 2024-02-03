import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from captcha_solvers import deathbycaptchasolver

URL = 'https://signup.live.com/signup'
WAIT = 15

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
    driver.find_element(By.ID, 'iSignupAction').click()
    
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

    # Get sitekey and solve captcha
    iframe = WebDriverWait(driver, WAIT).until(EC.presence_of_element_located((By.ID, 'enforcementFrame')))
    iframe_src_parts = iframe.get_attribute('src').split('/')
    site_key = iframe_src_parts[3]
    captcha_url = driver.current_url
    
    captcha_token = deathbycaptchasolver.solve_funcaptcha(captcha_key, captcha_url, site_key)
    if not captcha_token:
        logging.error("Captcha was not solved. Finishing..")
        driver.quit()
        return
    driver.execute_script(
            'parent.postMessage(JSON.stringify({eventId:"challenge-complete",payload:{sessionToken:"' + captcha_token + '"}}),"*")')

    driver.quit()


