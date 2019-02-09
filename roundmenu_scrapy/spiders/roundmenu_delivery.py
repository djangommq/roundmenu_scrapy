# -*- coding: utf-8 -*-
import csv
import json
import logging
import traceback

import scrapy
from bs4 import BeautifulSoup

from roundmenu_scrapy.items import RestaurantScrapyItem
from roundmenu_scrapy.pipelines import fields
from roundmenu_scrapy.spiders.roundmenu_all import load_urls


class RoundmenuSpider(scrapy.Spider):
    name = 'roundmenu_delivery'
    allowed_domains = ['roundmenu.com']
    # start_urls = ['http://roundmenu.com/']

    def __init__(self, query,**kwargs):
        self.query=query
        super().__init__(**kwargs)
        self.basic_url = 'https://www.roundmenu.com'
        self.headers = {
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0(WindowsNT6.1;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/68.0.3440.106Safari/537.36',
        }

    def start_requests(self):
        # 使用该方法获取文件中所有的城市信息,以列表的形式返回
        urls = load_urls()
        yield scrapy.Request(url=urls[int(self.query)].get('url'), headers=self.headers, callback=self.parse_delivery_url)

    # ajax请求获取参观页面
    def parse_delivery_url(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        # print(response.status)
        delivery_tag = soup.find('a', {'title': 'Delivery'})
        delivery_url = delivery_tag.get('href')
        delivery_count = int(delivery_tag.text.split('(')[1].split(')')[0])

        pagecount = int(delivery_count/20) + 5
        for i in range(1, pagecount+1):
            new_url = "https://www.roundmenu.com/frontend/index/deliveryrestaurantsajax?page={}".format(i)
            formdata = {
                'aid': '0',
            }
            # ajax请求:https://www.roundmenu.com/frontend/index/deliveryrestaurantsajax?page=*
            yield scrapy.FormRequest(url=new_url, headers=self.headers, formdata=formdata, callback=self.parse_list,dont_filter=True)

    # 获取每个餐馆url并请求
    def parse_list(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        # 每次大约30个餐馆
        r_urls = soup.find_all('h4')
        for r_url in r_urls:
            tmp_url = r_url.find('a').get('href')
            yield scrapy.Request(url=tmp_url, headers=self.headers, callback=self.parse_info)

    # 解析每个餐馆url请求结果,获取每个餐馆的信息
    def parse_info(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        js_text = soup.find_all('script', {'type':'application/ld+json'})[1].text
        js_text = js_text.replace('\n', '')
        js_text = js_text.encode('utf-8', 'ignore').decode('utf-8')
        # logging.error(js_text)
        try:
            try:
                data = json.loads(js_text, strict=False)
            except:
                data = json.loads(js_text.split('<script>')[0]+'"}]}', strict=False)

            item = RestaurantScrapyItem()

            item['url'] = data.get('@id')
            item['name'] = data.get('name')
            item['telephone'] = data.get('telephone')
            item['priceRange'] = data.get('priceRange')
            item["servesCuisine"] = data.get("servesCuisine")
            item['addressCountry'] = data.get('address').get('addressCountry')
            item['addressLocality'] = data.get('address').get('addressLocality')
            item['addressRegion'] = data.get('address').get('addressRegion')
            item['postalCode'] = data.get('address').get('postalCode')
            item['streetAddress'] = data.get('address').get('streetAddress')
            aggregate = data.get('aggregateRating')
            if aggregate is not None:
                item['ratingValue'] = data.get('aggregateRating').get('ratingValue')
                item['reviewCount'] = data.get('aggregateRating').get('reviewCount')
                item['bestRating'] = data.get('aggregateRating').get('bestRating')
                item['worstRating'] = data.get('aggregateRating').get('worstRating')
            item['latitude'] = data.get('geo').get('latitude')
            item['longitude'] = data.get('geo').get('longitude')

            yield item
        except Exception as e:
            logging.warning('********item错误')
            logging.warning(js_text)
            logging.warning(e, traceback.format_exc())
