from decouple import config
import mysql.connector
import argparse
import re


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
        self.cursor.execute(f"CREATE TABLE IF NOT EXISTS post_content (id INT NOT NULL AUTO_INCREMENT, post LONGTEXT, img_id INT, created_at DATETIME DEFAULT CURRENT_TIMESTAMP, FOREIGN KEY (img_id) REFERENCES {table}_img(id), PRIMARY KEY(id));")
        for image_table, table, default_table in zip(self.image_tables, self.tables, self.default_tables):
            sql = self.create_default_tables(image_table, table, default_table)
            # Execute Multiple queries            
            # self.cursor.execute(sql, multi=True)

        self.cursor.execute('CREATE TABLE IF NOT EXISTS keywords (id INT NOT NULL AUTO_INCREMENT, keyword varchar(100), PRIMARY KEY(id));')
        


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
        sql = f"insert into page set timestamp = {timestamp}  where id = {page_id}"
        self.commit_db(sql)
        
   
    
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

    parser.add_argument("-d", "--drop", action="store_true", help="Table you want to create")

    args = parser.parse_args()

    g = DBHandler()

    if args.migrate:
        g.create_table()
        g.import_default_data()

    if args.drop:
        g.drop_table()

