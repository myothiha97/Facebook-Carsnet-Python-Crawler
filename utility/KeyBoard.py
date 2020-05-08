from selenium.webdriver.common.keys import Keys
from selenium import webdriver

class KeyBoard():
    def click_esc_key(browser):
        return webdriver.ActionChains(browser).send_keys(Keys.ESCAPE).perform()