from utility.emoji_remover import EmojiRemover
import time
import re
import datetime
import sys
from selenium import webdriver
from time_extractor import get_publish_at
import csv
from ElementSelectors import *


class ContentExtractor:
    @classmethod
    def get_post_time_stamp(cls,post):
        # Get Date
        print("Retrieving post time stamp")
        try:

            date_content = post.find_element_by_css_selector(date_content_selector).get_attribute("aria-label")
            print(date_content)
            
            publish_at = get_publish_at(date_content)
            time.sleep(1)
        except:
            publish_at = ''
        # with open("Post_Dates.csv",'a') as fileobj:
        #     fieldnames = ['Raw_date','Format_date']
        #     writer = csv.DictWriter(fileobj,fieldnames=fieldnames)
        #     writer.writeheader()
        #     writer.writerow({'Raw_date': date_content,'Format_date': publish_at})
        return publish_at
    @classmethod
    def get_post_text(cls,post,browser):
        # Post content    
        post_text = ''        
        try: 
            # post_text = post.find_element_by_css_selector("div[data-ad-comet-preview='message']").get_property('textContent')
            post_text = post.find_element_by_css_selector(page_post_content_selector)
            # webdriver.ActionChains(browser).move_to_element(post_text).perform()
            post_text = post_text.text
            print('------------- retrieving text ------------------')
            print(post_text)
            # clean_emoji = EmojiRemover.remove_emoji(post_text)
        except Exception as e:
            print('Issue with retrieving content: ' + str(e))
            try:
                post_text = post.find_element_by_tag_name("blockquote")
                # webdriver.ActionChains(browser).move_to_element(post_text).perform()
                post_text = post_text.text
            except Exception as e:
                print("An error occur while trying to get blocktext ",str(e))
                post_text = ''
        time.sleep(1)
        return post_text
    
    @classmethod
    def get_post_text_for_gp(cls,post,browser):
        post_text = ''
        try:
            post_text = post.find_element_by_css_selector(group_post_content_selector)
            # webdriver.ActionChains(browser).move_to_element(post_text).perform()
            post_text = post_text.text
        except Exception as e:
            print("An error occur while trying to get post text ",str(e))
            print("try another method")
            try:
                post_text = post.find_element_by_tag_name("blockquote")
                # webdriver.ActionChains(browser).move_to_element(post_text).perform()
                post_text = post_text.text
            except Exception as e:
                print("An error occur while trying to get blocktext ",str(e))
                post_text = ''
                
        time.sleep(1)
        return post_text
                
    
    @classmethod
    def get_author_name(cls,post):
        # Author Name
        try:
            author_name = post.find_element_by_xpath(page_author_name_xpath_selector).get_property('innerText') 
            print(f"Author name ----------> {author_name}")        
        except Exception as e:
            print("Error retrieving author name" + str(e))  
            author_name = ''
        return author_name
    
    @classmethod
    def get_author_name_for_group(cls,post):
        author_name = ''
        try:
            # author_name = post.find_element_by_xpath("//*[contains(@id,'jsc_c')]/span/div/a/strong/span").get_property("innerText")
            # author_name = post.find_element_by_xpath("//h2[contains(@id,'jsc_c')]").get_property("textContent")
            author_name = post.find_element_by_css_selector(group_author_name_selector).get_property("textContent")
            if re.search("shared",author_name):
                author_name = re.sub(" shared a post.","",author_name)
            print(f"Author name --------> {author_name}")
        except Exception as e:
            print("Error retrieving author name : ",str(e))
        
        return author_name
    
    @classmethod
    def get_share_count(cls,post):
        try:
            shares = post.find_element_by_css_selector(share_count_selector_1).get_property("textContent")
            if re.search(r"share|shares",shares) == None:
                shares = post.find_element_by_css_selector(share_count_selector_2).get_property("textContent")
            
            print("raw shares text ------> ",shares)
            reg = r"\d+|\d+\.\d+"
            if re.search(r"k|K",shares):
                share = re.search(reg,shares).group()
                share_count = int(float(share) * 1000)
            else:
                share_count = re.search(reg,shares).group()
        except Exception as e:
            print("An error occur while trying to get share_count ",str(e))
            # print("raw share count ------> ", shares)
            share_count = 0
            
        print("share count ----------> ",share_count)
        time.sleep(0.5)
        return int(share_count)
    
    @classmethod
    def get_like_count(cls,post):
        try:
            likes=post.find_element_by_css_selector(like_count_selector).get_attribute("innerText")
            print("raw like string *******  ",likes)
            reg = r"\d+|\d+\.\d+"
            if re.search(r"k|K",likes):
                like = re.search(reg,likes).group()
                like_count = int(float(like) * 1000)
            else:
                like_count = re.search(reg,likes).group()
        except Exception as e:
            print("An error occur while trying to get like_count ",str(e))
            like_count = 0
        # like_count = re.search(reg,likes).group()
        # if likes == None:
        #     like_count =0
        time.sleep(0.5)
        print("like counts ------------> ",like_count)
        return int(like_count)
    
    @classmethod
    def get_comment_count(cls,post):
        try:
            comments = post.find_element_by_css_selector(cmt_count_selector).get_property("textContent")
            if "shares" in comments or 'share' in comments:
                comment_count = 0
                print("comment count ----------> ",comment_count)
                return comment_count
            # print("raw comments ----------------> ",comments)
            reg = r"\d+|\d+\.\d+"
            if re.search(r"k|K",comments):
                comment = re.search(reg,comments).group()
                comment_count = int(float(comment) * 1000)
            else:
                comment_count = re.search(reg,comments).group()
        except Exception as e:
            print("An error occur while trying to get comment_count ",str(e))
            comment_count = 0
            time.sleep(0.5)
        print("comment counts --------------> ",comment_count)
        return int(comment_count)
            
            