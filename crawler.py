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

from DigiZaayAPI import DigiZaayApiConnector
from FacebookPostAction import click_see_more_button
from FacebookPostContentExtractor import ContentExtractor
from ImageExtractor import FacebookImageExtractor
from segmentation.carsnet import Entity_extractor
from SearchCrawlPost import crawl_search_posts

class Crawler:
    def __init__(self, database, storage, depth, keep, filter):

        self.ids = None
        self.depth = depth
        self.delay = keep
        self.browser = webdriver.Chrome(executable_path=config('CHROMEDRIVER'))
        # self.browser = webdriver.Firefox(executable_path="./drivers/geckodriver.exe")
        self.db = database
        self.storage = storage
        self.table = None
        self.filter = filter
        self.table_img = None
        self.api_connector = DigiZaayApiConnector()

    def collect(self, type):
        # Create list for string of ("seameochat, facebookapp")
        objects = self.ids.strip().split(',')
        # pages_ids = self.db.extract_page_ids_from_page()
        # print(objects)
        # time.sleep(60)
        for ids in objects:
            # self.select_types(type, url.strip())
            if type == "search":
                # objects = self.ids.strip().split(',')
                # self.click_store_overview_posts(url)
                # self.click_store_overview_posts(ids)
                txt = ids
                self.browser.get("https://www.facebook.com/CarsNET-102005471291910")
                # time.sleep(self.delay)
                WebDriverWait(self.browser,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"div[aria-label = 'Search']")))
                search_box = self.browser.find_element_by_css_selector("div[aria-label = 'Search']")
                search_box.click()
                time.sleep(1)
                webdriver.ActionChains(self.browser).send_keys(txt).perform()
                # search_box.send_keys(txt)
                webdriver.ActionChains(self.browser).send_keys(Keys.ENTER).perform()
                # time.sleep(2)

                ### change page id when crawling other page .For now page id is 1 for carsnet #####
                crawl_history_id = self.api_connector.get_crawl_history_id(1)
                time.sleep(5)
                crawl_search_posts(browser = self.browser,history_id = crawl_history_id,page_id =1 )
            else:
                self.select_types(type,ids)
                
                time.sleep(4)
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
                self.browser.execute_script("window.scrollTo(document.body.scrollHeight,0)")
                print(f"This is {type}")
                time.sleep(5)
                if type == "page":
                    print("crawling with page type")
                    self.crawl_posts()
                if type == "group":
                    # print("This is market place")
                    gp_type = self.browser.find_element_by_css_selector("div.bp9cbjyn.j83agx80.btwxx1t3.k4urcfbm > a:nth-of-type(2) > div > span").text
                    if gp_type == "Discussion":
                        print("This group is normal gp")
                        self.crawl_posts(market_place=0,g_type = 1)
                    else:
                        print("This group is market place")
                        self.crawl_posts(market_place=1)
                
            # self.save_post_to_db(page_id)
    # Select types and return sql query for post and imges

    def collect_from_api(self,ids,url,market_place):
        self.browser.get(url)
        time.sleep(4)

        crawl_history_id = self.api_connector.get_crawl_history_id(ids)
        for scroll in range(self.depth):
            timestamp = calendar.timegm(time.gmtime())
            # Click Esc Key to prevent browser notification
            self.click_esc_key()

            time.sleep(self.delay)

            # Scrolling
            self.browser.execute_script(
                "window.scrollBy(0, document.body.scrollHeight)")
        time.sleep(0.5)
        self.browser.execute_script("window.scrollTo(document.body.scrollHeight,0)")
        time.sleep(0.5)
        if market_place == 0:
            print("This is page")
            self.crawl_posts(ids,crawl_history_id=crawl_history_id)
        else:
            WebDriverWait(self.browser,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"div.bp9cbjyn.j83agx80.btwxx1t3.k4urcfbm > a:nth-of-type(2) > div > span")))
            gp_type = self.browser.find_element_by_css_selector("div.bp9cbjyn.j83agx80.btwxx1t3.k4urcfbm > a:nth-of-type(2) > div > span").text
            if gp_type == "Discussion":
                print("This group is normal gp")
                self.crawl_posts(ids,crawl_history_id=crawl_history_id,market_place=0, g_type = 1)
            else:
                print("This group is market place")
                self.crawl_posts(ids,crawl_history_id=crawl_history_id,market_place=1)
        # self.crawl_posts(ids,market_place)

    def select_types(self, type, url):

        # Wait till the current browser is already login and reach home page
        # Verify by findFrindsNav
        WebDriverWait(self.browser, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "a[aria-label='Friends']"))
            )
        # time.sleep(5)
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
        # url = url.replace('/', '_')

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

    def crawl_posts(self,ids,crawl_history_id,market_place=0,g_type=0):

        posts = self.browser.find_elements_by_css_selector("div[data-testid='Keycommand_wrapper_feed_story']")
        
       
        check_already_safe_stimestamp = False
        for g,post in enumerate(posts):
            # Click See More Button if exist          
            click_see_more_button(browser= self.browser,post = post)
            share_check = post.find_element_by_css_selector('div.pybr56ya.dati1w0a.hv4rvrfc.n851cfcs.btwxx1t3.j83agx80.ll8tlv6m > div:nth-of-type(2) > div > div:nth-of-type(1) > span').text
            if re.search(r"shared|share|Shared|Share|shares|Shares",share_check):
                print("This is a shared post")
                time.sleep(1)
                continue
          
            # Check timestamp if the page is already scanned before            
            # if(timestamp < "1576813657"):
            # if(True):
            dataObj , status = self.api_connector.convert_digizaay_object(post,browser=self.browser,page_id=ids,market_place=market_place,g_type=g_type,crawl_history_id=crawl_history_id)

            count = 0
            while status and count  < 2:               
                # print(dataObj.items())
                # time.sleep(3)
                time.sleep(0.5)
                self.click_esc_key()
                time.sleep(0.5)
                click_see_more_button(browser = self.browser,post=post)
                dataObj , status  = self.api_connector.convert_digizaay_object(post,browser=self.browser,page_id=ids,market_place=market_place,g_type=g_type,crawl_history_id=crawl_history_id)
                print("")
                print(f"--------------recrawling post {g}----------------")
                print("")
                count+=1
                
            if dataObj['post_detail'] != '':
                print(dataObj)
                all_content = []
                all_content.append(dataObj)
                print(all_content)
                self.api_connector.sent_to_digizaay(all_content)
            print(f"------------------finished crawling post {g}--------------------------")
                                
                    

            # self.db.store_post_to_db(self.table,clean_emoji ,self.filter)
        # print(all_content)
        self.api_connector.end_crawling(crawl_history_id)
        # print("The number of data  ", len(all_content))
        print("The number of posts ",len(posts))

    
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
