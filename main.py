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
from DigiZaayAPI import DigiZaayApiConnector

token =  'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIyIiwianRpIjoiYzViNTM2ZjYwYmJkNmUzODE5OTY1NDU5Y2NhMDdkYWZkZWZmOGNhYzFmMWFlM2M4ZjM0NDNlNTliNmRkNjNhOWY5M2RlYjZlOWE3M2RkOWYiLCJpYXQiOjE1ODI4Nzc5NzIsIm5iZiI6MTU4Mjg3Nzk3MiwiZXhwIjoxNjE0NTAwMzcyLCJzdWIiOiIxIiwic2NvcGVzIjpbXX0.LO3h9dmRO3avdr0Xie6qju2SBYoN8Js283pRW2ajm1NGZeMRGB9mVBP0w6v7H4pkrvx1eAF0CFyFpEwWf5WF9FbEGbvBFMuVsYYfEQluAMYykPmR7RynXhBi_TVj7o2h7ZKK4RKCMqUdMD9R2S6K_ebtE0sfPn-Dh08pxwjYgx4ecpYImt0P6gfvhPON9tGzWrxd_GLeZ0Oqs5012v13gL1BKk45_op1_rovDG3o18eLk5ASYh38dkgT1My8zxN9Ommuz1EhDlwD0FcI_w6d1OYV0qprsxpvUUUT33tWeOhkC5Y1mViGGyPdQW3y08VGrUIaVGsPu6BpFx1whhDeDryTFY9FBv7dX3yhiz0mX51Tc5iOeIjXmy127PRBAzeYysHMG1I3WrE6It_LJ4r2BdVrLFfQc1zdNxC-KAy3CdwhHYsIYL9aGlSv2VPrXDRnNujF5nprZSTMbbgEbXW6ahAte2AyC6kFmfcl-Q-E2a7tCk_jMmo6lqiNR1RGhQjs-7j1SuNxvcVVm9mXO8z-L_k6Fh34SxkPD4_UR_EtGWV4XPpIEhxHJGzVfKR72LAgayfc5dnTZowKs2xMTsfAQLDLljuDmeDzgE1MIj1zgt9cQVQ9z5UUzfUiVQDMUW33uxQ07fasjFsGiGg9uQA6v_zO0epZ8c_Xl0bWbDGcNF0'
headers = {
            'Content-Type': "application/json",
            'Accept': "*/*",
            'Cache-Control': "no-cache",
            'Host': 'crawler-dev.digi-zaay.com.mm',
            'Accept-Encoding': "gzip, deflate",
            'Content-Length': "45",
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

# parser.add_argument("-p", "--page", type=str, action="store", nargs="?", metavar="",  const=PAGES, help="Pages You want to crawl")

# parser.add_argument("-g", "--group", type=str,  action="store", nargs="?", metavar="",  const=GROUPS, help="Groups You want to crawl")

parser.add_argument("-s", "--search", type=str,  action="store", nargs="?", metavar="",  const=SEARCHES, help="Search posts you want to crawl")


# parser.add_argument("-c", "--comment", type=bool, default=False,  metavar="", help="Comments included")

parser.add_argument("-d", "--depth", type=int, default=10, metavar="", help="Numbers of scroll")

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

    

    if args.crawl:
        pages = DigiZaayApiConnector.get_pages_from_api(header = headers)
        pages = pages.json()
        
        print('--- pages to crawl ---')
        print(pages)
        if pages:
            print(f"Total {len(pages)} page to crawl")
            for page in pages:
                p.collect_from_api(ids=page['id'],url=page['url'],market_place=page['is_marketplace'])
                time.sleep(1)
        else:
            print("There is no page to crawl")

    if args.search:
        # set attribute for argument parameters eg. ("12/PAZATA, 12/OUKATA")
        setattr(p, 'ids', args.search)
        # set type for group
        p.collect("search")
    
    if args.test_crawl:
        # ## Carsnet Page Test
        p.collect_from_api(ids=1,url = "https://www.facebook.com/CarsNET-102005471291910/",market_place=0)
        time.sleep(1)

        ## Group Test - Online ကားပြဲစားတန္း ( YGN )
        # p.collect_from_api(ids=2,url = 'https://www.facebook.com/groups/643021239182864/',market_place=1)
        # time.sleep(1)

        # # Group Test - Online ကားမျိုးစုံရောင်းဝယ်ရေး
        # p.collect_from_api(ids=3,url = 'https://www.facebook.com/groups/1695736407377955/?ref=share',market_place=1)
        # time.sleep(1)

        # ##ကားပွဲစားတန်း(ရန်ကုန်)
        # p.collect_from_api(ids=4,url = 'https://www.facebook.com/groups/378369752669659/?ref=share',market_place=1)
        # time.sleep(1)

        # ##online ကားပွဲစားတန်း
        # p.collect_from_api(ids=5,url = 'https://www.facebook.com/groups/carforsale01/?ref=share',market_place=1)
        # time.sleep(1)

        # # Car အရောင်းအဝယ် ရန်ကုန်မြို့
        # p.collect_from_api(ids=6,url = 'https://www.facebook.com/groups/323949978493502/?ref=share',market_place=1)
        # time.sleep(1)

        

    ### uncomment the following codes only when involving with databases. ###
    
    p.close_browser()
