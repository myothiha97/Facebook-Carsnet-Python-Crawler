import time
import datetime
import re
# content = '4 d'
def get_publish_at(content):
    year_reg = r"[1][9][9][0-9]|[2][0][0-9][0-9]"
    month_reg = r"\d*\s*January\s*\d*|\d*\s*February\s*\d*|\d*\s*March\s*\d*|\d*\s*April\s*\d*|\d*\s*May\s*\d*|\d*\s*June\s*\d*|\d*\s*July\s*\d*|\d*\s*August\s*\d*|\d*\s*September\s*\d*|\d*\s*October\s*\d*|\d*\s*November\s*\d*|\d*\s*December\s*\d*"
    published_date = ''
    if re.search(month_reg,content):
        try:
            day = re.search(r"\d+",re.search(month_reg,content).group()).group()
            month_name = re.sub(r"\d+","",re.search(month_reg,content).group())
            month_name = month_name.strip()
            date_obj = datetime.datetime.strptime(month_name,"%B")
            month = date_obj.month

            if re.search(r"\d+:\d+\s*A*M*|\d+:\d+\s*P*M*",content):
                hr = re.search(r"\d+|\d+",re.search(r"\d+:\d+\s*A*M*|\d+:\d+\s*P*M*",content).group()).group()
                mins = re.search(r":\d+",content).group()
                mins = re.sub(r":","",mins)
                if re.search(r"AM|PM",content):
                    am_pm = re.search(r"AM|PM",content).group()
                    if am_pm == "PM":
                        hr = int(hr) + 12
            else:
                hr , mins , secs = "00","00","00"
            if re.search(year_reg,content):
                year = re.search(year_reg,content).group()
            else:
                year = datetime.datetime.now().strftime("%Y")
            published_date = f"{year}-{month}-{day} {hr}:{mins}:00"
            print("published_date ---------------------> ",published_date)
            return published_date
        except Exception as e:
            print(f"An error occur while trying to get timestamp at month format : {e}")
            # print(published_date)
            return published_date
    elif re.search(r"yesterday|Yesterday",content):
        try:
            dateobj = datetime.datetime.strftime(datetime.datetime.now()- datetime.timedelta(1),r"%Y-%m-%d")
            year , month , day = dateobj.split("-")
            hr = re.search(r"\d+",content).group()
            mins = re.search(r":\d+",content).group()
            mins = re.sub(r":","",mins)
            published_date = f"{year}-{month}-{day} {hr}:{mins}:00"
            print("published_date ---------------------> ",published_date)
            return published_date
        except Exception as e:
            print(f"An error occur while trying to get timestamp at yesterday format: {e}")
            # print(published_date)
            return published_date
    else:
        # splited_value = content.split('')
        try:
            # time_type = splited_value[1]
            time_reg = r"\d+\s*h|\d+\s*hr|\d+\s*hrs|\d+\s*m|\d+\s*min|\d+\s*mins|\d+\s*d|\d+\s*day|\d+\s*days"
            time_type = re.search(time_reg,content).group()
            if(re.search(r"h|hr|hrs",time_type)):
                # total_hours = int(splited_value[0])
                total_hours = int(re.search(r"\d+",time_type).group())
                published_date = datetime.datetime.now() - datetime.timedelta(hours=total_hours)
                formatted_published_at = published_date.strftime("%Y-%m-%d %H:00:00")
                print(formatted_published_at)
                return formatted_published_at
            elif(re.search(r"m|min|mins",time_type)):
                # total_minutes = int(splited_value[0])
                total_minutes = int(re.search(r"\d+",time_type).group())
                published_date = datetime.datetime.now() - datetime.timedelta(minutes=total_minutes)
                formatted_published_at = published_date.strftime("%Y-%m-%d %H:%M:%S")
                print("Published_date ---------------------->",formatted_published_at)
                return formatted_published_at
            elif(re.search(r"d|day|days",time_type)):
                # total_days = int(splited_value[0])
                total_days = int(re.search(r"\d+",time_type).group())
                published_date = datetime.datetime.now() - datetime.timedelta(days=total_days)
                formatted_published_at = published_date.strftime(r"%Y-%m-%d 00:00:00")
                print("published date ---------------------->",formatted_published_at)
                return formatted_published_at
        except Exception as e:
            print(f"An error occur while trying to get timestamp at hr/min/day format: {e}")
            # print(published_date)
            return published_date


if __name__ == "__main__":
    content = "May 3,2016"
    get_publish_at(content)


