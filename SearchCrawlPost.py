from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ChromeOptions
import time
import re
from DigiZaayAPI import DigiZaayApiConnector
from FacebookPostAction import click_see_more_button
from FacebookPostContentExtractor import ContentExtractor
from ImageExtractor import FacebookImageExtractor
from segmentation.carsnet import Entity_extractor


def crawl_search_posts(browser, history_id, page_id):

    search_url = str(browser.current_url)
    try:
        posts = browser.find_elements_by_css_selector(
            "div.jb3vyjys.hv4rvrfc.ihqw7lf3.dati1w0a > a")

        time.sleep(1)
        crawl_post_url = []
        for post in posts:
            post_url = post.get_attribute("href")
            crawl_post_url.append(post_url)

        if len(posts) == 0:
            print("No search result")

        print("len posts ---------> ", len(posts))
        print("len urls ---------> ", len(crawl_post_url))
        for url in crawl_post_url:
            # WebDriverWait(browser,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"div.jb3vyjys.hv4rvrfc.ihqw7lf3.dati1w0a > a")))
            # time.sleep(10)
            browser.get(url)

            # browser.get(post_url)
            WebDriverWait(browser, 10).until(EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div[aria-posinset]")))
            # self.click_esc_key()
            # time.sleep(3)
            try:
                crawl_post = browser.find_element_by_css_selector(
                    "div[aria-posinset]")
                post_date = ContentExtractor.get_post_time_stamp(crawl_post)
                share_check = crawl_post.find_element_by_css_selector(
                    'div.pybr56ya.dati1w0a.hv4rvrfc.n851cfcs.btwxx1t3.j83agx80.ll8tlv6m > div:nth-of-type(2) > div > div:nth-of-type(1) > span').text
                if re.search(r"shared|share|Shared|Share|shares|Shares", share_check):
                    print("This is a shared post")
                    time.sleep(1)
                    # browser.get(search_url)
                    # WebDriverWait(browser,10).until(EC.presence_of_element_located((By.CSS_SELECTOR,"div.jb3vyjys.hv4rvrfc.ihqw7lf3.dati1w0a > a")))
                    continue
                else:
                    print("This is not a share post")
                print(crawl_post)
                # time.sleep(5)
                WebDriverWait(browser, 10).until(EC.presence_of_element_located(
                    (By.XPATH, "//div[contains(text(),'See more')]")))

                click_see_more_button(browser=browser, post=crawl_post, type=0)
                # data_obj , status = self.api_connector.convert_digizaay_object(crawl_post,browser=browser,page_id=None,market_place=0,g_type=0)
                post_texts = ContentExtractor.get_post_text(
                    crawl_post, browser=browser)
                if "See more" in post_texts:
                    try:
                        crawl_post.find_element_by_xpath(
                            "//div[contains(text(),'See more')]").send_keys(Keys.ENTER)
                        post_texts = ContentExtractor.get_post_text(
                            crawl_post, browser=browser)
                    except Exception as e:
                        print(
                            "An error occur while retrying to click see_more ", str(e))
                segments = Entity_extractor.retrieve_entity(post_texts)
                print(post_texts)
                post_images = FacebookImageExtractor.extract_images_from_normal_gallary(
                    browser=browser, post=crawl_post)
                if post_texts == '':
                    count = 0
                    while post_texts != '' and count < 2:
                        # print(dataObj.items())
                        # time.sleep(3)
                        time.sleep(0.5)
                        # self.click_esc_key()
                        webdriver.ActionChains(browser).send_keys(
                            Keys.ESCAPE).perform()
                        time.sleep(0.5)
                        click_see_more_button(browser=browser, post=crawl_post)
                        # dataObj , status  = self.api_connector.convert_digizaay_object(post,browser=browser,page_id=None,market_place=0,g_type=0)
                        post_texts = ContentExtractor.get_post_text(
                            crawl_post, browser=browser)
                        print("")
                        print(f"--------------recrawling post----------------")
                        print("")
                        count += 1
                # if data_obj['post_detail'] is not '':
                #     all_content.append(data_obj)
                print(
                    f"------------------finished crawling post--------------------------")

                dataobj = {
                    "post_detail": post_texts,
                    "published_at": post_date,
                    "author_name": None,
                    "post_images": post_images,
                    "segmentation": segments,
                    "comments_count": 0,
                    "likes_count": 0,
                    "shares_count": 0,
                    "page_id": page_id,
                    "crawl_history_id": history_id
                }
                print(post_images)
                for image_url in post_images:
                    print(image_url)
                    
                if dataobj['post_detail'] != '':
                    all_content = []
                    all_content.append(dataobj)
                    # print(all_content)
                # print(all_content)
                # DigiZaayApiConnector.sent_to_carsnet(all_content)
                time.sleep(3)
            except Exception as e:
                print(
                    f"An erro occur while trying to get post content : {str(e)}")

        # DigiZaayApiConnector.end_crawling(crawl_history_id = history_id)

    except Exception as e:
        print("An error occur while finding search post : ", str(e))
