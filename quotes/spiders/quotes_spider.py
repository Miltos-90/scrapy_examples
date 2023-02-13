from ..items import QuoteLoader

from scrapy import Spider
from scrapy.utils.project import get_project_settings
from scrapy.http import TextResponse
from scrapy.item import Item
from ..databases import QuoteDatabase

SETTINGS = get_project_settings()


class QuotesSpider(Spider):

    def __init__(self):

        self.allowed_domains = SETTINGS["ALLOWED_DOMAINS"]
        self.start_urls      = SETTINGS["START_URLS"]
        self.name            = SETTINGS["BOT_NAME"]
        self.db              = QuoteDatabase()


    def parse(self, response: TextResponse):
        """ Handler for the response downloaded for each of the requests made
            Inputs: response -> Instance of TextResponse that holds the page content
        """

        for quoteDiv in response.xpath('//div[@class="quote"]'):
            
            self.db.connect()
            quoteItem = self._parseItem(quoteDiv)
            dbOut = self.db.getAuthor(quoteItem['author'])
            self.db.close()

            if dbOut is not None:
                yield self._attachAuthor(quoteItem, dbOut)
                
            else:
                yield from response.follow_all(
                    urls        = quoteDiv.xpath('.//span[contains(text(), "by")]/a/@href').extract(),
                    callback    = self._parseAuthor, 
                    dont_filter = True,
                    meta        = {'item' : quoteItem}
                )
            
        # Yield link to the next page
        yield from response.follow_all(
            xpath    = '//li[@class="next"]//@href', 
            callback = self.parse
        )

        return

    def _parseItem(self, response: TextResponse):
        """ Parser for the item details """

        loader = QuoteLoader(selector = response)
        loader.add_xpath(field_name = 'quote',  xpath = './/span[@class = "text"]/text()')
        loader.add_xpath(field_name = 'author', xpath = './/small[@class = "author"]/text()')
        loader.add_xpath(field_name = 'tag',    xpath = './/meta[@class = "keywords"]/@content')
        return loader.load_item()


    def _parseAuthor(self, response: TextResponse):
        """ Parser for the author details """

        loader = QuoteLoader(item = response.meta['item'], selector = response)
        loader.add_xpath(field_name = 'author_birthdate', xpath = '//span[@class = "author-born-date"]/text()')
        loader.add_xpath(field_name = 'author_birth_loc', xpath = '//span[@class = "author-born-location"]/text()')
        loader.add_xpath(field_name = 'author_bio',       xpath = '//div[@class = "author-description"]/text()')

        yield loader.load_item()

    def _attachAuthor(self, item: Item, authorData: tuple):
        """ Adds author information from the existing database """

        _, _, birthDate, birthPlace, bio = authorData
        loader = QuoteLoader(item = item)
        loader.add_value(field_name = 'author_birthdate', value = birthDate)
        loader.add_value(field_name = 'author_birth_loc', value = birthPlace)
        loader.add_value(field_name = 'author_bio',       value = bio)

        return loader.load_item() 