from selenium.webdriver.common.keys import Keys
import time
from selenium import webdriver
import re

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

def share_check(browser,post):
    try:
        share_element = post.find_element_by_css_selector(
            'div.pybr56ya.dati1w0a.hv4rvrfc.n851cfcs.btwxx1t3.j83agx80.ll8tlv6m > div:nth-of-type(2) > div > div:nth-of-type(1) > span').text
        if re.search(r"shared|share|Shared|Share|shares|Shares", share_element):
            print("This is a shared post")
            time.sleep(1)
            return True
        else:
            return False

    except Exception as e:
        print(f'Share check failed')
        print(e)
