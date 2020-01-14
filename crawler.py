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
                    #self.click_see_more()

                    # Scrolling
                    self.browser.execute_script("window.scrollBy(0, document.body.scrollHeight)")

                    #time.sleep(self.delay)

                    self.save_img_to_db(scroll, timestamp, url)
                    
                self.save_post_to_db()
                    
                    
    
    # Select types and return sql query for post and imges
    def select_types(self, type, url):
        if type == "page":
            self.browser.get('https://www.facebook.com/pg/{}/posts/?ref=page_internal'.format(url))
            self.table = config('DB_NAME_PAGES')
            self.table_img = config('DB_NAME_PAGES_IMG')

        elif type == "group":
            self.browser.get('https://www.facebook.com/groups/{}/'.format(url))
            self.table = config('DB_NAME_GROUPS')
            self.table_img = config('DB_NAME_GROUPS_IMG')

        elif type == "search":
            self.browser.get(
                'https://www.facebook.com/search/posts/?q={}&epa=SEARCH_BOX'.format(url.strip().lower()))
            self.table = config('DB_NAME_SEARCHES')
            self.table_img = config('DB_NAME_SEARCHES_IMG')

        elif type == "comment":
            pass


    def take_screenshot(self, count, timestamp, url):
        return self.browser.save_screenshot('./screenshots/{}_{}_{}.png'.format(count,url, timestamp))


    def click_see_more(self):
            seemores = self.browser.find_elements_by_link_text("See more")
            for seemore in seemores:
                print("clicking a see more button")
                return seemore.send_keys(Keys.ENTER)


    def click_store_overview_posts(self, url):
            overview_posts = self.browser.find_elements_by_css_selector('._5bl2._401d')
            url = url.replace('/', '_')
            
            for count, overview_post in enumerate(overview_posts):
                timestamp = calendar.timegm(time.gmtime())
                
                # Click Posts
                self.browser.execute_script(
                            "arguments[0].click()", overview_post)
                
                time.sleep(self.delay)
                
                self.save_img_to_db(count, timestamp, url)

                try:
                    post_text = WebDriverWait(self.browser, self.delay).until(EC.presence_of_element_located((By.CLASS_NAME, "userContent"))).text
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


    def save_post_to_db(self):
         posts = self.browser.find_elements_by_class_name("userContentWrapper")
         for post in posts:
            # Click See More Button if exist
            try:
                seemore = post.find_element_by_link_text("See more")
                seemore.send_keys(Keys.ENTER)
            except:
                continue

            post_text = post.find_element_by_class_name('userContent').text  

            clean_emoji = self.remove_emoji(post_text)

            # response = requests.post(url="http://localhost:8000/api/v1/unicode-convertor", data = { 'content' : post})
            self.db.store_post_to_db(self.table,clean_emoji ,self.filter)
    
    def remove_emoji(self,string):
        emoji_pattern = re.compile("["
                            u"\U0001F600-\U0001F64F"  # emoticons
                            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                            u"\U0001F680-\U0001F6FF"  # transport & map symbols
                            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                            u"\U00002702-\U000027B0"
                            u"\U000024C2-\U0001F251"
                            "]+", flags=re.UNICODE)
        return emoji_pattern.sub(r'', string)

    def save_img_to_db(self, count, timestamp, url):
        # Store image and Get image URL from friebase
        self.take_screenshot(count,timestamp, url)
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
