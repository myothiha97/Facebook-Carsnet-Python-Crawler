# S-MotherFinance-FacebookCrawler

## Requirements

Python3.7 and above, Python Request Lib, Pip and Mysql Server

### Environment Setup

To install packages locally, you need to create virtual environment

```
pip install virtualenv
```

to launch virtual environment, you have to go to your project directory

```
cd your_project
```

Within your project, create virtual environment

```
virtualenv env -p python_path\python.exe
```

And activate your environment

In Window

```
.\env\Scripts\activate.bat
```

In Linux and Mac

```
source ./env/bin/activate
```

## .env

Copy .env-example file into .env with the associate database environment information

Please to check in schmea details to make sure  
in Windows and Mac

Default collation = utf8mb4_0900_ai_ci and  
Default characterset = utf8mb4

in Linux  
Default collation = utf8_unicode_ci and  
Default characterset = utf8mb4

Update DB_AUTH_PLUGIN into mysql_native_password if necessary

Add in firebase information to setup server to store images.

## Installation


### Installing Require Python Packages

Install mysql connector for python 

```
pip install mysql-connector-python
```

Install selenium

```
pip install selenium
```

Install python-decouple

```
pip install python-decouple
```
Install argparse

```
pip install argparse
```

Install pyrebase4

```
pip install pyrebase4
```

Install myanmartools

```
pip install myanmartools
```
Download relative chrome driver from https://chromedriver.chromium.org/ and place it on drivers folder.

Change the path of the driver in .env if necessary.

### Migration

To migrate data, you have to build database with new schema

Please to check in schmea details to make sure  
in Windows and Mac

Default collation = utf8mb4_0900_ai_ci and  
Default characterset would be utf8mb4

in Linux  
Default collation = utf8_unicode_ci and  
Default characterset would be utf8mb4

```
python db_handler.py -m
```

in case of dropping databases

```
python db_handler.py -d
```
For adding tables which manage the crawl time of crawler.Necessary tables are 'page' , 'scheduel' and 'history'.

```
python db_handler.py -i="page"
```
### Running the application

Create an environment with python 3.6 and above (3.7 prefer)

There are 3 main options

source ~/VirtualEnvs/FB_Crawler/bin/activate

-p for page

```
python main.py -p="CarsNET-102005471291910" # pages you want to crawl
```

-g for group 

```
python main.py -g="2283833765077318" # groups you want to crawl
```

-s for search.

```
python main.py -s="12/PAZATA" # searches you want to crawl
```

For multiple pages, groups and searches, you can add names by separating commas

```
python main.py -p="motherfinancemyanmar, GoogleCrowdsourceMyanmar" -g="2283833765077318, 2283833765077318" -s="12/PAZATA, motherfinance"
```

Additionally, adjustable options are
-d for depth which control the number of scroll
As default, it will crawl by 5 scrolls

```
python main.py -d=10 # 10 scrolls
```

-k for keep which wait for seconds after 1 scroll
As default, it will wait 5 seconds

```
python main.py -k=6 # wait for 6 seconds after 1 scroll
```

-C option for crawling pages/groups from api'

```
python main.py -C
```

### Filtering the data

-f or --filter option at the end of the commend will save the crawl data which only match with the filter keywords. 


### Default

By defaults, it will run pages, groups and searches from default_fb, default_fbgroups, default_fbsearches tables.

Thus, you can add specific pages, groups and searches into either tables with id or fbpages.txt, fbgroups.txt and fbsearches.txt

Then migrate the data again.

With all that said,  
you can run

-a for all defaults

```
python main.py -a
```

Likewise, you can crawl by specific options

```
python main.py -p -g -s
```

Create .sh script file with above options accordingly with the necessary page or group id and associate keyword for search with keywords function.

Set chmod +x /path/to/yourscript.sh your script.

Setup a cron job for the created .sh script.

### Transferring data

Update POST_URL from config with the API URL which can store the data in chunks.

### Env on main server
