from scrapy import Spider, signals
from logging import Filter
from sqlite3 import connect
from abc import ABCMeta
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
        pathToFile  : str,  # path to .db file
        schemaScript: str,  # sqlite script that defines the schema
        pragmaScript: str): # sqlite script that defines the pragmas):

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