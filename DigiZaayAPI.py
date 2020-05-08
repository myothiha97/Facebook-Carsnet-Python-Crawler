from ImageExtractor import FacebookImageExtractor
from entity_extration.carsnet import retrieve_entity
from FacebookPostContentExtractor import get_post_time_stamp,get_post_text,get_author_name
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
    def convert_digizaay_object(self,post,browser):
        post_text = get_post_text(post)

        dataObj = {
            'post_detail': post_text,
            'published_at': get_post_time_stamp(post),
            'author_name': get_author_name(post),
            'post_images': FacebookImageExtractor.extract_images_from_normal_gallary(post,browser),
            'segmentation': retrieve_entity(post_text),
            'comments_count': 0,
            'likes_count': 0,
            'shares_count': 0,
            'page_id': 1,
            'crawl_history_id': 41
        }

        return dataObj
