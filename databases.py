from scrapy.utils.project import get_project_settings
import sqlite3


def createConnection(dbFile: str) -> sqlite3.Connection:
    """ Create a database connection to the 
        SQLite database specified by the db_file
    """

    try:
        connection = sqlite3.connect(dbFile)
    
    except Exception as e:
        connection = None
        print(e)

    return connection

if __name__ == "__main__":

    dbFile     = get_project_settings().get("DB_FILE")
    dbPragma   = get_project_settings().get("DB_PRAGMA")
    dbSchema   = get_project_settings().get("DB_SCHEMA")

    connection = createConnection(dbFile)
    connection.executescript(dbPragma)
    connection.executescript(dbSchema)
    connection.commit()
    connection.close()