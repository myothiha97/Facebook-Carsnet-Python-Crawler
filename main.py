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
import os
import getpass
from DigiZaayAPI import DigiZaayApiConnector

token =  'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiI2IiwianRpIjoiYjViYzczNDJlYjVkOGVlZDhiMzhhOTlmZGE3NjcxZmFjMTAwMTExMTM0ZDcwNmNkN2FmY2Q4NjYzMmRmZTNkZjUxNjA5OWQ3MGNjMDQwOTMiLCJpYXQiOjE1OTg1ODUxNTIsIm5iZiI6MTU5ODU4NTE1MiwiZXhwIjoxNjMwMTIxMTUyLCJzdWIiOiIxIiwic2NvcGVzIjpbXX0.kWldsf_gBhpyy_GVJW4csxbeftDLf_ztwFdRPIdXckvsldQB-yU-eMzSAhm4Dw5CMV-NW61deZKr9wgekdPQcU4HwtSj3z3A6HS82nc-74p0eABWNIfHpqIeqcmzr8veUiWjwxhXgSo63oE-1JMzlsW0nxhMyUfL70nDTwWAmK0mbKBSr1dXsEhM51bcTLJ2EApViIziMTAc8l09vkme9bOHQ_NFxvmRVXD_NuHQXWdQK3EsCsekp-hmTi3sfjg_2VmzDOr0-P2GqdKfhrCfp5ki6KJDOSEGlimfCS8MKrfri2niZnYE-UZ4vRghLv1eNIUte6di5wTsCWrEMpbY0fVE0rO9BCoTMtnZfMEv_97AvSoxY05f31t1S4mr-ym7dxg84rWcs2G5qpxGQoS_MARuvSmpM8L7mUHrm3lslTXberNDxNibgEMgXKcgO7wmNHl_mP-KAw6OAlQj0JBQivUPpHBP9FlPbf0wzfP4f6L1G6VvkY4E_BPXg5S9WGABYvYMHkzbr9AtVtutMnH-9BgvzKTcz8afCK2AOfl8nYxAlM83a1aaZFGxg44SqvKtS7w_ZrDwAGOwwnzYkfKiWgTHh_Jnbvmlaq-J-5Q8Dldc5l5KbrJnSD0AA1Up6ERDSSxDxZSR5Ab1LubfsRAOjTVPHpcPv8SOkCAl2hL4t4E'
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


    # current_date = datetime.datetime.now()
    # username = getpass.getuser()
    # with open('crawler-history-log.txt','a') as fileobj:
    #     fileobj.write(f"User - {username} has run the crawler at {current_date}")
    #     fileobj.write("\n")

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
        # p.collect_from_api(ids=1,url = "https://www.facebook.com/CarsNET-102005471291910/",market_place=0)
        # time.sleep(1)

        ## Group Test - Online ကားပြဲစားတန္း ( YGN )
        p.collect_from_api(ids=2,url = 'https://www.facebook.com/groups/643021239182864/',market_place=1)
        time.sleep(1)

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
