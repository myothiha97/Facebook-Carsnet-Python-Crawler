from selenium.webdriver.common.keys import Keys
import time

def click_see_more_button(post):
        try:
            seemore = post.find_element_by_xpath("//div[contains(text(),'See more')]")
            time.sleep(.5)
            seemore.click()
            time.sleep(2)
        except Exception as e:
            print(e)