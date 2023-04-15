from scrapy import Spider, Item, signals
from scrapy.exceptions import DropItem
from scrapy.crawler import Crawler
from .helpers import Database
from typing import Tuple


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
    

class SavePipeline():
    """ Saves item to the database """


    def __init__(self, filePath: str, pragma: str, schema: str):
        """ Initialisation method """

        self.db = Database(filePath, schema, pragma)

        return
    

    @classmethod
    def from_crawler(cls, crawler: Crawler):
        """ Instantiates class """
        
        c = cls(
            filePath = crawler.settings.get("DB"), 
            pragma   = crawler.settings.get("DB_PRAGMA"),
            schema   = crawler.settings.get("DB_SCHEMA")
        )

        # Connect signals
        crawler.signals.connect(c.db.spiderOpened, signal = signals.spider_opened)
        crawler.signals.connect(c.db.spiderClosed, signal = signals.spider_closed)

        return c


    def process_item(self, item: Item, spider: Spider) -> Item:
        """ Save items in the database.
            This method is called for every item pipeline component
        """

        if not bool(item)  : raise DropItem()
        elif isAuthor(item): query, task = self.saveAuthorTask(item)
        elif isQuote(item) : query, task = self.saveQuoteTask(item)
        self.db.execute(query, task)

        return item
    

    @staticmethod
    def saveQuoteTask(item: Item) -> Tuple[str, tuple]:
        """ Returns the task of saving a quote to the database """
        
        query = "INSERT OR IGNORE INTO quotes (quote, keywords, author) VALUES (?, ?, ?);"
        task  = (item['quote'], item['keywords'], item['author'])

        return query, task
    

    @staticmethod
    def saveAuthorTask(item: Item) -> Tuple[str, tuple]:
        """ Returns the task of saving an author to the database """

        query = "INSERT OR IGNORE INTO authors (name, birthdate, birthplace, bio) VALUES (?, ?, ?, ?);"
        task  = (item['name'], item['birthdate'], item['birthplace'], item['bio'])

        return query, task