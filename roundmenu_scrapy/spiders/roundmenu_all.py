# -*- coding: utf-8 -*-
import csv
import re
import json
import logging
import traceback

import os
import scrapy
from bs4 import BeautifulSoup

from roundmenu_scrapy.items import RestaurantScrapyItem
from roundmenu_scrapy.pipelines import fields, fields_city
from roundmenu_scrapy.settings import VERSION


def load_urls():
    current_dir = os.path.split(__file__)[0]
    cities_path = current_dir + '/../../../crawlerOutput/{}/roundmenu/cities.csv'.format(VERSION)
    print(cities_path)
    result = []
    with open(cities_path, 'r', encoding='utf-8') as f:
        csv_reader = csv.DictReader(f, fieldnames=fields_city)
        for row in csv_reader:
            if csv_reader.line_num == 1:
                continue
            else:
                result.append(dict(row))
        return result


class RoundmenuSpider(scrapy.Spider):
    name = 'roundmenu_all'
    allowed_domains = ['roundmenu.com']
    # start_urls = ['http://roundmenu.com/']

    def __init__(self,query,**kwargs):
        self.query=query
        super().__init__(**kwargs)
        self.basic_url = 'https://www.roundmenu.com'
        self.headers = {
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0(WindowsNT6.1;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/68.0.3440.106Safari/537.36',
        }

    def start_requests(self):
        urls = load_urls()
        # for url in urls:
        #     tem_url=url.get('url')
        #     yield scrapy.Request(url=tem_url, headers=self.headers, callback=self.parse_url)
        yield scrapy.Request(url=urls[int(self.query)].get('url'), headers=self.headers, callback=self.parse_url)

    def parse_url(self,response):
        soup =BeautifulSoup(response.text,'html.parser')
        a_list=soup.select('ul.nav-submenu-items.themes.active li a')
        url_list = []
        for a in a_list:
            url_list.append(a.get('href'))

        for url in url_list:
            new_url=response.urljoin(url)
            yield scrapy.Request(url=new_url, headers=self.headers, callback=self.parse)

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        try:
            count_tag = soup.find('div', {'id': 'main-content-container'}).find('script', {'type': 'text/javascript'})
            # print(count_tag.text)
            with open('test.txt', 'w', encoding='utf-8') as f:
                f.write(response.text)
            # pagecount = int(count_tag.text.split(';')[10].split('=')[1])+20
            pagecount=50
            # r_urls = soup.find_all('h4')

            timeid=re.findall('<meta property="al:ios:url" content="roundmenu://search/cuisine_ids:0/locations:0/theme:(\d+)/sort:rank"',response.text)[0]
            for i in range(2, pagecount+1):
                a_url='https://www.roundmenu.com/frontend/index/ajaxsearchrestaurants?page={}'.format(i)
                formdata = {
                    'themeId': timeid,
                    'searchType': 'theme'
                }
                yield scrapy.FormRequest(url=a_url, headers=self.headers, formdata=formdata, callback=self.parse_list,dont_filter=True)

            # for r_url in r_urls:
            #     url = r_url.find('a').get('href')
            #     yield scrapy.Request(url=url, headers=self.headers, callback=self.parse_info)


        except Exception as e:
            with open('mark_faild.txt', 'a', encoding='utf-8') as f:
                f.write(response.url)


    def parse_list(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        # 每次大约30个餐馆
        r_urls = soup.find_all('h4')
        for r_url in r_urls:
            tmp_url = r_url.find('a').get('href')
            yield scrapy.Request(url=tmp_url, headers=self.headers, callback=self.parse_info,dont_filter=True)

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
            logging.warning('************')
            logging.warning(js_text)
            logging.warning(e, traceback.format_exc())
