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

    def parse(self, response):
        links = response.css("div.r235 > div.posts > div.post-title > a::attr('href')").extract()
        for url in links:
            if self.exit != 1:
                yield scrapy.Request(url=url, callback=self.movie_details)
        self.page += 1
        next_link = self.base_link + f'page/{self.page}/'
        if self.page > 2:
            return
        yield scrapy.Request(next_link)

    def movie_details(self, response):
        movie = MovieItem()
        imdb_link = response.css('li.rate-imdb > a::attr("href")').extract()[0]
        pattern = '[a-z]{2}[0-9]+'
        movie['imdb_id'] = re.search(pattern, imdb_link)[0]
        db = dataset.connect('sqlite:///movie.db')
        duplicate_check = db['movie'].find_one(imdb_id=movie['imdb_id'])
        if duplicate_check is not None:
            self.exit = 1
            return
        movie['description'] = ''
        if response.css('div.History-post > p:nth-child(2)::text').extract() != []:
            movie['description'] = response.css('div.History-post > p:nth-child(2)::text').extract()[0]
        movie['links'] = response.css('div > a.dl_bx_mv::attr("href")').extract()
        movie['quality'] = response.css('li.quality_nvr > p::text').extract()
        movie['encoder'] = response.css('div.post-box > div > ul > li:nth-child(3) > p::text').extract()
        movie['size'] = response.css('div.post-box > div > ul > li:nth-child(4) > p::text').extract()
        yield movie
