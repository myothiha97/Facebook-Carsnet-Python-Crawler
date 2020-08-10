import time
import datetime
import datetime

def eval_date_to_crawl(date):
    current_time = datetime.datetime.now().strftime(r"%Y-%m-%d 09:00:00")
    last_crawl_date = datetime.datetime.now() - datetime.timedelta(days=1)
    last_crawl_time = last_crawl_date.strftime(r"%Y-%m-%d 09:00:00")
    if last_crawl_time < date < current_time:
        print("Date in range")
        return True
    else:
        print("Date not in range")
        # print("Page date --->")
        print(f"last_crawl_time ------------> {last_crawl_time}")
        print(f"current_time ---------------> {current_time}")
        return False

if __name__ == "__main__":
    res = eval_date_to_crawl("2020-08-9 08:59:00")
    print(res)