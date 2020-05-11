import mysql.connector
from mysql.connector import Error
import json
def insert_data_to_page(datas,cursors):
    for i in range(len(datas)):
        info = datas[i]
        org_id = info['id']
        page = info['name']
        page_img = info['image']
        page_url = info['url']
        page_status = info['is_active']
        # last_crawl_date=info['last_crawl_at']
        insert_code = f"INSERT INTO `page`(original_id,page_status,page_name,icon,page_url) VALUES(%s,%s,%s,%s,%s)"
        val = (org_id, page_status, page, page_img, page_url)
        org_ids = []
        cursors.execute("SELECT original_id from `page`")
        for row in cursors:
            org_ids.append(row[0])
        if org_id not in org_ids:
            try:
                cursors.execute(insert_code, val)
                print("Inserting complete")
            except Error as e:
                print(e)
        else:
            print("The page is already exist!!")


def insert_data_to_schedule(datas,cursors):
    for i in range(len(datas)):
        info = datas[i]
        schedule_id = info['id']
        page_id = info['crawl_page_id']
        crawl_day = info['day']
        crawl_time = info['time']
        
        insert_code = f"INSERT INTO `schedule`(original_id,page_id,crawl_day,crawl_time) VALUES(%s,%s,%s,%s)"
        val = (schedule_id,page_id,crawl_day,crawl_time)
        
        org_ids = []
        cursors.execute("SELECT original_id from schedule")
        for row in cursors:
            org_ids.append(row[0])
        if schedule_id not in org_ids: 
            try:
                cursors.execute(insert_code,val) 
                print("Insert complete") 
            except Error as e:
                print(e)
        else:
            print("The original id is already exist")  
def inser_data_to_history(datas):
    pass

def reset_page_table():
    cursor.execute(f"DELETE FROM `page`")
    cursor.execute("ALTER TABLE `page` AUTO_INCREMENT = 1")


def reset_history_table():
    cursor.execute(f"DELETE FROM `history`")
    cursor.execute("ALTER TABLE `history` AUTO_INCREMENT = 1")


def reset_schedule_table():
    cursor.execute(f"DELETE FROM `schedule`")
    cursor.execute("ALTER TABLE `schedule` AUTO_INCREMENT = 1")


def insert_to_page(code):
    codes, vals = code()
    try:
        for i, y in (codes, vals):
            cursor.execute(i, y)
            print("insert complete")
    except Error as e:
        print(e)


if __name__ == "__main__":
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="123456",
        auth_plugin='mysql_native_password',
    )
    cursor = mydb.cursor()
    cursor.execute("USE testdb")
    insert_data_to_schedule(sort_by_time)
    insert_data_to_page(data)
    # reset_page_table()
    # reset_schedule_table()
    mydb.commit()
    
