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


class WordItem(Item):
    """ Declares the item fields. """

    field1 = Field()
    field2 = Field()
    field3 = Field()


class WordLoader(WordItem):
    """ Declares the processors used in the loader 
        for each field of the items.
    """

    default_item_class       = WordItem
    default_output_processor = TakeFirst()
    quote_in  = MapCompose(removeQuotes)
    author_in = MapCompose(str.strip)

