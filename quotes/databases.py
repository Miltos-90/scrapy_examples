""" Script that collects all helper functions used throughout """

from sqlite3 import connect as sqlconnect
from quotes.utils import Singleton


class Database(metaclass = Singleton):
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

