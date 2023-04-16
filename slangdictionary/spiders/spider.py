from scrapy.utils.project import get_project_settings
from scrapy.http import Response
#from .slangdictionary.items import WordLoader
from scrapy import Spider

from scrapy.shell import inspect_response

SETTINGS = get_project_settings()


class SlangSpider(Spider):

    name            = SETTINGS["BOT_NAME"]
    start_urls      = SETTINGS["START_URLS"]
    allowed_domains = SETTINGS["ALLOWED_DOMAINS"]
    custom_settings = SETTINGS["CUSTOM_SPIDER_SETTINGS"]


    def parse(self, response: Response):
        """ Handler for the response downloaded for each of the requests made """


        # Yield all links to the individual word pages
        yield from response.follow_all( 
            xpath    = './/table[@class="wordlist"]//@href', 
            callback = self._parseItem)
        
        # Yield link to the next pages
        #yield from response.follow_all( 
        #    xpath    = './/table[@class="nav"]//td/a/@href',
        #    callback = self.parse)

        return


    def _parseItem(self, response: Response):
        """ Parser for the item details """
        # TODO: Fix the below
        # TODO: Deal with nested link http://onlineslangdictionary.com/meaning-definition-of/5-by-5


        #loader = WordLoader(selector = response)
        
        # Extract word
        wordSelector  = response.xpath('.//div[@class="term featured"]//h2//a[contains(@href, "/meaning-definition")]/text()')

        # Extract definitions. These can be one or more of the following two:
        # (I)  The concatenated text of li with the text of a that contains an href "/meaning-definition-of/..." inside it
        # (II) The text of li (only) if it does not contain a

        # Extract (I)
        xPathI = """
        concat(
        .//div[@class="definitions"]/ul/li[a[contains(@href, "/meaning-definition-of/")]]/text()[normalize-space()],
        .//div[@class="definitions"]/ul/li/a/text()[normalize-space()]
        )
        """

        # Extract (II)
        xPathII = """
        .//div[@class="definitions"]/ul/li[not(a)]/text()[normalize-space()]
        """
        
        defSelectors = response.xpath(xPathI)
        defSelectors.extend(response.xpath(xPathII))
        
        print(response.url)
        print(f'scraping definition of: {wordSelector.extract()}')
        if not defSelectors:
            print(f'Definitions not found')
        else:
            for d in defSelectors:
                print(f'Definition: {d.extract()}')

        print('---------------------------------------------------------------')

        
        #inspect_response(response, self)
        # Make one item for each definition

        # Definition points to another word's definitions. Go get those
        # response meta = {'definition' : definition}


        return #loader.load_item()
    
