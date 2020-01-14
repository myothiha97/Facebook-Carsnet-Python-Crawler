import argparse
from decouple import config

from db_handler import DBHandler
from firebase import FirebaseHandler
from crawler import Crawler


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
        p.collect("page") 
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

    p.close_browser()
