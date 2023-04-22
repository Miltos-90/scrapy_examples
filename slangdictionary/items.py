# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from itemloaders.processors import MapCompose, TakeFirst
from scrapy.loader import ItemLoader
from scrapy import Item, Field
from datetime import datetime


""" Definition of functions used in the Itemloader """

def usageProcessor(d: list) -> list:
    """ Processor for the usage field. It converts the dict's values from lists, to scalars. """

    d = d[0] # unpack

    # Convert values from list[str] to integers
    return [{k: int(v[0]) for k, v in d.items()}]


def vulgarityProcessor(s: list) -> list:
    """ Processor for the vulgarity field. It strips the '%' cahracter """

    out = []
    for e in s:
        if e == 'None': 
            out.append(None)
        else: 
            out.append( int(e.strip('%')) )
    
    return out


def definitionProcessor(defs: list) -> list:
    """ Processor for the defintion field """

    # Merge fields and implicitly convert multiple whitespace characters 
    # to single whitespace, and sanitize

    newDefs = []
    for d in defs:
        d = ''.join(d)
        d = ' '.join(d.split()).strip('\r').strip('\n').strip()

        newDefs.append(d)
    
    return newDefs


class WordItem(Item):
    """ Declares the item fields. """

    word        = Field()
    usage       = Field()
    definitions = Field()
    vulgarity   = Field()


class WordLoader(ItemLoader):
    """ Declares the processors used in the loader for each field of the items.
    """

    definitions_in     = definitionProcessor
    vulgarity_in       = vulgarityProcessor
    usage_in           = usageProcessor
    default_item_class = WordItem
    default_output_processor = TakeFirst()
    


