from .utils import Database
from scrapy import Spider, Item
from scrapy.crawler import Crawler
from scrapy.exceptions import DropItem
from typing import Tuple
import os


def isAuthor(item) -> bool: return "name" in item.keys()
def isQuote(item)  -> bool: return "quote" in item.keys()

class DefaultValuesPipeline():
    """ Sets default values to all fields of an item """

    def process_item(self, item: Item, spider: Spider) -> Item:
        """ Save quotes in the database
            This method is called for every item pipeline component
        """

        if not bool(item)  : raise DropItem()
        elif isAuthor(item): return DefaultAuthorValuesPipeline.process_item(item)
        elif isQuote(item) : return DefaultQuoteValuesPipeline.process_item(item)
        

class DefaultQuoteValuesPipeline():
    """ Sets default values to all fields """

    @staticmethod
    def process_item(item: Item) -> Item:
        """ Save quotes in the database
            This method is called for every item pipeline component
        """

        # Set default values
        item.setdefault('quote',    'not found')
        item.setdefault('author',   'not found')
        item.setdefault('keywords', 'not found')
        
        return item
    

class DefaultAuthorValuesPipeline(object):
    """ Sets default values to all fields """

    @staticmethod
    def process_item(item: Item) -> Item:
        """ Save quotes in the database
            This method is called for every item pipeline component
        """

        # Set default values
        item.setdefault('name',       'not found')
        item.setdefault('bio',        'not found')
        item.setdefault('birthdate',  'not found')
        item.setdefault('birthplace', 'not found')
        
        return item


class SavePipeline():
    """ Saves item to the database """


    def __init__(self, filePath: str, pragma: str, schema: str):
        """ Initialisation method """

        # Make database if it does not exist yet.
        self.db = Database(pathToFile = filePath)
        if not os.path.isfile(filePath):
            
            self.db.make(schema, pragma)

        return
    

    @classmethod
    def from_crawler(cls, crawler: Crawler):
        """ Instantiates class """
        
        return cls(filePath = crawler.settings.get("DB"), 
                   pragma   = crawler.settings.get("DB_PRAGMA"),
                   schema   = crawler.settings.get("DB_SCHEMA")
        )


    def process_item(self, item: Item, spider: Spider) -> Item:
        """ Save items in the database.
            This method is called for every item pipeline component
        """

        if not bool(item)  : raise DropItem()
        elif isAuthor(item): query, task = SaveAuthorPipeline.process_item(item)
        elif isQuote(item) : query, task = SaveQuotePipeline.process_item(item)

        self.db.connect()
        self.db.cursor.execute(query, task)
        self.db.close()

        return item


class SaveQuotePipeline():
    """ Returns the task of saving a quote to the database """

    @staticmethod
    def process_item(item: Item) -> Tuple[str, tuple]:
        
        query = "INSERT OR IGNORE INTO quotes (quote, keywords, author) VALUES (?, ?, ?);"
        task  = (item['quote'], item['keywords'], item['author'])

        return query, task
    

class SaveAuthorPipeline(object):
    """ Returns the task of saving an author to the database """

    @staticmethod
    def process_item(item: Item) -> Tuple[str, tuple]:

        query = "INSERT OR IGNORE INTO authors (name, birthdate, birthplace, bio) VALUES (?, ?, ?, ?);"
        task  = (item['name'], item['birthdate'], item['birthplace'], item['bio'])

        return query, task

