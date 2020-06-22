from utility.emoji_remover import EmojiRemover
import time
import re
import datetime
import sys
from selenium import webdriver
class ContentExtractor:
    @classmethod
    def get_post_time_stamp(cls,post):
        # Get Date
        timestamp = ''
        try:
            date_content = post.find_element_by_css_selector("span[id*='jsc']  > span:nth-of-type(2) > span > a > span").get_attribute("innerText")
            # print("date_content -------> ",date_content)
            # time.sleep(60)
            if re.search(r"hr|hrs|min|mins",date_content):
                if re.search(r"\d+\s*hrs|\d+\s*hr",date_content):
                    time_diff = re.search(r"\d+",date_content).group()
                    dateobj = datetime.datetime.now() - datetime.timedelta(hours=int(time_diff))
                    hr = dateobj.strftime("%H")
                    # hr = int(time.strftime("%H")) - int(time_diff)
                    # date = datetime.date.today()
                    yr,month,day = dateobj.strftime(r"%Y-%m-%d").split("-")
                    # yr = date.strftime("%Y")
                    # day = date.strftime(r"%d")
                    timestamp = f"{yr}-{month}-{day} {hr}:00:00"
                    print("timestamp -----------------> ",timestamp)
                    time.sleep(1)
                    return timestamp
                
                if re.search(r"\d+\s*mins|\d+\s*min",date_content):
                    # hr=time.strftime("%H")
                    mins = re.search(r"\d+",date_content).group()
                    dateobj = datetime.datetime.now() - datetime.timedelta(minutes=int(mins))
                    hr = dateobj.strftime("%H")
                    mins = dateobj.strftime("%M")
                    # date = datetime.date.today()
                    yr,month,day = dateobj.strftime(r"%Y-%m-%d").split("-")
                    # yr = date.strftime("%Y")
                    # day = date.strftime(r"%d")
                    if len(mins) == 1:
                        mins = "0"+mins
                    timestamp = f"{yr}-{month}-{day} {hr}:{mins}:00"
                    print("timestamp -----------------> ",timestamp)
                    time.sleep(1)
                    return timestamp
            else:
                date_content = post.find_element_by_css_selector("span[id*='jsc'] > span:nth-of-type(2) > span > a > span").get_attribute("innerText")
                month_reg = r"\d*\s*January\s*\d*|\d*\s*February\s*\d*|\d*\s*March\s*\d*|\d*\s*April\s*\d*|\d*\s*May\s*\d*|\d*\s*June\s*\d*|\d*\s*July\s*\d*|\d*\s*August\s*\d*|\d*\s*September\s*\d*|\d*\s*October\s*\d*|\d*\s*November\s*\d*|\d*\s*December\s*\d*"
                year_reg = r"[1][9][0-9][0-9]|[2][0][0-9][0-9]"
                # print("-------------------date content-----------------------")
                # print(date_content)
                # time.sleep(60)
                if re.search("Yesterday|yesterday" , date_content):
                    dateobj = datetime.datetime.strftime(datetime.datetime.now()- datetime.timedelta(1),r"%Y-%m-%d")
                    year , month , day = dateobj.split("-")
                    hr = re.search(r"\d+",date_content).group()
                    mins = re.search(r":\d+",date_content).group()
                    mins = re.sub(r":","",mins)
                    timestamp = f"{year}-{month}-{day} {hr}:{mins}:00"
                    print("timestamp ---------------------> ",timestamp)
                    return timestamp

                if re.search(month_reg,date_content):
                    day = re.search(r"\d+",re.search(month_reg,date_content).group()).group()
                    month_name = re.sub(r"\d+","",re.search(month_reg,date_content).group())
                    month_name = month_name.strip()
                    date_obj = datetime.datetime.strptime(month_name,"%B")
                    month = date_obj.month

                if re.search(year_reg,date_content):
                    year = re.search(year_reg,date_content).group()
                else:
                    year = datetime.date.today().strftime("%Y")

                if re.search(r"\d+:\d+\s*A*M*|\d+:\d+\s*P*M*",date_content):
                    hr = re.search(r"\d+|\d+",re.search(r"\d+:\d+\s*A*M*|\d+:\d+\s*P*M*",date_content).group()).group()
                    mins = re.search(r":\d+",date_content).group()
                    mins = re.sub(r":","",mins)
                    if re.search(r"AM|PM",date_content):
                        am_pm = re.search(r"AM|PM",date_content).group()
                        if am_pm == "PM":
                            hr = int(hr) + 12
                timestamp = f"{year}-{month}-{day} {hr}:{mins}:00"
                print("\n")
                print("timestamp --------------------> ",timestamp)
                time.sleep(1)
                return timestamp
        except Exception as e:
            print("Error retrieving date : " + str(e))
            error_info = sys.exc_info()[2]  
            print("Error line number : ",error_info.tb_lineno)
            # time.sleep(60)
            return timestamp
        return timestamp
    @classmethod
    def get_post_text(cls,post,browser):
        # Post content    
        post_text = ''        
        try: 
            # post_text = post.find_element_by_css_selector("div[data-ad-comet-preview='message']").get_property('textContent')
            post_text = post.find_element_by_css_selector("div[data-ad-comet-preview='message']")
            webdriver.ActionChains(browser).move_to_element(post_text).perform()
            post_text = post_text.text
            print('------------- retrieving text ------------------')
            print(post_text)
            # clean_emoji = EmojiRemover.remove_emoji(post_text)
        except Exception as e:
            print('Issue with retrieving content: ' + str(e))
            try:
                post_text = post.find_element_by_tag_name("blockquote")
                webdriver.ActionChains(browser).move_to_element(post_text).perform()
                post_text = post_text.text
            except Exception as e:
                print("An error occur while trying to get blocktext ",str(e))
        time.sleep(1)
        return post_text
    
    @classmethod
    def get_post_text_for_gp(cls,post,browser):
        post_text = ''
        try:
            post_text = post.find_element_by_css_selector("div.rq0escxv.a8c37x1j.rz4wbd8a.a8nywdso > div:nth-of-type(2)")
            webdriver.ActionChains(browser).move_to_element(post_text).perform()
            post_text = post_text.text
        except Exception as e:
            print("An error occur while trying to get post text ",str(e))
            print("try another method")
            try:
                post_text = post.find_element_by_tag_name("blockquote")
                webdriver.ActionChains(browser).move_to_element(post_text).perform()
                post_text = post_text.text
            except Exception as e:
                print("An error occur while trying to get blocktext ",str(e))
        return post_text
                
    
    @classmethod
    def get_author_name(cls,post):
        # Author Name
        try:
            author_name = post.find_element_by_xpath("//*[contains(@id,'jsc_c')]/div/a/strong/span").get_property('innerText') 
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
            author_name = post.find_element_by_css_selector("h2.gmql0nx0.l94mrbxd.p1ri9a11.lzcic4wl.aahdfvyu.hzawbc8m").get_property("textContent")
            if re.search("shared",author_name):
                author_name = re.sub(" shared a post.","",author_name)
            print(f"Author name --------> {author_name}")
        except Exception as e:
            print("Error retrieving author name : ",str(e))
        
        return author_name
    
    @classmethod
    def get_share_count(cls,post):
        try:
            shares = post.find_element_by_css_selector("div.bp9cbjyn.j83agx80.pfnyh3mw.p1ueia1e > div:nth-of-type(1)").get_property("textContent")
            if re.search(r"share|shares",shares) == None:
                shares = post.find_element_by_css_selector("div.bp9cbjyn.j83agx80.pfnyh3mw.p1ueia1e > div:nth-of-type(2)").get_property("textContent")
            
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
            likes=post.find_element_by_css_selector("span.gpro0wi8.cwj9ozl2.bzsjyuwj.ja2t1vim > span > span").get_attribute("innerText")
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
            comments = post.find_element_by_css_selector("div.bp9cbjyn.j83agx80.pfnyh3mw.p1ueia1e > div:nth-of-type(1)").get_property("textContent")
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
            
            