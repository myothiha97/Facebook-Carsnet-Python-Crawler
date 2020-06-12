from ImageExtractor import FacebookImageExtractor
from segmentation.carsnet import Entity_extractor
from FacebookPostContentExtractor import ContentExtractor
import json
import requests
from decouple import config

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
    def convert_digizaay_object(self,post,browser,page_id,market_place):
        post_text = ContentExtractor.get_post_text(post)
        # print(post_text)
        # print("post text for segementation ----------> ")
        segments = Entity_extractor.retrieve_entity(post_text)
        authorname = ContentExtractor.get_author_name(post)
        
        if market_place == 0:
            images = FacebookImageExtractor.extract_images_from_normal_gallary(post,browser)
        else:
            images = FacebookImageExtractor.extract_images_from_market_gallary(post,browser)
        dataObj = {
            'post_detail': post_text,
            'published_at': ContentExtractor.get_post_time_stamp(post),
            'author_name': authorname,
            'post_images': images,
            'segmentation': segments, 
            'comments_count': 0,
            'likes_count': 0,
            'shares_count': 0,
            'page_id': page_id,
            'crawl_history_id': 41
        }

        return dataObj
