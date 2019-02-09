import os
import csv
from roundmenu_scrapy.settings import VERSION
from roundmenu_scrapy.mongodb_utils import get_db

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


if __name__ == '__main__':
    # 创建链接mongo数据库对象
    mongoclient=get_db()
    # 获取所有的数据
    data_info=mongoclient.all_items('roundmenu')

    # 将数据保存至csv文件
    path=os.path.join(os.path.dirname(__file__), '../crawlerOutput/{}/roundmenu'.format(VERSION))
    if not os.path.exists(path):
          os.makedirs(path)

    filename=os.path.join(path,'shops_mongo.csv')
    with open(filename,'a',encoding='utf-8',newline='')as f:
          writer=csv.DictWriter(f,fieldnames=roundmenu_app_fields)
          if not os.path.getsize(path):
                writer.writeheader()
          for data in data_info:
              writer.writerow(data)

    print('成功导出')