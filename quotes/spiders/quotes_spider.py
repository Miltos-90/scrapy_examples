from ..items import QuoteLoader, AuthorLoader
from scrapy import Spider
from scrapy.utils.project import get_project_settings
from scrapy.http import Response
from quotes import QuotesDatabase

SETTINGS = get_project_settings()


class QuotesSpider(Spider):

    allowed_domains = SETTINGS["ALLOWED_DOMAINS"]
    start_urls      = SETTINGS["START_URLS"]
    name            = SETTINGS["BOT_NAME"]
    custom_settings = {'JOBDIR': './crawls/quotes_spider'}

    def parse(self, response: Response):
        """ Handler for the response downloaded for each of the requests made
        """     

        # Loop over all quotes
        for quoteDiv in response.xpath('//div[@class="quote"]'):
            
            # Scrape quote
            yield self._parseItem(quoteDiv)
            
            # Scrape author
            xPathStr = './/span[contains(text(), "by")]/a/@href'
            yield from response.follow_all(
                urls     = quoteDiv.xpath(xPathStr).extract(),
                callback = self._parseAuthor
                )

        #self._addURL(response)

        # Yield link to the next page
        yield from response.follow_all(
            xpath    = '//li[@class="next"]//@href', 
            callback = self.parse
        )

        return

    def _addURL(self, response: Response):
        """ Adds scraped URL to the database """

        query = """
            INSERT OR IGNORE INTO 
            pages (url, status_code, date, fingerprint, IP_address, server_name, locale) 
            VALUES (?, ?, ?, ?, ?, ?, ?);
            """
        task = (
            response.url,                               # url
            response.status,                            # status_code
            response.headers['date'].decode("utf-8"),   # date
            response.request.meta['fingerprint'],       # fingerprint
            response.request.meta['IPaddress'],         # IP_address
            response.request.meta['nickname'],          # server_name
            response.request.meta['locale'],            # locale
        )
        
        QuotesDatabase.connect()
        QuotesDatabase.cursor.execute(query, task)
        QuotesDatabase.close()

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