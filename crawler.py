# Selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ChromeOptions

# Utils
from decouple import config
import time
import calendar
import argparse
import uuid
import re
import requests

from DigiZaayAPI import sent_to_digizaay,convert_digizaay_object
from FacebookPostAction import click_see_more_button
import json
import requests


class Crawler:
    def __init__(self, database, storage, depth, keep, filter):

        self.ids = None
        self.depth = depth
        self.delay = keep
        self.browser = webdriver.Chrome(executable_path=config('CHROMEDRIVER'))
        self.db = database
        self.storage = storage
        self.table = None
        self.filter = filter
        self.table_img = None

    def collect(self, type):
        # Create list for string of ("seameochat, facebookapp")
        objects = self.ids.strip().split(',')

        for url in objects:
            self.select_types(type, url.strip())
            if type == "search":
                self.click_store_overview_posts(url)
                time.sleep(self.delay)
            else:
                # Scroll down by depth count e.g 4
                for scroll in range(self.depth):
                    timestamp = calendar.timegm(time.gmtime())
                    # Click Esc Key to prevent browser notification
                    self.click_esc_key()

                    time.sleep(self.delay)

                    # Scrolling
                    self.browser.execute_script(
                        "window.scrollBy(0, document.body.scrollHeight)")

                    # time.sleep(self.delay)

                    # self.save_img_to_db(scroll, timestamp, url)

                self.crawl_posts()

    # Select types and return sql query for post and imges

    def select_types(self, type, url):

        # Wait till the current browser is already login and reach home page
        WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located(
                    (By.ID, "findFriendsNav"))
            )

        url_to_crawl = ""
        print(f"Type is {type}")
        if type == "page":
            url_to_crawl = 'https://www.facebook.com/pg/{}'.format(url)
            print(url_to_crawl)          

        elif type == "group":
            url_to_crawl = 'https://www.facebook.com/groups/{}/'.format(url)
            print(url_to_crawl)
            print("selecting group")

        result = self.browser.get(url_to_crawl)
        print(result)
        self.table = config('DB_NAME_GROUPS')
        self.table_img = config('DB_NAME_GROUPS_IMG')

        # elif type == "search":
        #     self.browser.get('https://www.facebook.com/search/posts/?q={}&epa=SEARCH_BOX'.format(url.strip().lower()))
        #     self.table = config('DB_NAME_SEARCHES')
        #     self.table_img = config('DB_NAME_SEARCHES_IMG')

        # elif type == "comment":
        #     pass

        print(f"Showing current url {self.browser.current_url}")

    def take_screenshot(self, count, timestamp, url):
        return self.browser.save_screenshot('./screenshots/{}_{}_{}.png'.format(count, url, timestamp))

    def click_store_overview_posts(self, url):
        overview_posts = self.browser.find_elements_by_css_selector(
            '._5bl2._401d')
        url = url.replace('/', '_')

        for count, overview_post in enumerate(overview_posts):
            timestamp = calendar.timegm(time.gmtime())

            # Click Posts
            self.browser.execute_script(
                "arguments[0].click()", overview_post)

            time.sleep(self.delay)

            # self.save_img_to_db(count, timestamp, url)

            try:
                post_text = WebDriverWait(self.browser, self.delay).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "userContent"))).text
                print(post_text)
            except:
                print("Can't import into database")
            else:
                self.db.store_post_to_db(self.table, post_text)

            # Click Esc Key
            self.click_esc_key()

    def click_esc_key(self):
        return webdriver.ActionChains(self.browser).send_keys(Keys.ESCAPE).perform()

    def click_store_comment(self, sql):
        comments = self.browser.find_elements_by_partial_link_text("View")

        for comment in comments:
            comment.send_keys(Keys.ENTER)
            text = comment.text

    def crawl_posts(self):
        posts = self.browser.find_elements_by_class_name("userContentWrapper")
        all_content = []
        for post in posts:
            all_content = []
            # Click See More Button if exist          
            click_see_more_button(post)           
          
            # Check timestamp if the page is already scanned before            
            # if(timestamp < "1576813657"):
            if(True):               
                dataObj = convert_digizaay_object(post)
                print(dataObj)
                print(dataObj.post_detail)
                if dataObj.post_detail is not '':
                    all_content.append(dataObj)
                    # sent_to_digizaay(all_content)

            # self.db.store_post_to_db(self.table,clean_emoji ,self.filter)

    def save_img_to_db(self, count, timestamp, url):
        # Store image and Get image URL from friebase
        self.take_screenshot(count, timestamp, url)
        image = self.storage.store_image_to_firebase(count, timestamp, url)

        self.db.store_imgurl_to_db(self.table_img, image)

    def login(self, email, password):
        self.browser.get("https://www.facebook.com")

        emailbox = self.browser.find_element_by_name("email")
        emailbox.clear()
        emailbox.send_keys(email)

        emailbox = self.browser.find_element_by_name("pass")
        emailbox.clear()
        emailbox.send_keys(password)

        emailbox.send_keys(Keys.ENTER)

    def close_browser(self):
        return self.browser.close()
