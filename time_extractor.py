import time
import datetime

content = '30 m'
splited_value = content.split(' ')
try:
    time_type = splited_value[1]
    if(time_type in ['h','hr','hrs']):
        total_hours = int(splited_value[0])
        published_date = datetime.datetime.now() - datetime.timedelta(hours=total_hours)
        formatted_published_at = published_date.strftime("%Y-%m-%d %H:00:00")
        print(formatted_published_at)
    elif(time_type in ['m','min','mins']):
        total_minutes = int(splited_value[0])
        published_date = datetime.datetime.now() - datetime.timedelta(minutes=total_minutes)
        formatted_published_at = published_date.strftime("%Y-%m-%d %H:%M:%S")
        print(formatted_published_at)

except Exception as ex:
    print(str(ex))


