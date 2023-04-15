from scrapy.utils.project import get_project_settings
from scrapy.http import Response
from ..items import WordLoader
from scrapy import Spider

SETTINGS = get_project_settings()


class SlangSpider(Spider):

    name            = SETTINGS["BOT_NAME"]
    start_urls      = SETTINGS["START_URLS"]
    allowed_domains = SETTINGS["ALLOWED_DOMAINS"]
    custom_settings = SETTINGS["CUSTOM_SPIDER_SETTINGS"]

    def parse(self, response: Response):
        """ Handler for the response downloaded for each of the requests made """
        
        # Scrape words
        for word in response.xpath('.//table[@class="wordlist"]//@href'): 
            yield self._parseItem(word)

        # Yield link to the next page
        yield from response.follow_all( 
            xpath    = './/table[@class="nav"]//td/a/@href',
            callback = self.parse)

        return


    def _parseDefinitions(self, response: Response):
        """ Parser for the item details """
        # TODO: Fix the below
        # TODO: Deal with nested link http://onlineslangdictionary.com/meaning-definition-of/5-by-5

        loader = WordLoader(selector = response)
        loader.add_xpath(field_name = 'quote',    xpath = './/span[@class = "text"]/text()')
        loader.add_xpath(field_name = 'author',   xpath = './/small[@class = "author"]/text()')
        loader.add_xpath(field_name = 'keywords', xpath = './/meta[@class = "keywords"]/@content')
        return loader.load_item()