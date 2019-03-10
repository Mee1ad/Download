# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MovieItem(scrapy.Item):
    url = scrapy.Field()
    description = scrapy.Field()
    links = scrapy.Field()
    quality = scrapy.Field()
    encoder = scrapy.Field()
    size = scrapy.Field()
    subtitle = scrapy.Field()
    imdb_id = scrapy.Field()
