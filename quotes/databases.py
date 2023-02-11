""" Script that collects all helper functions used throughout """

from scrapy.utils.project import get_project_settings
from scrapy.exceptions import IgnoreRequest
from datetime import datetime as dt
from sqlite3 import connect as sqlconnect
from abc import ABCMeta, ABC

SETTINGS = get_project_settings()


class Singleton(ABCMeta):
    """ Singleton metaclass """
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Database(ABC, metaclass = Singleton):
    """ Generic database class """

    def __init__(self, 
        pathToFile   : str, # sqlite .db file
        pragmaScript : str, # sqlitescript (usable with .executescript()) that defines the db PRAGMAs (https://www.sqlite.org/pragma.html)
        schemaScript : str
        ):

        self.file       = pathToFile
        self.connection = None
        self.cursor     = None

        self._make(schemaScript, pragmaScript)

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

    def _make(self,
        schemaScript: str,  # sqlite script that defines the schema
        pragmaScript: str): # sqlite script that defines the pragmas
        """ Creates an empty database """
        
        self.connect()
        self.connection.executescript(pragmaScript)
        self.connection.executescript(schemaScript)
        self.close()

        return


class QuoteDatabase(Database):
    """ Reader/writer of the quotes database """

    def __init__(self,
        pathToFile   = SETTINGS.get("DB_FILE"),
        pragmaScript = SETTINGS.get("DB_PRAGMA"),
        schemaScript = SETTINGS.get("DB_SCHEMA")
        ):

        super().__init__(pathToFile, pragmaScript, schemaScript)
        return


    def insertAuthor(self, item):
        """ Inserts an item's author in the database"""

        query = "INSERT OR IGNORE INTO authors (name, birthdate, birthplace, bio) VALUES (?, ?, ?, ?)"
        task  = (item['author'], item['author_birthdate'], item['author_birth_loc'], item['author_bio'])

        self.cursor.execute(query, task)

        return


    def insertQuote(self, item):
        """ Inserts an item's quote in the database """

        query = "SELECT id FROM authors WHERE name = ?"
        task  = (item['author'], )
        authID = self.cursor.execute(query, task).fetchone()[0]

        query  = "INSERT OR IGNORE INTO quotes (quote, tags, author_id) VALUES (?, ?, ?)"
        task   = (item['quote'], item['tag'], authID)

        self.cursor.execute(query, task)

        return


class URLDatabase(Database):

    def __init__(self, 
        pathToFile   = SETTINGS.get("URL_DB_FILE"),
        pragmaScript = SETTINGS.get("URL_DB_PRAGMA"),
        schemaScript = SETTINGS.get("URL_DB_SCHEMA")
        ):

        super().__init__(pathToFile, pragmaScript, schemaScript)

        return


    def insert(self, url: str):
        """ Inserts a url to the database """

        query = "INSERT OR IGNORE INTO pages (url, date) VALUES (?, ?)"
        task = (url, self._now())
        self.cursor.execute(query, task)

        return


    def has(self, url:str):
        """ Checks if a url exists in the database """

        query = "SELECT EXISTS(SELECT * FROM pages WHERE url = ?)"
        task  = (url, )
        out   = self.cursor.execute(query, task).fetchone()[0]
        
        return bool(out)


    def last(self):
        """ Returns the last url that was scraped """

        query = "SELECT url FROM pages WHERE ID = (SELECT MAX(ID) FROM pages)"
        out   = self.cursor.execute(query)
        out   = out.fetchone()[0]
        return out


    @staticmethod
    def _now():
        return dt.now().strftime("%d/%m/%Y %H:%M:%S")


