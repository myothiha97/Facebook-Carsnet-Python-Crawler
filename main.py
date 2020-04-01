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

parser.add_argument("-C","--crawl",type=str,action="store",help="Use this command to check whether it's time to crawl or not by checking with schedule table from database")

args = parser.parse_args()
   

if __name__ == '__main__':
    # Initializer Crawler
    p = Crawler(DATABASE, STORAGE, args.depth, args.keep,args.filter)

    setattr(p, 'depth', args.depth)
    setattr(p, 'delay', args.keep)

    # Login into Facebook Account
    p.login(config('EMAIL'), config('PASSWORD'))

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
        setattr(p, 'ids', args.group)

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
        # import main2.py
        # print("Start crawling ")
        weekday = datetime.datetime.today().isoweekday()
        # print(weekday , type(weekday))
        current_time = time.strftime('%H:%M:%S')
        print("current time",current_time,type(current_time))
        schedule_ids=DATABASE.extract_schedule_ids_from_schedule()
        
        crawltimes,crawldays=DATABASE.extract_times_and_crawldays_from_schedule()
        
        to_crawl_times = [str(i) for i in crawltimes]
        crawl_hrs=[]
        crawl_mins=[]
        crawl_secs=[]
        for x in range(len(to_crawl_times)):
            crawl_hr,crawl_min,crawl_sec = to_crawl_times[x].split(':')
            crawl_hrs.append(crawl_hr)
            crawl_mins.append(crawl_min)
            crawl_secs.append(crawl_sec)  
        current_hr,current_min,current_sec = current_time.split(":")          
        # to_crawl_times = []
        # for i in crawltimes:
            
        to_crawl_days =  [int(str(i)) for i in crawldays]
        # print(to_crawl_times,to_crawl_days)
        p_ids = DATABASE.extract_page_ids_from_schedule()
        # print(to_crawl_times[0])
        for i in range(len(crawl_hrs)):
            if weekday == to_crawl_days[i] and current_hr == crawl_hrs[i]:
                print(f"start crawling at weekday : {weekday} and time : {current_hr} hr")
                print(f"Crawl page id : {p_ids[i]}")
                c_time = time.strftime('%H:%M:%S')
                p.collect_by_page_ids(args.crawl,p_ids[i])
                e_time = time.strftime('%H:%M:%S')
                time_stamp = datetime.datetime.now()
                e_date= time_stamp.strftime("%d/%m/%Y")
                DATABASE.insert_data_to_history(page_id=p_ids[i],schedule_id=schedule_ids[i],start_time=c_time,end_time=e_time,date=e_date)
            else:
                print("Crawl time and day doesn't match yet!!")
                # print(f"Crawl time : {crawl_hr[i]} and crawl weekday : {to_crawl_days[i]}")
    
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
