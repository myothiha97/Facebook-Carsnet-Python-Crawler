from utility.KeyBoard import KeyBoard
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import NoSuchElementException
# from selenium.common.exceptions import InvalidSessionIdException
import sys , traceback
import time

class FacebookImageExtractor():

    def extract_images_from_market_gallary(post,browser):
        images = []
        try:
            video = post.find_element_by_css_selector('div.i09qtzwb.rq0escxv.n7fi1qx3.pmk7jnqg.j9ispegn.kr520xx4.nhd2j8a9')
            print('video detected')
            return images
        except:
            try:                
                # Might be a seller group            
                image_holder = post.find_element_by_css_selector("a.tm8avpzi")
                # image_holder.click()
                browser.execute_script("arguments[0].click();", image_holder)
                # webdriver.ActionChains(browser).move_to_element(image_holder).click(image_holder).perform()

                WebDriverWait(browser, 10).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "div.du4w35lb.k4urcfbm.stjgntxs.ni8dbmo4.taijpn5t.buofh1pr.j83agx80.bp9cbjyn"))
                )
                
                count = 0
                while(count < 70):

                    try:
                        WebDriverWait(browser, 300).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.du4w35lb.k4urcfbm.stjgntxs.ni8dbmo4.taijpn5t.buofh1pr.j83agx80.bp9cbjyn")))          
                        spotlight = browser.find_element_by_css_selector("div.du4w35lb.k4urcfbm.stjgntxs.ni8dbmo4.taijpn5t.buofh1pr.j83agx80.bp9cbjyn").find_element_by_tag_name("img")

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
                        next_btn = browser.find_element_by_css_selector("div[aria-label='View next image']")
                        next_btn.click()
                        count += 1
                        
                    except Exception as ex:
                        print("Issue from ImageExtractor : "+str(ex))
                        count += 1
                        time.sleep(1)
                KeyBoard.click_esc_key(browser)
            except Exception as e:
                # No image holder or images here
                print('Issue from ImageExtractor : ',str(e))
                KeyBoard.click_esc_key(browser)
            return images


    def extract_images_from_normal_gallary(post,browser):
        # actions = ActionChains(browser)
        
        images = []
        try:
            video = post.find_element_by_css_selector('div.i09qtzwb.rq0escxv.n7fi1qx3.pmk7jnqg.j9ispegn.kr520xx4.nhd2j8a9')
            print('video detected')
            return images
        except:
            try:                
                # Try clicking on the images
                
                image_holder = post.find_element_by_css_selector("a.tm8avpzi")
                # image_holder.click()
                browser.execute_script("arguments[0].click();", image_holder)
                # webdriver.ActionChains(browser).move_to_element(image_holder).click(image_holder).perform()

                WebDriverWait(browser, 10).until(
                    EC.presence_of_element_located(
                        (By.CSS_SELECTOR, "img.ji94ytn4"))
                )
                count = 0
                while(count < 70):            
                    try:     
                        WebDriverWait(browser, 300).until(EC.presence_of_element_located((By.CSS_SELECTOR, "img.ji94ytn4")))
                        # time.sleep(0.3)
                        spotlight = browser.find_element_by_css_selector("img.ji94ytn4")

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
                        next_btn = browser.find_element_by_css_selector(
                            "div[aria-label='Next photo']")
                        next_btn.click()
                        # webdriver.ActionChains(browser).send_keys(Keys.ARROW_RIGHT).perform()
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
                            WebDriverWait(browser,60).until(EC.presence_of_element_located((By.CSS_SELECTOR, "img.ji94ytn4")))


                        # elif exc_type == InvalidSessionIdException:
                        #     KeyBoard.click_esc_key(browser)
                        #     return images
                        count += 1
                        time.sleep(0.5)
                print("******* done crawling images for post*************")
                # time.sleep(0.5)
                KeyBoard.click_esc_key(browser)
                
                    
            except Exception as e:
                # No image holder or images here
                print('Issue from ImageHolder : ' + str(e))
                KeyBoard.click_esc_key(browser)
            
            return images

    