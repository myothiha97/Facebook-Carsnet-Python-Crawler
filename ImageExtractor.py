def extract_images_from_market_gallary(self,post):
    images = []
    try:                
        # Might be a seller group            
        image_holder = post.find_element_by_class_name(
            'mtm').find_element_by_css_selector('a._xcx')
        image_holder.click()

        WebDriverWait(self.browser, 2).until(
            EC.presence_of_element_located(
                (By.ID, "marketplace-modal-dialog-title"))
        )
        
        count = 0
        while(count < 15):                       
            try:          
                spotlight = self.browser.find_element_by_class_name(
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
                next_btn = self.browser.find_element_by_css_selector(
                    '.snowliftPager.prev')
                next_btn.click()
                count += 1
            except Exception as ex:
                print("Issue retrieving image"+str(ex))
                count += 1
                time.sleep(1)
        self.click_esc_key()
    except Exception as e:
        # No image holder or images here
        print('Issue retrieving the images: ' + str(e))
        self.click_esc_key()
    return images

def extract_images_from_normal_gallary(self,post):
    images = []
    try:                
        # Try clicking on the images
        image_holder = post.find_element_by_class_name(
            'mtm').find_element_by_css_selector('a[rel="theater"]')
        image_holder.click()

        WebDriverWait(self.browser, 2).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "spotlight"))
        )

        
        
        count = 0
        while(count < 15):                       
            try:          
                spotlight = self.browser.find_element_by_class_name(
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
                next_btn = self.browser.find_element_by_css_selector(
                    '.snowliftPager.prev')
                next_btn.click()
                count += 1
            except Exception as ex:
                print("Issue retrieving image"+str(ex))
                count += 1
                time.sleep(1)
        self.click_esc_key()
        
            
    except Exception as e:
        # No image holder or images here
        print('Issue retrieving the images: ' + str(e))
        self.click_esc_key()
    
    return images