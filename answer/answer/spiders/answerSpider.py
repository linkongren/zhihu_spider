# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from selenium import webdriver

class AnswerspiderSpider(scrapy.Spider):
    name = 'answerSpider'
    allowed_domains = ['zhihu.com']
    start_url = 'https://zhihu.com'
    cookie_file = "./cookie_file"
    path = "./"

    def __init__(self):
        driver = webdriver.Chrome()
        driver.set_page_load_timeout(10)
        driver.get("https://www.baidu.com")
        with open(self.cookie_file, "r") as fin:
            for line in fin:
                name, value, domain = line.strip().split("\t")
                cookie = {"name" : name, "value" : value, "domain" : domain}
                driver.add_cookie(cookie)
        self.driver = driver

    def start_requests(self):
        yield Request(url = self.start_url, meta = {"num" : 1}, callback = self.parse)


    def parse(self, response):
        vote_up = 0
        length = 0
        alist = response.xpath("//div[@class='Card TopstoryItem TopstoryItem-isRecommend']")
        for list in alist:
            vote = list.xpath("./descendant::*[@itemprop='upvoteCount']/@content")
            if len(vote.extract()) < 1:
                continue;
            if int(vote.extract()[0]) < 500:
                continue;
            vote_up = int(vote.extract()[0])


            con_list = list.xpath("./descendant::*[@class='RichText ztext CopyrightRichText-richText']/p")
            for con in con_list:
                test = con.xpath("./text()").extract()
                if len(test) > 0:
                    length = length + len(test[0])
                if length > 3000:
                    break;
            if length > 3000 or length == 0:
                continue;

            title = list.xpath("./descendant::*[@target='_blank']/text()")
            print(title[0].extract())
            print("点赞数： %d\n" % vote_up)
            print("文章长度： %d" % length)
            for con in con_list:
                test = con.xpath("./text()").extract()
                print(test)
            print("\n")
        #yield Request(url = "https://www.cnblogs.com/flowingcloud/p/5689513.html", callback = self.parse)
        if(response.meta["num"] < 10):
            num = response.meta["num"] + 1
            yield Request(url = "https//:www.baidu.com", meta = {"num" : num})
            yield Request(url = self.start_url, meta = {"num" : num}, callback = self.parse)

















