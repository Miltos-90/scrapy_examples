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
QuotesDatabase = Database(pathToFile = SETTINGS.get("DB"))
URLDatabase    = Database(pathToFile= SETTINGS.get("URL_LOG_DB"))

# If the databases do not exist, make them
if not os.path.isfile(SETTINGS["DB"]): 
    QuotesDatabase.make(SETTINGS["DB_SCHEMA"], SETTINGS["DB_PRAGMA"])

if not os.path.isfile(SETTINGS["URL_LOG_DB"]): 
    URLDatabase.make(SETTINGS["URL_LOG_SCHEMA"], SETTINGS["DB_PRAGMA"])
