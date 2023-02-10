# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field
from scrapy.loader import ItemLoader

from itemloaders.processors import MapCompose, TakeFirst
from datetime import datetime


def removeQuotes(text):
    """ Strip unicode characters """
    return text.strip(u'\u201c'u'\u201d')


def toDatetime(text):
    """ Convert string (format example: May 15, 2003) to datetime"""
    return datetime.strptime(text, '%B %d, %Y')

def toStringDatetime(datetimeObject):
    return datetimeObject.strftime('%Y-%m-%d')


def parse_location(text):
    "Parses location by stripping useless part of the string"
    return text.replace('in ', '')


class QuoteItem(Item):
    """ Declares the item fields. """

    quote            = Field()
    author           = Field()
    tag              = Field()
    author_bio       = Field()
    author_birthdate = Field()
    author_birth_loc = Field()


class QuoteLoader(ItemLoader):
    """ Declares the processors used in the loader 
        for each field of the items.
    """

    default_item_class       = QuoteItem
    default_output_processor = TakeFirst()

    quote_in            = MapCompose(removeQuotes)
    author_in           = MapCompose(str.strip)
    author_bio_in       = MapCompose(str.strip)
    author_birthdate_in = MapCompose(toDatetime, toStringDatetime)
    author_birth_loc_in = MapCompose(parse_location)



    
    

