# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv
import os
from roundmenu_scrapy.mongodb_utils import get_db
from roundmenu_scrapy.settings import VERSION

roundmenu_app_fields=[
    "id",
    "name",
    "name_localized",
    "link",
    "location",
    "location_localized",
    "lat",
    "lng",
    "cuisines",
    "tags",
    "min_order",
    "currency",
    "rating_average",
    "rating_count",
    "closed_status",
    "price_average",
    "price_range",
    "delivery_average",
    "delivery_range",
    "delivery_unit",
    "delivery_unit_localized",
    "delivery_source",
    "preparation_time",
    "promotions",
    "order_count",
    "brand_id",
    "_score"
]

fields = [
    "name",
    "url",
    "telephone",
    "servesCuisine",
    "priceRange",
    "addressCountry",
    "addressRegion",
    "addressLocality",
    "postalCode",
    "streetAddress",
    "ratingValue",
    "reviewCount",
    "bestRating",
    "worstRating",
    "latitude",
    "longitude",
]

fields_city = [
    'count',
    'city',
    'url'
]

rest_url_all = []
rest_url_del=[]

class RoundmenuScrapyPipeline(object):
    def __init__(self):
        cur_dir = os.path.dirname(os.path.realpath(__file__))
        self.file_dir = os.path.join(cur_dir, '../../crawlerOutput/{}/roundmenu'.format(VERSION))
        self.file_name = None
        self.file_path = None

        # 创建数据库连接对象
        self.mongoclient=get_db()

    def process_item(self, item, spider):

        # 输出参观信息
        if spider.name == 'roundmenu_all':
            if item['url'] not in rest_url_all:
                rest_url_all.append(item['url'])
                city = item.get('url').split('/')[3]
                self.file_name = "{}_all.csv".format(city)
                self.file_path = os.path.join(self.file_dir, self.file_name)
                if not os.path.exists(self.file_dir):
                    print(self.file_dir)
                    os.makedirs(self.file_dir)
                # 写表头
                if not os.path.exists(self.file_path):
                    with open(self.file_path, 'w', newline='', encoding='utf-8') as f:
                        f_csv = csv.DictWriter(f, fieldnames=fields)
                        f_csv.writeheader()
                with open(self.file_path, 'a', newline='', encoding='utf-8') as fw:
                    fw_csv = csv.DictWriter(fw, fieldnames=fields)
                    # item_content = [item.get(field) for field in fields]
                    fw_csv.writerow(dict(item))
                return item
        elif spider.name == 'roundmenu_delivery':
            if item['url']not in rest_url_del:
                rest_url_del.append(item['url'])
                city = item.get('url').split('/')[3]
                self.file_name = "{}_delivery.csv".format(city)
                self.file_path = os.path.join(self.file_dir, self.file_name)
                if not os.path.exists(self.file_dir):
                    print(self.file_dir)
                    os.makedirs(self.file_dir)
                # 写表头
                if not os.path.exists(self.file_path):
                    with open(self.file_path, 'w', newline='', encoding='utf-8') as f:
                        f_csv = csv.DictWriter(f, fieldnames=fields)
                        f_csv.writeheader()
                with open(self.file_path, 'a', newline='', encoding='utf-8') as fw:
                    fw_csv = csv.DictWriter(fw, fieldnames=fields)
                    # item_content = [item.get(field) for field in fields]
                    fw_csv.writerow(dict(item))
                return item
        elif spider.name == 'roundmenu_cities':
            self.file_name = "cities.csv"
            self.file_path = os.path.join(self.file_dir, self.file_name)
            if not os.path.exists(self.file_dir):
                print(self.file_dir)
                os.makedirs(self.file_dir)
            # 写表头
            if not os.path.exists(self.file_path):
                with open(self.file_path, 'w', newline='', encoding='utf-8') as f:
                    f_csv = csv.DictWriter(f, fieldnames=fields_city)
                    f_csv.writeheader()
            with open(self.file_path, 'a', newline='', encoding='utf-8') as fw:
                fw_csv = csv.DictWriter(fw, fieldnames=fields_city)
                # item_content = [item.get(field) for field in fields]
                fw_csv.writerow(dict(item))
            return item

        # # 写入到csv
        # elif spider.name == 'roundmenu_app':
        #     if not os.path.exists(self.file_dir):
        #             os.makedirs(self.file_dir)
        #
        #     filename=os.path.join(self.file_dir,'shops.csv')
        #     with open(filename,'a',encoding='utf-8',newline='')as f:
        #         writer=csv.DictWriter(f,fieldnames=roundmenu_app_fields)
        #         if not os.path.getsize(filename):
        #             writer.writeheader()
        #         for rest in item['parse_list']:
        #             info = {}
        #             for header in roundmenu_app_fields:
        #                 info[header] = rest[header]
        #             writer.writerow(info)

        # 将数据写入到数据库
        elif spider.name == 'roundmenu_app':
            for rest in item['parse_list']:
                info = {}
                for header in roundmenu_app_fields:
                    info[header] = rest[header]
                self.mongoclient.insert_one('roundmenu',info,condition=['id'])

