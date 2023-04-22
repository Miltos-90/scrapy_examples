from scrapy import Spider, Item 
from scrapy.exceptions import DropItem

import sys
sys.path.append('../utils')
from utils.helpers import AbstractDBSavePipeline


def isAuthor(item) -> bool: return "name" in item.keys()
def isQuote(item)  -> bool: return "quote" in item.keys()

class DefaultValuesPipeline():
    """ Sets default values to all fields of an item """

    def process_item(self, item: Item, spider: Spider) -> Item:
        """ Item processor """

        if not bool(item)  : raise DropItem()
        elif isAuthor(item): return self.processAuthorItem(item)
        elif isQuote(item) : return self.processQuoteItem(item)


    @staticmethod
    def processQuoteItem(item):
        """ Author item processor """

        item.setdefault('quote',    'not found')
        item.setdefault('author',   'not found')
        item.setdefault('keywords', 'not found')
        
        return item
    

    @staticmethod
    def processAuthorItem(item: Item) -> Item:
        """ Quote item processor """

        # Set default values
        item.setdefault('name',       'not found')
        item.setdefault('bio',        'not found')
        item.setdefault('birthdate',  'not found')
        item.setdefault('birthplace', 'not found')
        
        return item
    

class SavePipeline(AbstractDBSavePipeline):
    """ Saves item to the database """

    def process_item(self, item: Item, spider: Spider) -> Item:
        """ Save items in the database.
            This method is called for every item pipeline component
        """
    
