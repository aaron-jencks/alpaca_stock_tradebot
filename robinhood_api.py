from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys


def login(browser: webdriver.Firefox, username: str, password: str = "") -> None:
    """Logs the user into robinhood"""

    browser.get('https://robinhood.com/login')

    while True:
        try:
            submit = WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                                      'button[type="submit"]')))
            user_box = browser.find_element_by_css_selector('input[name="username"]')
            pass_box = browser.find_element_by_css_selector('input[name="password"]')
            break
        except TimeoutException as _:
            print("Failed to load the login screen, trying again")
            continue

    user_box.send_keys(username)
    pass_box.send_keys(password)

    submit.click()
