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
        # Handler for the response downloaded for each of the requests made #


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
        word = response.xpath('.//div[contains(@class,"term")]//h2//a[contains(@href,"/meaning-definition")]/text()')

        # Extract definitions.
        defs = []
        for dLink in response.xpath('//div[@class="definitions"]/ul/li'):
            #inspect_response(response, self)

            blockQuoteExists     = bool(int(dLink.xpath('boolean(./blockquote)').extract_first()))
            lineBreakExists      = bool(int(dLink.xpath('boolean(./br)').extract_first()))
            
            if lineBreakExists:
                
                d = dLink.xpath("""
                    ./br[1]/preceding-sibling::text()[normalize-space()]
                    |
                    ./br[1]/preceding-sibling::*//text()[normalize-space()]
                """)
            
            elif blockQuoteExists:

                d = dLink.xpath("""
                    ./blockquote[1]/preceding-sibling::text()[normalize-space()]
                    |
                    ./blockquote[1]/preceding-sibling::*//text()[normalize-space()]
                    """)

            else: # no blockQuoteExists and no lineBreakExists

                d = dLink.xpath("""
                    ./text()[normalize-space()]
                    |
                    ./a//text()[normalize-space()]
                    |
                    ./b/text()[normalize-space()]
                    |
                    ./i/text()[normalize-space()]
                    |
                    ./em/text()[normalize-space()]
                """)

            defs.append(d)
            
        # NOTE These elements need to be cleaned in the item pipeline, or dropped if empty
        # A possible result is the following (url): 
        # (http://onlineslangdictionary.com/meaning-definition-of/10-south)
        # ['When you are on your way down to your hands and knees on  the floor...sick.\r\n\r\n\r\n']
        # (http://onlineslangdictionary.com/meaning-definition-of/amazon) results in one empty definition (see origin)


        # Make one item for each definition
        # Definition points to another word's definitions. Go get those
        # response meta = {'definition' : definition}
       
        print(response.url)
        print(f'scraping definition of: {word.extract()}')
        
        for d in defs:
            if d:
                print(f'Definition: {d.extract()}')
            else:
                print(f'Definition: ')
        print('---------------------------------------------------------------')

        return #loader.load_item()
