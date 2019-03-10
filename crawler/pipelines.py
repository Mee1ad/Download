# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import dataset
from crawler.items import MovieItem

# db = dataset.connect('postgresql://cfadnjxdppfkkk:b18cdc6213f46f54e567f10cf43f0e8605bff09afd8e88ab9c177f389949c521@ec2-54-83-22-244.compute-1.amazonaws.com:5432/dfjl0tt67bfv2a')
db = dataset.connect('sqlite:///movie.db')


class MoviePipeline(object):

    def process_item(self, item, spider):
        if not isinstance(item, MovieItem):
            return item
        table = db['movie']
        table.insert(dict(url=item['url'], imdb_id=item['imdb_id'], description=item['description']))

        for url, quality, encoder, size in zip(item['links'], item['quality'], item['encoder'], item['size']):
            table = db['link']
            table.insert(dict(link=url, quality=quality, encoder=encoder, size=size, imdb_id=item['imdb_id']))
        return item
