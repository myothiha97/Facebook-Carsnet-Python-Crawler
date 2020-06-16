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
    token = f"Bearer {config('TOKEN')}"

    @classmethod
    def sent_to_digizaay(self,content):
        
        data = json.dumps({'crawl_posts': content})
        print(data)
        # print(data)
        # x = requests.post(url, data = data)

        # data = {'crawl_posts': [dataObj]})
        headers = {
            'Content-Type': "application/json",
            'Accept': "*/*",
            'Cache-Control': "no-cache",
            'Host': config('DIGIZAAY_HOST'),
            'Accept-Encoding': "gzip, deflate",
            'Content-Length': "45",
            'Connection': "keep-alive",
            'cache-control': "no-cache",
            'Authorization': self.token
        }
        print(self.api_url)

        x = requests.post(self.api_url, data=data, headers=headers)
        # print(x)
        print(x.text)

    @classmethod
    def convert_digizaay_object(self,post,browser,page_id,market_place,g_type):
        if market_place == 0 and g_type ==0:
            post_text = ContentExtractor.get_post_text(post)
            segments = Entity_extractor.retrieve_entity(post_text)
            images = FacebookImageExtractor.extract_images_from_normal_gallary(post,browser)
            authorname = ContentExtractor.get_author_name(post)
            
        if market_place == 1:
            post_text = ContentExtractor.get_post_text_for_gp(post)
            if "See more" in post_text:
                click_see_more_button(post)
                post_text = ContentExtractor.get_post_text_for_gp(post)
                time.sleep(0.5)
                
            segments = Entity_extractor.retrieve_entity(post_text)
            images = FacebookImageExtractor.extract_images_from_market_gallary(post,browser)
            authorname = ContentExtractor.get_author_name_for_group(post)
            
        if market_place == 0 and g_type == 1:
            post_text = ContentExtractor.get_post_text(post)
            if "See more" in post_text:
                click_see_more_button(post)
                post_text = ContentExtractor.get_post_text(post)
                time.sleep(0.5)
            segments = Entity_extractor.retrieve_entity(post_text)
            images = FacebookImageExtractor.extract_images_from_normal_gallary(post,browser)
            authorname=ContentExtractor.get_author_name_for_group(post)
        # images = 0
        if post_text == '':
            status = True
        else:
            status = False
        time_stamps = ContentExtractor.get_post_time_stamp(post)
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
            'crawl_history_id': 41
        }

        return dataObj , status
