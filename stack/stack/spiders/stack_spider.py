from scrapy import Spider
from scrapy.selector import Selector

from stack.items import StackItem

class StackSpider(Spider):
    name = "stack"
    #base URL
    allowed_domains = ["stackoverflow.com"]
    start_urls = [
        "http://stackoverflow.com/questions?pagesize=50&sort=newest",
    ]
    def parse(self, response):
        questions = Selector(response).xpath('//div[@class="s-post-summary--content-title"]/h3')
        
        for q in questions:
            item = StackItem()
            item.title = q.xpath('//a[@class="s-link"]/text()').extract()[0]
            item.url = q.xpath('//a[@class="s-link"]/@href').extract()[0]
            yield item