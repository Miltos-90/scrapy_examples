from scrapy.utils.project import get_project_settings
from scrapy.http import Response
#from .slangdictionary.items import WordLoader
from scrapy import Spider
from scrapy.selector import Selector

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


    def parse(self, response: Response):
        """ Parser for the item details """

        #loader = WordLoader(selector = response)
        inspect_response(response, self)
        
        # Extract word
        word = response.xpath('.//div[contains(@class,"term")]//h2//a[contains(@href,"/meaning-definition")]/text()')

        # Extract definitions.
        defs = [self._getDefinition(dLink) for dLink in response.xpath('//div[@class="definitions"]/ul/li')]

        # Extract commonality/usage statistics
        usageXpath = lambda text: f".//*[contains(text(),'{text}')]/parent::*/following-sibling::*[1]//span/span/text()"
        response.xpath(usageXpath('I use it')).extract()
        response.xpath(usageXpath('No longer use it')).extract()
        response.xpath(usageXpath('Heard it but never used it')).extract()
        response.xpath(usageXpath('Have never heard it')).extract()

        # Extract vulgarity

        
        # NOTE These elements need to be cleaned in the item pipeline, or dropped if empty
        # A possible result is the following (url): 
        # (http://onlineslangdictionary.com/meaning-definition-of/10-south)
        # ['When you are on your way down to your hands and knees on  the floor...sick.\r\n\r\n\r\n']
        # (http://onlineslangdictionary.com/meaning-definition-of/amazon) results in one empty definition (see origin)


        # Make one item for each definition
        # Definition points to another word's definitions. Go get those
        # response meta = {'definition' : definition}

        #"""
        print(response.url)
        print(f'scraping definition of: {word.extract()}')
        for d in defs:
            if d: print(f'Definition: {d.extract()}')
            else: print(f'Definition: ')
        print('---------------------------------------------------------------')
        #"""
       
        return #loader.load_item()

    
    def _getDefinition(self, selector: Selector) -> Selector:
        """ Extracts the text from a definition, discarding examples and on occasion superfluous sentences. """

        def xpathA(tag: str) -> str:
            """ Generates the appropriate xpath to grab the definition in the presence of 
                a blockquote or a linebreak tag.
            """

            # If xpath 2.0 was supported, this would have been more compact
            xp = f"""
                ./{tag}[1]/preceding-sibling::text()[normalize-space()]
                |
                ./{tag}[1]/preceding-sibling::*//text()[normalize-space()]
                """
            
            return xp
        
        def xpathB() -> str:
            """ Generates the appropriate xpath to grab the definition in the absence of 
                a blockquote or a linebreak tag.
            """

            # If xpath 2.0 was supported, this would have been more compact
            xp = """
                ./text()[normalize-space()]    | ./a//text()[normalize-space()] |
                ./b//text()[normalize-space()] | ./i//text()[normalize-space()] |
                ./em//text()[normalize-space()]
                """
            
            return xp

        hasBlockquote = bool(int(selector.xpath('boolean(./blockquote)').extract_first()))
        haslineBreak  = bool(int(selector.xpath('boolean(./br)').extract_first()))
        
        if haslineBreak    : d = selector.xpath(xpathA('br'))
        elif hasBlockquote : d = selector.xpath(xpathA('blockquote'))
        else               : d = selector.xpath(xpathB())

        return d