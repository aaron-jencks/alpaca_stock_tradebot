from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from login import verification_method


verification_methods = {"email", "text"}


def login(browser: webdriver.Firefox, username: str, password: str = "") -> None:
    """Logs the user into robinhood"""

    browser.get('https://robinhood.com/login')

    while True:
        try:
            submit = WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR,
                                                                                      'button[type="submit"]')))
            user_box = browser.find_element_by_css_selector('input[name="username"]')
            pass_box = browser.find_element_by_css_selector('input[name="password"]')

            user_box.send_keys(username)
            pass_box.send_keys(password)

            submit.click()
            break
        except TimeoutException as _:
            print("Failed to load the login screen, trying again")
            continue

    try:
        verify = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.hJ4K1g8Iw9BKNXpQ6RnRQ')))

        if verification_method not in verification_methods:
            print('Invalid verification method selected please use either "text" or "email".')
            return

        if verification_method == 'email':
            verify = browser.find_element_by_css_selector('._1uaripz9PIQ8yApSTs6BKk')

        verify.click()

        code = input('Please enter the code that was just {}ed to you: '.format(verification_method))

        while True:
            try:
                submit = WebDriverWait(browser, 30).until(EC.presence_of_element_located((By.CSS_SELECTOR, '._1uaripz9PIQ8yApSTs6BKk')))
                code_box = browser.find_element_by_css_selector('._5SOyDzBHYRW670BzEp1xY')
                code_box.send_keys(code)
                submit.click()
                return
            except TimeoutException as _:
                print("Something went wrong while loading the page, refreshing and trying again.")
                browser.refresh()
                continue
    except TimeoutException as _:
        return

