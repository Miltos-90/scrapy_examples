from logging import Filter
from abc import ABCMeta


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


from sqlite3 import connect as sqlconnect


class Database():
    """ Generic database class """

    def __init__(self, pathToFile : str):

        self.file       = pathToFile
        self.connection = None
        self.cursor     = None

        return


    def connect(self):
        """ Connects to the database """

        self.connection = sqlconnect(self.file)
        self.cursor     = self.connection.cursor()

        return


    def close(self, commit:bool = True):
        """ Closes connection and optionally commits changes """

        if commit: 
            self.connection.commit()

        self.cursor.close()
        self.connection.close()
        
        self.connection = None
        self.cursor     = None

        return

    def make(self,
        schemaScript: str,  # sqlite script that defines the schema
        pragmaScript: str): # sqlite script that defines the pragmas
        """ Creates an empty database """
        
        self.connect()
        self.connection.executescript(pragmaScript)
        self.connection.executescript(schemaScript)
        self.close()

        return