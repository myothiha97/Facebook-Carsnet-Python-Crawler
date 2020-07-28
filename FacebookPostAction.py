from selenium.webdriver.common.keys import Keys
import time
from selenium import webdriver

def click_see_more_button(browser,post,type):
    if type == 0:
        try:
            # seemore = post.find_element_by_xpath("//div[contains(text(),'See more')]")
            seemore = post.find_element_by_css_selector('div.j83agx80.cbu4d94t.ew0dbk1b.irj2b8pg > div > span > div > div:last-child > div')
            time.sleep(.5)
            # seemore.click()
            webdriver.ActionChains(browser).move_to_element(seemore).perform()
            browser.execute_script("arguments[0].click();", seemore)
            time.sleep(1)
        except Exception as e:
            print("An error occur while trying to click see_more button : ",str(e))

    elif type == 1:
        try:
            seemore = post.find_element_by_css_selector("div.dati1w0a.f10w8fjw.hv4rvrfc.jb3vyjys > span > div:last-child > div")
            time.sleep(.5)
            webdriver.ActionChains(browser).move_to_element(seemore).perform()
            browser.execute_script("arguments[0].click();", seemore)
            time.sleep(1)
        except Exception as e:
            print("An error occur while trying to click see_more button : ",str(e))
        