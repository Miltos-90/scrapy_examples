from abc import ABC, ABCMeta, abstractmethod
from scrapy import Spider, signals, Item
from .constants import DB_PRAGMA_DEFAULT
from scrapy.crawler import Crawler
from sqlite3 import connect
from logging import Filter
import os


class LoggerFilter(Filter):
    """ Filter that forbids scraped items to be logged """

    def filter(self, record):
        return not record.getMessage().startswith('Scraped from')


class Singleton(ABCMeta):
    """ Singleton metaclass """
    _instances = {}

    def __call__(cls, *args, **kwargs):

        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)

        return cls._instances[cls]


class Database():
    """ Generic database class """

    def __init__(self, 
        pathToFile  : str,                      # path to .db file
        schemaScript: str,                      # sqlite script that defines the schema
        pragmaScript: str = DB_PRAGMA_DEFAULT   # sqlite script that defines the pragmas
        ):  

        self.file       = pathToFile
        self.cursor     = None
        self.connection = None
    
        # Generate file if it does not exist
        if not os.path.isfile(self.file): 
            self._make(schemaScript, pragmaScript)
        
        return


    def _connect(self):
        """ Connects to the database """

        self.connection = connect(self.file)
        self.cursor     = self.connection.cursor()
        return
    

    def execute(self, query: str, task: str):
        """ Executes and commits a task to the database """

        self.cursor.execute(query, task)
        self.connection.commit()
        return


    def _close(self):
        """ Closes connection and optionally commits changes """

        self.cursor.close()
        self.connection.close()
        
        self.connection = None
        self.cursor     = None

        return


    def _make(self, 
        schemaScript: str,  # sqlite script that defines the schema
        pragmaScript: str): # sqlite script that defines the pragmas):
        
        """ Creates an empty database """
        
        self._connect()
        self.connection.executescript(pragmaScript)
        self.connection.executescript(schemaScript)
        self._close()

        return
    

    """ Signals """
    def spiderOpened(self, spider: Spider): self._connect()
    def spiderClosed(self, spider: Spider): self._close()


class AbstractDBSavePipeline(ABC):
    """ Abstract pipeline to save items in the database defined in the class above. """

    def __init__(self, filePath: str, pragma: str, schema: str):
        """ Initialisation method. Instantiates database if it does not exist. """

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
    

    @abstractmethod
    def process_item(self, item: Item, spider: Spider) -> Item:
        """ Saves item in the database. To be implemented by the concrete classes """
        pass