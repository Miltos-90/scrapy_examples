from scrapy.utils.project import get_project_settings
from ..items import QuoteLoader, AuthorLoader
from scrapy.http import Response
from scrapy import Spider

SETTINGS = get_project_settings()


class QuotesSpider(Spider):
    """ Spider to crawl quote and author information. """

    name            = SETTINGS["BOT_NAME"]
    start_urls      = SETTINGS["START_URLS"]
    allowed_domains = SETTINGS["ALLOWED_DOMAINS"]
    custom_settings = SETTINGS["CUSTOM_SPIDER_SETTINGS"]

    def parse(self, response: Response):
        """ Handler for the response downloaded for each of the requests made """
        
        # Loop over all quotes
        for quote in response.xpath('//div[@class="quote"]'):
            
            yield self._parseItem(quote) # Scrape quote
            
            # Scrape author
            xPathStr = './/span[contains(text(), "by")]/a/@href'
            yield from response.follow_all(
                urls     = quote.xpath(xPathStr).extract(),
                callback = self._parseAuthor)

        yield from response.follow_all( # Yield link to the next page
            xpath    = '//li[@class="next"]//@href', 
            callback = self.parse)

        return


    def _parseItem(self, response: Response):
        """ Parser for the item details """

        loader = QuoteLoader(selector = response)
        loader.add_xpath(field_name = 'quote',    xpath = './/span[@class = "text"]/text()')
        loader.add_xpath(field_name = 'author',   xpath = './/small[@class = "author"]/text()')
        loader.add_xpath(field_name = 'keywords', xpath = './/meta[@class = "keywords"]/@content')
        return loader.load_item()


    def _parseAuthor(self, response: Response):
        """ Parser for the author details """

        loader = AuthorLoader(selector = response)
        loader.add_xpath(field_name = 'name',      xpath = '//h3[@class = "author-title"]/text()')
        loader.add_xpath(field_name = 'birthdate', xpath = '//span[@class = "author-born-date"]/text()')
        loader.add_xpath(field_name = 'birthplace', xpath = '//span[@class = "author-born-location"]/text()')
        loader.add_xpath(field_name = 'bio',       xpath = '//div[@class = "author-description"]/text()')
        yield loader.load_item()