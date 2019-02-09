# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RestaurantScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    url = scrapy.Field()
    telephone = scrapy.Field()
    servesCuisine = scrapy.Field()
    priceRange = scrapy.Field()
    addressCountry = scrapy.Field()
    city = scrapy.Field()
    addressLocality = scrapy.Field()
    addressRegion = scrapy.Field()
    postalCode = scrapy.Field()
    streetAddress = scrapy.Field()
    ratingValue = scrapy.Field()
    reviewCount = scrapy.Field()
    bestRating = scrapy.Field()
    worstRating = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()


class CityScrapyItem(scrapy.Item):
    # define the fields for your item here like:
    count = scrapy.Field()
    country = scrapy.Field()
    city = scrapy.Field()
    url = scrapy.Field()