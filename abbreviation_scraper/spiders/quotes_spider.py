import scrapy
from ..items import QuoteLoader, QuoteItem

# scrapy startproject abbreviation_scraper
# scrapy crawl quotes -o quotes.jsonl:jsonlines
# More examples and patterns: https://docs.scrapy.org/en/latest/intro/tutorial.html#intro-tutorial

# https://towardsdatascience.com/a-minimalist-end-to-end-scrapy-tutorial-part-i-11e350bcdec0
# https://github.com/harrywang/scrapy-tutorial/blob/master/tutorial/spiders/quotes_spider_v2.py
# https://datawookie.dev/blog/2021/06/scrapy-rotating-tor-proxy/


""" TODO
1.    Check if page has been scraped inside parse. If it has, skip. Perhaps logging retains this info?
     (it might be slow re-reading constantly the logging file)
        CREATE TABLE IF NOT EXISTS pages (
        id          INTEGER PRIMARY KEY,
        url         TEXT    UNIQUE NOT NULL,
        date        TEXT    NOT NULL
    );
2. Clean up hardcoded constants
3. Check how logging works here
"""


class QuotesSpider(scrapy.Spider):

    name            = "quotes"                  # Unique spider ID
    allowed_domains = ['quotes.toscrape.com']   # Do not stray from this
    start_urls      = [                         # Initial URL to start crawling from
        'https://quotes.toscrape.com/page/1/'
        ]

    def parse(self, response):
        """ Handler for the response downloaded for each of the requests made
            Inputs: response -> Instance of TextResponse that holds the page content
        """

        

        if self.isOK(response):

            for quoteDiv in response.xpath('//div[@class="quote"]'):
                
                # Parse item details (can be put directly in the follow_all)
                quoteItem = self.parseItem(quoteDiv)

                # Next, go to and parse the author page
                yield from response.follow_all(
                    urls     = quoteDiv.xpath('.//span[contains(text(), "by")]/a/@href').extract(),
                    callback = self.parseAuthor, 
                    meta     = {'item' : quoteItem}
                )

        # Yield link to the next page
        yield from response.follow_all(xpath = '//li[@class="next"]//@href', callback = self.parse)

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


    @staticmethod
    def isOK(response):
        """ Checks if the appropriate response has been received from the server """
        return response.status == 200
