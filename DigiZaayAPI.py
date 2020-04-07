from ImageExtractor import extract_images_from_normal_gallary, extract_images_from_market_gallary
from entity_extraction import retrieve_entity
from FacebookPostContentExtractor import get_post_time_stamp,get_post_text,get_author_name


def sent_to_digizaay(self, content):
    url = config('DIGIZAAY_URL')
    # print(content)
    data = json.dumps({'crawl_posts': content})
    print(data)
    # print(data)
    # x = requests.post(url, data = data)

    # data = {'crawl_posts': [dataObj]})
    token = f"Bearer {config('TOKEN')}"
    headers = {
        'Content-Type': "application/json",
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Host': config('DIGIZAAY_HOST'),
        'Accept-Encoding': "gzip, deflate",
        'Content-Length': "45",
        'Connection': "keep-alive",
        'cache-control': "no-cache",
        'Authorization': token
    }
    x = requests.post(url, data=data, headers=headers)
    # print(x)
    print(x.text)


def convert_digizaay_object(self, post):
    post_text = get_post_text(post)

    dataObj = {
        'post_detail': post_text,
        'published_at': get_post_time_stamp(post),
        'author_name': get_author_name(author_name),
        'post_images': extract_images_from_normal_gallary(post),
        'segmentation': retrieve_entity(post_text),
        'comments_count': 0,
        'likes_count': 0,
        'shares_count': 0,
        'page_id': 3,
        'crawl_history_id': 31
    }

    return dataObj
