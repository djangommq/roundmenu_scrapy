# -*- coding: utf-8 -*-
import os
import csv
import time
import json
import scrapy
from urllib.parse import urlencode


class RoundmenuAppSpider(scrapy.Spider):
    name = 'roundmenu_app'
    allowed_domains = ['apigateway.careemdash.com']
    # start_urls = ['http://apigateway.careemdash.com/']

    def __init__(self):
        self.city_fields=[
            "country",
            "city",
            "Top_left_lat",
            "Top_left_lng",
            "Bottom_right_lat",
            "Bottom_right_lng"
        ]
        self.city_path=os.path.join(os.path.dirname(__file__),'input/cities.csv')
        self.url="https://apigateway.careemdash.com/v1/listings/restaurants"


    def start_requests(self):
        with open(self.city_path,'r',encoding='utf-8',newline='')as f:
            reader=csv.DictReader(f,fieldnames=self.city_fields)
            for row in reader:
                if reader.line_num==1:
                    continue
                else:
                    country=row['country']
                    tlat=float(row['Top_left_lat'])
                    tlng=float(row['Top_left_lng'])
                    blat=float(row['Bottom_right_lat'])
                    blng=float(row['Bottom_right_lng'])
                    i=blat
                    while i<=tlat:
                        j=tlng
                        while j<=blng:
                            headers = {
                                'method': "GET",
                                'path': "/v1/listings/restaurants?section=popular&sort=recommended",
                                'authority': "apigateway.careemdash.com",
                                'scheme': "https",
                                'time-zone': "Asia/Shanghai",
                                'accept-language': "zh-CN",
                                'application': "careemfood-mobile-v1",
                                'meta': "android;production;12.0.0 (1360);5.0.2;PLK-TL01H",
                                'uuid': "c367c5b6-3bfd-401b-9a92-cf2af8559b95",
                                'lat': str(i),
                                'lng': str(j),
                                'authorization': "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhY2Nlc3NfdHlwZSI6Imd1ZXN0IiwidXNlcl9pZCI6MjkwMDYwLCJ1dWlkIjoiYzM2N2M1YjYtM2JmZC00MDFiLTlhOTItY2YyYWY4NTU5Yjk1IiwiYWNjZXNzX3Rva2VuIjoiTU9pOERTV2h5QlN1OWN4d3NUQVZOSHI4R3Z2V3BlMWdZY3U5SDlOMGxkVGRBS1pJelZzcG9IY3FkNm9PUEkwMiJ9.QXGTX3TB52uTLWjD_FB6CzDIJ6iEva4s2naEYM1RRmE",
                                'city-id': "1",
                                'accept-encoding': "gzip",
                                'user-agent': "okhttp/3.12.0",
                                'cache-control': "no-cache",
                                'Postman-Token': "190ca3cd-7f4e-47c3-9dd4-2a7dd7ae6e39"
                            }
                            querystring = {
                                "section": 'popular',
                                "sort": "recommended"
                            }
                            print(querystring)
                            page=2
                            # 请求其他页餐馆的请求参数信息列表
                            grouped_brand_ids = []
                            url=self.url+'?'+urlencode(querystring)
                            # 请求第一页餐馆列表
                            print(country+'\t请求 lat:'+str(i)+'\t'+'lng:'+str(j))
                            self.log_schedule(country+'\t请求 lat:'+str(i)+'\t'+'lng:'+str(j))
                            yield scrapy.Request(url=url,method='GET',headers=headers,callback=self.parse_restlist,meta={'page':page,'grouped_brand_ids':grouped_brand_ids,'headers':headers},dont_filter=True)

                            j+=0.01
                        i+=0.01


    # 解析其他页餐馆信息
    def parse_restlist(self, response):
        rest_list=[]
        info_page = json.loads(response.text)
        # 将第一页的餐馆加入到餐馆列表中
        rest_list.extend(info_page['restaurants'])

        # 获取每个餐馆的brand_id列表
        response.request.meta['grouped_brand_ids'].extend(self.get_brand_ids(response.text))

        # while response.request.meta['page']<=total_pages+1:
        querystring = {
            "section": 'popular',
            "sort": "recommended",
            "grouped_brand_ids": response.request.meta['grouped_brand_ids'],
            "page": response.request.meta['page']
        }
        url = self.url + '?' + urlencode(querystring)
        response.request.meta['page']+=1

        print(len(rest_list))
        # 请求第二页餐馆页
        if len(rest_list) != 0:
            yield scrapy.Request(url=url, method='GET', headers=response.request.meta['headers'], callback=self.parse_restlist,meta={'page':response.request.meta['page'], 'grouped_brand_ids':response.request.meta['grouped_brand_ids'],'headers':response.request.meta['headers']},dont_filter=True)
        # else:
        #     return
            # 解析餐馆信息
            parse_list=self.parse_info(rest_list)
            yield {'parse_list':parse_list}



    # 获取brand_id
    def get_brand_ids(self,res):
        rest_list = json.loads(res)['restaurants']
        grouped_brand_ids = []
        for rest in rest_list:
            grouped_brand_ids.append(rest['brand_id'])

        return grouped_brand_ids



    # 解析餐馆数据
    def parse_info(self,res_list):
      parse_list = []
      for res in res_list:
          # coordinate
          coordinate = res['coordinate']
          res1 = dict(res, **coordinate)
          # rating
          r = {}
          rating = res['rating']
          for k in rating.keys():
            r['rating_' + k] = rating[k]
          res2 = dict(res1, **r)
          # price
          p = {}
          price = res['price']
          for k in price.keys():
            p['price_' + k] = price[k]
          res3 = dict(res2, **p)
          # delivery
          d = {}
          delivery = res['delivery']
          for k in delivery.keys():
            d['delivery_' + k] = delivery[k]
          res4 = dict(res3, **d)

          parse_list.append(res4)

      return parse_list

    # 进度日志
    def log_schedule(self,str):
        filepath=os.path.join(os.path.dirname(__file__),'log')
        if not os.path.exists(filepath):
            os.makedirs(filepath)

        filename=os.path.join(filepath,'log.txt')
        with open(filename,'a',encoding='utf-8')as f:
            f.write(str+'\n')