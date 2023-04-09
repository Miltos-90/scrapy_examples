from ..items import QuoteLoader

from scrapy import Spider
from scrapy.utils.project import get_project_settings
from scrapy.http import TextResponse
from scrapy.item import Item
from quotes import QuotesDatabase
import logging

SETTINGS = get_project_settings()


class QuotesSpider(Spider):

    allowed_domains = SETTINGS["ALLOWED_DOMAINS"]
    start_urls      = SETTINGS["START_URLS"]
    name            = SETTINGS["BOT_NAME"]

    def parse(self, response: TextResponse):
        """ Handler for the response downloaded for each of the requests made
            Inputs: response -> Instance of TextResponse that holds the page content
        """     
        
        if self._isNewUrl(response.url):

            for quoteDiv in response.xpath('//div[@class="quote"]'):
                
                quoteItem = self._parseItem(quoteDiv)
                authorDB  = self._getAuthorFromDB(quoteItem['author'])

                if authorDB is not None:
                    yield self._attachExistingAuthor(quoteItem, authorDB)
                
                else:
                    yield from response.follow_all(
                        urls        = quoteDiv.xpath('.//span[contains(text(), "by")]/a/@href').extract(),
                        meta        = {'item' : quoteItem},
                        callback    = self._parseAuthor, 
                        dont_filter = True
                    )

            self._addURL(response)

        else:
            logging.debug(f"Bypassed {response.url}")
        
        # Yield link to the next page
        yield from response.follow_all(
            xpath    = '//li[@class="next"]//@href', 
            callback = self.parse
        )

        return


    def _getAuthorFromDB(self, name: str):
        """ Grabs author data from the DB given its name """

        QuotesDatabase.connect()
        query = "SELECT * FROM authors WHERE name = ?;"
        task  = (name, )
        authorDB = QuotesDatabase.cursor.execute(query, task).fetchone()
        QuotesDatabase.close()

        return authorDB


    def _isNewUrl(self, url: str):
        """ Checks if URL has been already scraped """

        QuotesDatabase.connect()
        query  = "SELECT * FROM pages WHERE url = ?;"
        newURL = QuotesDatabase.cursor.execute(query, (url, )).fetchone()
        QuotesDatabase.close()

        return newURL is None


    def _addURL(self, response: TextResponse):
        """ Adds scraped URL to the database """

        QuotesDatabase.connect()
        query = "INSERT INTO pages (url, date, status_code, crawl_success) VALUES (?, ?, ?, ?);"
        task  = (response.url, response.headers['date'].decode("utf-8"), response.status, 1)
        QuotesDatabase.cursor.execute(query, task)
        QuotesDatabase.close()

        address = response.request.meta['IPaddress']
        fingerprint = response.request.meta['fingerprint']
        nickname =response.request.meta['nickname']
        locale = response.request.meta['locale']

        with open('./output.txt', mode = 'a', encoding = 'utf-8') as f:
            f.write("\n")
            f.write("====================================================\n")
            f.write("  Exit relay for our connection to %s\n" % (response.url))
            f.write("  address: %s\n" % address)
            f.write("  fingerprint: %s\n" % fingerprint)
            f.write("  nickname: %s\n" % nickname)
            f.write("  locale: %s\n" % locale)
            f.write("====================================================")
            f.write("\n")

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


    def _attachExistingAuthor(self, item: Item, authorData: tuple):
        """ Adds author information from the existing database """

        _, _, birthDate, birthPlace, bio = authorData
        loader = QuoteLoader(item = item)
        loader.add_value(field_name = 'author_birthdate', value = birthDate)
        loader.add_value(field_name = 'author_birth_loc', value = birthPlace)
        loader.add_value(field_name = 'author_bio',       value = bio)
        return loader.load_item()