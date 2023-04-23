from itemloaders.processors import MapCompose, TakeFirst, Identity
from scrapy.loader import ItemLoader
from scrapy import Item, Field


""" Definition of functions used in the Itemloader """

def usageProcessor(d: dict) -> list:
    """ Processor for the usage field. It converts the dict's values from lists, to scalars. """

    # Convert values from list[str] to integers
    return [{k: int(v[0]) for k, v in d.items()}]


def vulgarityProcessor(s: str) -> list:
    """ Processor for the vulgarity field. It strips the '%' cahracter """

    if s == 'None': s = None
    else: s = int(s.strip('%'))
    
    return s


def definitionProcessor(d: str) -> list:
    """ Processor for the defintion field """

    # Merge fields and implicitly convert multiple whitespace characters 
    # to single whitespace, and sanitize

    return d.strip('\r').strip('\n').strip()


class WordItem(Item):
    """ Declares the item fields. """

    word        = Field()
    usage       = Field()
    definitions = Field()
    vulgarity   = Field()


class WordLoader(ItemLoader):
    """ Declares the processors used in the loader for each field of the items.
    """

    default_item_class = WordItem
    definitions_in     = MapCompose(definitionProcessor)
    vulgarity_in       = MapCompose(vulgarityProcessor)
    usage_in           = MapCompose(usageProcessor)
    definitions_out    = Identity()
    default_output_processor = TakeFirst()


