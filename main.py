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
                if page['is_active'] == 1:
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
        ## Carsnet Page Test
        # p.collect_from_api(ids=1,url = "https://www.facebook.com/CarsNET-102005471291910/",market_place=0)
        # time.sleep(1)

        # # Group Test - Online ကားပြဲစားတန္း ( YGN )
        p.collect_from_api(ids=2,url = 'https://www.facebook.com/groups/643021239182864/',market_place=1)
        time.sleep(1)

        # # Group Test - Online ကားမျိုးစုံရောင်းဝယ်ရေး
        # p.collect_from_api(ids=3,url = 'https://www.facebook.com/groups/1695736407377955/?ref=share',market_place=1)
        # time.sleep(1)

        # ##ကားပွဲစားတန်း(ရန်ကုန်)
        # p.collect_from_api(ids=4,url = 'https://www.facebook.com/groups/378369752669659/?ref=share',market_place=1)
        # time.sleep(1)

        # # online ကားပွဲစားတန်း
        # p.collect_from_api(ids=5,url = 'https://www.facebook.com/groups/carforsale01/?ref=share',market_place=1)
        # time.sleep(1)

        # Car အရောင်းအဝယ် ရန်ကုန်မြို့
        # p.collect_from_api(ids=6,url = 'https://www.facebook.com/groups/323949978493502/?ref=share',market_place=1)
        # time.sleep(1)

        # # ကားပွဲစားတန်း
        # p.collect_from_api(ids=7,url = 'https://www.facebook.com/groups/1382476945385129/?ref=share',market_place=1)
        # time.sleep(1)

        # # CarZay (ကားဈေး)
        # p.collect_from_api(ids=8,url = 'https://www.facebook.com/groups/1627128580904864/?ref=share',market_place=1)
        # time.sleep(1)

        # #  သိန်း၂၀၀အောက် ကားမျိုးစုံ ဝယ်ရောင်း
        # p.collect_from_api(ids=9,url = 'https://www.facebook.com/groups/643021239182864/?ref=share',market_place=1)
        # time.sleep(1)

        # #  အိမ်စီးကားမျိုးစုံအရောင်းအဝယ်
        # p.collect_from_api(ids=10,url = 'https://www.facebook.com/groups/1473937692898588/?ref=share',market_place=1)
        # time.sleep(1)        

        # # 11	ကားအရောင်းဝယ် Online .	https://www.facebook.com/groups/onlinecarsales/?ref=share
        # p.collect_from_api(ids=11,url = 'https://www.facebook.com/groups/onlinecarsales/?ref=share',market_place=1)
        # time.sleep(1)   

        # # 12	ကားရောင်း / ကားဝယ် ကားပွဲစား များဆုံစည်းရာ	https://www.facebook.com/groups/1786089771666089/?ref=share
        # p.collect_from_api(ids=12,url = 'https://www.facebook.com/groups/1786089771666089/?ref=share',market_place=1)
        # time.sleep(1)   

        # # 13	Auto Car Market ကားအရောင်းအ၀ယ်	https://www.facebook.com/groups/myanmarcarmarket/
        # p.collect_from_api(ids=13,url = 'https://www.facebook.com/groups/myanmarcarmarket/',market_place=1)
        # time.sleep(1)   

        # # 14	မြန်မာ ကားရောင်းဝယ် (Myanmar Car Dealer)	https://www.facebook.com/groups/369828630054592/
        # p.collect_from_api(ids=14,url = 'https://www.facebook.com/groups/369828630054592/',market_place=1)
        # time.sleep(1)   

        # # 15	USED MYANMAR CAR	https://www.facebook.com/groups/520776898092100/
        # p.collect_from_api(ids=15,url = 'https://www.facebook.com/groups/520776898092100/',market_place=1)
        # time.sleep(1)  

        # # 16	35လမ်း,MDY Car, သီးသန့်(ဝယ်/ရောင်း)	https://www.facebook.com/groups/632262877126267/
        # p.collect_from_api(ids=16,url = 'https://www.facebook.com/groups/632262877126267/',market_place=1)
        # time.sleep(1)  
        
        # ## 17	Myanmar Car Showroom	https://www.facebook.com/groups/1265995456818130/
        # p.collect_from_api(ids=17,url = 'https://www.facebook.com/groups/1265995456818130/',market_place=1)
        # time.sleep(1)  
        
        # # 18	Toyota Crown နှင့် ဂျပန်မော်တော်ကားမျိုးစုံရောင်းဝယ်ရေး (Group)	https://www.facebook.com/groups/213191119285748/
        # p.collect_from_api(ids=18,url = 'https://www.facebook.com/groups/213191119285748/',market_place=1)
        # time.sleep(1)  

        # 19	Yangon Car Online Sale Group	https://www.facebook.com/groups/240683956371062/
        # p.collect_from_api(ids=19,url = 'https://www.facebook.com/groups/240683956371062/',market_place=1)
        # time.sleep(1)  

        # # 20	Car အရောင်းအဝယ် Group MDY	https://www.facebook.com/groups/233517020338369/
        # p.collect_from_api(ids=20,url = 'https://www.facebook.com/groups/233517020338369/',market_place=1)
        # time.sleep(1)  

        # # c-> 21	မန်းလေးကားမျိုးစုံရောင်းဝယ်ရေး	https://www.facebook.com/groups/1640172876271325/
        # p.collect_from_api(ids=21,url = 'https://www.facebook.com/groups/1640172876271325/',market_place=1)
        # time.sleep(1)  

        # c-> 22 	Taxi ရောင်းဝယ်ရေး	https://www.facebook.com/groups/155793198089677/
        # p.collect_from_api(ids=22,url = 'https://www.facebook.com/groups/155793198089677/',market_place=1)
        # time.sleep(1)  

        # # c-> 23	TAXI Sales ( အငှားယာဉ်သီးသန့်ရောင်းရန် )	https://www.facebook.com/groups/1468044100104906/
        # p.collect_from_api(ids=23,url = 'https://www.facebook.com/groups/1468044100104906/',market_place=1)
        # time.sleep(1) 

        # # 24	ရန်ကုန်လိုင်စင် အိမ်စီးကားသီးသန့်အရောင်းအဝယ်	https://www.facebook.com/groups/1573085942991070/?ref=share
        # p.collect_from_api(ids=24,url = 'https://www.facebook.com/groups/1573085942991070/',market_place=1)
        # time.sleep(1) 

        # # 25	ကားမျိုးစုံရောင်းဝယ်ရာနေရာ	https://www.facebook.com/groups/1377034182534659/
        # p.collect_from_api(ids=25,url = 'https://www.facebook.com/groups/1377034182534659/',market_place=1)
        # time.sleep(1) 

        # # 26	Online ကား ပွဲ စား တန်း	https://www.facebook.com/groups/carforsale01/?ref=share
        # p.collect_from_api(ids=26,url = 'https://www.facebook.com/groups/carforsale01/',market_place=1)
        # time.sleep(1) 

        ## 27	ကားအမြန်ရောင်းဝယ်ရေး	https://www.facebook.com/groups/824818357601140/?ref=share
        # p.collect_from_api(ids=27,url = 'https://www.facebook.com/groups/824818357601140/',market_place=1)
        # time.sleep(1) 


        

    ### uncomment the following codes only when involving with databases. ###
    
    p.close_browser()
