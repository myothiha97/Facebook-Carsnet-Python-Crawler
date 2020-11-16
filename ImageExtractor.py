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
from ElementSelectors import image_holder_selector,image_paginator_selector,page_image_selector,page_next_btn_selector 
from ElementSelectors import gp_image_selector,gp_next_btn_selector
from ElementSelectors import gp_video_btn_selector , page_video_btn_selector
import sys , traceback
import time

class FacebookImageExtractor():

    def extract_images_from_market_gallary(post,browser):
        images = []
        try:                
            # Might be a seller group            
            image_holder = post.find_element_by_css_selector(image_holder_selector)
            # image_holder.click()
            # browser.execute_script("arguments[0].click();", image_holder)
            webdriver.ActionChains(browser).move_to_element(image_holder).click(image_holder).perform()

            try:
                WebDriverWait(browser, 10).until(
                EC.presence_of_element_located(
                    (By.CSS_SELECTOR, image_paginator_selector))
            )
                # Selector image paginator and retrieve all images at once. 
                images_pager = browser.find_element_by_css_selector(image_paginator_selector)
                print("Image selector found")
                image_elements = images_pager.find_elements_by_css_selector('img')
                for image in image_elements:
                    try:
                        images.append(image.get_attribute("src")) 
                    except Exception as e:
                        print(e)
            except Exception as e:
                    print("Error extracting image object")
                    print(str(e))  
            KeyBoard.click_esc_key(browser)
            
        except Exception as e:
            # No image holder or images here
            print('Issue from ImageExtractor : ',str(e))
            KeyBoard.click_esc_key(browser)
        
        print(images)
        return images


    def extract_images_from_normal_gallary(post,browser):
        # actions = ActionChains(browser)
        
        images = []
        
        try:                
            # Try clicking on the images
            
            image_holder = post.find_element_by_css_selector(image_holder_selector)
            # image_holder.click()
            browser.execute_script("arguments[0].click();", image_holder)
            # webdriver.ActionChains(browser).move_to_element(image_holder).click(image_holder).perform()

            # WebDriverWait(browser, 10).until(
            #     EC.presence_of_element_located(
            #         (By.CSS_SELECTOR, page_image_selector))
            # )
            count = 0
            while(count < 70):            
                try:     
                    # WebDriverWait(browser, 300).until(EC.presence_of_element_located((By.CSS_SELECTOR, "img.ji94ytn4")))
                    WebDriverWait(browser,300).until(
                            lambda x: x.find_element(By.CSS_SELECTOR,page_video_btn_selector + ',' + page_image_selector)
                        )
                    
                    try:
                        video_btn = browser.find_element_by_css_selector(page_video_btn_selector)
                        print("\n----------Video Detected---------")
                        next_btn = browser.find_element_by_css_selector(page_next_btn_selector)
                        next_btn.click()
                        count += 1
                        continue
                    except:
                        pass
                    # time.sleep(0.3)
                    spotlight = browser.find_element_by_css_selector(page_image_selector)

                    # print('---------------------------------')                    
                    image_url = spotlight.get_attribute("src")
                    i = 0
                    if len(images) > 0:                        
                        while image_url == images[-1] and i < 15:
                            time.sleep(0.2)
                            i+=1                            
                            image_url = spotlight.get_attribute("src")
                            print(f'the loop count of the image is {i}')
                    print(f'Successfully retrieve image ${image_url}')
                    if image_url in images:                        
                        print('This image is already retrieved')
                        count = 80
                        # hasMore = False
                    else:
                        print('Appending image into the image list')
                        images.append(image_url)

                    ## Clicking next image    
                    next_btn = browser.find_element_by_css_selector(page_next_btn_selector)
                    next_btn.click()
                    # webdriver.ActionChains(browser).send_keys(Keys.ARROW_RIGHT).perform()
                    # time.sleep(1.2)
                    count += 1
                except Exception as ex:
                    print("Issue from ImageExtractor : ",ex)                                        

                    exc_type, exc_value, exc_traceback = sys.exc_info()
                    print("error type : ",exc_type)
                    print(f"Error message ---------> {exc_value} & data type --------> {type(exc_value)} ")
                    if exc_type == ElementNotInteractableException:
                        count = 72
                    elif exc_type == NoSuchElementException:
                        # WebDriverWait(browser,60).until(EC.presence_of_element_located((By.CSS_SELECTOR, page_image_selector)))
                        try:
                            WebDriverWait(browser, 10).until(
                            EC.presence_of_element_located(
                                (By.CSS_SELECTOR, image_paginator_selector))
                        )
                            # Selector image paginator and retrieve all images at once. 
                            images_pager = browser.find_element_by_css_selector(image_paginator_selector)
                            print("Image selector found")
                            image_elements = images_pager.find_elements_by_css_selector('img')
                            for image in image_elements:
                                images.append(image.get_attribute("src")) 
                            
                            return images
                        except Exception as exc:
                            pass


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

    