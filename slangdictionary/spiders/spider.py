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

        if response.url == 'http://onlineslangdictionary.com/meaning-definition-of/10-2-2-10':
            inspect_response(response, self)
        
        # Extract word
        word = response.xpath('.//div[contains(@class,"term")]//h2//a[contains(@href,"/meaning-definition")]/text()')
        if not word: inspect_response(response, self)

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
        defs = response.xpath(xPathI)

        # Extract (II)
        xPathII = """
        .//div[@class="definitions"]/ul/li[not(a)]/text()[normalize-space()]
        """
        
        if not defs: # (I) was empty. Skip it
            defs = response.xpath(xPathII)
        else : # Merge (I) and (II)
            defs.extend(response.xpath(xPathII))
        
        defs = [d for d in defs if d] # Skip None elements if exist
        

        if not defs: inspect_response(response, self)
        
        print(response.url)
        print(f'scraping definition of: {word.extract()}')
        for d in defs:
            print(f'Definition: {d.extract()}')
        print('---------------------------------------------------------------')

        
        #
        # Make one item for each definition

        # Definition points to another word's definitions. Go get those
        # response meta = {'definition' : definition}


        return #loader.load_item()
    
