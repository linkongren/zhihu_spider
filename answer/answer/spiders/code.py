# -*- coding: utf-8 -*-
import scrapy


class CodeSpider(scrapy.Spider):
    name = 'code'
    allowed_domains = ['zhihu.com']
    start_urls = ['http://zhihu.com/']

    def parse(self, response):
        pass
