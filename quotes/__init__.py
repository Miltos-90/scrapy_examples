from quotes.utils import LoggerFilter

from logging import getLogger
from scrapy.utils.log import configure_logging 
from scrapy.utils.project import get_project_settings
from quotes.databases import Database
import os

SETTINGS = get_project_settings()

""" =================== LOGGER CONFIGURATION =================== """
configure_logging(
    settings = {
        "LOG_FILE"   : SETTINGS.get("LOG_FILE"),
        "LOG_FORMAT" : SETTINGS.get("LOG_FORMAT"),
        "LOG_LEVEL"  : SETTINGS.get("LOG_LEVEL")
        }
    )

getLogger('scrapy.core.scraper').addFilter(LoggerFilter())


""" =================== DATABASE CONFIGURATION =================== """
QuotesDatabase = Database(pathToFile = SETTINGS.get("DB_FILE"))

# If the database does not exist, make it
if not os.path.isfile(SETTINGS["DB_FILE"]): 
    QuotesDatabase.make(SETTINGS["DB_SCHEMA"], SETTINGS["DB_PRAGMA"])

else:
    # If resuming from previous crawl, remove last recorded URL so that it will be re-scraped
    QuotesDatabase.connect()
    query = "DELETE FROM pages WHERE id = (SELECT MAX(id) FROM pages);"
    QuotesDatabase.cursor.execute(query)
    QuotesDatabase.close()


