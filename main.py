import argparse
from decouple import config
from db_handler import DBHandler
from firebase import FirebaseHandler
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
DATABASE = DBHandler()
STORAGE = FirebaseHandler()

# Get Default types from db_handler
PAGES, GROUPS, SEARCHES = DATABASE.select_defaults()

parser = argparse.ArgumentParser(description="Facebook Crawler for pages, groups and searches")

parser.add_argument("-p", "--page", type=str, action="store", nargs="?", metavar="",  const=PAGES, help="Pages You want to crawl")

parser.add_argument("-g", "--group", type=str,  action="store", nargs="?", metavar="",  const=GROUPS, help="Groups You want to crawl")

parser.add_argument("-s", "--search", type=str,  action="store", nargs="?", metavar="",  const=SEARCHES, help="Search posts you want to crawl")

parser.add_argument("-a", "--all", action="store_true",   help="All default pages, groups and searches")

# parser.add_argument("-c", "--comment", type=bool, default=False,  metavar="", help="Comments included")

parser.add_argument("-d", "--depth", type=int, default=5, metavar="", help="Numbers of scroll")

parser.add_argument("-k", "--keep", type=int, default=5, metavar="", help="Seconds you want to delay after scroll")

parser.add_argument("-f", "--filter",  action="store_true", help="With or without keyword filter")

parser.add_argument("-sd","--store_db",action="store_true",help="Use this command to store api data to page table and scheduel table from database")

parser.add_argument("-C","--crawl",action="store_true",help="Use this command to check whether it's time to crawl or not by checking with schedule table from database")

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
    try:
        acc = browser.find_element_by_xpath('//*[@id="mount_0_0"]/div/div/div[2]/div[4]/div[1]/span/div/div[1]')
        acc.click()
        time.sleep(2)
        change_fb = browser.find_element_by_xpath('/html/body/div[1]/div/div/div[2]/div[4]/div[2]/div/div/div[1]/div[1]/div/div/div/div/div/div/div/div[1]/div[3]/div/div[4]/div')
        change_fb.click()
    except:
        print("This is an old faceboook")


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
        print(f"end_time --> {end_time}")
        # set type for group
        p.collect("group")
    if args.search:
        # set attribute for argument parameters eg. ("12/PAZATA, 12/OUKATA")
        setattr(p, 'ids', args.search)
        # set type for group
        p.collect("search")
    # For all commands
    if args.all:
        setattr(p, 'ids', PAGES)
        p.collect("page")
        setattr(p, 'ids', GROUPS)
        p.collect("group")
        setattr(p, 'ids', SEARCHES)
        p.collect("search")

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
    if args.store_db:
        # print("Store data to database")
        url = config('ALL_PAGES_URL')
        r = requests.get(url, headers = headers )
        data = r.json()
        weekday = datetime.datetime.today().weekday()
        print("Today : ",weekday)
        weekday = weekday + 1
        timestamp = time.strftime('%H:%M:%S')

        today_schedules = []

        for page in data:
            # print(page['schedules'])    

            if page['is_active'] == 1:
                for item in page['schedules']:
                    print('Crawled on WeekDay ',item['day'])
                    
                    ### Check WeekDay Here , If matches, append it to today_schedules
                    if item['day'] == weekday or item['day'] == 7:
                        today_schedules.append(item)
        sort_by_time= sorted(today_schedules, key = lambda i: int(i['time'].replace(':','')))
        from insert_data_to_database import insert_data_to_page , insert_data_to_schedule
        insert_data_to_page(data,DATABASE.cursor)
        insert_data_to_schedule(sort_by_time,DATABASE.cursor)
        DATABASE.db.commit()
    p.close_browser()
