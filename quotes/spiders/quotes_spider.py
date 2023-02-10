import scrapy
from ..items import QuoteLoader
import logging
from scrapy.utils.log import configure_logging 
from scrapy.utils.project import get_project_settings
from quotes.utils import LoggerFilter

# scrapy startproject abbreviation_scraper
# scrapy crawl quotes -o quotes.jsonl:jsonlines
# More examples and patterns: https://docs.scrapy.org/en/latest/intro/tutorial.html#intro-tutorial

# https://towardsdatascience.com/a-minimalist-end-to-end-scrapy-tutorial-part-i-11e350bcdec0
# https://github.com/harrywang/scrapy-tutorial/blob/master/tutorial/spiders/quotes_spider_v2.py
# https://datawookie.dev/blog/2021/06/scrapy-rotating-tor-proxy/

"""
TODO
Middlewares
pipelines -> database insert and has functions
check how not to be banned
"""

SETTINGS = get_project_settings()

class QuotesSpider(scrapy.Spider):

    allowed_domains = SETTINGS["ALLOWED_DOMAINS"] 
    name       = SETTINGS["BOT_NAME"]     
    start_urls = SETTINGS["START_URLS"]

    def __init__(self):
        
        configure_logging(
            settings = {
                "LOG_FILE"   : SETTINGS.get("LOG_FILE"),
                "LOG_FORMAT" : SETTINGS.get("LOG_FORMAT"),
                "LOG_LEVEL"  : SETTINGS.get("LOG_LEVEL")
            }
        )

        logging.getLogger('scrapy.core.scraper').addFilter(LoggerFilter())

        return 


    def parse(self, response):
        """ Handler for the response downloaded for each of the requests made
            Inputs: response -> Instance of TextResponse that holds the page content
        """

        for quoteDiv in response.xpath('//div[@class="quote"]'):
                
            # Parse item and proceed to the author page
            quoteItem = self.parseItem(quoteDiv)

            # Next, go to and parse the author page
            yield from response.follow_all(
                urls     = quoteDiv.xpath('.//span[contains(text(), "by")]/a/@href').extract(),
                callback = self.parseAuthor, 
                meta     = {'item' : quoteItem}
            )
            
        # Yield link to the next page
        yield from response.follow_all(
            xpath    = '//li[@class="next"]//@href', 
            callback = self.parse
        )

        return


    def parseItem(self, response):
        """ Parser for the item details """

        loader = QuoteLoader(selector = response)
        loader.add_xpath(field_name = 'quote',  xpath = './/span[@class = "text"]/text()')
        loader.add_xpath(field_name = 'author', xpath = './/small[@class = "author"]/text()')
        loader.add_xpath(field_name = 'tag',    xpath = './/meta[@class = "keywords"]/@content')
        return loader.load_item()


    def parseAuthor(self, response):
        """ Parser for the author details """

        loader = QuoteLoader(item = response.meta['item'], selector = response)
        loader.add_xpath(field_name = 'author_birthdate', xpath = '//span[@class = "author-born-date"]/text()')
        loader.add_xpath(field_name = 'author_birth_loc', xpath = '//span[@class = "author-born-location"]/text()')
        loader.add_xpath(field_name = 'author_bio',       xpath = '//div[@class = "author-description"]/text()')

        yield loader.load_item()