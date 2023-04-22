from scrapy.utils.project import get_project_settings
from slangdictionary.items import WordLoader
from scrapy.http import Response
from scrapy import Spider

from scrapy.shell import inspect_response


SETTINGS = get_project_settings()


class SlangSpider(Spider):

    name            = SETTINGS["BOT_NAME"]
    start_urls      = SETTINGS["START_URLS"]
    allowed_domains = SETTINGS["ALLOWED_DOMAINS"]
    custom_settings = SETTINGS["CUSTOM_SPIDER_SETTINGS"]
    

    def parse(self, response: Response):
        """ Handler for the response downloaded for each of the requests made. """

        # Yield all links to the individual word pages
        yield from response.follow_all( 
            xpath    = './/table[@class="wordlist"]//@href', 
            callback = self._parseItem)
        
        # Yield link to the next pages
        yield from response.follow_all( 
            xpath    = './/table[@class="nav"]//td/a/@href',
            callback = self.parse)

        return


    def _parseItem(self, response: Response):
        """ Parser for the item details. """

        loader = WordLoader()
        loader.add_value('word',        self._getWord(response))
        loader.add_value('definitions', self._getDefinitions(response))
        loader.add_value('vulgarity',   self._getVulgarity(response))
        loader.add_value('usage',       self._getUsage(response))

        return loader.load_item()
    

    def _getVulgarity(self, response: Response) -> float:
        """ Extracts vulgarity. """
        return response.xpath(".//span[@id='vulgarity-vote-average']/text()").extract()


    def _getWord(self, response: Response) -> str:
        """ Extracts word. """
        return response.xpath('.//div[contains(@class,"term")]//h2//a[contains(@href,"/meaning-definition")]/text()').extract()


    def _getUsage(self, response: Response) -> dict:
        """ Gathers usage statistics for the current word. """

        usageXpath = lambda text: f".//*[contains(text(),'{text}')]/parent::*/following-sibling::*[1]//span/span/text()"

        return {
            'use'    : response.xpath(usageXpath('I use it')).extract(),
            'hear'   : response.xpath(usageXpath('Heard it but never used it')).extract(),
            'no-use' : response.xpath(usageXpath('No longer use it')).extract(),
            'no-hear': response.xpath(usageXpath('Have never heard it')).extract()
            }

    
    def _getDefinitions(self, response: Response) -> list:
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

        defs = []
        for selector in response.xpath('//div[@class="definitions"]/ul/li'):

            hasBlockquote = bool(int(selector.xpath('boolean(./blockquote)').extract_first()))
            haslineBreak  = bool(int(selector.xpath('boolean(./br)').extract_first()))
            
            if   haslineBreak : d = selector.xpath(xpathA('br'))
            elif hasBlockquote: d = selector.xpath(xpathA('blockquote'))
            else              : d = selector.xpath(xpathB())

            defs.append(d.extract())

        return defs