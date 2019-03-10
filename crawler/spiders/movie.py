import scrapy.spiders
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
import re
import dataset
from crawler.items import MovieItem
import os


class MovieSpider(scrapy.Spider):
    name = "movie"
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def __init__(self, *args, **kwargs):
        self.allowed_domains = ['1fardadl.com']
        self.base_link = 'https://www1.1fardadl.com/category/%D9%81%DB%8C%D9%84%D9%85-%D8%AE%D8%A7%D8%B1%D8%AC%DB%8C/'
        self.page = 1
        self.start_urls = [self.base_link + f'page/{self.page}/', ]
        self.rules = Rule(LinkExtractor(allow=r'page/[1-1]/'), callback='parse', follow=True)
        self.exit = 0
        self.movie = MovieItem()
        # self.db = dataset.connect('postgresql://cfadnjxdppfkkk:b18cdc6213f46f54e567f10cf43f0e8605bff09afd8e88ab9c177f389949c521@ec2-54-83-22-244.compute-1.amazonaws.com:5432/dfjl0tt67bfv2a')
        self.db = db = dataset.connect('sqlite:///movie.db')

    def parse(self, response):
        links = response.css("div.r235 > div.posts > div.post-title > a::attr('href')").extract()
        for url in links:
            duplicate_check = self.db['movie'].find_one(url=url)
            if duplicate_check is None:
                print('new movie:', url)
                yield scrapy.Request(url=url, callback=self.movie_details)
            else:
                print('duplicate is:', url)
                return
        self.page += 1
        next_link = self.base_link + f'page/{self.page}/'
        # if self.page > 3:
        #     return
        yield scrapy.Request(next_link)

    def movie_details(self, response):
        self.movie['url'] = response.url
        imdb_link = response.css('li.rate-imdb > a::attr("href")').extract()[0]
        pattern = '[a-z]{2}[0-9]+'
        self.movie['imdb_id'] = re.search(pattern, imdb_link)[0]
        self.movie['description'] = ''
        if response.css('div.History-post > p:nth-child(2)::text').extract() != []:
            self.movie['description'] = response.css('div.History-post > p:nth-child(2)::text').extract()[0]
        self.movie['links'] = response.css('div > a.dl_bx_mv::attr("href")').extract()
        self.movie['quality'] = response.css('li.quality_nvr > p::text').extract()
        self.movie['encoder'] = response.css('div.post-box > div > ul > li:nth-child(3) > p::text').extract()
        self.movie['size'] = response.css('div.post-box > div > ul > li:nth-child(4) > p::text').extract()
        yield self.movie
