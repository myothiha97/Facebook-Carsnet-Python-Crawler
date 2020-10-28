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
from FacebookPostAction import share_check
from ElementSelectors import post_no_selector,gp_type_check_selector2

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
        self.browser.get('https://www.facebook.com/groups/1640172876271325/')
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
                (By.CSS_SELECTOR, gp_type_check_selector2)))
            gp_type = self.browser.find_element_by_css_selector(gp_type_check_selector2).text

            if gp_type == "Discussion":
                print("This group is normal gp")
                images = self.click_normal_gallery()
            else:
                print("This group is market place")
                images = self.click_market_gallery()
            
            print("------>Total Images<--------")
            print(images)
        
    def click_market_gallery(self):
        posts = self.browser.find_elements_by_css_selector(post_no_selector)
        print('posts --> ',len(posts))
        posts_images = [] ### two dimensional array
        for post in posts:
            self.browser.execute_script(
                    "arguments[0].scrollIntoView();", post)
            time.sleep(1)
            is_share_post = share_check(browser=self.browser,post=post)
            if is_share_post: ### if post is share post , we skipped
                continue
            images = FacebookImageExtractor.extract_images_from_market_gallary(post=post,browser= self.browser)
            posts_images.append(images)
        return posts_images

    def click_normal_gallery(self):
        posts = self.browser.find_elements_by_css_selector(post_no_selector)
        print('posts --> ',len(posts))
        posts_images = [] ### two dimensional array
        for post in posts:
            self.browser.execute_script(
                    "arguments[0].scrollIntoView();", post)
            time.sleep(1)
            is_share_post = share_check(browser=self.browser,post=post)
            if is_share_post: ### if post is share post , we skipped
                continue
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