import os
from scrapy.cmdline import execute

# os.system('scrapy list')
# os.system('scrapy crawl roundmenu_cities')
#
# for i in range(0,18):
#   i=str(i)
#   os.system('scrapy crawl roundmenu_delivery -a query=%s'%i)
#   os.system('scrapy crawl roundmenu_all -a query=%s'%i)
#   # execute(('scrapy crawl roundmenu_all -a query='+i).split())

execute('scrapy crawl roundmenu_app'.split())

