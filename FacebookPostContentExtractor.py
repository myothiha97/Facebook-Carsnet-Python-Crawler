from utility.emoji_remover import EmojiRemover
import time

class ContentExtractor:
    @classmethod
    def get_post_time_stamp(cls,post):
        # Get Date
        timestamp = ''
        try:
            date_obj = post.find_element_by_css_selector('._5ptz')
            timestamp = date_obj.get_attribute("data-utime")
        except Exception as e:
            print("Error retrieving date " + str(e))

        return timestamp
    
    @classmethod
    def get_post_text(cls,post):
        # Post content            
        try: 
            # post_text = post.find_element_by_css_selector("div[data-ad-comet-preview='message']").get_property('textContent')
            post_text = post.find_element_by_css_selector("div[data-ad-comet-preview='message']").text
            # clean_emoji = EmojiRemover.remove_emoji(post_text)
        except Exception as e:
            print('Issue with retrieving content: ' + str(e))
            print("Target might be market place")
            try:
                post_text = post.find_element_by_css_selector("div.rq0escxv.a8c37x1j.rz4wbd8a.a8nywdso > div:nth-of-type(2)").text
            except Exception as e:
                print('Issue with retrieving content: ' + str(e))
        time.sleep(1)
        return post_text
    
    @classmethod
    def get_author_name(cls,post):
        # Author Name
        author_name = ''
        try:
            author_name = post.find_element_by_xpath("//*[contains(@id,'jsc_c')]/div/a/strong/span").get_property('innerText')         
        except Exception as e:
            print("Error retrieving author name" + str(e))
            try:
                author_name = post.find_element_by_xpath("//*[contains(@id,'jsc_c')]/span/div/a/strong/span").text
            except Exception as e:
                print("Error retrieving author name : ",str(e))
                
        return author_name