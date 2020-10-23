from utility.KeyBoard import KeyBoard
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import NoSuchElementException
from decouple import config
import argparse
import sys
import time
import re
from ImageExtractor import FacebookImageExtractor

class ImageClickTester():

    def __init__(self,mail=config('EMAIL') , password = config('PASSWORD'),depth=3,keep=3):
        self.mail = mail
        self.password = password
        self.depth = depth
        self.keep = keep
        self.browser = webdriver.Chrome('./drivers/chromedriver')
        self.market_place = 1

    def click_images(self):
        self.login(self.mail,self.password)
        time.sleep(5)
        self.browser.get('https://www.facebook.com/groups/378369752669659/?ref=share')
        time.sleep(3)
        for i in range(self.depth):
            # self.click_esc_key()
            KeyBoard.click_esc_key(self.browser)

            time.sleep(self.keep)

            # Scrolling
            self.browser.execute_script(
                "window.scrollBy(0, document.body.scrollHeight)")

        time.sleep(1)
        self.browser.execute_script(
            "window.scrollTo(document.body.scrollHeight,0)")
        # time.sleep(0.5)
        time.sleep(3)
        if self.market_place == 0:
            print("This is page")
            images = self.click_normal_gallery()
            print("------>Total Images<--------")
            print(images)
        else:
            WebDriverWait(self.browser, 10).until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div.cb02d2ww.ni8dbmo4.stjgntxs.l9j0dhe7.k4urcfbm.du4w35lb.lzcic4wl > div > div:nth-of-type(2) > a:nth-of-type(2)")))
            gp_type = self.browser.find_element_by_css_selector(
                "div.cb02d2ww.ni8dbmo4.stjgntxs.l9j0dhe7.k4urcfbm.du4w35lb.lzcic4wl > div > div:nth-of-type(2) > a:nth-of-type(2)").text

            if gp_type == "Discussion":
                print("This group is normal gp")
                images = self.click_normal_gallery()
            else:
                print("This group is market place")
                images = self.click_market_gallery()
            
            print("------>Total Images<--------")
            print(images)
        
    def click_market_gallery(self):
        posts = self.browser.find_elements_by_css_selector("div[aria-labelledby*='jsc']")
        posts_images = [] ### two dimensional array
        for post in posts:
            self.browser.execute_script(
                    "arguments[0].scrollIntoView();", post)
            try:
                share_check = post.find_element_by_css_selector(
                    'div.pybr56ya.dati1w0a.hv4rvrfc.n851cfcs.btwxx1t3.j83agx80.ll8tlv6m > div:nth-of-type(2) > div > div:nth-of-type(1) > span').text
                if re.search(r"shared|share|Shared|Share|shares|Shares", share_check):
                    print("This is a shared post")
                    time.sleep(1)
                    continue
            except Exception as e:
                print(f'Share check failed')
                continue
            images = FacebookImageExtractor.extract_images_from_market_gallary(post=post,browser= self.browser)
            posts_images.append(images)
        return posts_images

    def click_normal_gallery(self):
        posts = self.browser.find_elements_by_css_selector("div[aria-labelledby*='jsc']")
        print('posts --> ',len(posts))
        posts_images = [] ### two dimensional array
        for post in posts:
            self.browser.execute_script(
                    "arguments[0].scrollIntoView();", post)
            try:
                share_check = post.find_element_by_css_selector(
                    'div.pybr56ya.dati1w0a.hv4rvrfc.n851cfcs.btwxx1t3.j83agx80.ll8tlv6m > div:nth-of-type(2) > div > div:nth-of-type(1) > span').text
                if re.search(r"shared|share|Shared|Share|shares|Shares", share_check):
                    print("This is a shared post")
                    time.sleep(1)
                    continue
            except Exception as e:
                print(f'Share check failed')
                # print(e)
            images = FacebookImageExtractor.extract_images_from_normal_gallary(post=post , browser= self.browser)
            posts_images.append(images)
        return posts_images
        
    def login(self,mail,password):

        self.browser.get("https://www.facebook.com")

        emailbox = self.browser.find_element_by_name("email")
        emailbox.clear()
        emailbox.send_keys(mail)

        emailbox = self.browser.find_element_by_name("pass")
        emailbox.clear()
        emailbox.send_keys(password)

        emailbox.send_keys(Keys.ENTER)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Facebook Image Tester")
    parser.add_argument("-d", "--depth", type=int, default=3, metavar="", help="Numbers of scroll")
    parser.add_argument("-k", "--keep", type=int, default=3, metavar="", help="Seconds you want to delay after scroll")
    args = parser.parse_args()

    imgTester = ImageClickTester(depth=args.depth,keep=args.keep)
    imgTester.click_images()