""" Script that collects all helper functions used throughout """

from scrapy.utils.project import get_project_settings
import sqlite3
import logging

SETTINGS  = get_project_settings()
ERROR_MSG = "Connection to database could not be established."


class LoggerFilter(logging.Filter):
    def filter(self, record):
        """ Forbides scraped items to be logged """
        return not record.getMessage().startswith('Scraped from')


def createConnection(
    dbFile: str = SETTINGS.get("DB_FILE")
    ) -> sqlite3.Connection:
    """ Create a database connection to the 
        SQLite database specified by the db_file
    """

    try:
        connection = sqlite3.connect(dbFile)
    
    except Exception as e:
        connection = None
        logging.error(ERROR_MSG)

    return connection


def makeDatabase(
    pathToFile : str, # Path to database file
    pragma     : str, # sqlite script to set pragmas (see: https://www.sqlite.org/pragma.html)
    schema     : str  # Database table creation script
    ):

    """ Create an empty database if called. """
    
    connection = createConnection(pathToFile)

    if connection is not None:
        connection.executescript(pragma)
        connection.executescript(schema)
        connection.commit()
        connection.close()

    else:
        raise ConnectionError(ERROR_MSG)

if __name__ == "__main__":

    makeDatabase(
        pathToFile = SETTINGS.get("DB_FILE"),
        pragma     = SETTINGS.get("DB_PRAGMA"),
        schema     = SETTINGS.get("DB_SCHEMA")
    )

    makeDatabase(
        pathToFile = SETTINGS.get("URL_DB_FILE"),
        pragma     = SETTINGS.get("DB_PRAGMA"),
        schema     = SETTINGS.get("URL_DB_SCHEMA")
    )
    
