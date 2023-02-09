from scrapy.utils.project import get_project_settings
import sqlite3

"""
Database schema
--------------
table AUTHORS
col ID          int         PRIMARY KEY
col FULLNAME    text        UNIQUE NOT NULL
col BIO         text        NOT NULL
col BIRTHDATE   datetime    NOT NULL

table PAGES
col ID          int         PRIMARY KEY
col PAGE        text        UNIQUE NOT NULL

table QUOTES
col ID          int         PRIMARY KEY
col QUOTE       text        UNIQUE NOT NULL
col TAGS        text        NOT NULL
col AUTHOR_ID   text        FOREIGN KEY
COL PAGE_ID     text        FOREIGN KEY
"""

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
    dbSchema   = get_project_settings().get("DB_SCHEMA")
    dbPragma   = get_project_settings().get("DB_PRAGMA")
    connection = createConnection(dbFile)

    connection.executescript(dbPragma)
    connection.executescript(dbSchema)
    connection.commit()
    connection.close()

    """
#   TO BE DELETED
    query = "INSERT INTO authors (name, birthdate, bio) VALUES (?, ?, ?)"
    cursor.execute(query, ("c", datetime.strptime("1990-05-26", '%Y-%m-%d'), " this is me"))
    cursor.execute(query, ("d", datetime.strptime("2002-01-23", '%Y-%m-%d'),"this is also me"))

    query = "INSERT INTO pages (url) VALUES (?)"
    cursor.execute(query, ("https://bs2.com", ))
    cursor.execute(query, ("http://bs_more2.com", ))

    query = "SELECT id FROM authors WHERE name = ?"
    authorID = cursor.execute(query, ("b",))
    authorID = authorID.fetchone()[0]

    query = "SELECT id FROM pages WHERE url = ?"
    pageID = cursor.execute(query, ("https://bs.com",))
    pageID = pageID.fetchone()[0]

    query = "INSERT INTO quotes (quote, tags, author_id, page_id) VALUES (?, ?, ?, ?)"
    task  = ("this is a quote2", "myTags", authorID, pageID)
    cursor.execute(query, task)

    query = "SELECT * FROM quotes WHERE author_id == ?"
    task = (authorID, )
    res = cursor.execute(query, task)
    print(res.fetchone())

    # At the end
    cursor.close()
    connection.commit()
    connection.close()
    """
