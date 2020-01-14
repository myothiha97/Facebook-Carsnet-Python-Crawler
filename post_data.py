from env import EMAIL, PASSWORD, HOST, USER, DB_DATABASE, DB_PASSWORD, CHROMEDRIVER,POST_URL
import mysql.connector
import requests

class PostData:
    def __init__(self):
        self.db = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=DB_PASSWORD,
            database=DB_DATABASE
        )

    def post_data(self):
        cursor = self.db.cursor()
        sql = "SELECT * FROM fb_pages"
        cursor.execute(sql)
        result = cursor.fetchall()
        my_array = {i: value[1] for i, value in enumerate(result)}

        requests.post(POST_URL, data=my_array)
            

if __name__ == '__main__':
    c = PostData()
    c.post_data()