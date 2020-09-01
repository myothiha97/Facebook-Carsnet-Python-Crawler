import time
import datetime
import re

def format_time(timestamp):
    published_date = ""
    try:
        day_month_reg = r"\d*\s*January|\d*\s*February|\d*\s*March|\d*\s*April|\d*\s*May|\d*\s*June|\d*\s*July|\d*\s*August|\d*\s*September|\d*\s*October|\d*\s*November|\d*\s*December"
        year_reg = r"[1][9][9][0-9]|[2][0][0-9][0-9]"
        day_month = re.search(day_month_reg,timestamp).group()
        day = re.search(r"\d+",day_month).group()
        month_name = re.sub(r"\d+","",day_month)
        month_name = month_name.strip()
        date_obj = datetime.datetime.strptime(month_name,"%B")
        month = date_obj.month
        year = re.search(year_reg,timestamp).group()
        times = re.search(r"\d+\s*:\s*\d+",timestamp).group()
        hr , mins = times.split(":")
        published_date = f"{year}-{month}-{day} {hr}:{mins}:00"
        return published_date

    except Exception as e:
        print("An error occur while formating hover time : ",str(e))
        return published_date