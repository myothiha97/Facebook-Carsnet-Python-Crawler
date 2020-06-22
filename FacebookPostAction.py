from selenium.webdriver.common.keys import Keys
import time
from selenium import webdriver

def click_see_more_button(browser,post):
        try:
            seemore = post.find_element_by_xpath("//div[contains(text(),'See more')]")
            time.sleep(.5)
            # seemore.click()
            webdriver.ActionChains(browser).move_to_element(seemore).click(seemore).perform()
            time.sleep(2)
        except Exception as e:
            print(e)