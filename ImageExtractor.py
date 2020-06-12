from utility.KeyBoard import KeyBoard
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import ElementNotInteractableException
import sys , traceback
import time

class FacebookImageExtractor():

    def extract_images_from_market_gallary(post,browser):
        images = []
        try:                
            # Might be a seller group            
            image_holder = post.find_element_by_class_name(
                'mtm').find_element_by_css_selector('a._xcx')
            image_holder.click()

            WebDriverWait(browser, 2).until(
                EC.presence_of_element_located(
                    (By.ID, "marketplace-modal-dialog-title"))
            )
            
            count = 0
            while(count < 15):                       
                try:          
                    spotlight = browser.find_element_by_class_name(
                        'spotlight')

                    # print('---------------------------------')                    
                    image_url = spotlight.get_attribute("src")
                    # print(image_url)
                    if image_url in images:
                        pass
                        # print('same image already')
                        # hasMore = False
                    else:
                        images.append(image_url)                                     
                    next_btn = browser.find_element_by_css_selector(
                        '.snowliftPager.prev')
                    next_btn.click()
                    count += 1
                except Exception as ex:
                    print("Issue from ImageExtractor : "+str(ex))
                    count += 1
                    time.sleep(1)
            KeyBoard.click_esc_key(browser)
        except Exception as e:
            # No image holder or images here
            print('Issue from ImageExtractor : ' + str(e))
            KeyBoard.click_esc_key(browser)
        return images

    def extract_images_from_normal_gallary(post,browser):
        actions = ActionChains(browser)
        
        images = []
        try:                
            # Try clicking on the images
            
            image_holder = post.find_element_by_css_selector("a.tm8avpzi")
            image_holder.click()

            WebDriverWait(browser, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, "img.ji94ytn4"))
            )
            count = 0
            while(count < 20):            
                try:
                             
                    WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "img.ji94ytn4")))
                    # time.sleep(0.3)
                    spotlight = browser.find_element_by_css_selector("img.ji94ytn4")

                    # print('---------------------------------')                    
                    image_url = spotlight.get_attribute("src")
                    i = 0
                    if len(images) > 0:
                        print(f'last image url is { images[-1]}')
                        while image_url == images[-1] and i < 8:
                            time.sleep(0.2)
                            i+=1
                            print(f'image url is {image_url}')
                            image_url = spotlight.get_attribute("src")
                            print(f'the loop count of the image is {i}')
                    # print(image_url)
                    if image_url in images:
                        pass
                        # print('same image already')
                        # hasMore = False
                    else:
                        images.append(image_url)
                                                            
                    next_btn = browser.find_element_by_css_selector(
                        "div[aria-label='Next photo']")
                    next_btn.click()
                    # time.sleep(1.2)
                    # time.sleep(0.2)
                    count += 1
                except Exception as ex:
                    print("Issue from ImageExtractor : "+str(ex))
                    # print(f"Error message -------> {ex.message}")
                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    print("error type : ",exc_type)
                    print(f"Error message ---------> {exc_value} & data type --------> {type(exc_value)} ")
                    if exc_type == ElementNotInteractableException:
                        count = 22
                    count += 1
                    time.sleep(1)
            KeyBoard.click_esc_key(browser)
            
                
        except Exception as e:
            # No image holder or images here
            print('Issue from ImageHolder : ' + str(e))
            # KeyBoard.click_esc_key(browser)
        
        return images

    