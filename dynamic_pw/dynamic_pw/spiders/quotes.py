import scrapy
from scrapy.utils.response import open_in_browser

#scrapy crawl quotes # -L INFO (for less details in console)
# ctr + shift + p to enable / disable javascript
#xhr -> to check response data from server

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    
    def start_requests(self):
        yield scrapy.Request(
            url="http://quotes.toscrape.com/js/",
            meta={"playwright":True},
        )

    def parse(self, response):
        for q in response.css('.quote'):
            yield {
                'author': q.css('.author ::text').get(),
                'quote': q.css('.text ::text').get()
            }
