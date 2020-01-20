import requests
import json

url = 'https://carsnet-staging.mm-digital-solutions.com/api/v1/crawl-data-store'
# print(content)
dataObj = {
    "post_detail": "Toyota Kluger 2001model",
    "post_url": 'https://www.facebook.com/pg/CarsNET-102005471291910/posts/?ref=page_internal',
    "published_at": '2019-11-20 14:40:00',
    "segmentation": {'make': 'toyota', 'year': '2001', 'fuel': '-', 'model': '-', 'price': '355 Lakhs', 'color': 'pearl white', 'engine': '-', 'mileage': '130000 km', 'license-initial': '-'},
    "post_image": ['https://scontent.frgn3-1.fna.fbcdn.net/v/t1.0-9/79951569_116285769863880_1664474215757119488_n.jpg?_nc_cat=102&_nc_ohc=1ESr6bYoV8QAX_10WBf&_nc_ht=scontent.frgn3-1.fna&oh=728cbc6e7fc629625b2ab88a581ab9fa&oe=5E94A89F', 'https://scontent.frgn3-1.fna.fbcdn.net/v/t1.0-9/80277897_116285803197210_3451717872647143424_n.jpg?_nc_cat=100&_nc_ohc=DiZw3KC-ilkAX_EA_65&_nc_ht=scontent.frgn3-1.fna&oh=4f072452fc7696eccc6ec108c7e52405&oe=5E8DAAEA', 'https://scontent.frgn3-1.fna.fbcdn.net/v/t1.0-9/79576762_116285839863873_1824360678362710016_n.jpg?_nc_cat=109&_nc_ohc=C8O97I9bRiEAX-CnK1z&_nc_ht=scontent.frgn3-1.fna&oh=310edd5bdaaf5ee02ffa38a2826e4bad&oe=5EDA7CF6', 'https://scontent.frgn3-1.fna.fbcdn.net/v/t1.0-9/80888052_116285909863866_436777845922988032_n.jpg?_nc_cat=109&_nc_ohc=sqTipxUx-PsAX958sD0&_nc_ht=scontent.frgn3-1.fna&oh=15122bc24cf4a2a377d42ec3117b87cd&oe=5EA01455']
}
# dataObj = ['a','b','c','d']

data = json.dumps({'crawl_posts': [dataObj]})
headers = {
    'Content-Type': "application/json",
    'Accept': "*/*",
    'Cache-Control': "no-cache",
    'Host': "carsnet-staging.mm-digital-solutions.com",
    'Accept-Encoding': "gzip, deflate",
    'Content-Length': "45",
    'Connection': "keep-alive",
    'cache-control': "no-cache"
    }
x = requests.post(url, data=data,headers=headers)
print(x)
print(x.text)