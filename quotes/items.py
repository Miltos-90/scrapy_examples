# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from itemloaders.processors import MapCompose, TakeFirst
from dateutil.parser import parse as parseDate
from scrapy.loader import ItemLoader
from scrapy import Item, Field
from datetime import datetime


""" Definition of functions used in the Itemloader """
def removeQuotes(text: str) -> str:
    """ Strip quotation marks """
    return text.strip(u'\u201c'u'\u201d')


def toDatetime(text: str) -> datetime:
    """ Convert string (format example: May 15, 2003) to datetime"""
    return parseDate(text)


def toStringDate(date: datetime) -> str:
    return date.strftime('%Y-%m-%d')


def parseLocation(text: str) -> str:
    "Parses location by stripping useless part of the string"
    return text.replace('in ', '')


class QuoteItem(Item):
    """ Declares the item fields. """

    quote    = Field()
    author   = Field()
    keywords = Field()


class QuoteLoader(ItemLoader):
    """ Declares the processors used in the loader 
        for each field of the items.
    """

    default_item_class       = QuoteItem
    default_output_processor = TakeFirst()
    quote_in  = MapCompose(removeQuotes)
    author_in = MapCompose(str.strip)


class AuthorItem(Item):
    """ Declares the item fields. """

    name       = Field()
    bio        = Field()
    birthdate  = Field()
    birthplace = Field()


class AuthorLoader(ItemLoader):
    """ Declares the processors used in the loader 
        for each field of the items.
    """

    default_item_class       = AuthorItem
    default_output_processor = TakeFirst()
    name_in       = MapCompose(str.strip)
    bio_in        = MapCompose(str.strip)
    birthdate_in  = MapCompose(toDatetime, toStringDate)
    birthplace_in = MapCompose(parseLocation)
    
    

