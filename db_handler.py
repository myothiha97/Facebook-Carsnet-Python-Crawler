from decouple import config
import mysql.connector
import argparse
import re
# from mysql.connector import errorcode


class DBHandler:
    _instance = None


    # Keywords for filtering
    keywords = []
    regex_string = None

    default_tables = ['default_fbpages', 
                    'default_fbgroups',
                    'default_fbsearches',]

    @staticmethod
    def instance():
        if '_instance' not in DBHandler.__dict__:
            DBHandler._instance = DBHandler()
        return DBHandler._instance


    def __init__(self):
        if DBHandler._instance != None:
            raise Exception("This class is singleton")
        else:
            DBHandler._instance = self
        self.db = mysql.connector.connect(
            host=config('HOST'),
            user=config('DB_USER'),
            password=config('DB_PASSWORD'),
            database=config('DB_DATABASE'),
            auth_plugin=config('DB_AUTH_PLUGIN')
        )
        self.cursor = self.db.cursor()
        self.img_id = None
        self.image_tables = [config('DB_NAME_PAGES_IMG'),
                             config('DB_NAME_GROUPS_IMG'),
                             config('DB_NAME_SEARCHES_IMG')]
        
        self.default_tables = ['default_fbpages', 
                               'default_fbgroups',
                               'default_fbsearches',]   

    def retrieve_filter_keyword(self):
        keyword_list = []
        self.cursor.execute("Select * from keywords")            
        try:    
            for keyword in self.cursor.fetchall():
                keyword_list.append(keyword[1])            
        except:
            pass

        self.regex_string = '(?:% s)' % '|'.join(keyword_list)

    def __repr__(self):
        return (f'{self.__class__.__name__}')


    def select(self, table, *args):
        return 'SELECT {select} FROM {table}'.format(
                table=table,
                select=','.join(item for item in args) if '*' not in args else '*'
        )


    def drop(self, table):
        return 'DROP TABLE IF EXISTS {}'.format(table)


    def create_default_tables(self, image_table, table, default_table):        
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS {default_table} (id INT NOT NULL AUTO_INCREMENT, {default_table.split('_')[1]} VARCHAR(225), PRIMARY KEY(id));            ")       
    
    #Retrieve Create Statement For keywords table
    
    
    # Select pages, groups and searches from defaults_tables
    def select_defaults(self, limit=5):
        for default in self.default_tables:
            sql = self.select(default, default.split('_')[1])
            self.cursor.execute(sql)
            results = self.cursor.fetchall()

            if default == 'default_fbpages':
                pages = ','.join(str(result[0]) for result in results)
            if default == 'default_fbgroups':
                groups = ','.join(str(result[0]) for result in results)
            if default == 'default_fbsearches':
                searches = ','.join(str(result[0]) for result in results)

        return pages, groups, searches


    def create_table(self):


        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS screenshots (id INT NOT NULL AUTO_INCREMENT, img_url LONGTEXT, PRIMARY KEY(id)); ")
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS post_content (id INT NOT NULL AUTO_INCREMENT, post LONGTEXT, img_id INT, created_at DATETIME DEFAULT CURRENT_TIMESTAMP, PRIMARY KEY(id));")
        for image_table, table, default_table in zip(self.image_tables, self.tables, self.default_tables):
            sql = self.create_default_tables(image_table, table, default_table)
            # Execute Multiple queries            
            # self.cursor.execute(sql, multi=True)

        self.cursor.execute('CREATE TABLE IF NOT EXISTS keywords (id INT NOT NULL AUTO_INCREMENT, keyword varchar(100), PRIMARY KEY(id));')
        
                
    def insert_tables(self,table_name):
        if table_name == "page":
            try:
                self.cursor.execute("CREATE TABLE IF NOT EXISTS `page`(id int NOT NULL AUTO_INCREMENT PRIMARY KEY,original_id int, page_url varchar(200),page_name varchar(200),last_crawled_date date, page_status boolean,icon varchar(200),time_stamp VARCHAR(50))")
            except:
                print("Page table already exist")
            else:
                print("table created")
                self.db.commit()
        elif table_name == "schedule":
            try:
                self.cursor.execute("CREATE TABLE IF NOT EXISTS `schedule`(id int NOT NULL AUTO_INCREMENT PRIMARY KEY,original_id int,page_id int,crawl_day int,crawl_time TIME(0) NOT NULL)")
            except:
                print("Schedule table already exist")
            else:
                print("table created")
                self.db.commit()
        elif table_name == "history":
            try:
                self.cursor.execute("CREATE TABLE IF NOT EXISTS `history`(id int NOT NULL AUTO_INCREMENT PRIMARY KEY,page_id int,schedule_id int,start_time VARCHAR(50),end_time VARCHAR(50),crawled_date VARCHAR(50))")
            except:
                print("History table already exists")
            else:
                print("Table created")
                self.db.commit()


    def drop_table(self, tablename=None):        
        self.cursor.execute(self.drop('keywords'))
        for default_table, table, image_table in zip(self.default_tables, self.tables, self.image_tables):
            # sql = ';'.join([self.drop(default_table), self.drop(table), self.drop(image_table)])
            # Execute Multiple queries
            self.cursor.execute(self.drop(default_table))
            self.cursor.execute(self.drop(table))
            self.cursor.execute(self.drop(image_table))
            
        

    # Import default pages, groups and searches from .txt files
    def import_default_data(self):        
        for default in self.default_tables:
            file = default.split('_')[1]
            with open(file + '.txt', 'r') as f:
                contents = f.read().split('\n')
                for content in contents:
                    self.store_defaults_to_db(default, content)
        self.store_default_keywords()
        

    def store_default_keywords(self):
        file = 'keywords.txt'
        sql = "INSERT INTO keywords (keyword) VALUES (%s)"
        with open(file, 'r') as f:
            contents = f.read().split('\n')
            for content in contents:                
                self.commit_db(sql, content)

    def store_imgurl_to_db(self, table, img_url):
        sql = "INSERT INTO {} (img_url) VALUES (%s)".format(table)
        self.cursor.execute(sql, (img_url,))
        self.img_id = self.cursor._last_insert_id
        self.db.commit()


    def save_timestamp_for_page(self,page_id,timestamp):
        p_id = int(page_id[0])
        # sql = f"INSERT INTO `page` set `time_stamp` = {timestamp}  where `original_id` = {p_id}"
        # sql = f"INSERT INTO `page`(time_stamp) VALUES({timestamp}) WHERE id = {p_id}"
        sql = f"UPDATE `page` SET `time_stamp` = {timestamp} WHERE id = {p_id}"
        # self.commit_db(sql)
        self.cursor.execute(sql)
        self.db.commit()
        
    def extract_page_ids_from_page(self):
        sql = f"SELECT id FROM `page`"
        self.cursor.execute(sql)
        page_ids = []
        for i in self.cursor:
            page_ids.append(i[0])
        return page_ids
    
    def extract_timestamp_from_page(self):
        sql=f"SELECT time_stamp FROM `page`"
        self.cursor.execute(sql)
        page_time_stamps = []
        for i in self.cursor:
            page_time_stamps.append(i)
        return page_time_stamps
    
    def extract_times_and_crawldays_from_schedule(self):
        sql1=f"SELECT crawl_time FROM `schedule`"
        sql2=f"SELECT crawl_day FROM `schedule`"
        self.cursor.execute(sql1)
        crawl_times=[]
        for i in self.cursor:
            crawl_times.append(i[0])
        self.cursor.execute(sql2)
        crawl_days = []
        for i in self.cursor:
            crawl_days.append(i[0])
        return crawl_times,crawl_days
    
    def extract_page_ids_from_schedule(self):
        sql = f"SELECT page_id FROM `schedule`"
        self.cursor.execute(sql)
        schedule_page_ids = []
        for i in self.cursor:
            schedule_page_ids.append(i[0])
        return schedule_page_ids
    
    def insert_data_to_history(self,page_id,schedule_id,start_time,end_time,date):
        command = f"INSERT INTO `history`(page_id,schedule_id,start_time,end_time,crawled_date) VALUES(%s,%s,%s,%s,%s)"
        val=(page_id,schedule_id,start_time,end_time,date)
        self.cursor.execute(command,val)
        self.db.commit()
    
    def extract_schedule_ids_from_schedule(self):
        sql=f"SELECT id FROM `schedule`"
        self.cursor.execute(sql)
        schedule_id=[]
        for i in self.cursor:
            schedule_id.append(i[0])
        return schedule_id
        
    
    def store_post_to_db(self, table, post,has_filter):
        
        sql = "INSERT INTO {} (post, img_id) VALUES (%s, (SELECT id FROM {} WHERE id = {}))".format(table, table + "_img", self.img_id)
        try:
            if has_filter:     
                if self.regex_string is None:
                    self.retrieve_filter_keyword()           
                if re.search(self.regex_string, post):
                    self.commit_db(sql, post)
            else:            
                self.commit_db(sql, post)
        except Exception as e:
            print('Issue saving the data: '+ str(e))
            print(f"There is an issue saving the following content to {table} table")
            print(f"{post}")
            print(f"----------------")


    def store_defaults_to_db(self, table, content):        
        sql = "INSERT INTO {} ({}) VALUES (%s)".format(table, table.split('_')[1])
        self.commit_db(sql, content)


    def commit_db(self, sql, obj):
        self.cursor.execute(sql, (obj,))
        self.db.commit()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Database Handling for Crawler")

    parser.add_argument("-m", "--migrate",  action="store_true",   help="Table you want to create")

    parser.add_argument("-d", "--drop", action="store_true", help="Table you want to drop")
    
    parser.add_argument("-p","--create_table" , action="store_true",help="use this command if u dont have require tables ")
    
    parser.add_argument("-i","--insert_table",type=str,action="store",help="use this command to insert require tables to database")
    args = parser.parse_args()

    g = DBHandler()
    # g.insert_data_to_history(page_id = 1,schedule_id=2,start_time="12:30:40",end_time="13:30:40",date="31/3/2020")
    # g.extract_schedule_ids_from_schedule()
    g.extract_page_ids_from_schedule()
    if args.migrate:
        g.create_table()
        g.import_default_data()

    if args.drop:
        g.drop_table()

    if args.create_table:
        g.create_table()
        
    if args.insert_table:
        commands = ["page","schedule","history"]
        if args.insert_table not in commands:
            print("Invalid table")
            print("The available tables are [page,schedule,history]")
        else:
            g.insert_tables(args.insert_table)