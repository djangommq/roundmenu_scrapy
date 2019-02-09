# -*- coding: utf-8 -*-
import json
import logging
import traceback

import scrapy
from bs4 import BeautifulSoup

from roundmenu_scrapy.items import RestaurantScrapyItem, CityScrapyItem
from roundmenu_scrapy.pipelines import fields


class RoundmenuSpider(scrapy.Spider):
    name = 'roundmenu_cities'
    allowed_domains = ['roundmenu.com']
    # start_urls = ['http://roundmenu.com/']

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.basic_url = 'https://www.roundmenu.com'
        self.headers = {
            'Referer': 'https://www.roundmenu.com',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0(WindowsNT6.1;Win64;x64)AppleWebKit/537.36(KHTML,likeGecko)Chrome/68.0.3440.106Safari/537.36',
        }

    def start_requests(self):
        start_url = 'https://www.roundmenu.com'
        # 请求网址,将响应信息交给解析函数parse解析
        yield scrapy.Request(url=start_url, headers=self.headers, callback=self.parse)

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        cities = []
        # 获取所有的城市名, 构造请求
        city_box = soup.find('div', {'class': 'city-box'})
        a_tags = city_box.find_all('a')
        # countries_menu_tags = city_box.find_all('li', {'class': 'countries-menu'})
        count = 0
        for a_tag in a_tags:
            tmp_city = {
                    'city': a_tag.text,
                    'url': a_tag.get('href'),
            }
            count += 1
            item = CityScrapyItem()
            item['city'] = a_tag.text
            item['count'] = count
            item['url'] = a_tag.get('href')
            cities.append(tmp_city)
            print(tmp_city)
            yield item
        # for countries_menu_tag in countries_menu_tags:
        #     # h3_tags = countries_menu_tag.city_box.find_all('h3')
        #     ul_tags = countries_menu_tag.city_box.find_all('ul')
        #     for i in range(len()):
        #         h3_tag = h3_tags[i]
        #         city_tags = ul_tags[i].find_all('a')
        #         tmp_country = h3_tag.text
        #         for city_tag in city_tags:
        #             tmp_city = {
        #                 'country': tmp_country,
        #                 'city': city_tag.text,
        #                 'url': city_tag.get('href'),
        #             }
        #             count += 1
        #             item = CityScrapyItem()
        #             item['country'] = tmp_country
        #             item['city'] = city_tag.text
        #             item['count'] = count
        #             item['url'] = city_tag.get('href')
        #             cities.append(tmp_city)
        #             print(tmp_city)
        #             yield item
