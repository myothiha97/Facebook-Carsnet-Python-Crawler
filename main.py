import argparse
from decouple import config
# from db_handler import DBHandler
# from firebase import FirebaseHandler
from crawler import Crawler
import requests
import mysql.connector
from mysql.connector import Error
import time
import datetime

token =  'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIyIiwianRpIjoiYzViNTM2ZjYwYmJkNmUzODE5OTY1NDU5Y2NhMDdkYWZkZWZmOGNhYzFmMWFlM2M4ZjM0NDNlNTliNmRkNjNhOWY5M2RlYjZlOWE3M2RkOWYiLCJpYXQiOjE1ODI4Nzc5NzIsIm5iZiI6MTU4Mjg3Nzk3MiwiZXhwIjoxNjE0NTAwMzcyLCJzdWIiOiIxIiwic2NvcGVzIjpbXX0.LO3h9dmRO3avdr0Xie6qju2SBYoN8Js283pRW2ajm1NGZeMRGB9mVBP0w6v7H4pkrvx1eAF0CFyFpEwWf5WF9FbEGbvBFMuVsYYfEQluAMYykPmR7RynXhBi_TVj7o2h7ZKK4RKCMqUdMD9R2S6K_ebtE0sfPn-Dh08pxwjYgx4ecpYImt0P6gfvhPON9tGzWrxd_GLeZ0Oqs5012v13gL1BKk45_op1_rovDG3o18eLk5ASYh38dkgT1My8zxN9Ommuz1EhDlwD0FcI_w6d1OYV0qprsxpvUUUT33tWeOhkC5Y1mViGGyPdQW3y08VGrUIaVGsPu6BpFx1whhDeDryTFY9FBv7dX3yhiz0mX51Tc5iOeIjXmy127PRBAzeYysHMG1I3WrE6It_LJ4r2BdVrLFfQc1zdNxC-KAy3CdwhHYsIYL9aGlSv2VPrXDRnNujF5nprZSTMbbgEbXW6ahAte2AyC6kFmfcl-Q-E2a7tCk_jMmo6lqiNR1RGhQjs-7j1SuNxvcVVm9mXO8z-L_k6Fh34SxkPD4_UR_EtGWV4XPpIEhxHJGzVfKR72LAgayfc5dnTZowKs2xMTsfAQLDLljuDmeDzgE1MIj1zgt9cQVQ9z5UUzfUiVQDMUW33uxQ07fasjFsGiGg9uQA6v_zO0epZ8c_Xl0bWbDGcNF0'
headers = {
            'Content-Type': "application/json",
            'Accept': "*/*",
            'Cache-Control': "no-cache",
            'Host': 'crawler-dev.digi-zaay.com.mm',
            'Accept-Encoding': "gzip, deflate",
            # 'Content-Length': "45",
            'Connection': "keep-alive",
            'cache-control': "no-cache",
            'Authorization':token
        }
# DATABASE = DBHandler()
# STORAGE = FirebaseHandler()

# Get Default types from db_handler
PAGES, GROUPS, SEARCHES = None , None , None
# PAGES, GROUPS, SEARCHES = DATABASE.select_defaults()

parser = argparse.ArgumentParser(description="Facebook Crawler for pages, groups and searches")

parser.add_argument("-p", "--page", type=str, action="store", nargs="?", metavar="",  const=PAGES, help="Pages You want to crawl")

parser.add_argument("-g", "--group", type=str,  action="store", nargs="?", metavar="",  const=GROUPS, help="Groups You want to crawl")

parser.add_argument("-s", "--search", type=str,  action="store", nargs="?", metavar="",  const=SEARCHES, help="Search posts you want to crawl")


# parser.add_argument("-c", "--comment", type=bool, default=False,  metavar="", help="Comments included")

parser.add_argument("-d", "--depth", type=int, default=5, metavar="", help="Numbers of scroll")

parser.add_argument("-k", "--keep", type=int, default=5, metavar="", help="Seconds you want to delay after scroll")

parser.add_argument("-f", "--filter",  action="store_true", help="With or without keyword filter")


parser.add_argument("-C","--crawl",action="store_true",help="Use this command to crawl pages/groups from api")

parser.add_argument("-t","--test_crawl",action="store_true" , help="for crawl testing ")

args = parser.parse_args()
   

if __name__ == '__main__':
    # Initializer Crawler
    p = Crawler(database=None, storage=None, depth=args.depth, keep=args.keep,filter=args.filter)

    setattr(p, 'depth', args.depth)
    setattr(p, 'delay', args.keep)

    # Login into Facebook Account
    p.login(config('EMAIL'), config('PASSWORD'))
    time.sleep(5)

    if args.page:
        # set attribute for argument parameters eg. ("seameochat, facebookapp")
        setattr(p, 'ids', args.page)

        # set type for page
        start_time = time.strftime("%H:%M:%S")
        print(f"start_time --> {start_time}")
        time.sleep(2)
        p.collect("page")
        end_time = time.strftime("%H:%M:%S")
        print(f"end_time --> {end_time}")
    if args.group:
        # set attribute for argument parameters eg. ("2283833765077318, 2283833765077318")
        start_time = time.strftime("%H:%M:%S")
        print(f"start_time --> {start_time}")
        setattr(p, 'ids', args.group)
        end_time = time.strftime("%H:%M:%S")
        # set type for group
        p.collect("group")
        print(f"end_time --> {end_time}")
    if args.search:
        # set attribute for argument parameters eg. ("12/PAZATA, 12/OUKATA")
        setattr(p, 'ids', args.search)
        # set type for group
        p.collect("search")
    # For all commands

    if args.crawl:
        url = config('CURRENT_CRAWL_PAGES')
        pages = requests.get(url,headers=headers)
        pages = pages.json()
        if pages:
            print(f"Total {len(pages)} page to crawl")
            for page in pages:
                p.collect_from_api(ids=page['id'],url=page['url'],market_place=page['is_marketplace'])
        else:
            print("There is no page to crawl")
    
    if args.test_crawl:
        urls = ["https://www.facebook.com/groups/643021239182864/?ref=share","https://www.facebook.com/groups/1627128580904864/?ref=share"]
        for url in urls:
            p.collect_from_api(ids=1,url = url,market_place=1)
            time.sleep(1)
    
    
    p.close_browser()
