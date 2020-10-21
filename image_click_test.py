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
        self.browser.get('https://www.facebook.com/groups/643021239182864/')
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
                print("------>Total Images<--------")
                print(images)
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
            images = []
            try:
                video = post.find_element_by_css_selector('div.i09qtzwb.rq0escxv.n7fi1qx3.pmk7jnqg.j9ispegn.kr520xx4.nhd2j8a9')
                posts_images.append(images)
                continue
            except:
                try:                
                    # Might be a seller group            
                    image_holder = post.find_element_by_css_selector("a.tm8avpzi")
                    # image_holder.click()
                    self.browser.execute_script("arguments[0].click();", image_holder)
                    # webdriver.ActionChains(self.browser).move_to_element(image_holder).click(image_holder).perform()

                    WebDriverWait(self.browser, 10).until(
                        EC.presence_of_element_located(
                            (By.CSS_SELECTOR, "div.du4w35lb.k4urcfbm.stjgntxs.ni8dbmo4.taijpn5t.buofh1pr.j83agx80.bp9cbjyn"))
                    )
                    
                    count = 0
                    while(count < 70):

                        try:
                            WebDriverWait(self.browser, 300).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.du4w35lb.k4urcfbm.stjgntxs.ni8dbmo4.taijpn5t.buofh1pr.j83agx80.bp9cbjyn")))          
                            spotlight = self.browser.find_element_by_css_selector("div.du4w35lb.k4urcfbm.stjgntxs.ni8dbmo4.taijpn5t.buofh1pr.j83agx80.bp9cbjyn").find_element_by_tag_name("img")

                            # print('---------------------------------')                    
                            image_url = spotlight.get_attribute("src")
                            i = 0
                            
                            if len(images) > 0:
                                print(f'last image url is { images[-1]}')
                                while image_url == images[-1] and i < 30:
                                    time.sleep(0.2)
                                    i+=1
                                    print(f'image url is {image_url}')
                                    image_url = spotlight.get_attribute("src")
                                    print(f'the loop count of the image is {i}')
                                    
                                if image_url == images[0]:
                                    print("the image is already crawled")
                                    count = 72
                                    # continue
                                    
                            # print(image_url)
                            if image_url in images:
                                pass
                                # print('same image already')
                                # hasMore = False
                            else:
                                images.append(image_url)                                     
                            next_btn = self.browser.find_element_by_css_selector("div[aria-label='View next image']")
                            next_btn.click()
                            count += 1
                            
                        except Exception as ex:
                            print("Issue from ImageExtractor : "+str(ex))
                            count += 1
                            time.sleep(1)
                    KeyBoard.click_esc_key(self.browser)
                except Exception as e:
                    # No image holder or images here
                    print('Issue from ImageExtractor : ',str(e))
                    KeyBoard.click_esc_key(self.browser)
                posts_images.append(images)
                time.sleep(1)

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
                    # continue
            except Exception as e:
                print(f'Share check failed')
                print(e)
                continue
            images = []
            try:
                video = post.find_element_by_css_selector('div.i09qtzwb.rq0escxv.n7fi1qx3.pmk7jnqg.j9ispegn.kr520xx4.nhd2j8a9')
                posts_images.append(images)
                print("Video Detected")
                continue
            except:
                try:                
                    # Try clicking on the images
                    
                    image_holder = post.find_element_by_css_selector("a.tm8avpzi")
                    # image_holder.click()
                    self.browser.execute_script("arguments[0].click();", image_holder)
                    # webdriver.ActionChains(self.browser).move_to_element(image_holder).click(image_holder).perform()

                    WebDriverWait(self.browser, 10).until(
                        EC.presence_of_element_located(
                            (By.CSS_SELECTOR, "img.ji94ytn4"))
                    )
                    count = 0
                    while(count < 70):            
                        try:     
                            WebDriverWait(self.browser, 300).until(EC.presence_of_element_located((By.CSS_SELECTOR, "img.ji94ytn4")))
                            # time.sleep(0.3)
                            spotlight = self.browser.find_element_by_css_selector("img.ji94ytn4")

                            # print('---------------------------------')                    
                            image_url = spotlight.get_attribute("src")
                            i = 0
                            if len(images) > 0:                        
                                while image_url == images[-1] and i < 30:
                                    time.sleep(0.2)
                                    i+=1                            
                                    image_url = spotlight.get_attribute("src")
                                    print(f'the loop count of the image is {i}')
                            print(f'Successfully retrieve image ${image_url}')
                            if image_url in images:                        
                                print('This image is already retrieved')
                                # hasMore = False
                            else:
                                print('Appending image into the image list')
                                images.append(image_url)

                            ## Clicking next image    
                            next_btn = self.browser.find_element_by_css_selector(
                                "div[aria-label='Next photo']")
                            next_btn.click()
                            # webdriver.ActionChains(self.browser).send_keys(Keys.ARROW_RIGHT).perform()
                            # time.sleep(1.2)
                            count += 1
                        except Exception as ex:
                            print("Issue from ImageExtractor : ")
                            
                            exc_type, exc_value, exc_traceback = sys.exc_info()
                            print("error type : ",exc_type)
                            print(f"Error message ---------> {exc_value} & data type --------> {type(exc_value)} ")
                            if exc_type == ElementNotInteractableException:
                                count = 72
                            elif exc_type == NoSuchElementException:
                                WebDriverWait(self.browser,60).until(EC.presence_of_element_located((By.CSS_SELECTOR, "img.ji94ytn4")))

                            # elif exc_type == InvalidSessionIdException:
                            #     KeyBoard.click_esc_key(self.browser)
                            #     return images
                            count += 1
                            time.sleep(0.5)
                    print("******* done crawling images for post*************")
                    # time.sleep(0.5)
                    KeyBoard.click_esc_key(self.browser)
                    
                        
                except Exception as e:
                    # No image holder or images here
                    print('Issue from ImageHolder : ' + str(e))
                    KeyBoard.click_esc_key(self.browser)
                
                posts_images.append(images)
                time.sleep(1)

    
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