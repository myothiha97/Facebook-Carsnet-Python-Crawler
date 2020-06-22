from ImageExtractor import FacebookImageExtractor
from segmentation.carsnet import Entity_extractor
from FacebookPostContentExtractor import ContentExtractor
from FacebookPostAction import click_see_more_button
import json
import requests
from decouple import config
import time
class DigiZaayApiConnector():

    api_url = config('DIGIZAAY_URL')
    # token = f"Bearer {config('TOKEN')}"
    # headers = {
    #         'Content-Type': "application/json",
    #         'Accept': "*/*",
    #         'Cache-Control': "no-cache",
    #         'Host': config('DIGIZAAY_HOST'),
    #         'Accept-Encoding': "gzip, deflate",
    #         'Content-Length': "45",
    #         'Connection': "keep-alive",
    #         'cache-control': "no-cache",
    #         'Authorization':'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIyIiwianRpIjoiNzI2ZDU4NzE2OTJhMzVjNjg5NDUwMjUzYzlmMDgwOTRmN2VhMWVjZDQ5MGZhMTNhZjFmNTA4NDFmYTJhM2QzMDc4NzY5NDlkNDdhYWVkMWYiLCJpYXQiOjE1ODQ5NjExMzEsIm5iZiI6MTU4NDk2MTEzMSwiZXhwIjoxNjE2NDk3MTMxLCJzdWIiOiIxIiwic2NvcGVzIjpbXX0.VThupbO-JgoSuU_JdyaW27H3DL9yYv8SxCZn_kwkpVcUy13R0dLBPhhh9yx9wFj1zU0q9-GIO4sskdHM1QJ3EtGVh8mHged01cpLkxxQ7dz-vgEGtZUcl6u8QWelqcKUqUjPXJJFNeekTJGHHTsywGEv8pJWZ0-rt9ljfLtSE9PzOy4hWgITyooRshLMEemtwKBs-ctY-QexfVRtaqhGYNCdFZNqWO3pBJRly_sD0b-oSBdArFMqUp_IkyXIKJe4hfdoBmdIF47TU7rImEC2K1RlaMdRKiYlmOXtvw1e0YO29mBIQJfVrXKH8wxC3WWtqg_Z-sC3MWrTfNjn1UPHRF0264YBMc2sFrEp3eI35Y5gelzpC_ciPh6XUKJxvivF6cNNeXTReRZZF2gssoMo-fyneh5TXZpN3_0YJuhl7NpA43lXsTqnabkpZRCooke4ERHGtXDLuQCpLw2zsg6EZ9J0QGIHnlGNpO6aZvceo_fkZJ_E989XR4Ul-INAC-K00lAXB-cC8Evhl81YzGCTn1Lk90zMjk-KgBjQ0KdFEkMxwZE2CJf7b9UKtpuzBrq-A4TgIJLvfWsRYAUzqR470hlqUNGAdZeqGtg7fMN2zgPRame90sXZJUmbna4YEy9uq45wSJyvK8-AklY7InNjIxkmAo1HV2JkGt92Q5b_T20'
    #         # 'Authorization': f"Bearer {config('TOKEN')}"
    #     }

    headers = {
        'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIyIiwianRpIjoiNzI2ZDU4NzE2OTJhMzVjNjg5NDUwMjUzYzlmMDgwOTRmN2VhMWVjZDQ5MGZhMTNhZjFmNTA4NDFmYTJhM2QzMDc4NzY5NDlkNDdhYWVkMWYiLCJpYXQiOjE1ODQ5NjExMzEsIm5iZiI6MTU4NDk2MTEzMSwiZXhwIjoxNjE2NDk3MTMxLCJzdWIiOiIxIiwic2NvcGVzIjpbXX0.VThupbO-JgoSuU_JdyaW27H3DL9yYv8SxCZn_kwkpVcUy13R0dLBPhhh9yx9wFj1zU0q9-GIO4sskdHM1QJ3EtGVh8mHged01cpLkxxQ7dz-vgEGtZUcl6u8QWelqcKUqUjPXJJFNeekTJGHHTsywGEv8pJWZ0-rt9ljfLtSE9PzOy4hWgITyooRshLMEemtwKBs-ctY-QexfVRtaqhGYNCdFZNqWO3pBJRly_sD0b-oSBdArFMqUp_IkyXIKJe4hfdoBmdIF47TU7rImEC2K1RlaMdRKiYlmOXtvw1e0YO29mBIQJfVrXKH8wxC3WWtqg_Z-sC3MWrTfNjn1UPHRF0264YBMc2sFrEp3eI35Y5gelzpC_ciPh6XUKJxvivF6cNNeXTReRZZF2gssoMo-fyneh5TXZpN3_0YJuhl7NpA43lXsTqnabkpZRCooke4ERHGtXDLuQCpLw2zsg6EZ9J0QGIHnlGNpO6aZvceo_fkZJ_E989XR4Ul-INAC-K00lAXB-cC8Evhl81YzGCTn1Lk90zMjk-KgBjQ0KdFEkMxwZE2CJf7b9UKtpuzBrq-A4TgIJLvfWsRYAUzqR470hlqUNGAdZeqGtg7fMN2zgPRame90sXZJUmbna4YEy9uq45wSJyvK8-AklY7InNjIxkmAo1HV2JkGt92Q5b_T20'
    }

    @classmethod
    def sent_to_digizaay(self,content):

        payload = json.dumps({'crawl_posts': content})
        # print(data)
        # x = requests.post(url, data = data)

        # data = {'crawl_posts': [dataObj]})
        # print("--------------------->>> The api object<<<---------------")
        # print(payload)
        # time.sleep(60)
        headers = {
            'Content-Type': "application/json",
            'Accept': "*/*",
            'Cache-Control': "no-cache",
            'Host': config('DIGIZAAY_HOST'),
            'Accept-Encoding': "gzip, deflate",
            'Content-Length': "45",
            'Connection': "keep-alive",
            'cache-control': "no-cache",
            'Authorization': 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIyIiwianRpIjoiNzI2ZDU4NzE2OTJhMzVjNjg5NDUwMjUzYzlmMDgwOTRmN2VhMWVjZDQ5MGZhMTNhZjFmNTA4NDFmYTJhM2QzMDc4NzY5NDlkNDdhYWVkMWYiLCJpYXQiOjE1ODQ5NjExMzEsIm5iZiI6MTU4NDk2MTEzMSwiZXhwIjoxNjE2NDk3MTMxLCJzdWIiOiIxIiwic2NvcGVzIjpbXX0.VThupbO-JgoSuU_JdyaW27H3DL9yYv8SxCZn_kwkpVcUy13R0dLBPhhh9yx9wFj1zU0q9-GIO4sskdHM1QJ3EtGVh8mHged01cpLkxxQ7dz-vgEGtZUcl6u8QWelqcKUqUjPXJJFNeekTJGHHTsywGEv8pJWZ0-rt9ljfLtSE9PzOy4hWgITyooRshLMEemtwKBs-ctY-QexfVRtaqhGYNCdFZNqWO3pBJRly_sD0b-oSBdArFMqUp_IkyXIKJe4hfdoBmdIF47TU7rImEC2K1RlaMdRKiYlmOXtvw1e0YO29mBIQJfVrXKH8wxC3WWtqg_Z-sC3MWrTfNjn1UPHRF0264YBMc2sFrEp3eI35Y5gelzpC_ciPh6XUKJxvivF6cNNeXTReRZZF2gssoMo-fyneh5TXZpN3_0YJuhl7NpA43lXsTqnabkpZRCooke4ERHGtXDLuQCpLw2zsg6EZ9J0QGIHnlGNpO6aZvceo_fkZJ_E989XR4Ul-INAC-K00lAXB-cC8Evhl81YzGCTn1Lk90zMjk-KgBjQ0KdFEkMxwZE2CJf7b9UKtpuzBrq-A4TgIJLvfWsRYAUzqR470hlqUNGAdZeqGtg7fMN2zgPRame90sXZJUmbna4YEy9uq45wSJyvK8-AklY7InNjIxkmAo1HV2JkGt92Q5b_T20'
        }
        print(f'----- Triggering API request to {self.api_url} -----------')

        response = requests.request("POST", self.api_url, headers=headers, data = payload)

        print(f'>>>Return from API<<<')
        # print(response.text.encode('utf8'))
        print(f"status code ------> ",response.status_code)


    @classmethod
    def get_crawl_history_id(self,id):
        url = config('DIGIZAAY_CRAWL_HISTORY_START')
        payload = {'crawl_page_id':id,'start_at':time.strftime('%H:%M:%S')}
        crawl_history = requests.post(url,data = payload,headers=self.headers)
        print(crawl_history.text)
        json_obj =  crawl_history.json()        
        return json_obj['id']
    
    @classmethod
    def get_pages_from_api(cls,header):
        url=config('CURRENT_CRAWL_PAGES')
        pages = requests.get(url,headers = header)
        return pages

    @classmethod
    def end_crawling(self,crawl_history_id):
        url = config('DIGIZAAY_CRAWL_HISTORY_END').replace('{id}', str(crawl_history_id))
        payload = {'end_at':time.strftime('%H:%M:%S')}
        # result = requests.request("PUT", url, headers=self.headers, data = payload)
        result = requests.put(url, headers=self.headers, data = payload)
        print(f'>>>Return from API {url}<<<')
        print(result.text.encode('utf8'))

    @classmethod
    def convert_digizaay_object(self,post,browser,page_id,market_place,g_type,crawl_history_id):
        if market_place == 0 and g_type ==0:
            post_text = ContentExtractor.get_post_text(post,browser=browser)
            segments = Entity_extractor.retrieve_entity(post_text)
            images = FacebookImageExtractor.extract_images_from_normal_gallary(post,browser)
            authorname = ContentExtractor.get_author_name(post)
            
        if market_place == 1:
            post_text = ContentExtractor.get_post_text_for_gp(post,browser=browser)
            if "See more" in post_text:
                click_see_more_button(browser=browser,post=post)
                post_text = ContentExtractor.get_post_text_for_gp(post,browser=browser)
                time.sleep(0.5)
                
            segments = Entity_extractor.retrieve_entity(post_text)
            images = FacebookImageExtractor.extract_images_from_market_gallary(post,browser)
            authorname = ContentExtractor.get_author_name_for_group(post)
            
        if market_place == 0 and g_type == 1:
            post_text = ContentExtractor.get_post_text(post,browser=browser)
            if "See more" in post_text:
                click_see_more_button(browser = browser , post=post)
                post_text = ContentExtractor.get_post_text(post,browser=browser)
                time.sleep(0.5)
            segments = Entity_extractor.retrieve_entity(post_text)
            images = FacebookImageExtractor.extract_images_from_normal_gallary(post,browser)
            authorname=ContentExtractor.get_author_name_for_group(post)
        # images = 0
        if post_text == '':
            status = True
        else:
            status = False
        # time_stamps = ContentExtractor.get_post_time_stamp(post)
        # print(time_stamps)
        # print("Getting time stamp ")
        # time.sleep(60)
        dataObj = {
            'post_detail': post_text,
            'published_at': ContentExtractor.get_post_time_stamp(post),
            'author_name': authorname,
            'post_images': images,
            'segmentation': segments, 
            'comments_count': ContentExtractor.get_comment_count(post),
            'likes_count': ContentExtractor.get_like_count(post),
            'shares_count': ContentExtractor.get_share_count(post),
            'page_id': page_id,
            'crawl_history_id': crawl_history_id
        }

        return dataObj , status
